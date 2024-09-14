from django.urls import path
from .views import subir_audio, chat_gpt, crear_paciente

urlpatterns = [
    path('subiraudio', subir_audio, name='subir_audio'),
    path('chat-gpt/', chat_gpt, name='chat_gpt'),
    path('crear-paciente/',crear_paciente, name='crear_paciente'),
]

