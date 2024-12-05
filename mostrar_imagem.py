import cv2

# Abra a imagem
imagem = cv2.imread('caminho/para/a/imagem.jpg')

# Exibe a imagem
cv2.imshow('Imagem', imagem)

# Espera até que uma tecla seja pressionada
cv2.waitKey(0)

# Fecha as janelas abertas pelo OpenCV
cv2.destroyAllWindows()
