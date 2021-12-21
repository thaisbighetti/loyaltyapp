import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import generics, status
from member.models import Member
from .models import Coupon
from .serializers import CouponSerializer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Generatecoupon(generics.CreateAPIView):
    serializer_class = CouponSerializer
    queryset = CouponSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                Member.objects.get(cpf=request.data['source'])
            except ObjectDoesNotExist:
                logger.error(f'{timezone.now()} | 400 | Source does not exist |')
                return Response({'O usuário de origem não existe': request.data['source']},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                Member.objects.get(cpf=request.data['target'])
            except Member.DoesNotExist:
                pass
            if request.data['source'] == request.data['target']:
                logger.error(f'{timezone.now()} | 400 | Source and target are equal |')
                return Response({'você não pode enviar um cupom pra você mesmo'}, status=status.HTTP_400_BAD_REQUEST)

            elif Member.objects.filter(cpf=request.data['target']).exists():
                logger.error(f'{timezone.now()} | 400 | Target already exists |')
                return Response({'Esse usuário já tem cadastro'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                with transaction.atomic():
                    logger.info(f'{timezone.now()} | Saving |')
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        logger.error(f'{timezone.now()}| 400 | Serializer is not valid |')
        return Response(status.HTTP_400_BAD_REQUEST)


class CouponSearch(generics.ListAPIView):
    model = Coupon
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['source', 'target']
    search_fields = ['source', 'target', 'expires', 'created', 'coupon']


class CouponList(generics.ListAPIView):
    serializer_class = CouponSerializer

    def list(self, request, cpf1, cpf2):
        source = Coupon.objects.get(source=cpf1, target=cpf2)
        serializer = CouponSerializer(source)
        return Response(serializer.data)
