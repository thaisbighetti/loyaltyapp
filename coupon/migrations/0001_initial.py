# Generated by Django 4.0 on 2021-12-27 11:58

import coupon.models
import datetime
import django.core.validators
from django.db import migrations, models
import localflavor.br.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', localflavor.br.models.BRCPFField(max_length=14, validators=[django.core.validators.RegexValidator(regex='^.{11}$')])),
                ('target', localflavor.br.models.BRCPFField(max_length=14, validators=[django.core.validators.RegexValidator(regex='^.{11}$')])),
                ('coupon', models.UUIDField(default=uuid.uuid4)),
                ('created', models.DateField(default=datetime.date(2021, 12, 27))),
                ('expires', models.DateField(default=coupon.models.valid_to)),
            ],
        ),
    ]
