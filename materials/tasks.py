from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_information_about_update(subject, message, email):
    subject = "Обновление курса"
    message = f"{email} обновил свой курс"
    send_response = send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
    )

    return send_response