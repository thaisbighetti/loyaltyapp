import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status

from member.models import Member
from .models import Recommend
from .serializers import RecommendSerializer


# Create your views here.

class Generatecoupon(generics.ListCreateAPIView):
    queryset = Recommend.objects.all()
    serializer_class = RecommendSerializer

    def list(self, request):
        queryset = Recommend.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            coupon_source = get_object_or_404(Member, pk=request.data['source'])
            coupon_target = get_object_or_404(Member, pk=request.data['target'])
            if coupon_target == coupon_source:
                return Response({'Você não pode um cupom para você mesmo'})
            else:
                with transaction.atomic():
                    serializer.save()
                    return Response(serializer.data)
        return Response(status.HTTP_400_BAD_REQUEST)
