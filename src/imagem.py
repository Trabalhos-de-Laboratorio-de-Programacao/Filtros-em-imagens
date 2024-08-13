import os
from tkinter import *
from tkinter import Toplevel, Frame
from PIL import Image, ImageTk
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
        messagebox.showinfo('Informações da imagem',f'Nome: {self.nome_arquivo}\nDimensoes:{self.dimensoes()}\nFormato: {self.formato()}\nTamanho: {self.tamanho()} B')
        
class WindowImageViewer:
    """
    Classe para mostrar uma imagem em uma janela tkinter
    """

    def __init__(self, image_name, image_path, menu_window, main):
        """
        Inicializa o image viewer com uma janela parent e um image path

        Args:
        image_path: O path do arquivo de imagem que será exibido
        menu_window: A janela parent dessa janela
        """
        self.app = Toplevel()
        self.app.title(f"{image_name} - Visualizar Imagem")
        
        # Armazenar referência à janela principal
        self.main = main
        
        # Store reference to parent window
        self.menu_window = menu_window

        # Create a frame to hold the image
        self.image_frame = Frame(self.app)
        
        # Error handling: Check if image exists before loading
        if not os.path.exists(image_path):
            messagebox.showerror("ERRO", "Imagem não encontrada!")
            return

        # Load image using PIL
        self.image = Image.open(image_path)
        self.image_frame.pack(expand=True, fill=BOTH)

        self.create_widgets(image_path)  # Separate function to create widgets

        # Bind the close button to the destroy function
        self.app.protocol("WM_DELETE_WINDOW", self.destroy)

    def create_widgets(self, image_path):
        """
        Creates the canvas, scrollbars, and displays the image.

        Args:
        image_path: The path to the image file to be displayed.
        """
        self.canvas = Canvas(self.image_frame, relief=SUNKEN)
        self.canvas.config(width=800, height=800, highlightthickness=0)

        self.sbarV = Scrollbar(self.image_frame, orient=VERTICAL)
        self.sbarH = Scrollbar(self.image_frame, orient=HORIZONTAL)

        self.sbarV.config(command=self.canvas.yview)
        self.sbarH.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarV.set)
        self.canvas.config(xscrollcommand=self.sbarH.set)

        self.sbarV.pack(side=RIGHT, fill=Y)
        self.sbarH.pack(side=BOTTOM, fill=X)

        self.canvas.pack(side=LEFT, expand=True, fill=BOTH)

        self.display_image(image_path)  # Separate function to display the image

    def display_image(self, image_path):
        """
        Opens the image, sets scroll region, and displays it.

        Args:
        image_path: The path to the image file to be displayed.
        """
        try:
            self.image = Image.open(image_path)
            width, height = self.image.size
            self.canvas.config(scrollregion=(0, 0, width, height))
            self.image2 = ImageTk.PhotoImage(self.image)
            self.imgtag = self.canvas.create_image(0, 0, anchor="nw", image=self.image2)
        except FileNotFoundError:
            messagebox.showerror("ERRO", "Erro: Imagem não encontrada!")

    def destroy(self):
        # Reabilita o botão na janela principal
        try:
            self.main.open_button.config(state="normal")
        except:
            self.main.open_button_filtro.config(state="normal")
        self.app.destroy()