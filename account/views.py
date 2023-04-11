from django.shortcuts import render

from rest_framework import generics, viewsets, status, permissions, authentication
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes=[JWTAuthentication, authentication.BasicAuthentication]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_class(self):
        return CompanyDetailSerializer if self.action in ['list', 'retrieve'] else CompanySerializer
    
    def list(self, request, *args, **kwargs):
        user = request.user
        try:
            company = CompanyModel.objects.get(user=user)
        except Exception:
            return Response({'error': 'company not found'}, status= status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(company)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = request.user
        try:
            company = CompanyModel.objects.get(user=user, pk=pk)
        except Exception:
            return Response({'error': 'company not found'}, status= status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(company)

        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeModel.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes=[JWTAuthentication, authentication.BasicAuthentication]

    def get_serializer_class(self):
        return EmployeeDetailsSerializer if self.action in ['list', 'retrieve'] else EmployeeSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        try:
            company = CompanyModel.objects.get(user=user)
        except Exception:
            return Response({'error': 'company not found'}, status= status.HTTP_404_NOT_FOUND)

        employee = EmployeeModel.objects.filter(company=company)

        serializer = self.get_serializer(employee, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = request.user

        try:
            employee = EmployeeModel.objects.get(company__user=user, pk=pk)
        except Exception:
            return Response({'error': 'employee not found'}, status= status.HTTP_404_NOT_FOUND)    

        serializer = self.get_serializer(employee)

        return Response(serializer.data, status=status.HTTP_200_OK)