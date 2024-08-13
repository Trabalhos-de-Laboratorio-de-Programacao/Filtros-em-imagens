import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu, simpledialog
from PIL import Image, ImageTk
from download import Download
import filtros, imagem  # Certifique-se de que o caminho do módulo está correto

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Display")
        self.root.geometry("1000x600")  # Aumentar o tamanho da janela inicial

        # Frame para os controles à esquerda
        self.control_frame = tk.Frame(root, padx=10, pady=10)  # Adiciona padding ao frame
        self.control_frame.grid(row=0, column=0, sticky="nw")

        # Button to load image
        self.button = tk.Button(self.control_frame, text="Carregar Imagem", command=self.carregar_imagem)
        self.button.pack(pady=5)

        # Dropdown for filters
        self.selected_filter = StringVar(root)
        self.selected_filter.set("Escolha um filtro")  # Default value
        self.filter_menu = OptionMenu(self.control_frame, self.selected_filter, "Escala de Cinza", "Preto e Branco", "Cartoon", "Negative", "Contour", "Blurred")
        self.filter_menu.pack(pady=5)

        # Button to apply filter
        self.apply_filter_button = tk.Button(self.control_frame, text="Aplicar Filtro", command=self.aplicar_filtro)
        self.apply_filter_button.pack(pady=5)

        # Button to restore original image
        self.restore_button = tk.Button(self.control_frame, text="Restaurar Imagem", command=self.restaurar_imagem)
        self.restore_button.pack(pady=5)

        # Button to save image
        self.save_button = tk.Button(self.control_frame, text="Salvar Como", command=self.salvar_imagem)
        self.save_button.pack(pady=5)

        # Frame para a imagem com borda
        self.image_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)  # Adiciona uma borda ao frame
        self.image_frame.grid(row=0, column=1, sticky="nsew")

        self.canvas = tk.Canvas(self.image_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Frame para as thumbnails
        self.thumbnail_frame = tk.Frame(root)
        self.thumbnail_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.thumbnail_buttons = []  # Lista para armazenar os botões de thumbnail
        self.thumbnails = []  # Lista para armazenar as thumbnails
        self.images = []  # Lista para armazenar as imagens carregadas

        self.image = None
        self.imagem_original = None  # Atributo para armazenar a imagem original
        self.tk_image = None
        self.downloader = Download()

        # Bind the resize event
        self.root.bind("<Configure>", self.atualizar_canvas)

        # Configurar a expansão das colunas
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)
        self.root.grid_rowconfigure(0, weight=1)

    def carregar_imagem(self):
        # Solicita a URL ou o caminho do arquivo através de uma janela de diálogo
        url_or_path = simpledialog.askstring("Carregar Imagem", "Digite a URL ou o caminho do arquivo:")
        
        if url_or_path:
            try:
                imagens = self.downloader.buscar_imagem(url_or_path)
                if imagens:
                    print("Imagem carregada com sucesso.")
                    for img_data in imagens:
                        try:
                            if len(self.images) < 10:  # Limitar a 10 imagens
                                self.imagem_original = Image.open(img_data)  # Armazena a imagem original
                                self.images.append(self.imagem_original)  # Adiciona a imagem à lista
                                self.atualizar_thumbnails()  # Atualiza as thumbnails
                                self.image = self.imagem_original.copy()  # Copia a imagem original para a imagem atual
                                self.atualizar_canvas()
                            else:
                                messagebox.showwarning("Limite de Imagens", "Você só pode carregar até 10 imagens.")
                            break
                        except Exception as e:
                            print(f"Erro ao abrir a imagem: {e}")
                            continue
                else:
                    print("Nenhuma imagem foi encontrada.")
            except Exception as e:
                print(f"Erro ao carregar a imagem: {e}")
                messagebox.showerror("Erro", f"Não foi possível carregar a imagem: {e}")

    def atualizar_thumbnails(self):
        # Limpa os botões de thumbnail existentes
        for button in self.thumbnail_buttons:
            button.destroy()
        self.thumbnail_buttons.clear()

        # Cria novos botões para as thumbnails
        for img in self.images:
            thumb = img.copy()
            thumb.thumbnail((100, 100))  # Redimensiona a thumbnail
            self.thumbnails.append(thumb)
            tk_thumb = ImageTk.PhotoImage(thumb)
            button = tk.Button(self.thumbnail_frame, image=tk_thumb, command=lambda img=img: self.carregar_thumbnail(img))
            button.image = tk_thumb  # Manter uma referência à imagem
            button.pack(side=tk.LEFT, padx=5, pady=5)
            self.thumbnail_buttons.append(button)

    def carregar_thumbnail(self, img):
        self.image = img.copy()  # Carrega a imagem correspondente à thumbnail
        self.atualizar_canvas()

    def aplicar_filtro(self):
        if self.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return
        
        filtro_selecionado = self.selected_filter.get()
        try:
            self.restaurar_imagem()  # Restaura a imagem original antes de aplicar um novo filtro
            if filtro_selecionado == "Escala de Cinza":
                filtro = filtros.grayscale(self.image)
            elif filtro_selecionado == "Preto e Branco":
                filtro = filtros.blackAndWhite(self.image)
            elif filtro_selecionado == "Cartoon":
                filtro = filtros.cartoon(self.image)
            elif filtro_selecionado == "Negative":
                filtro = filtros.negative(self.image)
            elif filtro_selecionado == "Contour":
                filtro = filtros.contour(self.image)
            elif filtro_selecionado == "Blurred":
                filtro = filtros.blurred(self.image)
            else:
                raise ValueError("Filtro desconhecido.")

            self.image = filtro.applyFilter()
            self.atualizar_canvas()
            print(f"Filtro '{filtro_selecionado}' aplicado com sucesso.")
        except Exception as e:
            print(f"Erro ao aplicar o filtro: {e}")
            messagebox.showerror("Erro", f"Não foi possível aplicar o filtro: {e}")

    def restaurar_imagem(self):
        if self.imagem_original is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem original carregada.")
            return

        self.image = self.imagem_original.copy()  # Restaura a imagem original
        self.atualizar_canvas()
        print("Imagem restaurada para o estado original.")

    def salvar_imagem(self):
        if self.image is None:
            messagebox.showwarning("Aviso", "Nenhuma imagem carregada.")
            return

        nome_arquivo = simpledialog.askstring("Salvar Como", "Digite o nome do arquivo:")
        if nome_arquivo:
            try:
                imagem_obj = imagem.Imagem(self.image, nome_arquivo)
                messagebox.showinfo("Sucesso", f"Imagem salva como: {imagem_obj.local_referencia}")
            except Exception as e:
                print(f"Erro ao salvar a imagem: {e}")
                messagebox.showerror("Erro", f"Não foi possível salvar a imagem: {e}")

    def atualizar_canvas(self, event=None):
        # Tamanho máximo do canvas
        max_width = 600
        max_height = 450
        
        # Limpa o canvas antes de adicionar a nova imagem
        self.canvas.delete("all")

        if self.image:
            # Obtém as dimensões da imagem
            img_width, img_height = self.image.size
            
            # Calcula a nova largura e altura mantendo a proporção
            ratio = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)

            # Redimensiona a imagem
            resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)

            # Atualiza o canvas
            self.canvas.config(scrollregion=(0, 0, new_width, new_height))

            # Centraliza a imagem no canvas
            x_offset = (self.canvas.winfo_width() - new_width) // 2
            y_offset = (max_height - new_height) // 2
            self.tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(x_offset, y_offset, image=self.tk_image, anchor=tk.NW)
        else:
            # Se não houver imagem, exibe uma mensagem
            self.canvas.create_text(max_width / 2, max_height / 2, text="Carregue uma imagem", fill="gray", font=("Arial", 16))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
