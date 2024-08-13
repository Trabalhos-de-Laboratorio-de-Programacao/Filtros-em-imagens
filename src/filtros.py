import cv2
import numpy as np
from PIL import Image
from skimage import filters, color, exposure

class grayscale:
    def __init__(self, image):
        self.image = np.array(image)

    def applyFilter(self):
        # Verifica se a imagem tem 3 canais (RGB)
        if len(self.image.shape) == 3 and self.image.shape[2] == 3:
            grayscaleImage = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        else:
            raise ValueError("A imagem de entrada deve ter 3 canais (RGB).")
        return Image.fromarray(grayscaleImage)

    def getOriginalImage(self):
        return self.image


class blackAndWhite:
    def __init__(self, image):
        self.image = np.array(image)

    def applyFilter(self):
        # Verifica se a imagem tem 3 canais (RGB)
        if len(self.image.shape) == 3 and self.image.shape[2] == 3:
            # Aplica um desfoque suave antes de converter em preto e branco
            blurred = cv2.GaussianBlur(self.image, (5, 5), 0)
            gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
            (thresh, blackAndWhiteImage) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        else:
            raise ValueError("A imagem de entrada deve ter 3 canais (RGB).")
        return Image.fromarray(blackAndWhiteImage)

    def getOriginalImage(self):
        return self.image


class cartoon:
    def __init__(self, image):
        self.image = np.array(image)

    def applyFilter(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 5)  # Manter o blur mais sutil para mais detalhes

        # Aumentar os parâmetros para uma detecção de bordas mais intensa
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 20)  # Ajustar o valor de subtração para maior contraste

        # Aumentar a suavidade do filtro bilateral
        color = cv2.bilateralFilter(self.image, 9, 250, 250)  # Parâmetros aumentados para mais suavidade

        # Combinar a imagem de cor e as bordas
        cartoonImage = cv2.bitwise_and(color, color, mask=edges)
        return Image.fromarray(cartoonImage)



class negative:
    def __init__(self, image):
        self.image = np.array(image)

    def applyFilter(self):
        negativeImage = cv2.bitwise_not(self.image)
        return Image.fromarray(negativeImage)

    def getOriginalImage(self):
        return self.image


class contour:
    def __init__(self, image):
        self.image = np.array(image)

    def applyFilter(self):
        # Converte a imagem para escala de cinza
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        # Aplica Canny para detectar bordas
        edges = cv2.Canny(gray, 100, 200)
        return Image.fromarray(edges)

    def getOriginalImage(self):
        return self.image


class blurred:
    def __init__(self, image):
        self.image = np.array(image)

    def applyFilter(self):
        # Aumenta a intensidade do desfoque
        blurredImage = cv2.GaussianBlur(self.image, (35, 35), 0)  # Aumentar o tamanho do kernel
        return Image.fromarray(blurredImage)


# from PIL import ImageFilter, Image, ImageChops, ImageOps, ImageEnhance

# class GrayScale: # Filtro escala de cinza
#     def __init__(self, image):
#         self.image = image

#     def applyFilter(self):
#         grayscaleImage = self.image.convert("L")
#         return grayscaleImage

#     def getOriginalImage(self):
#         return self.image

# class BlackWhite: # Filtro preto e branco
#     def __init__(self, image):
#         self.image = image

#     def applyFilter(self):
#         grayscaleImage = self.image.convert("L")
#         blackAndWhiteImage = grayscaleImage.convert("1")
#         return blackAndWhiteImage

#     def getOriginalImage(self):
#         return self.image
    
# class Cartoon: # Filtro cartoon
#     def __init__(self, image):
#         self.image = image

#     def applyFilter(self):
#         #Convertemos a imagem para a escala cinza, e suavizamos para reduzir os ruídos da imagem e deixa-lá mais facial para processa-lá.
#         grayscaleImage = self.image.convert("L")
#         #Detectamos as bordas para destacar as linhas da imagem.
#         edgesImage = grayscaleImage.filter(ImageFilter.FIND_EDGES)
#         edgesImage = ImageOps.autocontrast(edgesImage)
#         #suavizando
#         smoothImage = edgesImage.filter(ImageFilter.SMOOTH_MORE)

#         opacity = 20
#         smoothImage = smoothImage.point(lambda p: p * opacity)
#         cartoonImage = Image.composite(self.image, Image.new("RGB", self.image.size, (255, 255, 255)), smoothImage)
#         return cartoonImage
        

#     def getOriginalImage(self):
#         return self.image
    
# class Negative: # Filtro imagem negativa (cores invertidas)
#     def __init__(self, image):
#         self.image = image

#     def applyFilter(self):
#         negativeImage = ImageChops.invert(self.image)
#         return negativeImage

#     def getOriginalImage(self):
#         return self.image
    
# class Contour: # Filtro Contorno
#     def __init__(self, image):
#         self.image = image

#     def applyFilter(self):
#         contourFilter = self.image.filter(ImageFilter.CONTOUR)
#         return contourFilter

#     def getOriginalImage(self):
#         return self.image

# class Blur: # Filtro blur / embaçado
#     def __init__(self, image):
#         self.image = image

#     def applyFilter(self):
#         blurredImage = self.image.filter(ImageFilter.GaussianBlur(5))
#         return blurredImage

#     def getOriginalImage(self):
#         return self.image
    
# class FullHD: # Filtro estilo FullHD
#     def __init__(self, image):
#         self.image = image

#     def applyFilter(self):
#         # Convert to RGB if not already in that mode
#         if self.image.mode != 'RGB':
#             self.image = self.image.convert('RGB')
        
#         # Apply a smooth filter
#         smooth_image = self.image.filter(ImageFilter.SMOOTH_MORE)
        
#         # Enhance the image (contrast, brightness)
#         enhancer = ImageEnhance.Contrast(smooth_image)
#         enhanced_image = enhancer.enhance(1.5)
        
#         enhancer = ImageEnhance.Brightness(enhanced_image)
#         final_image = enhancer.enhance(1.2)
        
#         return final_image

#     def getOriginalImage(self):
#         return self.image