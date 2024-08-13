from PIL import ImageFilter, Image, ImageChops, ImageOps, ImageEnhance

class GrayScale: # Filtro escala de cinza
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        grayscaleImage = self.image.convert("L")
        return grayscaleImage

    def getOriginalImage(self):
        return self.image

class BlackWhite: # Filtro preto e branco
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        grayscaleImage = self.image.convert("L")
        blackAndWhiteImage = grayscaleImage.convert("1")
        return blackAndWhiteImage

    def getOriginalImage(self):
        return self.image
    
class Cartoon: # Filtro cartoon
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        #Convertemos a imagem para a escala cinza, e suavizamos para reduzir os ruídos da imagem e deixa-lá mais facial para processa-lá.
        grayscaleImage = self.image.convert("L")
        #Detectamos as bordas para destacar as linhas da imagem.
        edgesImage = grayscaleImage.filter(ImageFilter.FIND_EDGES)
        edgesImage = ImageOps.autocontrast(edgesImage)
        #suavizando
        smoothImage = edgesImage.filter(ImageFilter.SMOOTH_MORE)

        opacity = 20
        smoothImage = smoothImage.point(lambda p: p * opacity)
        cartoonImage = Image.composite(self.image, Image.new("RGB", self.image.size, (255, 255, 255)), smoothImage)
        return cartoonImage
        

    def getOriginalImage(self):
        return self.image
    
class Negative: # Filtro imagem negativa (cores invertidas)
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        negativeImage = ImageChops.invert(self.image)
        return negativeImage

    def getOriginalImage(self):
        return self.image
    
class Contour: # Filtro Contorno
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        contourFilter = self.image.filter(ImageFilter.CONTOUR)
        return contourFilter

    def getOriginalImage(self):
        return self.image

class Blur: # Filtro blur / embaçado
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        blurredImage = self.image.filter(ImageFilter.GaussianBlur(5))
        return blurredImage

    def getOriginalImage(self):
        return self.image
    
class FullHD: # Filtro estilo FullHD
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        # Convert to RGB if not already in that mode
        if self.image.mode != 'RGB':
            self.image = self.image.convert('RGB')
        
        # Apply a smooth filter
        smooth_image = self.image.filter(ImageFilter.SMOOTH_MORE)
        
        # Enhance the image (contrast, brightness)
        enhancer = ImageEnhance.Contrast(smooth_image)
        enhanced_image = enhancer.enhance(1.5)
        
        enhancer = ImageEnhance.Brightness(enhanced_image)
        final_image = enhancer.enhance(1.2)
        
        return final_image

    def getOriginalImage(self):
        return self.image