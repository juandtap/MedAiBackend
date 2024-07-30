from django.shortcuts import render
import os.path
import re

from django.conf import settings
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from io import BytesIO
import matplotlib.pyplot as plt
from rest_framework.parsers import MultiPartParser
import requests
from django.core.files.base import ContentFile

# Se importa serializer
from .serializer import PacienteSerializer

## Se importa la APIKEY
from .apikey import API_KEY

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
headers = {"Authorization": "Bearer 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"}

@csrf_exempt
@api_view(['POST'])
def subir_audio(request):
    if request.method == "POST" and request.FILES.get('file'):
        audio_file = request.FILES['file']
        file_path = default_storage.save('tmp/' + audio_file.name, ContentFile(audio_file.read()))
        full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

        with open(full_file_path, "rb") as f:
            data = f.read()
        
        response = requests.post(API_URL, headers=headers, data=data)
        result = response.json()
        print(result)
        os.remove(full_file_path)  # Optional: Remove the file after processing

        return JsonResponse({'transcription': result['text']})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@api_view(['POST'])
def chat_gpt(request):
    try:
        data = request.data
        if not data or 'message' not in data:
            return Response({'error': 'No message provided'}, status=status.HTTP_400_BAD_REQUEST)

        message = data['message']

        def chat_gpt_api(message):
            try:
                url = 'https://api.openai.com/v1/chat/completions'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer '+API_KEY
                }
                payload = {
                    'model': 'gpt-3.5-turbo',
                    'messages': [
                        {
                            'role': 'user',
                            'content': message
                        }
                    ],
                    'max_tokens': 200
                }

                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and result['choices']:
                        return result['choices'][0]['message'].get('content', '').strip()
                    else:
                        return 'No se encontró una respuesta válida en la API'
                else:
                    return f'Error en la solicitud a la API: {response.status_code} - {response.text}'

            except Exception as e:
                return f'Error en la solicitud a la API: {str(e)}'

        response_text = chat_gpt_api(message)
        return Response({'response': response_text})

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def crear_paciente(request):
    if request.method == 'POST':
        serializer = PacienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
