from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db import models
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from inventory.models import SiteConfiguration
from django.conf import settings
from django.utils.http import urlencode

def catalog(request):
    query = request.GET.get("q")
    cat_id = request.GET.get("cat")
    
    products = Product.objects.filter(available=True)
    offer_products = Product.objects.filter(available=True, is_on_offer=True).order_by("-created_at")[:4]
    
    if query:
        products = products.filter(models.Q(name__icontains=query) | models.Q(description__icontains=query))
    
    if cat_id:
        products = products.filter(category_id=cat_id)
        
    products = products.order_by("-created_at")
    
    return render(request, "products/catalog.html", {
        "products": products,
        "offer_products": offer_products,
        "categories": Category.objects.all(),
        "search_query": query,
        "selected_cat": int(cat_id) if cat_id and cat_id.isdigit() else None,
        "active_nav": "catalog"
    })

def offers(request):
    products = Product.objects.filter(available=True, is_on_offer=True).order_by("-created_at")
    return render(request, "products/catalog.html", {
        "products": products,
        "categories": Category.objects.all(),
        "active_nav": "offers",
        "title_suffix": "Mejores Ofertas"
    })

def seasonal(request):
    products = Product.objects.filter(available=True).order_by("-created_at")[:8]
    return render(request, "products/catalog.html", {
        "products": products,
        "categories": Category.objects.all(),
        "active_nav": "seasonal",
        "title_suffix": "Productos de Temporada"
    })

@staff_member_required(login_url='login')
def admin_products_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'products/admin_products_list.html', {'products': products})

@staff_member_required(login_url='login')
def admin_update_stock(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        new_stock = request.POST.get('stock')
        try:
            product.stock = int(new_stock)
            product.save()
            messages.success(request, f"Stock de {product.name} actualizado a {product.stock}.")
        except ValueError:
            messages.error(request, "El stock debe ser un número entero.")
    return redirect('admin_products_list')

@staff_member_required(login_url='login')
def admin_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Intentar guardar sin imagen primero si hay un error de storage persistente
                product = form.save()
                messages.success(request, f"Producto '{product.name}' creado correctamente.")
                return redirect('admin_products_list')
            except Exception as e:
                # Si falla por storage (S3), intentamos avisar
                if 'PutObject' in str(e):
                    messages.error(request, f"Error de almacenamiento (S3): {e}. Verifica que el bucket 'products' sea público en Supabase.")
                else:
                    messages.error(request, f"Error al guardar: {e}")
        else:
            messages.error(request, "Error en el formulario. Revisa los campos.")
    else:
        form = ProductForm()
    return render(request, 'products/admin_product_form.html', {'form': form, 'title': 'Nuevo Producto'})

@staff_member_required(login_url='login')
def admin_product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Producto '{product.name}' actualizado correctamente.")
            return redirect('admin_products_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/admin_product_form.html', {'form': form, 'title': 'Editar Producto', 'product': product})

@staff_member_required(login_url='login')
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Producto '{name}' eliminado.")
        return redirect('admin_products_list')
    return render(request, 'products/admin_product_confirm_delete.html', {'product': product})

@staff_member_required(login_url='login')
def admin_inventory_config(request):
    config = SiteConfiguration.objects.first()
    if not config:
        config = SiteConfiguration.objects.create()
    if request.method == 'POST':
        config.whatsapp_number = request.POST.get('whatsapp_number')
        config.business_hours = request.POST.get('business_hours')
        config.facebook_url = request.POST.get('facebook_url')
        config.instagram_url = request.POST.get('instagram_url')
        config.order_wa_prefix = request.POST.get('order_wa_prefix')
        config.default_shipping_cost = request.POST.get('default_shipping_cost', 10000)
        config.free_shipping_threshold = request.POST.get('free_shipping_threshold', 100000)
        config.save()
        messages.success(request, "Configuración actualizada correctamente.")
        return redirect('admin_inventory_config')
    return render(request, 'products/admin_config.html', {'config': config})

# --- CRUD CATEGORÍAS ---

@staff_member_required(login_url='login')
def admin_category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'products/admin_category_list.html', {'categories': categories})

@staff_member_required(login_url='login')
def admin_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Categoría '{category.name}' creada correctamente.")
            return redirect('admin_category_list')
    else:
        form = CategoryForm()
    return render(request, 'products/admin_category_form.html', {'form': form, 'title': 'Nueva Categoría'})

@staff_member_required(login_url='login')
def admin_category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Categoría '{category.name}' actualizada correctamente.")
            return redirect('admin_category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/admin_category_form.html', {'form': form, 'title': 'Editar Categoría', 'category': category})

@staff_member_required(login_url='login')
def admin_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f"Categoría '{name}' eliminada.")
        return redirect('admin_category_list')
    return render(request, 'products/admin_category_confirm_delete.html', {'category': category})
