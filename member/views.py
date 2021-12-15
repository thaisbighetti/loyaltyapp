import http

from django.db import transaction
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import generics, status
from member.models import Member, RegisterMember
from .serializers import MemberSerializer, RegistrationSerializer


class MemberList(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    queryset = MemberSerializer

    def list(self, request, ):
        users = Member.objects.all()
        serializer = MemberSerializer(users, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.data['cpf'].isalnum():
                with transaction.atomic():
                    serializer.save()
                return HttpResponseRedirect(redirect_to=f'http://127.0.0.1:8000/user/{request.data["cpf"]}')
            return Response({'Erro': "O CPF deve ser sem ponto e traço"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MemberView(generics.ListAPIView):
    serializer_class = MemberSerializer
    queryset = Member.objects.all()

    def list(self, request, cpf):
        users = Member.objects.filter(cpf=cpf)
        serializer = MemberSerializer(users, many=True)
        return Response(serializer.data)


class RegisterMember(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = RegistrationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
            return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/signup/')
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class VerifyMember(generics.CreateAPIView):
#     serializer_class = VerifyMemberSerializer
#     queryset = VerifyMemberSerializer
#
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             with transaction.atomic():
#                 serializer.save()
#             return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/register/')
#         return Response(status=status.HTTP_400_BAD_REQUEST)
