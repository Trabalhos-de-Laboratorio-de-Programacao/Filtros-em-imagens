class BlackWhite: # Filtro preto e branco
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        grayscaleImage = self.image.convert("L")
        blackAndWhiteImage = grayscaleImage.convert("1")
        return blackAndWhiteImage

    def getOriginalImage(self):
        return self.image