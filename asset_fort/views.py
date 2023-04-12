from django.db.models import Q

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

        assets = AssetModel.objects.filter(company__in=company, is_active=True)
        serializer = AssetDetailSerializer(assets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)   

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = self.request.user

        try:
            company = CompanyModel.objects.filter(user=user)
        except Exception:
            return Response({'error': 'Company not found'}, status = status.HTTP_400_BAD_REQUEST)

        assets = AssetModel.objects.filter(company__in=company, pk=pk, is_active=True)
        serializer = self.get_serializer(assets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    
class AssetIssuedViewSet(viewsets.ModelViewSet):
    queryset = AssetIssuedModel.objects.all()
    serializer_class = AssetIssuedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(asset_assignee=self.request.user)

    def get_serializer_class(self):
        return AssetIssuedDetailSerializer if self.action in ['list', 'retrieve', 'asset_checked_log'] else AssetIssuedSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user

        try:
            company = CompanyModel.objects.filter(user=user)
        except Exception:
            return Response({'error': 'Company not found'}, status = status.HTTP_400_BAD_REQUEST)

        assets = AssetIssuedModel.objects.filter(
                Q(asset__company__in=company)
            )
        serializer = self.get_serializer(assets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def asset_bought_by_employee(self, request, employee_id):
        user = self.request.user

        issued_assets = AssetIssuedModel.objects.filter(
                Q(asset_assigned_to__employee_id = employee_id),
                Q(asset__company__in = CompanyModel.objects.filter(user=user))
            )
        serializer = self.get_serializer(issued_assets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def asset_checked_log(self, request):
        user = self.request.user

        try:
            company = CompanyModel.objects.filter(user=user)
        except Exception:
            return Response({'error': 'Company not found'}, status = status.HTTP_400_BAD_REQUEST)

        assets = AssetIssuedModel.objects.filter(
                Q(asset__company__in=company), 
                Q(is_active = True) | 
                Q(is_active=False),
                ~Q(is_returned=True)
            )
        serializer = self.get_serializer(assets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def asset_return_log(self, request):
        user = self.request.user

        try:
            company = CompanyModel.objects.filter(user=user)
        except Exception:
            return Response({'error': 'Company not found'}, status = status.HTTP_400_BAD_REQUEST)

        assets = AssetIssuedModel.objects.filter(
                Q(asset__company__in=company), 
                Q(is_returned=True)
            )
        serializer = AssetReturnSerializer(assets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# class AssetLogViewSet(viewsets.ModelViewSet):
#     queryset = AssetLogModel.objects.all()
#     serializer_class = AssetLogSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_serializer_class(self):
#         return AssetLogDetailSerializer if self.action in ['list', 'retrieve'] else AssetLogSerializer

#     def list(self, request, *args, **kwargs):
#         user = self.request.user

#         try:
#             company = CompanyModel.objects.filter(user=user)
#         except Exception:
#             return Response({'error': 'Company not found'}, status = status.HTTP_400_BAD_REQUEST)

#         asset_logs = AssetLogModel.objects.filter(asset__company__in=company)
#         serializer = self.get_serializer(asset_logs, many=True)

#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def create_log(self, request, *args, **kwargs):
#         data = request.data
#         assets = AssetIssuedModel.objects.filter(status='RETURNED')

#         if assets.exists():
#             for obj in assets:
#                 log_obj = AssetLogModel.objects.create(
#                     issue_no = obj.issue_no,
#                     asset = obj.asset,
#                     asset_assignee = obj.asset_assignee,
#                     asset_assigned_to = obj.asset_assigned_to,
#                     assign_date = obj.assign_date,
#                     return_date = obj.return_date,
#                     note = obj.note,
#                     asset_conditions = data['asset_conditions'],
#                     asset_condition_description = data['asset_condition_description']
#                 )
#                 self.delete_asset(obj)
#             return Response({'detail': 'Log Created'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'detail': 'No asset to return'}, status=status.HTTP_404_NOT_FOUND)        

#     def delete_asset(self, items):
#         return items.delete()

