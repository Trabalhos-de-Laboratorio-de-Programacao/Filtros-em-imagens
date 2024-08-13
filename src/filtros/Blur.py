class Blur: # Filtro blur / embaçado
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        blurredImage = self.image.filter(ImageFilter.GaussianBlur(5))
        return blurredImage

    def getOriginalImage(self):
        return self.image