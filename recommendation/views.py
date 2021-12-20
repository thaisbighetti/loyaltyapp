from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.response import Response
from rest_framework import generics, status
from member.models import Member
from .models import Recommend
from .serializers import RecommendSerializer


class Generatecoupon(generics.CreateAPIView):
    serializer_class = RecommendSerializer
    queryset = RecommendSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                Member.objects.get(cpf=request.data['source'])
            except ObjectDoesNotExist:
                return Response({'O usuário de origem não existe': request.data['source']},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                Member.objects.get(cpf=request.data['target'])
            except Member.DoesNotExist:
                pass

            if request.data['source'] == request.data['target']:
                return Response({'você não pode enviar um cupom pra você mesmo'}, status=status.HTTP_400_BAD_REQUEST)

            elif Member.objects.filter(cpf=request.data['target']).exists():
                return Response({'Esse usuário já tem cadastro'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                target = Recommend.objects.filter(target=request.data['target']).last()
                if target is not None:
                    oi = target.hoje - date.today()
                    if oi.days <= 30:
                        return Response({'Não podemos gerar outro cupom, essa pessoa já foi indicada'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    else:
                        pass
                else:
                    with transaction.atomic():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)
