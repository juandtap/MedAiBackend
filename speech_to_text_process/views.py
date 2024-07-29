from django.shortcuts import render
import os.path
import re
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from io import BytesIO
import matplotlib.pyplot as plt
from rest_framework.parsers import MultiPartParser
import requests
from django.core.files.base import ContentFile
# Create your views here.
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