
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('employee', EmployeeViewSet, basename='employee')
router.register('company', CompanyViewSet, basename='company')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("login/token/verify/", TokenVerifyView.as_view()),
] + router.urls