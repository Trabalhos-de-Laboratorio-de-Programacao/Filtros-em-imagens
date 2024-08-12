from PIL import Image
from tkinter import messagebox

class Imagem: 
    minha_imagem = None
    def __init__(self, id, nome_arquivo, path_arquivo):
        self.id = id
        self.nome_arquivo = nome_arquivo
        self.local_referencia = path_arquivo
        try:
            self.minha_imagem = Image.open(path_arquivo)
        except Exception as ex:
            messagebox.showerror('ERRO', f'Erro ao criar a imagem com o arquivo {nome_arquivo} na referência {path_arquivo}: {str(ex)}')

    def dimensoes(self):
        return self.minha_imagem.size

    def tamanho(self):
        return os.path.getsize(self.local_referencia)

    def formato(self):
        return self.minha_imagem.format

    def conteudo(self):
        return self.minha_imagem

    def informacoes(self):
        messagebox.showinfo(f'Nome: {self.nome_arquivo}\nDimensoes:{self.dimensoes()}\nFormato: {self.formato()}\nTamanho: {self.tamanho()}')