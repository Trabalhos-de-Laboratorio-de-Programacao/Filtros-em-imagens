import os
from PIL import Image
from tkinter import messagebox

class Imagem: 
    def __init__(self, imagem, nome):
        self.minha_imagem = imagem
        self.nome = nome
        self.local_referencia = self.salvar_imagem()

    def salvar_imagem(self):
        # Diretório onde a imagem será salva
        directory = r"C:\ImagensApp"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Verifica a extensão do nome da imagem
        base_name, extension = os.path.splitext(self.nome)
        if not extension:  # Se não tiver extensão, define como .jpeg
            extension = ".jpeg"
        
        # Gera um caminho inicial para o arquivo
        file_name = f"{base_name}{extension}"
        file_path = os.path.join(directory, file_name)

        # Incrementa o sufixo se o arquivo já existir
        count = 1
        while os.path.exists(file_path):
            file_path = os.path.join(directory, f"{base_name} ({count}){extension}")
            count += 1

        # Salva a imagem
        self.minha_imagem.save(file_path)
        return file_path

    def dimensoes(self):
        return self.minha_imagem.size

    def tamanho(self):
        return os.path.getsize(self.local_referencia)

    def formato(self):
        return self.minha_imagem.format

    def conteudo(self):
        return self.minha_imagem

    def informacoes(self):
        messagebox.showinfo(
            f'Nome: {os.path.basename(self.local_referencia)}\n'
            f'Dimensões: {self.dimensoes()}\n'
            f'Formato: {self.formato()}\n'
            f'Tamanho: {self.tamanho()} bytes'
        )
