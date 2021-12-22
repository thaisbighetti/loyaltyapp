import logging
from datetime import date
from django.utils import timezone
from rest_framework import serializers
from member.models import Member
from .models import Coupon

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'
        read_only_fields = ['coupon', 'expires', 'created']

    def save(self):
        cpf = self.validated_data['source']
        if not Member.objects.filter(cpf=cpf).exists():
            logger.error(f'{timezone.now()} | 400 | Source does not exist |')
            raise serializers.ValidationError(f"O usuário de origem não existe: {self.validated_data['source']}")
        else:
            try:
                Member.objects.get(cpf=self.validated_data['target'])
                logger.error(f'{timezone.now()} | 400 | Target already exists |')
                raise serializers.ValidationError('Esse usuário já tem cadastro')
            except Member.DoesNotExist:
                if Coupon.objects.filter(target=self.validated_data['target']).exists():
                    validate_target = Coupon.objects.filter(target=self.validated_data['target']).last()
                    timedelta_coupon = validate_target.created - date.today()
                    if timedelta_coupon.days < -30:
                        pass
                    else:
                        raise serializers.ValidationError('Já foi gerado um cupom pra esse cpf nos últimos 30 dias')
