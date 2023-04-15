from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from ...models import (
    Gamer,
    GameObject
)

from .sciences import sciences


User = get_user_model()


class Command(BaseCommand):
    help = "Generate meta data for game."

    def _create_test_user(self) -> User:
        user = User.objects.get_or_create(
            username='test1',
            email='test1@mail.ru',
        )[0]
        user.is_active = True
        user.set_password('12345')
        user.save()

        return user

    def _create_test_gamer(self, user: User) -> Gamer:
        gamer = Gamer.objects.get_or_create(
            user=user
        )[0]

        return gamer

    def _init_sciences(self, gamer: Gamer) -> None:
        order_number = 1
        for s in sciences:
            game_object = GameObject.objects.get_or_create(
                name=s['name'],
                owner=gamer,
                coords=[0, 0, 0]
            )[0]

            s['id'] = game_object.id

        for s in sciences:
            game_object = GameObject.objects.get(id=s['id'])

            dep_ids = []
            for name in s['dependencies']:
                dep_object = GameObject.objects.get(name=name)
                dep_ids.append({
                    'id': dep_object.id,
                    'level': 0,
                })
            game_object.state = GameObject.STATE_READY
            game_object.obj_type = GameObject.TYPE_RESEARCH
            game_object.order_number = order_number
            order_number += 1
            game_object.props = {
                'dependencies': dep_ids
            }
            game_object.save()

    def handle(self, *args, **kwargs):
        user = self._create_test_user()
        gamer = self._create_test_gamer(user)
        self._init_sciences(gamer)
