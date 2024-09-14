# from django.test import TestCase


import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def guardar_corte_axial_sin_ejes(nii_path, corte):
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

# Ruta del archivo .nii.gz
nii_path = './ml_model/temp/tomografia-t2f.nii.gz'

# Número del corte axial que quieres mostrar
corte = 80

# Guardar el corte axial como imagen PNG sin ejes
#output_path = guardar_corte_axial_sin_ejes(nii_path, corte)
#print(f'Imagen guardada en: {output_path}')



import cv2

def combinar_imagenes(img_path1, img_path2, alpha=0.5, beta=0.5, gamma=0):
    # Cargar las dos imágenes
    img1 = cv2.imread(img_path1, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(img_path2, cv2.IMREAD_UNCHANGED)
    print("path de la imagen 1", img_path1)
    # Redimensionar la segunda imagen para que tenga el mismo tamaño que la primera
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Combinar las imágenes con pesos específicos
    result = cv2.addWeighted(img1, alpha, img2_resized, beta, gamma)

    # Guardar la imagen combinada
    output_path = '/ml_model/temp/imagen_combinada.png'
    cv2.imwrite(output_path, result)

    return output_path

# Ruta de las imágenes PNG
img_path1 = './ml_model/temp/tomografia-t2f.nii.gz_corte_80.png'
img_path2 = './ml_model/temp/tomografia_prediction.png'

# Combinar las imágenes y guardar el resultado
output_path = combinar_imagenes(img_path1, img_path2, alpha=0.5, beta=0.5)
print(f'Imagen combinada guardada en: {output_path}')
