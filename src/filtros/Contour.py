class Contour: # Filtro Contorno
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        contourFilter = self.image.filter(ImageFilter.CONTOUR)
        return contourFilter

    def getOriginalImage(self):
        return self.image