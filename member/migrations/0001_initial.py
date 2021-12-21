# Generated by Django 3.2.9 on 2021-12-20 19:29

from django.db import migrations, models
import localflavor.br.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('cpf', localflavor.br.models.BRCPFField(help_text='Formato: 00011122233', max_length=14, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(help_text='Formato DDD + Número', max_length=128, region='BR', verbose_name='Telefone')),
                ('endereço', models.CharField(max_length=50)),
                ('cep', localflavor.br.models.BRPostalCodeField(help_text='Formato 00000-000', max_length=9)),
                ('pontos', models.PositiveIntegerField(default=5000)),
                ('creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('cpf', localflavor.br.models.BRCPFField(help_text='Formato: 00011122233', max_length=14, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
