from cv2 import *
import pyzbar.pyzbar as pyzbar
import numpy as np

W_NAME_FRM = 'Frame'
W_NAME_ROI = 'ROI'

BORDA = 5
LINHA = 1
ALTURA_ROI = 50
NVL_ESCURO = 50

vidcap = VideoCapture(0)
success,frame = vidcap.read()
count = 0
success = True

while success:
    success, image = vidcap.read()

    #Selecionando a area da ROI
    ROI_Y_INI = (image.shape[0]/2) - ALTURA_ROI
    ROI_Y_FIM = (image.shape[0]/2) + ALTURA_ROI
    ROI_LARGURA = image.shape[1]
    ROI_MEIO = image.shape[0]//2

    ROI_Y_INI = int(ROI_Y_INI)
    ROI_Y_FIM = int(ROI_Y_FIM)
    ROI_LARGURA = int(ROI_LARGURA)

    #Recortando a ROI da imagem
    imgROI = image[ROI_Y_INI:ROI_Y_FIM, 0:ROI_LARGURA].copy()

    #Escurecendo areas fora da ROI
    image = (NVL_ESCURO/255.0) * image
    image = np.uint8(image)
    image[ROI_Y_INI:ROI_Y_FIM, 0:ROI_LARGURA] = imgROI

    # Desenhando as bordas:
    # BORDA SUPERIOR
    image[(ROI_Y_INI - BORDA):ROI_Y_INI, 0:ROI_LARGURA, :] = 0
    image[(ROI_Y_INI - BORDA):ROI_Y_INI, 0:ROI_LARGURA, 0] = 255
    # BORDA INFERIOR
    image[ROI_Y_FIM:(ROI_Y_FIM + BORDA), 0:ROI_LARGURA, :] = 0
    image[ROI_Y_FIM:(ROI_Y_FIM + BORDA), 0:ROI_LARGURA, 0] = 255
    # BORDA ESQUERDA
    image[ROI_Y_INI:ROI_Y_FIM, 0:(0 + BORDA), :] = 0
    image[ROI_Y_INI:ROI_Y_FIM, 0:(0 + BORDA), 0] = 255
    # BORDA DIREITA
    image[ROI_Y_INI:ROI_Y_FIM, (ROI_LARGURA -BORDA):ROI_LARGURA, :] = 0
    image[ROI_Y_INI:ROI_Y_FIM, (ROI_LARGURA -BORDA):ROI_LARGURA, 0] = 255
    # LINHA VERMELHA
    image[ROI_MEIO:(ROI_MEIO + LINHA), 30:(ROI_LARGURA-30), :] = 0
    image[ROI_MEIO:(ROI_MEIO + LINHA), 30:(ROI_LARGURA-30), 2] = 255

    # Mostrar o video inteiro
    imshow(W_NAME_FRM, image)
    #Mostra a ROI
    imshow(W_NAME_ROI , imgROI)

    # Decodificar os codigos de barras
    decodedObjects = pyzbar.decode(imgROI)

    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')
    '''
    if(len(decodedObjects) > 0):
        break
    '''
    if cv2.waitKey(10) == 27: # ESC para sair
        break
