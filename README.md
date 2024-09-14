<hr color="#D2BA05">

<font size="9" color="#195E87"><b><p align="center">Med Ai Assistant<p></b></font>
<font size="6" color="#195E87"><b><p align="center">Alavarado Nixon - Astudillot Paul - Tapia Diego <p></b></font>

<hr  color="#D2BA05" >

### Estructura

El proyecto de Django se divide en dos aplicaciones:
- **brain_tumor_segmentation**
- **speech_to_text_process**

#### Brain Tumor Segmentation

![app1](https://raw.githubusercontent.com/juandtap/MedAiBackend/voiceApi/screenshoots/app1.png)

En esta aplicación se realiza la segmentación de tumores cerebrales a partir de la carga de archivos `.nii.gz` desde el frontend.
Dentro de la aplicación se encuentra el directorio `ml_model` este contiene los subdirectorios `seg_model` y `temp` y el archivo `segmentation.py`

En el modulo `segmentation.py` se tienen la clase `ModeloSegmentacion` con los siguientes métodos:

- `cargar_modelo_cnn_unet` : Este método carga el modelo CNN UNET desde el módulo `seg_model/model_unet.py` que carga el archivo .h5 (la red CNN entrenada)
- `obtener_segmentacion`: Calcula la segmentación a partir de los archivos cargados y el modelo y se exporta la segmentacion en el corte 80 a una imagen .png
- `combinar_imagenes`: Combina la imagen original y la segmentación usando la librería opencv

En el archivo `views.py` se llama a la clase `ModeloSegmentacion` y se envía la imagen combinada al front por medio de una api Rest.

#### Speech to Text Process
![app2](https://raw.githubusercontent.com/juandtap/MedAiBackend/voiceApi/screenshoots/app2.png)

En esta aplicación se tienen dos métodos POST, el uno que envía el audio recibido desde el front a la API de whisper para el proceso de voz a texto.
Esta API retorna el texto el cual es enviado el front.

![app3](https://raw.githubusercontent.com/juandtap/MedAiBackend/voiceApi/screenshoots/app3.png)

El otro método POST se encarga de enviar el prompt recibido desde el front para enviarlo a la API de chatGPT

![app4](https://raw.githubusercontent.com/juandtap/MedAiBackend/voiceApi/screenshoots/app4.png)

Este método devuelve la respuesta de chatgpt en formato JSON al front.

