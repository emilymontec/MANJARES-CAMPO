from django.conf import settings
from decimal import Decimal
from products.models import Product, Category
from inventory.models import SiteConfiguration

def app_context(request):
    """Context processor global para toda la aplicación."""
    
    # 1. Configuración del Sitio (WhatsApp, Redes, etc.)
    config = SiteConfiguration.objects.first()
    if not config:
        config_data = {
            "WHATSAPP_NUMBER": getattr(settings, "WHATSAPP_NUMBER", ""),
            "BUSINESS_HOURS": "Lun-Sáb 8:00-18:00",
            "SOCIAL_FACEBOOK_URL": "#",
            "SOCIAL_INSTAGRAM_URL": "#",
            "WELCOME_MESSAGE": "¡Hola! Bienvenido.",
            "ORDER_WA_PREFIX": "Hola!, quiero hacer este pedido",
        }
    else:
        config_data = {
            "WHATSAPP_NUMBER": config.whatsapp_number,
            "BUSINESS_HOURS": config.business_hours,
            "SOCIAL_FACEBOOK_URL": config.facebook_url,
            "SOCIAL_INSTAGRAM_URL": config.instagram_url,
            "WELCOME_MESSAGE": config.welcome_message,
            "ORDER_WA_PREFIX": config.order_wa_prefix,
        }

    # 2. Resumen del Carrito (Conteo y Total)
    cart = request.session.get("cart", {})
    cart_count = 0
    cart_total = Decimal("0")
    
    if cart:
        for pid, qty in cart.items():
            try:
                # Usamos values para eficiencia
                p = Product.objects.filter(id=int(pid), available=True).values("price").first()
                if p:
                    quantity = max(1, int(qty))
                    cart_count += quantity
                    cart_total += Decimal(str(p["price"])) * quantity
            except (ValueError, TypeError):
                continue
    
    # 3. Datos Globales adicionales
    ctx = {
        "cart_count": cart_count,
        "cart_total": cart_total,
        "categories": Category.objects.all(),
        "today_now": request.user.is_authenticated # Ejemplo de flag útil
    }
    
    ctx.update(config_data)
    return ctx
