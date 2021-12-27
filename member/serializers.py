import logging
from datetime import date
from django.utils import timezone
from rest_framework import serializers
from coupon.models import Coupon
from .models import Member
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

"""
Made 2 serializers for Member. First serializer is a basic serializer, second is to validate the coupon"
"""


class MemberSerializer(serializers.ModelSerializer):

    """
    Serializer for Member.
    """

    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['cpf', 'points', 'created']


class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for Member.
    Charfield to validate coupon because I do not want save coupon in db, just check if it exists, if not exists, raise
    a validation error.
    If it exists:
    - Check if its valid by timedelta between date was created and today,
      if < -30, coupon is valid, if is not valid, raise a validation error.
    """

    coupon = serializers.CharField(max_length=255)

    class Meta:
        model = Member
        fields = ['cpf', 'coupon']

    def save(self):
        try:
            Member.objects.get(cpf=self.validated_data['cpf'])
        except ObjectDoesNotExist:
            pass

        try:
            validate_coupon = Coupon.objects.get(coupon=self.validated_data['coupon'])
            logger.info(f'{timezone.now()} | 102 | Checking if coupon is valid |')
            if validate_coupon.target == self.validated_data['cpf']:
                timedelta_coupon = validate_coupon.created - date.today()
                if timedelta_coupon.days >= -30:
                    logger.info(f'{timezone.now()} | 102 | Coupon is valid |')
                    source = Member.objects.get(cpf=validate_coupon.source)
                    source.points += 500
                    source.save()
                else:
                    logger.error(f'{timezone.now()}| 400 |Something went wrong | Coupon is expired |{timedelta_coupon}')
                    raise serializers.ValidationError({'Cupom Expirado'})
            else:
                logger.info(f'{timezone.now()} | 400 |Something went wrong | CPF not found |')
                raise serializers.ValidationError('CPF não encontrado')
        except ObjectDoesNotExist:
            logger.error(f'{timezone.now()} | 400 |Something went wrong | Coupon not found |')
            raise serializers.ValidationError({'Cupom não encontrado'})
