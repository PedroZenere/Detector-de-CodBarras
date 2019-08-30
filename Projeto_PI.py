from __future__ import print_function
from cv2 import *
import pyzbar.pyzbar as pyzbar
import numpy as np

W_NAME_FRM = 'Frame'
W_NAME_ROI = 'ROI'

BORDA = 5
ALTURA_ROI = 50

vidcap = VideoCapture(0)
success,frame = vidcap.read()
count = 0
success = True

while success:
    success, image = vidcap.read()

    '''
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_GRAROI_HPBGR)
    '''

    ROI_HP = (image.shape[0]/2) + ALTURA_ROI
    ROI_HN = (image.shape[0]/2) - ALTURA_ROI
    ROI_W = image.shape[1]

    ROI_HN = int(ROI_HN)
    ROI_HP = int(ROI_HP)
    ROI_W = int(ROI_W)

    imgROI = image[ROI_HN:ROI_HP, 0:ROI_W].copy()
    # Recorte do ROI
    roi = image[ROI_HN:ROI_HP, 0:ROI_W]

    image = (50/255.0) * image
    image = np.uint8(image)
    image[ROI_HN:ROI_HP, 0:ROI_W] = imgROI

    #BORDA SUPERIOR
    image[(ROI_HN - BORDA):ROI_HN, 0:ROI_W, :] = 0
    image[(ROI_HN - BORDA):ROI_HN, 0:ROI_W, 0] = 255
    #BORDA INFERIOR
    image[ROI_HP:(ROI_HP + BORDA), 0:ROI_W, :] = 0
    image[ROI_HP:(ROI_HP + BORDA), 0:ROI_W, 0] = 255
    #BORDA ESQUERDA
    image[ROI_HN:ROI_HP, 0:(0 + BORDA), :] = 0
    image[ROI_HN:ROI_HP, 0:(0 + BORDA), 0] = 255
    #BORDA DIREITA
    image[ROI_HN:ROI_HP, (ROI_W -BORDA):ROI_W, :] = 0
    image[ROI_HN:ROI_HP, (ROI_W -BORDA):ROI_W, 0] = 255

    # Mostrar o video inteiro
    imshow(W_NAME_FRM, image)
    #Mostra a ROI
    imshow(W_NAME_ROI , roi)

    # Decodificar os codigos de barras
    decodedObjects = pyzbar.decode(roi)

    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')

    if cv2.waitKey(10) == 27: # ESC para sair
        break
