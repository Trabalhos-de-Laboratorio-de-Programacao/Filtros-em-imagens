from tkinter import *
from tkinter import filedialog, simpledialog
from src.download import download_image
from src.imagem import Imagem

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
        choice = simpledialog.askstring("Input", "Digite 'local' para carregar uma imagem local ou 'url' para carregar uma imagem da internet:")
        if choice == 'local':
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
            if file_path:
                self.process_image(file_path)
        elif choice == 'url':
            url = simpledialog.askstring("Input", "Digite a URL da imagem:")
            if url:
                file_path = download_image(url)
                #self.process_image(file_path)

    def process_image(self, file_path):
        # Process the image using the Imagem class
        img = Imagem(file_path)
        # Add further processing and display logic here

if __name__ == '__main__':
    app = App()
    app.mainloop()