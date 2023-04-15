from typing import Any
from datetime import timedelta

from django.conf import settings
from asgiref.sync import async_to_sync
from django.utils import timezone, dateformat

from celery import shared_task
from celery.exceptions import Ignore

from channels.layers import get_channel_layer

from main.models import (
    Gamer,
    GameObject
)


@shared_task(ignore_result=True)
def start_progress(*args: Any):
    game_group_name = args[0]
    user_id = args[1]
    game_object_id = args[2]

    channel_layer = get_channel_layer()
    channel_name = game_group_name

    gamer = Gamer.objects.filter(user=user_id).first()

    if not gamer:
        async_to_sync(channel_layer.group_send)(channel_name, {
            'type': 'start_progress_result',
            'user_id': user_id,
            'game_object_id': game_object_id,
            'message': "Task <start_progress> failed: Gamer not found.",
            'result': False
        })
        raise Ignore()

    game_object = GameObject.objects.filter(
        owner=gamer.id,
        id=game_object_id
    ).first()

    if not game_object:
        async_to_sync(channel_layer.group_send)(channel_name, {
            'type': 'start_progress_result',
            'user_id': user_id,
            'game_object_id': game_object_id,
            'message': "Task <start_progress> failed: GameObject not found.",
            'result': False
        })
        raise Ignore()

    if game_object.state != GameObject.STATE_READY:
        async_to_sync(channel_layer.group_send)(channel_name, {
            'type': 'start_progress_result',
            'user_id': user_id,
            'game_object_id': game_object_id,
            'message': (
                "Task <start_progress> failed: GameObject is not"
                " ready."
            ),
            'result': False
        })
        raise Ignore()

    for depence in game_object.props['dependencies']:
        obj = GameObject.objects.filter(id=depence['id']).first()

        if not obj:
            async_to_sync(channel_layer.group_send)(channel_name, {
                'type': 'start_progress_result',
                'user_id': user_id,
                'game_object_id': game_object_id,
                'message': (
                    "Task <start_progress> failed: Depence GameObject not"
                    " found."
                ),
                'result': False
            })
            raise Ignore()

        if (obj.level + int(depence['level'])) < game_object.level:
            async_to_sync(channel_layer.group_send)(channel_name, {
                'type': 'start_progress_result',
                'user_id': user_id,
                'game_object_id': game_object_id,
                'message': (
                    "Task <start_progress> failed: The level of the dependent"
                    " game_object is less than necessary."
                ),
                'ressult': False
            })
            raise Ignore()

    expired_date = timezone.now() + \
        timedelta(seconds=settings.START_TIMEDELTA * (game_object.level + 1))

    game_object.state = GameObject.STATE_IN_PROGRESS
    game_object.expired_date = expired_date
    game_object.save(update_fields=['state', 'expired_date'])

    async_to_sync(channel_layer.group_send)(channel_name, {
        'type': 'start_progress_result',
        'user_id': user_id,
        'game_object_id': game_object_id,
        'message': 'Task <start_progress> done.',
        'result': True,
        'expired_date': dateformat.format(
            expired_date, settings.DATETIME_FORMAT)
    })

    end_progress.apply_async(
        (game_group_name, user_id, game_object_id),
        eta=expired_date
    )


@shared_task(ignore_result=True)
def end_progress(*args: Any):
    game_group_name = args[0]
    user_id = args[1]
    game_object_id = args[2]

    channel_layer = get_channel_layer()
    channel_name = game_group_name

    gamer = Gamer.objects.filter(user=user_id).first()

    if not gamer:
        async_to_sync(channel_layer.group_send)(channel_name, {
            'type': 'end_progress_result',
            'user_id': user_id,
            'game_object_id': game_object_id,
            'message': "Task <end_progress> failed: Gamer not found.",
            'result': False
        })
        raise Ignore()

    game_object = GameObject.objects.filter(
        owner=gamer.id,
        id=game_object_id
    ).first()

    if not game_object:
        async_to_sync(channel_layer.group_send)(channel_name, {
            'type': 'end_progress_result',
            'user_id': user_id,
            'game_object_id': game_object_id,
            'message': "Task <end_progress> failed: GameObject not found.",
            'result': False
        })
        raise Ignore()

    if game_object.state != GameObject.STATE_IN_PROGRESS:
        async_to_sync(channel_layer.group_send)(channel_name, {
            'type': 'end_progress_result',
            'user_id': user_id,
            'game_object_id': game_object_id,
            'message': (
                "Task <end_progress> failed: GameObject is not"
                " in_progress."
            ),
            'result': False
        })
        raise Ignore()

    game_object.state = GameObject.STATE_READY
    game_object.level = game_object.level + 1
    game_object.expired_date = None
    game_object.save(update_fields=('state', 'level', 'expired_date'))

    async_to_sync(channel_layer.group_send)(channel_name, {
        'type': 'end_progress_result',
        'user_id': user_id,
        'game_object_id': game_object_id,
        'message': 'Task <end_progress> done.',
        'result': True
    })
