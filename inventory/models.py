from django.db import models

class SiteConfiguration(models.Model):
    whatsapp_number = models.CharField(max_length=20, default="573001234567", verbose_name="Número de WhatsApp")
    business_hours = models.CharField(max_length=200, default="Lun-Sáb 8:00-18:00 · Dom 8:00-13:00", verbose_name="Horarios de atención")
    facebook_url = models.URLField(default="https://facebook.com/tu_pagina", verbose_name="URL de Facebook")
    instagram_url = models.URLField(default="https://instagram.com/tu_perfil", verbose_name="URL de Instagram")
    
    # Mensajes automáticos
    welcome_message = models.TextField(default="¡Hola! Bienvenido a MANJARES DEL CAMPO. ¿En qué podemos ayudarte?", verbose_name="Mensaje de bienvenida")
    order_wa_prefix = models.CharField(max_length=100, default="Hola!, quiero hacer este pedido de Manjares del Campo", verbose_name="Prefijo de pedido WhatsApp")
    
    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuraciones del Sitio"

    def __str__(self):
        return "Configuración Global de Manjares del Campo"

    def save(self, *args, **kwargs):
        # Asegurar que solo exista un registro
        if not self.pk and SiteConfiguration.objects.exists():
            return
        return super().save(*args, **kwargs)
