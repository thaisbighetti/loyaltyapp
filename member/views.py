import logging
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from member.models import Member
from .serializers import MemberSerializer, RegistrationSerializer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MainPage(generics.ListAPIView):
    def list(self, request):
        urls = {'Tem um cupom? Clique nesse link ->': 'http://127.0.0.1:8000/register/',
                'Já é cadastrado e quer indicar alguem? Clique nesse link ->': 'http://127.0.0.1:8000/coupon/',
                }
        return Response(urls)


class RegisterMember(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = RegistrationSerializer

    def create(self, request):
        logger.info(f'{timezone.now()} | Request: POST |{request.data}')
        serializer = self.serializer_class(data=request.data)
        logger.info(f'{timezone.now()} | Checking if request data is valid |')
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                member = Member.objects.create(cpf=request.data['cpf'], )
                member.save()
                logger.info(f'{timezone.now()}| 201 | Success, saving and redirecting to member page |')
                return HttpResponseRedirect(redirect_to=f'http://127.0.0.1:8000/member/{request.data["cpf"]}')
        logger.info(f'{timezone.now()} | 400 |Something went wrong | CPF already exists |')
        return Response({'CPF já existe'}, status=status.HTTP_400_BAD_REQUEST)


class MemberView(generics.UpdateAPIView):
    serializer_class = MemberSerializer
    queryset = MemberSerializer

    def get(self, request, cpf):
        member = get_object_or_404(Member, pk=cpf)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, cpf):
        member = get_object_or_404(Member, pk=cpf)
        serializer = MemberSerializer(member, data=request.data, partial=True)
        logger.info(f'{timezone.now()} | Checking if request data is valid | ')
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
        logger.info(f'{timezone.now()}| 200 | Changes made sucessfully |')
        return Response({'Usuário atualizado:': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, cpf):
        member = get_object_or_404(Member, pk=cpf)
        member.delete()
        logger.info(f'{timezone.now()}| 200 | Deleted member sucessfully |')
        return Response({'Usuário deletado'})


class MemberList(generics.ListAPIView):
    model = Member
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cpf']



