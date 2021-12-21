import logging
from datetime import date
from django.utils import timezone
from rest_framework import serializers
from coupon.models import Coupon
from .models import Member, Register
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['cpf', 'points', 'created']


class RegistrationSerializer(serializers.ModelSerializer):
    coupon = serializers.CharField(max_length=255)

    class Meta:
        model = Member
        fields = ['cpf', 'coupon']

    def save(self):
        register = Register()
        cpf = self.validated_data['cpf']
        try:
            cpf2 = Register.objects.get(cpf=cpf)
        except ObjectDoesNotExist:
            register.cpf = cpf
            register.save()
        try:
            validate_coupon = Coupon.objects.get(coupon=self.validated_data['coupon'])
            logger.info(f'{timezone.now()} | Checking if coupon is valid')
            if validate_coupon.target == self.validated_data['cpf']:
                if validate_coupon is not None:
                    oi = validate_coupon.created - date.today()
                    if oi.days <= 30:
                        pass
                        logger.error(f'{timezone.now()} | Coupon is valid |')
                        source = Member.objects.get(cpf=validate_coupon.source)
                        source.points += 500
                        source.save()
                    else:
                        logger.error(f'{timezone.now()} |Something went wrong | Coupon is expired')
                        raise serializers.ValidationError({'Cupom Expirado'})
            else:
                logger.info(f'{timezone.now()} | 400 |Something went wrong | CPF not found |')
                raise serializers.ValidationError('CPF não encontrado')
        except ObjectDoesNotExist:
            logger.error(f'{timezone.now()} | 400 |Something went wrong | Coupon not found |')
            raise serializers.ValidationError({'Cupom não encontrado'})




