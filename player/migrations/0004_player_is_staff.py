# Generated by Django 4.0.3 on 2022-03-24 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_remove_player_is_stuff_alter_player_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
