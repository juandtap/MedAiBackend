import os.path

from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

from .ml_model.segmentation import ModeloSegmentacion


@csrf_exempt
@api_view(['POST'])
def cargar_imagen(request):
    if request.method == 'POST':
        t1c_file = request.FILES.get('t1c_file')
        t2f_file = request.FILES.get('t2f_file')

        if not t1c_file or not t2f_file:
            return JsonResponse({'error': 'Ambos archivos son necesarios.'}, status=400)

        t1c_path = default_storage.save(t1c_file.name, t1c_file)
        t2f_path = default_storage.save(t2f_file.name, t2f_file)

        # se llama al modelo
        sample_path = os.path.splitext(t1c_path)[0]
        prediction_image_path = ModeloSegmentacion.obtener_segmentacion(sample_path,
                                                                        slice_to_plot=20)
        with open(prediction_image_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/png")

    return JsonResponse({'error': 'No se enviaron archivos.'}, status=400)