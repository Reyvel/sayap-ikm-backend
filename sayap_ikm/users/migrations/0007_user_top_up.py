# Generated by Django 2.2.7 on 2020-02-10 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='top_up',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
