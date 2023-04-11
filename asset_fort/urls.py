from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register("category", CategoryViewSet, basename="category")
router.register('', AssetViewSet, basename="asset")

urlpatterns = [

] + router.urls