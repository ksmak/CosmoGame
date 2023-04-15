from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from abstracts.utils import generate_code


class CustomUserManager(BaseUserManager):
    """CustomUser manager."""
    def _validate(
        self,
        username: str,
        email: str,
        password: str
    ) -> None:
        if not username:
            raise ValidationError(_("Username required."))

        if not email:
            raise ValidationError(_("Email required."))

        if not password:
            raise ValidationError(_("Password required."))

    def create_user(
        self,
        username: str,
        email: str,
        password: str
    ) -> 'CustomUser':
        self._validate(
            username=username,
            email=email,
            password=password
        )

        user: 'CustomUser' = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        username: str,
        email: str,
        password: str
    ) -> 'CustomUser':
        self._validate(
            username=username,
            email=email,
            password=password
        )
        user: 'CustomUser' = self.model(
            username=username,
            email=email,
            password=password
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """CustomUser model."""
    ACTIVATION_CODE_SIZE = 30

    username = models.CharField(
        verbose_name=_('username'),
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=100,
        unique=True
    )
    is_active = models.BooleanField(
        verbose_name=_('is active'),
        default=False
    )
    is_superuser = models.BooleanField(
        verbose_name=_('is superuser'),
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name=_('is staff'),
        default=False
    )
    activation_code = models.CharField(
        verbose_name=_('activation code'),
        max_length=ACTIVATION_CODE_SIZE
    )
    registration_date = models.DateTimeField(
        verbose_name=_('registration date'),
        auto_now_add=True
    )
    change_date = models.DateTimeField(
        verbose_name=_('change date'),
        auto_now=True
    )
    activation_date = models.DateTimeField(
        verbose_name=_('activation date'),
        null=True,
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('username', )

    def save(self, *args, **kwargs) -> None:
        self.activation_code = generate_code(self.ACTIVATION_CODE_SIZE)

        return super().save(*args, **kwargs)
