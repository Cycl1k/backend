from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as views_auth
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from equipment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'), 
    path('api/equipment-type', views.TypeEquipmentAPIView.as_view()),
    path('api/equipment', views.EquipmentAPIView.as_view()),
    path('api/equipment/<int:id>', views.EquipmentAPIViewList.as_view()),
    path('api/user/login', views_auth.obtain_auth_token)
]