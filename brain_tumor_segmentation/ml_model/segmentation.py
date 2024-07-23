from .seg_model.modelo_unet import build_unet

import nibabel as nib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from skimage.transform import rotate
from skimage.util import montage
import os
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


from skimage import measure

import plotly.express as px


class ModeloSegmentacion:

    _modelo_cnn_unet = None
    IMG_SIZE = 128

    def __init__(self):
        print("modelo segmentacion creado (debe mostrarse una vez)")

    # El modelo cnn-unet no se carga directamente lo que se hace es definir la cnn y luego cargar los pesos
    # desde el archivo model-unet-brats.weights.h5
    @staticmethod
    def cargar_modelo_cnn_unet(self):
        input_layer = keras.Input((self.IMG_SIZE, self.IMG_SIZE, 2))
        # se define el modelo
        modelo = build_unet(input_layer, 'he_normal', 0.2)
        modelo.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        # cargar los pesos
        modelo.load_weights('./seg_model/model-unet-brats.weights.h5')
        print("pesos cargados en el modelo unet (debe mostrarse una vez)")
        print(modelo.summary())
        return modelo

    def obtener_segmentacion(self):
        pass

