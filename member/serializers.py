from django.http import HttpResponseRedirect
from rest_framework import serializers
from .models import Member, RegisterMember
from localflavor.br.models import BRCPFField


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['pontos', 'creation']


# class VerifyMemberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RegisterMember
#         fields = ['cpf', ]
#
#     def save(self, **kwargs):
#         membercpf = Member.objects.get(cpf=self.validated_data['cpf'])
#         if membercpf == self.validated_data['cpf']:
#             raise serializers.ValidationError("já existe um cadastro com esse cpf")
#         else:
#             return HttpResponseRedirect(redirect_to='http://127.0.0.1:8000/register/')


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = RegisterMember
        fields = ['cpf', 'username', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        register = RegisterMember(username=self.validated_data['username'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError("passwords must match")
        else:
            register.password = password
            register.save()
            return HttpResponseRedirect
