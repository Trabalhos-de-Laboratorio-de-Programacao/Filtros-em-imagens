from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
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
        
        # Frame dos thumbnails
        self.thumbnail_frame = Frame(self, width=200)
        self.thumbnail_frame.pack(side=LEFT, fill=Y) # Com fill ocupa todo o espaço vertical
        
        self.load_thumbnails()
        
    def load_thumbnails(self):
        image_folder = 'imagens'
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
        
        for image_file in os.listdir(image_folder):
            if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_path = os.path.join(image_folder, image_file)
                img = Image.open(image_path)
                img.thumbnail((100, 100))
                img = ImageTk.PhotoImage(img)
                
                btn = Button(self.thumbnail_frame, image=img, command=lambda p=image_path: self.select_image(p))
                btn.image = img  # Keep a reference to avoid garbage collection
                btn.pack(pady=5)

    def load_image(self):
        # Criar uma nova janela
        self.carregar_imagem_window = Toplevel(self)
        self.carregar_imagem_window.title("Carregar Imagem")
        
        # Botão para carregar arquivo local
        load_local_button = Button(self.carregar_imagem_window, text="Carregar arquivo local", command=self.load_local_file)
        load_local_button.pack()

        # Botão para download de URL
        download_url_button = Button(self.carregar_imagem_window, text="Download URL", command=self.download_url)
        download_url_button.pack()
        
    def load_local_file(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
        if caminho:
            download = Download(path_arquivo=caminho)
            download.executa()
            return True
        messagebox.showerror("Erro", "URL vazia")
        return False
        
    def download_url(self):
        caminho = simpledialog.askstring("Input", "Digite a URL da imagem:", parent=self.carregar_imagem_window)
        if caminho:
            download = Download(url=caminho)
            download.executa()
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