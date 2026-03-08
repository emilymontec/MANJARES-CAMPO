from django.urls import path
from .views import admin_dashboard

urlpatterns = [
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
]
