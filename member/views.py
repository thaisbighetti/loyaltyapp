import http

from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from member.models import Member, Register
from .serializers import MemberSerializer, RegistrationSerializer, PasswordChange


class RegisterMember(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    queryset = RegistrationSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                member = Member.objects.create(cpf=request.data['cpf'], )
                member.save()
                return HttpResponseRedirect(redirect_to=f'http://127.0.0.1:8000/member/{request.data["cpf"]}')
        return Response({'CPF já existe'}, status=status.HTTP_400_BAD_REQUEST)


class MemberList(generics.ListAPIView):
    serializer_class = MemberSerializer
    queryset = MemberSerializer

    def list(self, request, cpf):
        member = get_object_or_404(Member, pk=cpf)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, cpf):
        member = get_object_or_404(Member, pk=cpf)
        serializer = MemberSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
        return Response({'Usuário atualizado:': serializer.data}, status=http.HTTPStatus.OK)

    def delete(self, request, cpf):
        member = get_object_or_404(Member, pk=cpf)
        register = get_object_or_404(Register, pk=cpf)
        register.delete()
        member.delete()
        return Response(status=http.HTTPStatus.NO_CONTENT)


class PasswordChange(generics.ListAPIView):
    serializer_class = PasswordChange
    queryset = PasswordChange

    def list(self, request, cpf):
        seila = get_object_or_404(Register, pk=cpf)
        serializer = self.serializer_class(seila)
        return Response(serializer.data)

    def put(self, request, cpf):
        seila = get_object_or_404(Register, pk=cpf)
        serializer = self.serializer_class(seila, data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
        return Response({'Usuário atualizado:': serializer.data}, status=http.HTTPStatus.OK)
