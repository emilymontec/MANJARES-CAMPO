from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order, OrderItem
from products.models import Product


@staff_member_required
def admin_dashboard(request):
    now = timezone.now()
    month_orders = Order.objects.filter(created_at__year=now.year, created_at__month=now.month)
    sales_month = month_orders.aggregate(total=Sum("total"))["total"] or 0
    orders_count = month_orders.count()
    income = sales_month

    top_qs = (
        OrderItem.objects.filter(order__created_at__year=now.year, order__created_at__month=now.month)
        .values("product__name")
        .annotate(qty=Sum("quantity"))
        .order_by("-qty")[:5]
    )
    top_labels = [x["product__name"] for x in top_qs]
    top_values = [int(x["qty"] or 0) for x in top_qs]

    low_inventory = Product.objects.filter(available=True).order_by("stock")
    low_inventory = [p for p in low_inventory if getattr(p, "low_stock", False)][:10]

    ctx = {
        "sales_month": sales_month,
        "orders_count": orders_count,
        "income": income,
        "top_labels": top_labels,
        "top_values": top_values,
        "low_inventory": low_inventory,
        "month_str": now.strftime("%B %Y"),
    }
    return render(request, "reports/admin_dashboard.html", ctx)

# Create your views here.
