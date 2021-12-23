from datetime import timedelta, date
import uuid

from django.core.validators import RegexValidator
from django.db import models
from localflavor.br.models import BRCPFField


def valid_to():
    return date.today() + timedelta(days=30)


class Coupon(models.Model):
    source = BRCPFField(validators=[RegexValidator(regex="^.{11}$")])
    target = BRCPFField(validators=[RegexValidator(regex="^.{11}$")])
    coupon = models.UUIDField(default=uuid.uuid4)
    created = models.DateField(default=date.today())
    expires = models.DateField(default=valid_to)

    def __str__(self):
        return f'De: {self.source} | Para: {self.target}'



