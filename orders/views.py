from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.http import urlencode
from decimal import Decimal
from products.models import Product
from .models import ShippingZone
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

def _get_cart(session):
    return session.setdefault("cart", {})

def _save_session(request):
    request.session.modified = True

def _cart_items(cart):
    items = []
    total = Decimal("0")
    for pid, qty in cart.items():
        p = Product.objects.filter(id=int(pid), available=True).first()
        if not p:
            continue
        quantity = int(qty)
        subtotal = Decimal(p.price) * quantity
        total += subtotal
        items.append({"product": p, "quantity": quantity, "subtotal": subtotal})
    return items, total

def _shipping_cost(total, shipping_opts=None):
    free_threshold = getattr(settings, "FREE_SHIPPING_OVER", 100000)
    default_shipping = getattr(settings, "DEFAULT_SHIPPING_COST", 10000)
    shipping_opts = shipping_opts or {}
    method = shipping_opts.get("method", "delivery")
    if method == "pickup":
        return Decimal("0")
    zone_id = shipping_opts.get("zone_id")
    if zone_id:
        try:
            zone = ShippingZone.objects.get(id=int(zone_id), active=True)
            zone_cost = Decimal(zone.cost)
        except (ShippingZone.DoesNotExist, ValueError):
            zone_cost = Decimal(default_shipping)
    else:
        zone_cost = Decimal(default_shipping)
    if total >= Decimal(free_threshold):
        return Decimal("0")
    return zone_cost

def _discount_amount(total):
    percent = getattr(settings, "DISCOUNT_PERCENT", 0)
    if not percent:
        return Decimal("0")
    return (Decimal(total) * Decimal(percent) / Decimal("100")).quantize(Decimal("1."))

def cart_view(request):
    cart = _get_cart(request.session)
    items, total = _cart_items(cart)
    discount = _discount_amount(total)
    shipping_opts = request.session.get("shipping", {"method": "delivery"})
    shipping = _shipping_cost(total - discount, shipping_opts)
    grand_total = total - discount + shipping
    wa_number = getattr(settings, "WHATSAPP_NUMBER", "")
    wa_text = "Pedido CAMPOVERDE:\n"
    for i in items:
        wa_text += f"- {i['quantity']} x {i['product'].name} = ${i['subtotal']}\n"
    wa_text += f"Subtotal: ${total}\n"
    if discount > 0:
        wa_text += f"Descuento: -${discount}\n"
    wa_text += f"Envío ({shipping_opts.get('method', 'delivery')}): ${shipping}\n"
    wa_text += f"Total: ${grand_total}\n"
    wa_link = f"https://wa.me/{wa_number}?{urlencode({'text': wa_text})}" if wa_number else ""
    zones = ShippingZone.objects.filter(active=True).order_by("name")
    ctx = {
        "items": items,
        "total": total,
        "discount": discount,
        "shipping": shipping,
        "grand_total": grand_total,
        "wa_link": wa_link,
        "zones": zones,
        "shipping_opts": shipping_opts,
    }
    return render(request, "orders/cart.html", ctx)

@require_POST
def add_to_cart(request, product_id):
    qty = int(request.POST.get("qty", "1"))
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = _get_cart(request.session)
    current = int(cart.get(str(product_id), 0))
    cart[str(product_id)] = current + max(1, qty)
    _save_session(request)
    return redirect("cart_view")

def remove_from_cart(request, product_id):
    cart = _get_cart(request.session)
    cart.pop(str(product_id), None)
    _save_session(request)
    return redirect("cart_view")

def quick_buy_product(request, product_id):
    p = get_object_or_404(Product, id=product_id, available=True)
    wa_number = getattr(settings, "WHATSAPP_NUMBER", "")
    text = f"Hola, quiero comprar 1 x {p.name} por ${p.price}"
    link = f"https://wa.me/{wa_number}?{urlencode({'text': text})}" if wa_number else "/"
    return redirect(link)

@require_POST
def set_shipping_options(request):
    method = request.POST.get("method", "delivery")
    zone_id = request.POST.get("zone_id")
    address = request.POST.get("address", "")
    request.session["shipping"] = {"method": method, "zone_id": zone_id, "address": address}
    _save_session(request)
    return redirect("cart_view")


@staff_member_required
def order_invoice_pdf(request, order_id):
    from .models import Order, OrderItem
    order = get_object_or_404(Order, pk=order_id)
    items = OrderItem.objects.filter(order=order).select_related("product")
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Factura CAMPOVERDE - Pedido #{order.id}", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, f"Fecha: {order.created_at.strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.cell(0, 8, f"Cliente: {order.customer.get_username()}", ln=True)
        if order.customer_phone:
            pdf.cell(0, 8, f"Teléfono: {order.customer_phone}", ln=True)
        if order.address:
            pdf.multi_cell(0, 8, f"Dirección: {order.address}")
        pdf.ln(2)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(100, 8, "Producto", 1)
        pdf.cell(30, 8, "Cantidad", 1, align="R")
        pdf.cell(60, 8, "Subtotal", 1, ln=True, align="R")
        pdf.set_font("Arial", "", 11)
        total = Decimal("0")
        for it in items:
            subtotal = Decimal(it.quantity) * Decimal(it.price)
            total += subtotal
            pdf.cell(100, 8, it.product.name, 1)
            pdf.cell(30, 8, str(it.quantity), 1, align="R")
            pdf.cell(60, 8, f"${subtotal}", 1, ln=True, align="R")
        pdf.ln(2)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(130, 8, "Total", 1)
        pdf.cell(60, 8, f"${total}", 1, ln=True, align="R")
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="factura_{order.id}.pdf"'
        response.write(pdf.output(dest='S').encode('latin-1'))
        return response
    except Exception:
        return render(request, "orders/invoice_fallback.html", {"order": order, "items": items})


@staff_member_required
def monthly_sales_pdf(request):
    from .models import Order, OrderItem
    now = timezone.now()
    month_orders = Order.objects.filter(created_at__year=now.year, created_at__month=now.month)
    total = sum((o.total for o in month_orders), Decimal("0"))
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Reporte Mensual de Ventas - {now.strftime('%B %Y')}", ln=True, align='C')
        pdf.ln(4)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(30, 8, "ID", 1)
        pdf.cell(80, 8, "Cliente", 1)
        pdf.cell(40, 8, "Fecha", 1)
        pdf.cell(40, 8, "Total", 1, ln=True, align="R")
        pdf.set_font("Arial", "", 11)
        for o in month_orders:
            pdf.cell(30, 8, str(o.id), 1)
            pdf.cell(80, 8, o.customer.get_username(), 1)
            pdf.cell(40, 8, o.created_at.strftime("%d/%m/%Y"), 1)
            pdf.cell(40, 8, f"${o.total}", 1, ln=True, align="R")
        pdf.ln(4)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(150, 8, "TOTAL MES", 0)
        pdf.cell(40, 8, f"${total}", 0, ln=True, align="R")
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="reporte_{now.strftime("%m_%Y")}.pdf"'
        response.write(pdf.output(dest='S').encode('latin-1'))
        return response
    except Exception:
        return render(request, "orders/report_fallback.html", {"orders": month_orders, "total": total, "now": now})

# Create your views here.
