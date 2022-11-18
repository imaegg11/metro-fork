from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, permissions
from rest_framework import serializers

from ....models import BlogPost
from .base import BaseProvider


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        ordering = ["-created_date"]
        fields = "__all__"


class Provider(BaseProvider):
    serializer_class = Serializer
    model = BlogPost

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def permission_classes(self):
        return [permissions.DjangoModelPermissions] if self.request.mutate else [permissions.AllowAny]

    def get_queryset(self, request):
        if request.user.has_perm('core.blog_post.view') or request.user.is_superuser:
            return BlogPost.objects.all()
        else:
            return BlogPost.objects.filter(is_published=True)

    def get_last_modified(self, view):
        return view.get_object().last_modified_date

    def get_last_modified_queryset(self):
        return LogEntry.objects \
            .filter(content_type=ContentType.objects.get(app_label='core', model='blogpost')) \
            .latest('action_time') \
            .action_time