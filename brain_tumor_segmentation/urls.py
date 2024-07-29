
from django.urls import path
from .views import cargar_imagen

urlpatterns = [
    path('subirtomografia', cargar_imagen, name='cargar_imagen'),
]
