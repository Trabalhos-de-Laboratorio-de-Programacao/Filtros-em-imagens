from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
from src.download import *
from src.imagem import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Filtros de imagens')
        self.geometry('{}x{}'.format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.wm_state('zoomed')
        self.image_paths = self.list_files_by_date("imagens") #Carrega as imagens salvas
        # Pré-carrega action-frame para que seja reconhecido em open_image
        self.action_frame = None
        # Definindo open_button no init para que seja possível desabilitá-lo
        self.open_button = None
        self.create_widgets()
        
    def restart_app(self):
        self.destroy()  # Destrói a janela atual
        self.__init__()  # Recria a instância da classe App
        
    def list_files_by_date(self,directory_path):
        try:
            file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path)]
            # Cria lista de file paths com suas datas de criações
            file_info = []
            for file_path in file_paths:
                try:
                    # Captura a data de criação e transforma em um objeto datetime
                    creation_time = os.path.getctime(file_path)
                    creation_datetime = datetime.fromtimestamp(creation_time)
                    file_info.append((file_path, creation_datetime))
                except Exception as e:
                    print(f"Error getting creation time for {file_path}: {e}")

            file_info.sort(key=lambda x: x[1])
            # Extract only the file paths
            return [file_path for file_path, _ in file_info]
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def create_widgets(self):
        # Menu
        menu_bar = Menu(self)
        file_menu = Menu(menu_bar, tearoff=0)
        
        # Submenu "Carregar Imagem"
        load_image_menu = Menu(file_menu, tearoff=0)
        load_image_menu.add_command(label="Carregar Arquivo Local", command=self.load_local_file)
        load_image_menu.add_command(label="Download URL", command=self.download_url)
        
        file_menu.add_cascade(label="Carregar Imagem", menu=load_image_menu) # file_menu contém load_image_menu
        file_menu.add_separator()
        file_menu.add_command(label="Reiniciar", command=self.restart_app)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.quit)
        menu_bar.add_cascade(label="Arquivo", menu=file_menu)
        
        self.config(menu=menu_bar)
        
        # Frame dos thumbnails
        self.thumbnail_frame = Frame(self, width=200)
        self.thumbnail_frame.pack(side=LEFT, fill=Y) # Com fill ocupa todo o espaço vertical
        
        self.load_thumbnails()
        
    def load_thumbnails(self):        
         # Create a canvas for scrolling
        self.canvas = Canvas(self.thumbnail_frame)
        self.canvas.config(width=150, height=320)
        self.canvas.pack(side=LEFT, fill=Y, expand=True)

        # Create a scrollbar
        self.scrollbar = Scrollbar(self.thumbnail_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Configure scrollbar and canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # Bind mouse wheel event to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)

        # Create inner frame to hold buttons (avoid directly adding to canvas)
        self.inner_frame = Frame(self.canvas)

        self.display_thumbnails()  # Separate function to display the buttons
        
    def _on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                
    def display_thumbnails(self):
        for i, image_path in enumerate(self.image_paths):
            # Cria um thumbnail usando PIL
            # thumbnail = Image.open(image_path).resize((100, 100), Image.ANTIALIAS) # IMCOMPATÍVEL
            thumbnail = Image.open(image_path).resize((100, 100), Image.Resampling.LANCZOS)
            thumbnail_photo = ImageTk.PhotoImage(thumbnail)
            # Cria um botão com o thumbnail e caminho do arquivo
            thumbnail_button = Button(self.inner_frame, image=thumbnail_photo, command=lambda path=image_path: self.select_image(path))
            thumbnail_button.image = thumbnail_photo
            thumbnail_button.pack(side=TOP)
        
        # Coloca um frame interno no canvas com uma âncora (opcional)
        self.canvas.create_window((0, 0), anchor="nw", window=self.inner_frame)

        # Update the scroll region of the canvas
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    
    def refresh_thumbnails(self):
        # Lógica para atualizar os thumbnails
        # Por exemplo, limpar e recarregar os thumbnails
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.load_thumbnails()  # Supondo que exista uma função para carregar os thumbnails
        
    def select_image(self, image_path):
        image_name = os.path.basename(image_path) # Armazena o nome da imagem para que seja exibido ao abrir
        # Remove o frame anterior, se existir
        if hasattr(self, 'action_frame') and self.action_frame is not None:
            self.action_frame.destroy()
        
        # Cria um novo frame ao lado dos thumbnails
        self.action_frame = Frame(self, width=200, height=100)
        self.action_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)
        
        # Label Nome do arquivo
        filename_label = Label(self.action_frame, text=image_name)
        filename_label.pack(pady=5)
        
        # Botão "Abrir"
        self.open_button = Button(self.action_frame, text="Abrir", command=lambda: self.open_image(image_name, image_path))
        self.open_button.pack(pady=5)
        
        # Botão "Aplicar Filtro"
        filter_button = Button(self.action_frame, text="Aplicar Filtro", command=lambda: self.apply_filter(image_path))
        filter_button.pack(pady=5)
        
        # Botão "Excluir"
        delete_button = Button(self.action_frame, text="Excluir", command=lambda: self.delete_image(image_path))
        delete_button.pack(pady=5)
        
    # Abrir imagem ao apertar em "Abrir"
    def open_image(self, image_name, image_path):
        self.open_button.config(state="disabled")
        
        # Cria uma instância WindowImageViewer para a imagem selecionada
        WindowImageViewer(image_name, image_path, self.action_frame, self)
        
    def apply_filter(self, image_path):
        # Implementar lógica para aplicar filtro na imagem
        return

    def delete_image(self, image_path):
        # Implementar lógica para excluir a imagem
        return
        
    def load_local_file(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.jpg *.jpeg *.png"), ("URLs", "*.txt")])
        if caminho:
            download = Download(path_arquivo=caminho)
            execucao = download.executa()
            if execucao:
                messagebox.showinfo("SUCESSO", f"Arquivo salvo em:\n{execucao}")
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