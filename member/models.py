import datetime
from django.db import models
from localflavor.br.models import BRCPFField, BRPostalCodeField
from phonenumber_field.modelfields import PhoneNumberField


class RegisterMember(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    cpf = BRCPFField('CPF', help_text='Formato: 00011122233')


class Member(models.Model):
    nome = models.CharField(max_length=255)
    cpf = BRCPFField(help_text='Formato: 00011122233', primary_key=True)
    email = models.EmailField()
    telefone = PhoneNumberField(region='BR', help_text='Formato DDD + Número', verbose_name='Telefone')
    endereço = models.CharField(max_length=50)
    cep = BRPostalCodeField(help_text='Formato 00000-000')
    pontos = models.PositiveIntegerField(default=5000)
    creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cpf
