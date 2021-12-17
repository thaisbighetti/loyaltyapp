from datetime import timedelta, date
import uuid
from django.db import models
from localflavor.br.models import BRCPFField


# Create your models here.
def valid_to():
    return date.today() + timedelta(days=30)


class Recommend(models.Model):
    source = BRCPFField()
    target = BRCPFField()
    cupom = models.UUIDField(default=uuid.uuid4)
    today = models.DateField(default=date.today())
    expires = models.DateField(default=valid_to)
