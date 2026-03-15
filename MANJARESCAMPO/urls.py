from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from users.views import login_success, CustomLoginView, profile_view

def admin_redirect(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('login')

urlpatterns = [
    path('login-success/', login_success, name='login_success'),
    path('admin/login/', CustomLoginView.as_view(), name='login'),
    path('admin/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/profile/', profile_view, name='profile'),
    path('admin/', admin_redirect),
    path('', include('products.urls')),
    path('', include('orders.urls')),
    path('', include('reports.urls')),
    path('chatbot/', include('chatbot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
