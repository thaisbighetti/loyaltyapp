from datetime import timedelta, date
import uuid

from django.contrib import admin
from django.db import models
from localflavor.br.models import BRCPFField


# Create your models here.
def valid_to():
    return date.today() + timedelta(days=30)


class Recommend(models.Model):
    source = BRCPFField()
    target = BRCPFField()
    cupom = models.UUIDField(default=uuid.uuid4)
    hoje = models.DateField(default=date.today())
    expires = models.DateField(default=valid_to)

    def __str__(self):
        return f'De: {self.source} | Para: {self.target}'



