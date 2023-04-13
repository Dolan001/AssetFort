from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token
    

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.is_staff = True
        user.save()

        return user


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyModel
        fields = '__all__'

        extra_kwargs = {
            'slug': {'read_only': True},
            'user' : {'read_only': True}
            }

class UserSerializer(serializers.ModelSerializer):

    # company = serializers.CharField(source = 'company_user', read_only = True)
    company = CompanySerializer(read_only = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'company')



class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeModel
        fields = '__all__'


class EmployeeDetailsSerializer(serializers.ModelSerializer):

    company = CompanySerializer()
    class Meta:
        model = EmployeeModel
        fields = '__all__'


class CompanyDetailSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    company_employee = EmployeeSerializer(many=True)

    class Meta:
        model = CompanyModel
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionModel
        fields = '__all__'


class SubscriptionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionModel
        fields = '__all__'
