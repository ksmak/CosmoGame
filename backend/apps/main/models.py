from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import (
    ArrayField
)
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError


User = get_user_model()


class Game(models.Model):
    """Game model."""
    name = models.CharField(
        verbose_name=_('name'),
        max_length=150
    )
    gamers = models.ManyToManyField(
        to='Gamer',
        related_name='gamers'
    )


class Gamer(models.Model):
    """Gamer model."""
    IMAGE_MAX_HEIGHT = 100
    IMAGE_MAX_WIDTH = 100
    IMAGE_SIZE = 20
    user = models.OneToOneField(
        verbose_name=_('user'),
        to=User,
        on_delete=models.RESTRICT
    )
    avatar = models.ImageField(
        verbose_name=_('avatar'),
        upload_to='media/avatars/',
        null=True,
        blank=True
    )
    props = models.JSONField(
        verbose_name=_('properties'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('gamer')
        verbose_name_plural = _('gamers')

    def __str__(self) -> str:
        return self.user.username

    def clean(self) -> None:
        if self.avatar:
            # validate avatar
            w, h = get_image_dimensions(self.avatar)

            # validate dimensions
            if w > self.IMAGE_MAX_WIDTH or h > self.IMAGE_MAX_HEIGHT:
                raise ValidationError(
                    _('Please use an image that is %s x %s pixels or smaller.'
                        % (self.IMAGE_MAX_WIDTH, self.IMAGE_MAX_HEIGHT))
                )

            # validate file size
            if len(self.avatar) > (self.IMAGE_SIZE * 1024):
                raise ValidationError(
                    _(f'Avatar file size may not exceed {self.IMAGE_SIZE}k.'))

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class GameObject(models.Model):
    """Game object model."""
    STATE_READY = 0
    STATE_IN_PROGRESS = 1
    STATES = (
        (STATE_READY, 'Ready'),
        (STATE_IN_PROGRESS, 'In progress')
    )

    TYPE_UNKNOWN = 0
    TYPE_RESEARCH = 1
    OBJ_TYPES = (
        (TYPE_UNKNOWN, 'Unknown'),
        (TYPE_RESEARCH, 'Research'),
    )

    state = models.IntegerField(
        verbose_name=_('state'),
        choices=STATES,
        default=STATE_READY
    )
    obj_type = models.PositiveIntegerField(
        verbose_name=_('object type'),
        choices=OBJ_TYPES,
        default=TYPE_UNKNOWN
    )
    order_number = models.PositiveIntegerField(
        verbose_name=_('position'),
        default=0
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=150
    )
    owner = models.ForeignKey(
        verbose_name=_('owner'),
        to=Gamer,
        on_delete=models.RESTRICT
    )
    coords = ArrayField(
        verbose_name=_('coordinats'),
        base_field=models.PositiveIntegerField(default=0),
        size=3
    )
    level = models.PositiveIntegerField(
        verbose_name=_('level'),
        default=0
    )
    props = models.JSONField(
        verbose_name=_('props'),
        null=True,
        blank=True
    )
    expired_date = models.DateTimeField(
        verbose_name=_('expired date'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('game object')
        verbose_name_plural = _('game object')
        ordering = ('obj_type', 'order_number')

    def __str__(self) -> str:
        return (
            (f"{self.name}, state:{self.state}, "
             f"owner:{self.owner.user.username}, "
             f"level: {self.level}")
        )
