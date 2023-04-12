from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register("category", CategoryViewSet, basename="category")
router.register('issued', AssetIssuedViewSet, basename="issued")
router.register('asset-log', AssetLogViewSet, basename="log")
router.register('', AssetViewSet, basename="asset")

urlpatterns = [

] + router.urls