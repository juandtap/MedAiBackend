
from django.urls import path
from .views import cargar_imagen
from .views import subir_audio

urlpatterns = [
    path('subirtomografia', cargar_imagen, name='cargar_imagen'),
    path('subiraudio', subir_audio, name='subir_audio')
]
