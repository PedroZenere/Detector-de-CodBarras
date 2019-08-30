from __future__ import print_function
from cv2 import *
import pyzbar.pyzbar as pyzbar
import numpy as np

W_NAME_FRM = 'Frame'
W_NAME_ROI = 'ROI'

BORDA = 5

# ROI:
X1 = 0
Y1 = 180
X2 = 640
Y2 = 300


vidcap = VideoCapture(0)
success,frame = vidcap.read()
count = 0
success = True

while success:
    success, frame = vidcap.read()

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    image[Y1:Y2, X1:X2,:] = frame[Y1:Y2, X1:X2,:]

    #BORDA SUPERIOR
    image[(Y1 - BORDA):Y1, X1:X2, :] = 0
    image[(Y1 - BORDA):Y1, X1:X2, 0] = 255
    #BORDA INFERIOR
    image[Y2:(Y2 + BORDA), X1:X2, :] = 0
    image[Y2:(Y2 + BORDA), X1:X2, 0] = 255
    #BORDA ESQUERDA
    image[Y1:Y2, X1:(X1 + BORDA), :] = 0
    image[Y1:Y2, X1:(X1 + BORDA), 0] = 255
    #BORDA DIREITA
    image[Y1:Y2, (X2 -BORDA):X2, :] = 0
    image[Y1:Y2, (X2 -BORDA):X2, 0] = 255

    # Recorte do ROI
    roi = frame[Y1:Y2, X1:X2]

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
