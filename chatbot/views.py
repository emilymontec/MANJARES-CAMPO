from django.http import JsonResponse
from django.conf import settings
from payments.models import Payment
from orders.models import ShippingZone


def qa(request):
    q = (request.GET.get("q") or "").lower()
    if any(k in q for k in ["hora", "horario", "horarios", "apertura", "cierre"]):
        return JsonResponse({"answer": f"Nuestro horario: {getattr(settings, 'BUSINESS_HOURS', 'Lun-Sáb 8:00-18:00 · Dom 8:00-13:00')}."})
    if any(k in q for k in ["pago", "pagos", "método", "metodo"]):
        methods = dict(Payment.PAYMENT_METHODS)
        readable = ", ".join(methods.get(k) for k, _ in Payment.PAYMENT_METHODS)
        return JsonResponse({"answer": f"Métodos de pago disponibles: {readable}. También puedes enviarnos comprobante por WhatsApp."})
    if any(k in q for k in ["zona", "entrega", "domicilio", "cobertura", "envío", "envio"]):
        zones = ShippingZone.objects.filter(active=True).order_by("name")
        if zones:
            listed = "; ".join([f"{z.name} ${z.cost}" for z in zones])
            return JsonResponse({"answer": f"Zonas de entrega (Área Metropolitana del Atlántico): {listed}. Si tu zona no aparece, consúltanos por WhatsApp."})
        return JsonResponse({"answer": "Realizamos domicilios y recogida en punto. Consulta tu zona por WhatsApp."})
    if "whatsapp" in q or "contacto" in q:
        wa = getattr(settings, "WHATSAPP_NUMBER", "")
        link = f"https://wa.me/{wa}" if wa else "https://wa.me/"
        return JsonResponse({"answer": f"Escríbenos por WhatsApp: {link}"})
    return JsonResponse({"answer": "Puedo ayudarte con horarios, métodos de pago y zonas de entrega. ¿Qué te gustaría saber?"})

# Create your views here.
