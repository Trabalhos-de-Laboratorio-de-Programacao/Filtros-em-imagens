from PIL import Image

class Imagem:
    def __init__(self, file_path):
        self.image = Image.open(file_path)

    def apply_filter(self, filter):
        # Apply the selected filter to the image
        pass