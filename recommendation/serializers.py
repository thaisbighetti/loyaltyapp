from datetime import timedelta, date

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import serializers, request
from rest_framework.response import Response

from member.models import Member
from .models import Recommend


class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = "__all__"
        read_only_fields = ['cupom', 'expires', 'hoje']

    # try:
    #     coupon_target = Member.objects.get(cpf=self.validated_data['target'])
    #     coupon = Recommend.objects.get(target=self.validated_data['target'])
    #
    #
    #     timedelta(days=(coupon - date.today()))
    #     if timedelta(days=(coupon - date.today())) > 30:
    #         return serializers.ValidationError('Cupom expirou')
    #     else:
    #         new_coupon.save()
    # except Member.DoesNotExist:
    #     return Response({'O usuário de origem não existe': coupon_target})
    # except Recommend.DoesNotExist:
    #     return Response({''})

    # if coupon_target != coupon_source:
    #
    # else:
    #     return Response({'Você não pode um cupom para você mesmo'})

# Um indicador pode ter várias (ilimitadas) indicações;
# Uma pessoa só pode ser indicada por um único indicador. Dois usuários diferentes
# não podem indicar a mesma pessoa;
# O usuário não pode se indicar (ser indicada e indicadora para a mesma indicação);
# A indicação é valida por 30 dias. Após isso, o indicado não pode aceitar a indicação
# e outro membro pode realizar a indicação;
# Uma vez que a indicação seja aceita, a pessoa que foi indicada não pode ser indicada de novo;
