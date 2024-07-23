from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from .ml_model.segmentation import ModeloSegmentacion

@csrf_exempt
def cargar_imagen(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_path = default_storage.save(file.name, file)

