from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register("category", CategoryViewSet, basename="category")
router.register('issued', AssetIssuedViewSet, basename="issued")
# router.register('asset-log', AssetLogViewSet, basename="log")
router.register('', AssetViewSet, basename="asset")

urlpatterns = [

    path('asset-check-out/', AssetIssuedViewSet.as_view({'get': 'asset_checked_log'}), name='asset_checked_log'),
    path('asset-return-out/', AssetIssuedViewSet.as_view({'get': 'asset_return_log'}), name='asset_return_log'),
    path('asset-bought/<employee_id>/', AssetIssuedViewSet.as_view({'get': 'asset_bought_by_employee'}), name='asset_bought_by_employee'),

] + router.urls