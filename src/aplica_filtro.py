import os
from src.filtros import *
class AplicaFiltro:
    def aplica_filtro_grayscale(self, minha_imagem, nome):
        directory = 'filtradas'
        if not os.path.exists(directory):
            os.makedirs(directory)
        grayscale_filter = GrayScale(minha_imagem)
        filtered_image_grayscale = grayscale_filter.applyFilter()
        nome = os.path.join('filtradas', nome + '_grayscale.jpg')
        filtered_image_grayscale.save(nome)

    def aplica_filtro_blackwhite(self, minha_imagem, nome):
        directory = 'filtradas'
        if not os.path.exists(directory):
            os.makedirs(directory)
        blackwhite_filter = BlackWhite(minha_imagem)
        filtered_image_blackwhite = blackwhite_filter.applyFilter()
        nome = os.path.join('filtradas', nome + '_blackwhite.jpg')
        filtered_image_blackwhite.save(nome)

    def aplica_filtro_cartoon(self, minha_imagem, nome):
        directory = 'filtradas'
        if not os.path.exists(directory):
            os.makedirs(directory)
        cartoon_filter = Cartoon(minha_imagem)
        filtered_image_cartoon = cartoon_filter.applyFilter()
        nome = os.path.join('filtradas', nome + '_cartoon.jpg')
        filtered_image_cartoon.save(nome)

    def aplica_filtro_negative(self, minha_imagem, nome):
        directory = 'filtradas'
        if not os.path.exists(directory):
            os.makedirs(directory)
        negative_filter = Negative(minha_imagem)
        filtered_image_negative = negative_filter.applyFilter()
        nome = os.path.join('filtradas', nome + '_negative.jpg')
        filtered_image_negative.save(nome)

    def aplica_filtro_contour(self, minha_imagem, nome):
        directory = 'filtradas'
        if not os.path.exists(directory):
            os.makedirs(directory)
        contour_filter = Contour(minha_imagem)
        filtered_image_contour = contour_filter.applyFilter()
        nome = os.path.join('filtradas', nome + '_contour.jpg')
        filtered_image_contour.save(nome)

    def aplica_filtro_blur(self, minha_imagem, nome):
        directory = 'filtradas'
        if not os.path.exists(directory):
            os.makedirs(directory)
        blur_filter = Blur(minha_imagem)
        filtered_image_blur = blur_filter.applyFilter()
        nome = os.path.join('filtradas', nome + '_blur.jpg')
        filtered_image_blur.save(nome)
        
    def save_filtro(self):
        pass