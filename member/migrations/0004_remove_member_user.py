# Generated by Django 3.2.9 on 2021-12-17 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_alter_member_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='user',
        ),
    ]