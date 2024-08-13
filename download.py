# Description: Módulo responsável por baixar imagens de uma URL, de um arquivo .txt ou de um arquivo local.

import requests
from io import BytesIO

class Download:
    def __init__(self):
        pass

    def buscar_imagem(self, source):
        if source.startswith('http'):
            return [self._baixar_de_url(source)]
        elif source.endswith('.txt'):
            return self._baixar_de_txt(source)
        else:
            return [self._ler_de_arquivo(source)]

    def _baixar_de_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return BytesIO(response.content)

    def _baixar_de_txt(self, filepath):
        imagens = []
        with open(filepath, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
                    imagens.append(self._baixar_de_url(url))
        return imagens

    def _ler_de_arquivo(self, filepath):
        with open(filepath, 'rb') as file:
            return BytesIO(file.read())
    