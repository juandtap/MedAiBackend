from .seg_model.modelo_unet import build_unet

import nibabel as nib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from skimage.transform import rotate
from skimage.util import montage
import os
from django.conf import settings
from sklearn.model_selection import train_test_split
import keras

import tensorflow
import random
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
import numpy as np

import zipfile

import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as mpatches

from skimage import measure

import plotly.express as px

import cv2


class ModeloSegmentacion:
    _modelo_cnn_unet = None
    IMG_SIZE = 128
    VOLUME_START_AT = 60
    VOLUME_SLICES = 75

    def __init__(self):
        print("modelo segmentacion creado (debe mostrarse una vez)")
        self._modelo_cnn_unet = self.cargar_modelo_cnn_unet()

    # El modelo cnn-unet no se carga directamente lo que se hace es definir la cnn y luego cargar los pesos
    # desde el archivo model-unet-brats.weights.h5

    def cargar_modelo_cnn_unet(self):
        input_layer = keras.Input((self.IMG_SIZE, self.IMG_SIZE, 2))
        # se define el modelo
        modelo = build_unet(input_layer, 'he_normal', 0.2)
        modelo.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        # cargar los pesos
        # Carga los pesos
        weights_path = os.path.join(settings.BASE_DIR, 'brain_tumor_segmentation', 'ml_model', 'seg_model', 'model-unet-brats.weights.h5')
        modelo.load_weights(weights_path)
        print("pesos cargados en el modelo unet (debe mostrarse una vez)")
        print(modelo.summary())
        return modelo

    def predict_segmentation(self, sample_path):
        t1ce_path = sample_path + '-t1c.nii.gz'
        flair_path = sample_path + '-t2f.nii.gz'

        t1ce = nib.load(t1ce_path).get_fdata()
        flair = nib.load(flair_path).get_fdata()

        X = np.empty((self.VOLUME_SLICES, self.IMG_SIZE, self.IMG_SIZE, 2))

        for j in range(self.VOLUME_SLICES):
            X[j, :, :, 0] = cv2.resize(flair[:, :, j + self.VOLUME_START_AT], (self.IMG_SIZE, self.IMG_SIZE))
            X[j, :, :, 1] = cv2.resize(t1ce[:, :, j + self.VOLUME_START_AT], (self.IMG_SIZE, self.IMG_SIZE))

        return self._modelo_cnn_unet.predict(X / np.max(X), verbose=1)


    def obtener_segmentacion(self, sample_path, slice_to_plot):
        predicted_seg = self.predict_segmentation(sample_path)

        #seg_path = sample_path + '-seg.nii.gz'
        #seg = nib.load(seg_path).get_fdata()
        #seg = cv2.resize(seg[:, :, slice_to_plot + self.VOLUME_START_AT], (self.IMG_SIZE, self.IMG_SIZE),
        #                 interpolation=cv2.INTER_NEAREST)
        #seg[seg == 0] = np.nan

        my_pred = np.argmax(predicted_seg, axis=3)
        my_pred = my_pred[slice_to_plot, :, :]
        my_pred = my_pred.astype(float)
        my_pred[my_pred == 0] = np.nan

        fig, axstest = plt.subplots(1, 1, figsize=(8, 6))
        # axstest[0].imshow(seg, cmap='gray', norm=None)
        # axstest[0].set_title('Segmentación original')
        # axstest[1].imshow(my_pred, cmap='gray', norm=None)
        # axstest[1].set_title('Predicción sin postprocesamiento (layers 1,2,3)')

        cmap = mpl.colors.ListedColormap(['#440054', '#3b528b', '#18b880', '#e6d74f'])
        norm = mpl.colors.BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], cmap.N)

        axstest.imshow(my_pred, cmap, norm)
        #axstest.set_title('Predición')

        # Ocultar los ejes
        axstest.axis('off')

        # Crear la leyenda
        legend_labels = ['núcleo tumoral necrótico (NCR)', 'tejido edematoso peritumoral (ED)', 'tumor resaltado (ET)']
        legend_colors = ['#3b528b', '#18b880', '#e6d74f']
        patches = [mpatches.Patch(color=color, label=label) for color, label in zip(legend_colors, legend_labels)]

        axstest.legend(handles=patches, loc='upper right', bbox_to_anchor=(1.1, 1))

        plt.subplots_adjust(wspace=0.8)
        output_path = f'{sample_path}_prediction.png'
        plt.savefig(output_path)
        plt.close()
        return output_path

    def obtener_original(self, nii_path, corte):
        # Cargar la imagen .nii.gz
        img = nib.load(nii_path)
        data = img.get_fdata()

        # Extraer el corte axial específico
        corte_axial = data[:, :, corte]

        # Voltear la imagen verticalmente
        corte_axial_flipped = np.flipud(corte_axial)

        # Crear una figura y un eje sin mostrar los ejes
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(corte_axial_flipped, cmap='gray', origin='lower')
        ax.axis('off')  # Ocultar los ejes

        # Guardar la imagen como PNG
        output_path = f'{nii_path}_corte_{corte}.png'
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()

        return output_path

    def combinar_imagenes(self, img_path1, img_path2, alpha=0.5, beta=0.5, gamma=0):
        # Cargar las dos imágenes
        img1 = cv2.imread(img_path1, cv2.IMREAD_UNCHANGED)
        img2 = cv2.imread(img_path2, cv2.IMREAD_UNCHANGED)
        print("path de la imagen 1", img_path1)
        # Redimensionar la segunda imagen para que tenga el mismo tamaño que la primera
        img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        # Combinar las imágenes con pesos específicos
        result = cv2.addWeighted(img1, alpha, img2_resized, beta, gamma)

        # Guardar la imagen combinada
        abspath = img_path2
        abspath = abspath.replace('tomografia_prediction.png', '')
        output_path = abspath+'imagen_combinada.png'
        cv2.imwrite(output_path, result)

        return output_path
