from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, ShippingZone
from payments.models import Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "quantity", "price", "subtotal_display")
    readonly_fields = ("subtotal_display",)

    def subtotal_display(self, obj):
        try:
            return f"${obj.subtotal()}"
        except Exception:
            return "-"
    subtotal_display.short_description = "Subtotal"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "customer_phone", "created_at", "total_display", "delivery_method", "status_timeline", "invoice_link", "wa_invoice")
    list_filter = ("status", "delivery_method", "created_at", "customer")
    search_fields = ("id", "customer__username", "customer__email", "customer_phone")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]
    
    def get_inlines(self, request, obj=None):
        class PaymentInline(admin.TabularInline):
            model = Payment
            extra = 0
            fields = ("method", "amount", "reference", "confirmed")
        return [OrderItemInline, PaymentInline]

    ORDER_FLOW = ["pending", "confirmed", "preparing", "sent", "delivered"]
    LABELS = {
        "pending": "Nuevo pedido",
        "confirmed": "Confirmado",
        "preparing": "En preparación",
        "sent": "Enviado",
        "delivered": "Entregado",
    }

    def total_display(self, obj):
        return f"${obj.total}"
    total_display.short_description = "Total"

    def status_timeline(self, obj):
        current = obj.status
        try:
            idx = self.ORDER_FLOW.index(current)
        except ValueError:
            idx = 0

        items = []
        for i, key in enumerate(self.ORDER_FLOW):
            active = i <= idx
            color = "#111827" if active else "#d1d5db"
            label = self.LABELS.get(key, key.title())
            items.append(
                f"""
                <div style="display:flex;align-items:center;gap:8px;">
                    <div style="width:10px;height:10px;border-radius:50%;background:{color};"></div>
                    <span style="font-size:11px;color:{color};white-space:nowrap;">{label}</span>
                </div>
                """
            )
        return format_html(
            '<div style="display:flex;gap:12px;align-items:center;flex-wrap:wrap;">{}</div>',
            format_html("".join(items)),
        )

    status_timeline.short_description = "Estado"

    def invoice_link(self, obj):
        return format_html('<a href="/admin/orders/invoice/{}/" target="_blank">Factura PDF</a>', obj.id)
    invoice_link.short_description = "Factura"

    def wa_invoice(self, obj):
        if getattr(obj, "customer_phone", ""):
            from django.utils.http import urlencode
            from django.urls import reverse
            # El admin genera el link para que el cliente lo descargue
            base_url = "https://manjarescampo-shop.com" # Cambiar por el dominio real
            path = reverse('order_invoice_pdf', args=[obj.id])
            msg = f"Hola, te compartimos la factura de tu Pedido #{obj.id} de Manjares del Campo. Puedes descargarla aquí: {base_url}{path}"
            
            return format_html(
                '<a href="https://wa.me/{}?{}" target="_blank" class="button" style="padding:4px 8px; background:#25D366; color:#fff; border-radius:4px; font-size:11px;">WhatsApp</a>',
                obj.customer_phone,
                urlencode({"text": msg})
            )
        return "—"
    wa_invoice.short_description = "Enviar Factura"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price", "subtotal_display")
    search_fields = ("order__id", "product__name")
    list_filter = ("order__status",)

    def subtotal_display(self, obj):
        try:
            return f"${obj.subtotal()}"
        except Exception:
            return "-"
    subtotal_display.short_description = "Subtotal"


@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "active", "notes")
    list_editable = ("cost", "active")
    search_fields = ("name", "notes")
    ordering = ("name",)
