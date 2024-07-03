from datetime import timedelta

from django.utils import timezone

from users.models import User
from celery import shared_task


@shared_task
def check_activity():
    inactive_users = User.objects.filter(last_login__lt=timezone.now() - timedelta(days=30))
    inactive_users.update(is_active=False)