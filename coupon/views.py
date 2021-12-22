import logging
from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Coupon
from .serializers import CouponSerializer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Generatecoupon(generics.CreateAPIView):
    serializer_class = CouponSerializer
    queryset = CouponSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        logger.info(f'{timezone.now()} | Checking if serializer is valid | ')
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                coupon = Coupon.objects.create(source=request.data['source'], target=request.data['target'])
                logger.info(f'{timezone.now()} | Request data is valid |')
                logger.info(f'{timezone.now()} | Saving coupon ')
                coupon.save()
                logger.info(f'{timezone.now()} | 200 | Coupon saved ')
                return Response(f'Cupom de {coupon.source} para {coupon.target} gerado com sucesso!: {coupon.coupon}  '
                                f' |  válido de {coupon.created} até {coupon.expires}|', status=status.HTTP_200_OK)
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
