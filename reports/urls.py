from django.urls import path
from .views import admin_dashboard, export_monthly_excel

urlpatterns = [
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/export/excel/', export_monthly_excel, name='export_monthly_excel'),
]
