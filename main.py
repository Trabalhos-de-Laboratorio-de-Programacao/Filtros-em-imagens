from tkinter import *
from tkinter import filedialog, simpledialog
from src.download import *
from src.imagem import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Filtros de imagens')
        self.geometry('{}x{}'.format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.wm_state('zoomed')
        self.create_widgets()

    def create_widgets(self):
        menu_bar = Menu(self)
        
        # Menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Carregar Imagem", command=self.load_image)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.quit)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        
        self.config(menu=menu_bar)

    def load_image(self):
        # Criar uma nova janela
        carregar_imagem_window = Toplevel(self)
        carregar_imagem_window.title("Carregar Imagem")
        
        # Botão para carregar arquivo local
        load_local_button = Button(carregar_imagem_window, text="Carregar arquivo local", command=self.load_local_file)
        load_local_button.pack()

        # Botão para download de URL
        download_url_button = Button(carregar_imagem_window, text="Download URL", command=self.download_url)
        download_url_button.pack()
        
    def load_local_file(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
        if caminho:
            save_image(caminho, False)
        
    def download_url(self):
        url = simpledialog.askstring("Input", "Digite a URL da imagem:", parent=self)
        if url:
            file_path = save_image(url, True)
            return True
        messagebox.showerror("Erro", "URL vazia")
        return False

    def process_image(self, file_path):
        # Process the image using the Imagem class
        img = Imagem(file_path)
        # Add further processing and display logic here

if __name__ == '__main__':
    app = App()
    app.mainloop()