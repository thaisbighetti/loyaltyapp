import logging
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import generics, status
from member.models import Member
from .serializers import MemberSerializer, RegistrationSerializer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MainPage(generics.ListAPIView):
    def list(self, request):
        urls = {'Tem um cupom e quer fazer seu cadastro? Clique nesse link ->': 'https://thaisbighetti-loyaltyapp.herokuapp.com/register/',
                'Já é cadastrado e quer indicar alguem? Clique nesse link ->': 'https://thaisbighetti-loyaltyapp.herokuapp.com/coupon/',
                'Pesquisar um membro': 'https://thaisbighetti-loyaltyapp.herokuapp.com/search/member/',
                'Pesquisar um cupom': 'https://thaisbighetti-loyaltyapp.herokuapp.com/search/coupon/',
                }
        return Response(urls)


class RegisterMember(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = RegistrationSerializer

    def create(self, request):
        logger.info(f'{timezone.now()} | Request: POST | Member |')
        serializer = self.serializer_class(data=request.data)
        logger.info(f'{timezone.now()} | 102 | Checking if request data is valid |')
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                member = Member.objects.create(cpf=request.data['cpf'], )
                member.save()
                logger.info(f'{timezone.now()}| 200 | Success, saving and redirecting to member page |')
                return HttpResponseRedirect(redirect_to=f'/member/{request.data["cpf"]}')
        logger.error(f'{timezone.now()} | 400 |Something went wrong | CPF already exists |')
        return Response({'CPF já existe'}, status=status.HTTP_400_BAD_REQUEST)


class MemberView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemberSerializer
    queryset = MemberSerializer

    def get(self, request, cpf):
        get_member = get_object_or_404(Member, pk=cpf)
        serializer = MemberSerializer(get_member)
        return Response(serializer.data)

    def put(self, request, cpf):
        get_member = get_object_or_404(Member, pk=cpf)
        serializer = MemberSerializer(get_member,data=request.data, partial=True)
        logger.info(f'{timezone.now()} | 102 | Checking if request data is valid | ')
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                logger.info(f'{timezone.now()}| 200 | Changes made sucessfully |')
                return HttpResponseRedirect(redirect_to=f'/member/{cpf}',)
        return Response({'Usuário não pode ser atualizado:': 'Nome e Telefone são campos obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cpf):
        get_member = get_object_or_404(Member, pk=cpf)
        get_member.delete()
        logger.info(f'{timezone.now()}| 200 | Deleted member sucessfully |')
        return HttpResponseRedirect(redirect_to=f'/')


class MemberList(generics.ListAPIView):
    model = Member
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cpf']



