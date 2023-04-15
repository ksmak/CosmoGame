from asgiref.sync import async_to_sync
from django.contrib.auth.models import AnonymousUser

from channels.exceptions import DenyConnection
from channels.generic.websocket import JsonWebsocketConsumer

from .tasks import start_progress


class ProgressConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.username = None
        self.game_group_name = None
        self.user = None

    def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.game_group_name = f'game_user_{self.username}'

        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("User does not exists.")

        self.user = self.scope['user']

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name,
        )

    def receive_json(self, content):
        message = content['message']

        if message == 'progress':
            async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'type': 'progress',
                    'game_object_id': content['game_object_id'],
                }
            )

    def progress(self, event):
        start_progress.delay(
            self.game_group_name,
            self.user.id,
            event['game_object_id']
        )

    def start_progress_result(self, event):
        self.send_json(event)

    def end_progress_result(self, event):
        self.send_json(event)
