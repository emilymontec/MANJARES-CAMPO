from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.urls import reverse_lazy

class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('catalog')

@login_required
def login_success(request):
    """
    Fallback redirect view.
    """
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('catalog')

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Usamos SetPasswordForm para que no pida la contraseña anterior
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para mantener la sesión
            messages.success(request, '¡Tu contraseña ha sido actualizada con éxito!')
            return redirect('profile')
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = SetPasswordForm(request.user)
    
    return render(request, 'registration/profile.html', {
        'form': form,
        'active_nav': 'profile'
    })
