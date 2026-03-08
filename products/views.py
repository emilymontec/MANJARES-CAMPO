from django.shortcuts import render
from django.db import models
from .models import Product
from django.conf import settings
from django.utils.http import urlencode

def catalog(request):
    query = request.GET.get("q")
    cat_id = request.GET.get("cat")
    
    products = Product.objects.filter(available=True)
    
    if query:
        products = products.filter(models.Q(name__icontains=query) | models.Q(description__icontains=query))
    
    if cat_id:
        products = products.filter(category_id=cat_id)
        
    products = products.order_by("-created_at")
    
    wa_number = getattr(settings, "WHATSAPP_NUMBER", "")
    items = []
    for p in products:
        text = f"Hola, quiero comprar 1 x {p.name} por ${p.price}"
        wa_link = f"https://wa.me/{wa_number}?{urlencode({'text': text})}" if wa_number else ""
        items.append(
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "description": p.description,
                "image": p.image.url if p.image else "",
                "wa_link": wa_link,
            }
        )
    return render(request, "products/catalog.html", {
        "products": items,
        "search_query": query,
        "selected_cat": int(cat_id) if cat_id and cat_id.isdigit() else None,
        "active_nav": "catalog"
    })

def offers(request):
    # Lógica específica para ofertas (ej: precio < 5000)
    products = Product.objects.filter(available=True, price__lt=5000).order_by("-created_at")
    
    wa_number = getattr(settings, "WHATSAPP_NUMBER", "")
    items = []
    for p in products:
        text = f"Hola, quiero aprovechar la oferta de {p.name} por ${p.price}"
        wa_link = f"https://wa.me/{wa_number}?{urlencode({'text': text})}" if wa_number else ""
        items.append({
            "id": p.id, "name": p.name, "price": p.price, "description": p.description,
            "image": p.image.url if p.image else "", "wa_link": wa_link,
        })
    return render(request, "products/catalog.html", {
        "products": items,
        "active_nav": "offers",
        "title_suffix": "Mejores Ofertas"
    })

def seasonal(request):
    # Lógica específica para temporada (ej: los más recientes o marcados como temporada)
    # Por ahora tomamos los últimos 8 productos
    products = Product.objects.filter(available=True).order_by("-created_at")[:8]
    
    wa_number = getattr(settings, "WHATSAPP_NUMBER", "")
    items = []
    for p in products:
        text = f"Hola, me interesa este producto de temporada: {p.name}"
        wa_link = f"https://wa.me/{wa_number}?{urlencode({'text': text})}" if wa_number else ""
        items.append({
            "id": p.id, "name": p.name, "price": p.price, "description": p.description,
            "image": p.image.url if p.image else "", "wa_link": wa_link,
        })
    return render(request, "products/catalog.html", {
        "products": items,
        "active_nav": "seasonal",
        "title_suffix": "Productos de Temporada"
    })

# Create your views here.
