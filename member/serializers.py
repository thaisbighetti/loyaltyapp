from datetime import date

from rest_framework import serializers
from .models import Member, Register
from django.core.exceptions import ObjectDoesNotExist


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['cpf', 'pontos', 'creation']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    coupon = serializers.CharField(max_length=100)

    class Meta:
        model = Register
        fields = ['cpf', 'password', 'password2', 'coupon']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        register = Register()
        cpf = self.validated_data['cpf']
        try:
            cpf2 = Register.objects.get(cpf=cpf)
        except ObjectDoesNotExist:
            register.cpf = cpf
            register.save()

        validate_coupon = Recommend.objects.get(coupon=self.validated_data['coupon'])
        if validate_coupon.cpf == self.validated_data['cpf']:
            if validate_coupon is not None:
                validate = validate_coupon.hoje - date.today()
                if validate.days <= 30:
                    pass
                else:
                    raise serializers.ValidationError({'Cupom Expirado'})
            else:
                raise serializers.ValidationError({'Cupom não encontrado'})
        else:
            raise serializers.ValidationError({'Cpf nao encontrado'})

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
        model = Register
        fields = ['cpf', 'new_password2', 'new_password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        cpf = Register.objects.get(cpf=self.validated_data['cpf'])

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
