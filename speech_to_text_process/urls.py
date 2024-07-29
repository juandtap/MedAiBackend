from django.urls import path
from .views import subir_audio, chat_gpt

urlpatterns = [
    path('subiraudio', subir_audio, name='subir_audio'),
    path('chat-gpt/', chat_gpt, name='chat_gpt'),
]

