from rest_framework import serializers
from .models import Member, RegisterMember
from django.core.exceptions import ObjectDoesNotExist


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['cpf', 'pontos', 'creation']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = RegisterMember
        fields = ['cpf', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        register = RegisterMember()
        cpf = self.validated_data['cpf']
        try:
            cpf2 = RegisterMember.objects.get(cpf=cpf)
        except ObjectDoesNotExist:
            register.cpf = cpf
            register.save()

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError("passwords must match")
        else:
            register.password = password
            if password.isnumeric():
                raise serializers.ValidationError("senha tem que ter:, letras e pelo menos 6 dígitos")

            if password.isalpha():
                raise serializers.ValidationError("senha tem que ter: números, e pelo menos 6 dígitos")

            if len(password) <= 5:
                raise serializers.ValidationError("senha tem que ter: números, letras e ")
            else:
                register.save()


class PasswordChange(serializers.ModelSerializer):
    new_password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = RegisterMember
        fields = ['cpf', 'new_password2', 'new_password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        cpf = RegisterMember.objects.get(cpf=self.validated_data['cpf'])

        new_password = self.validated_data['new_password']
        new_password2 = self.validated_data['new_password2']

        if new_password != new_password2:
            raise serializers.ValidationError("passwords must match")
        else:
            cpf.password = new_password
            if new_password.isnumeric():
                raise serializers.ValidationError("senha tem que ter:, letras e pelo menos 6 dígitos")

            if new_password.isalpha():
                raise serializers.ValidationError("senha tem que ter: números, e pelo menos 6 dígitos")

            if len(new_password) <= 5:
                raise serializers.ValidationError("senha tem que ter: números, letras e ")
            else:
                cpf.save()
