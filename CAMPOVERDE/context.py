from django.conf import settings
from decimal import Decimal
from products.models import Product, Category

def app_context(request):
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values()) if cart else 0
    
    total = Decimal("0")
    if cart:
        for pid, qty in cart.items():
            p = Product.objects.filter(id=int(pid), available=True).values("price").first()
            if p:
                total += Decimal(p["price"]) * int(qty)
    
    return {
        "WHATSAPP_NUMBER": getattr(settings, "WHATSAPP_NUMBER", ""),
        "BUSINESS_HOURS": getattr(settings, "BUSINESS_HOURS", "Lun-Sáb 8:00-18:00 · Dom 8:00-13:00"),
        "SOCIAL_FACEBOOK_URL": getattr(settings, "SOCIAL_FACEBOOK_URL", "#"),
        "SOCIAL_INSTAGRAM_URL": getattr(settings, "SOCIAL_INSTAGRAM_URL", "#"),
        "cart_count": cart_count,
        "cart_total": total,
        "categories": Category.objects.all()
    }
