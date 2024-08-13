class Negative: # Filtro imagem negativa (cores invertidas)
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        negativeImage = ImageChops.invert(self.image)
        return negativeImage

    def getOriginalImage(self):
        return self.image