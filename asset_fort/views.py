from rest_framework import viewsets, status, permissions, authentication
from rest_framework.response import Response

from .models import *
from .serializers import *


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = AssetModel.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_class(self):
        return AssetDetailSerializer if self.action =='list' else AssetSerializer
    
    def list(self, request, *args, **kwargs):
        user = self.request.user

        try:
            company = CompanyModel.objects.filter(user=user)
        except Exception:
            return Response({'error': 'Company not found'}, status = status.HTTP_400_BAD_REQUEST)

        assets = AssetModel.objects.filter(company__in=company)
        serializer = AssetDetailSerializer(assets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)   

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = self.request.user

        try:
            company = CompanyModel.objects.filter(user=user)
        except Exception:
            return Response({'error': 'Company not found'}, status = status.HTTP_400_BAD_REQUEST)

        assets = AssetModel.objects.filter(company__in=company, pk=pk)
        serializer = AssetDetailSerializer(assets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    
class AssetIssuedViewSet(viewsets.ModelViewSet):
    queryset = AssetIssuedModel.objects.all()
    serializer_class = AssetIssuedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(asset_assignee=self.request.user)

    def get_serializer_class(self):
        return AssetIssuedDetailSerializer if self.action in ['list', 'retrieve'] else AssetIssuedSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user

        try:
            company = CompanyModel.objects.filter(user=user)
        except Exception:
            return Response({'error': 'Company not found'}, status = status.HTTP_400_BAD_REQUEST)

        assets = AssetIssuedModel.objects.filter(asset__company__in=company)
        serializer = self.get_serializer(assets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

