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

   
