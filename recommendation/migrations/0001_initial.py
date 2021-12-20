# Generated by Django 3.2.9 on 2021-12-20 13:29

import datetime
from django.db import migrations, models
import localflavor.br.models
import recommendation.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', localflavor.br.models.BRCPFField(max_length=14)),
                ('target', localflavor.br.models.BRCPFField(max_length=14)),
                ('cupom', models.UUIDField(default=uuid.uuid4)),
                ('today', models.DateField(default=datetime.date(2021, 12, 20))),
                ('expires', models.DateField(default=recommendation.models.valid_to)),
            ],
        ),
    ]
