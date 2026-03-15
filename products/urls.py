from django.urls import path
from .views import (
    catalog, 
    offers, 
    seasonal, 
    admin_products_list, 
    admin_product_create,
    admin_product_update,
    admin_product_delete,
    admin_update_stock, 
    admin_inventory_config,
    admin_category_list,
    admin_category_create,
    admin_category_update,
    admin_category_delete
)

urlpatterns = [
    path('', catalog, name='catalog'),
    path('ofertas/', offers, name='offers'),
    path('temporada/', seasonal, name='seasonal'),
    path('dashboard/admin/products/', admin_products_list, name='admin_products_list'),
    path('dashboard/admin/products/create/', admin_product_create, name='admin_product_create'),
    path('dashboard/admin/products/update/<int:product_id>/', admin_product_update, name='admin_product_update'),
    path('dashboard/admin/products/delete/<int:product_id>/', admin_product_delete, name='admin_product_delete'),
    path('dashboard/admin/products/stock/<int:product_id>/', admin_update_stock, name='admin_update_stock'),
    path('dashboard/admin/categories/', admin_category_list, name='admin_category_list'),
    path('dashboard/admin/categories/create/', admin_category_create, name='admin_category_create'),
    path('dashboard/admin/categories/update/<int:category_id>/', admin_category_update, name='admin_category_update'),
    path('dashboard/admin/categories/delete/<int:category_id>/', admin_category_delete, name='admin_category_delete'),
    path('dashboard/admin/config/', admin_inventory_config, name='admin_inventory_config'),
]
