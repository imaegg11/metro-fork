"""
WSGI config for metropolis project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

warnings.filterwarnings(
	"ignore", lineno=37, module="dateutil.tz", category=DeprecationWarning)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metropolis.settings")

application = get_wsgi_application()
