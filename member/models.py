from django.core.validators import RegexValidator
from django.db import models
from localflavor.br.models import BRCPFField, BRPostalCodeField
from phonenumber_field.modelfields import PhoneNumberField


class Member(models.Model):
    cpf = BRCPFField('CPF', help_text='Formato: 00011122233', primary_key=True, validators=[RegexValidator(regex="^.{11}$")])
    name = models.CharField(max_length=255, verbose_name='Nome')
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(region='BR', help_text='Formato DDD + Número', verbose_name='Telefone')
    address = models.CharField(max_length=50, verbose_name='Endereço', blank=True)
    zipcode = BRPostalCodeField(help_text='Formato 00000-000', verbose_name='CEP', blank=True)
    points = models.PositiveIntegerField(default=5000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cpf)
