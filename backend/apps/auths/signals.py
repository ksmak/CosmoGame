from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
# from django.core.mail import send_mail
# from django.conf import settings


User = get_user_model()


# HOST_NAME = "http://0.0.0.0:8000"


@receiver(post_save, sender=User)
def send_activation_code_handler(
    **kwargs: dict
) -> None:
    pass
    # if not kwargs['created']:
    #     return

    # link: str = ''.join((
    #     HOST_NAME,
    #     '/api/activate/',
    #     kwargs['instance'].activation_code
    # ))

    # send_mail(
    #     _("User Registration Confirmation"),
    #     _(f"To confirm registration, go to the following link: {link}"),
    #     settings.EMAIL_HOST_USER,
    #     [kwargs['instance'].email],
    #     fail_silently=False
    # )
