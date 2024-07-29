from django.urls import path
from .views import subir_audio

urlpatterns = [
    path('subiraudio', subir_audio, name='subir_audio')
]

