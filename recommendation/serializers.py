from rest_framework import serializers, request
from .models import Recommend


class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = "__all__"
        read_only_fields = ['cupom', 'expires', 'hoje']
