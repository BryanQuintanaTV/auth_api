from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

# Include the REST routes:
# - {URL}/api/v1/users/
# - {URL}/api/v1/users/{id}/
router = DefaultRouter()
router.register(r'v1/users', UserViewSet, basename='user')

# Nos basamos en el patron:
# - {URL}/api/v1/login/
# - {URL}/api/v1/token/refresh/     (Usando las herramientas de SimpleJWT)
# - {URL}/api/v1/token/access/      (Usando las herramientas de SimpleJWT)
urlpatterns = [
    path('', include(router.urls)),
    path('v1/login/', LoginView.as_view(), name='login'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/token/access/', TokenVerifyView.as_view(), name='token_verify'),
]