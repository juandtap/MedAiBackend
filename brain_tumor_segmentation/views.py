import os.path
import re
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from io import BytesIO
import matplotlib.pyplot as plt
from .ml_model.segmentation import ModeloSegmentacion
from rest_framework.parsers import MultiPartParser


@csrf_exempt
@api_view(['POST'])
def cargar_imagen(request):
    parser_classes = [MultiPartParser]

    if request.method == 'POST':
        t1c_file = request.FILES.get('t1c_file')
        t2f_file = request.FILES.get('t2f_file')

        if not t1c_file or not t2f_file:
            return JsonResponse({'error': 'Ambos archivos son necesarios.'}, status=400)

        # Guarda los archivos en una carpeta temporal
        temp_dir = os.path.join(settings.BASE_DIR, 'brain_tumor_segmentation', 'ml_model', 'temp')

        os.makedirs(temp_dir, exist_ok=True)
        print("directorios: >>")
        print(temp_dir)
        print(t1c_file.name, t2f_file.name)
        t1c_temp_path = os.path.join(temp_dir, t1c_file.name)
        t2f_temp_path = os.path.join(temp_dir, t2f_file.name)
        print("directorio a guardar")
        print(t1c_temp_path, t2f_temp_path)
        print("valor de files: ")
        print(t1c_file)
        print(t2f_file)
        with open(t1c_temp_path, 'wb') as f:
            f.write(t1c_file.read())

        with open(t2f_temp_path, 'wb') as f:
            f.write(t2f_file.read())

        #t1c_filename = re.sub(r'-[^-]+$', '', t1c_file.name)
        #t2f_filename = re.sub(r'-[^-]+$', '', t2f_file.name)

        #t1c_final_path = os.path.join(temp_dir, t1c_filename)
        #t2f_final_path = os.path.join(temp_dir, t2f_filename)

        #os.rename(t1c_temp_path, t1c_final_path)
        #os.rename(t2f_temp_path, t2f_final_path)

        #sample_path = t2f_final_path

        modelo_seg = ModeloSegmentacion()
        sample_path = re.sub(r'-[^-]+$', '', t1c_temp_path)
        print(">>>SAMPLE PATH : ", sample_path, " >>> \n")
        prediction_image = modelo_seg.obtener_segmentacion(sample_path=sample_path, slice_to_plot=20)
        print("salida>>")
        print(prediction_image)
        output_path = prediction_image
        # Envía la imagen de vuelta al frontend
        with open(output_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="prediction.png"'
            return response

    return JsonResponse({'error': 'No se enviaron archivos.'}, status=400)
