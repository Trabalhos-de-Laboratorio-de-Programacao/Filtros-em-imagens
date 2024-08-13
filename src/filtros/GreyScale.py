class GreyScale:
    def __init__(self, image):
        self.image = image

    def applyFilter(self):
        grayscaleImage = self.image.convert("L")
        return grayscaleImage

    def getOriginalImage(self):
        return self.image