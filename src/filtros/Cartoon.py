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