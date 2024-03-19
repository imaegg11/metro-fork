import datetime as dt
import functools

import pytz
import requests
from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings

from django.db.models import F, Field, JSONField, Q, Value
from django.db.models.functions.text import Concat
from django.utils import timezone
from django.utils.translation import gettext_lazy as _l
from django.utils.translation import ngettext
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushTicketError,
)
from oauth2_provider.models import clear_expired
from requests.exceptions import ConnectionError, HTTPError

from core.models import Announcement, BlogPost, Comment, Event, User
from core.utils.tasks import get_random_username
from metropolis.celery import app

logger = get_task_logger(__name__)
session = requests.Session()
session.headers.update(
    {
        # "Authorization": f"Bearer {os.getenv('EXPO_TOKEN')}", # TODO: expo push notifications authn?
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
)
for m in ("get", "options", "head", "post", "put", "patch", "delete"):
    setattr(
        session,
        m,
        functools.partial(getattr(session, m), timeout=settings.NOTIF_EXPO_TIMEOUT_SECS),
    )


def users_with_token():
    return User.objects.exclude(Q(expo_notif_tokens=Value({}, JSONField())))


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=0, minute=0), delete_expired_users)
    sender.add_periodic_task(crontab(hour=18, minute=0), notif_events_singleday)
    sender.add_periodic_task(crontab(day_of_month=1), run_group_migrations)
    sender.add_periodic_task(
        crontab(hour=1, minute=0), clear_expired
    )  # Delete expired oauth2 tokens from db everyday at 1am


@app.task
def delete_expired_users():
    """Scrub user data from inactive accounts that have not logged in for 14 days. (marked deleted)"""
    queryset = User.objects.filter(
        is_deleted=True,
        last_login__lt=dt.datetime.now() - dt.timedelta(days=14),
    )
    comments = Comment.objects.filter(author__in=queryset)
    comments.update(
        body=None, last_modified=timezone.now()
    )  # if body is None "deleted on %last_modified% would be shown
    queryset.update(  # We need to object to not break posts or comments
        first_name="Deleted",
        last_name="User",
        username=get_random_username(),
        bio="",
        timezone="",
        graduating_year=None,
        is_teacher=False,
        organizations=[],
        tags_following=[],
        qltrs=None,
        saved_blogs=[],
        saved_announcements=[],
        expo_notif_tokens={},
    )
    queryset.update(email=Concat(F("random_username"), Value("@maclyonsden.com")))


@app.task
def run_group_migrations():
    from scripts.migrations import migrate_groups

    print(migrate_groups())


@app.task
def notif_broker_announcement(obj_id):
    logger.info(f"notif_broker_announcement for {obj_id}")
    try:
        ann = Announcement.objects.get(id=obj_id)
    except Announcement.DoesNotExist:
        logger.warning(f"notif_broker_announcement: announcement {obj_id} does not exist")
        return
    affected = users_with_token()
    if ann.organization.id in settings.ANNOUNCEMENTS_NOTIFY_FEEDS:
        category = "ann.public"
    else:
        affected = affected.filter(
            Q(tags_following__in=ann.tags.all()) | Q(organizations__in=[ann.organization])
        )
        category = "ann.personal"
    for u in affected.all():
        notif_single.delay(
            u.id,
            dict(
                title=_l("New Announcement: %(title)s") % dict(title=ann.title),
                body=ann.body,
                category=category,
            ),
        )


@app.task
def notif_broker_blogpost(obj_id):
    logger.info(f"notif_broker_blogpost for {obj_id}")
    try:
        post = BlogPost.objects.get(id=obj_id)
    except BlogPost.DoesNotExist:
        logger.warning(f"notif_broker_blogpost: blogpost {obj_id} does not exist")
        return
    affected = users_with_token()
    for u in affected.all():
        notif_single.delay(
            u.id,
            dict(
                title=_l("New Blog Post: %(title)s") % dict(title=post.title),
                body=post.body,
                category="blog",
            ),
        )


@app.task
def notif_events_singleday(date: dt.date = None):
    tz = pytz.timezone(settings.TIME_ZONE)
    if date is None:
        date = dt.date.today() + dt.timedelta(days=1)
    elif isinstance(date, str):  # ken things
        date = dt.datetime.fromisoformat(date)
        raise RuntimeError(f"date {type(date)} {date}")
    eligible = users_with_token()
    for u in eligible.all():
        # assume we don't have 10 million events overlapping a single day (we can't fit it in a single notif aniway)
        date_mintime = tz.localize(dt.datetime.combine(date, dt.datetime.min.time()))
        date_maxtime = tz.localize(dt.datetime.combine(date, dt.datetime.max.time()))
        covering = list(
            Event.get_events(u)
            .filter(
                start_date__lte=date_maxtime,
                end_date__gte=date_mintime,
            )
            .all()
        )
        if len(covering) == 0:
            continue
        covering.sort(key=lambda e: int(e.schedule_format == "default"))
        covering.sort(key=lambda e: e.start_date - date_mintime)
        body = ngettext(
            "%(count)d Event:\n",
            "%(count)d Events:\n",
            len(covering),
        ) % dict(count=len(covering))
        for i, e in enumerate(covering):
            body += _l("%(i)d. %(title)s\n") % dict(i=i + 1, title=e.name)
        headline = covering[0]
        notif_single.delay(
            u.id,
            dict(
                title=_l("%(date)s: %(headline)s")
                % dict(date=date.strftime("%a %b %d"), headline=headline.name),
                body=body,
                category="event.singleday",
            ),
        )


@app.task(bind=True)
def notif_single(self, recipient_id: int, msg_kwargs):
    recipient = User.objects.get(id=recipient_id)
    logger.info(
        f"notif_single to {recipient} ({recipient.expo_notif_tokens}): {msg_kwargs}"
        + ("(dry run)" if settings.NOTIF_DRY_RUN else "")
    )
    if settings.NOTIF_DRY_RUN:
        return
    notreg_tokens = set()
    for token, options in recipient.expo_notif_tokens.items():
        if options is not None:
            allowlist = options.get("allow")
            if isinstance(allowlist, dict) and msg_kwargs["category"] not in allowlist.keys():
                logger.info(
                    f"notif_single (category {msg_kwargs['category']}) not allowed to {recipient} (allowlist {allowlist}) ({recipient.expo_notif_tokens}): {msg_kwargs}"
                    + ("(dry run)" if settings.NOTIF_DRY_RUN else "")
                )
                continue
        try:
            resp = PushClient(session=session).publish(
                PushMessage(to=f"ExponentPushToken[{token}]", **msg_kwargs)
            )
        except (ConnectionError, HTTPError) as exc:
            raise self.retry(exc=exc)
        try:
            resp.validate_response()
        except DeviceNotRegisteredError:
            notreg_tokens.add(token)
        except PushTicketError as exc:
            raise self.retry(exc=exc)
    if notreg_tokens:
        u = User.objects.filter(id=recipient_id).first()
        for token in notreg_tokens:
            del u.expo_notif_tokens[token]
        u.save()
