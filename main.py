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
            self.download_with_progress_bar(url)
            return True
        messagebox.showerror("Erro", "URL vazia")
        return False

    def download_with_progress_bar(self,url, path_arquivo=None):
        try:
            nome, extensao = self.utilidades.extrair_nome_extensao_url(url)
            filename = nome + extensao
            self.set_filename(filename)
            
            if path_arquivo: 
                download = Download(url, path_arquivo)
            else:
                download = Download(url, filename)

            def progress_callback(total_size, current_progress):
                percentual_avanco = int((current_progress/total_size)*100)
                self.my_var.set(str(int(percentual_avanco)) + '%')
                self.progress_bar["value"] = current_progress
                self.progress_bar["maximum"] = total_size
                self.app.update_idletasks()  # Update the progress bar smoothly

            download.set_callback(progress_callback)
            self.my_msg.set('Aguarde...')
            url = download.executa()
            file_path = save_image(url, True)
            self.my_msg.set(f'Download {self.filename} concluído com sucesso!')
        except Exception as ex:
            print(f'Erro: {str(ex)}')
            self.my_msg.set(f'Erro :{str(ex)}')
            self.my_var.set('0%')
            self.progress_bar['value'] = 0

    def process_image(self, file_path):
        # Process the image using the Imagem class
        img = Imagem(file_path)
        # Add further processing and display logic here

if __name__ == '__main__':
    app = App()
    app.mainloop()