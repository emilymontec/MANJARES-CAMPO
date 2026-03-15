from django.contrib import admin
from .models import SiteConfiguration

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "whatsapp_number", "business_hours")
    
    def has_add_permission(self, request):
        # Impedir agregar más si ya existe uno
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Impedir borrar el único registro
        return False
