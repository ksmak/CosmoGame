# Generated by Django 4.1.7 on 2023-04-07 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_gameobject_order_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gameobject',
            options={'ordering': ('obj_type', 'order_number'), 'verbose_name': 'game object', 'verbose_name_plural': 'game object'},
        ),
        migrations.AddField(
            model_name='gameobject',
            name='obj_type',
            field=models.PositiveIntegerField(choices=[(0, 'Unknown'), (1, 'Research')], default=0, verbose_name='object type'),
        ),
    ]
