from django.urls import path
from .views import catalog, offers, seasonal

urlpatterns = [
    path('', catalog, name='catalog'),
    path('ofertas/', offers, name='offers'),
    path('temporada/', seasonal, name='seasonal'),
]
