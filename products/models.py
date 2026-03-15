from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="🥦", blank=True, help_text="Emoji o clase de Bootstrap (bi-...)")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogramo'),
        ('libra', 'Libra'),
        ('unidad', 'Unidad'),
        ('combo', 'Combo'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='unidad')
    stock = models.IntegerField()
    min_stock = models.IntegerField(default=5)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_on_offer = models.BooleanField(default=False, verbose_name="¿Está en oferta?")
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Precio de oferta")
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def low_stock(self):
        try:
            return int(self.stock) <= int(self.min_stock)
        except Exception:
            return False

    @property
    def wa_link(self):
        from inventory.models import SiteConfiguration
        from django.utils.http import urlencode
        from django.conf import settings
        
        wa_number = getattr(settings, "WHATSAPP_NUMBER", "")
        config = SiteConfiguration.objects.first()
        if config and config.whatsapp_number:
            wa_number = config.whatsapp_number
            
        if not wa_number:
            return ""
            
        price = self.offer_price if self.is_on_offer and self.offer_price else self.price
        text = f"Hola, quiero comprar 1 x {self.name} por ${price}"
        return f"https://wa.me/{wa_number}?{urlencode({'text': text})}"
