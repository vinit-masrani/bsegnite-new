# Generated by Django 2.1.4 on 2019-01-12 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AddField(
            model_name='profile',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
