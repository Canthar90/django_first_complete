from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'


class MyAdminConfig(AdminConfig):
    default_site = 'polls.admin.MyAdminSite'