import requests
import os
from tkinter import messagebox
import base64
import re
from tqdm import tqdm
from urllib.parse import urlparse

class Download:
    def __init__(self, url=None, path_arquivo=None):
        self.url = url
        self.path_arquivo = path_arquivo
        self.callback = None  # Function to be called for progress updates

    def set_callback(self, callback):
        self.callback = callback
        
    def extrair_nome_extensao_url(self, url):
        try:
            parsed_url = urlparse(url)
            if parsed_url.scheme not in ('http', 'https', 'ftp'):
                raise ValueError(f"Unsupported protocol: {parsed_url.scheme}")

            caminho_arquivo = parsed_url.path
            if not caminho_arquivo:
                raise ValueError("Missing file path in URL")

            # Split the path to get the filename and handle query parameters
            nome_arquivo_completo = os.path.basename(caminho_arquivo).split('?')[0]
            nome_arquivo, extensao = os.path.splitext(nome_arquivo_completo)
            return nome_arquivo, extensao

        except Exception as ex:
            raise ValueError(f"{str(ex)}") from ex 

    def executa(self):
        if self.url:
            if self.url.startswith("http://") or self.url.startswith("https://"):
                return self.download_from_url()
            elif self.url.startswith("data:image/"):
                return self.save_image_from_base64()
        elif self.path_arquivo:
            if self.path_arquivo[-4:] == ".txt": # Se for feito upload de uma arquivo .txt
                return self.download_arquivos_txt()
            else:
                return self.save_local_file()
        else:
            raise Exception("Nenhuma URL ou caminho de arquivo fornecido.")

    def download_from_url(self):
        try:
            _, file_extension = self.extrair_nome_extensao_url(self.url)
            response = requests.get(self.url, stream=True)  # Habilita streaming para progresso
            response.raise_for_status()  # Verifica se houve algum erro na requisição
            total_size = int(response.headers.get('content-length', 0))  # Tamanho total do arquivo
            directory = "imagens"
            if not os.path.exists(directory):
                os.makedirs(directory)
            next_number = self.get_next_image_number(directory)
            file_name = f"image-{next_number}{file_extension}"
            destination_path = os.path.join(directory, file_name)
            self.progress_bar(destination_path, total_size, response)
            return destination_path
        except Exception as e:
            messagebox.showerror("ERRO", f"Erro ao baixar a imagem: {e}")
        except requests.exceptions.MissingSchema:
            messagebox.showerror("ERRO", "URL inválida. Certifique-se de fornecer uma URL válida.")
            raise Exception('URL inválida. Certifique-se de fornecer uma URL válida.')
        except requests.exceptions.RequestException as e:
            messagebox.showerror("ERRO", f"Erro na conexão: {e}")
            raise Exception(f"Erro na conexão: {e}")
        
    def progress_bar(self, destination_path, total_size, response = None):
        if self.url: # Arquivo online
            with open(destination_path, 'wb') as file:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=destination_path) as pbar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            if self.url.startswith("data:image/"):
                                file.write(base64.b64decode(encoded))
                            else:
                                file.write(chunk)
                            pbar.update(len(chunk))
                            if self.callback:
                                self.callback(total_size, pbar.n)  # Chama o callback com o tamanho total e o progresso atual
        elif self.path_arquivo: # Arquivo local
            with open(destination_path, 'wb') as new_file:
                with open(self.path_arquivo, 'rb') as file:
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc=destination_path) as pbar:
                        while True:
                            chunk = file.read(1024)
                            if not chunk:
                                break
                            new_file.write(chunk)
                            pbar.update(len(chunk))
                            if self.callback:
                                self.callback(total_size, pbar.n)  # Chama o callback com o tamanho total e o progresso atual
                new_file.flush()
        
    def get_next_image_number(self, directory):
        existing_files = os.listdir(directory)
        image_number = 0
        for f in existing_files: # Percorre os arquivos do diretório imagens
            match = re.search(r'image-(\d+)', f)
            if match: # Verifica apenas os arquivos iniciados por "image-"
                image_number += 1
        return image_number + 1
    
    def download_arquivos_txt(self):
        with open(self.path_arquivo, 'r') as file:
            links = file.read().splitlines()
        destinos = []
        for link in links:
            download_url = Download(url = link)
            destinos.append(download_url.executa())
        destinos = '\n'.join(destinos) # Concatena caminhos dos arquivos criados
        return destinos

    def save_local_file(self):
        try:
            directory = "imagens"
            if not os.path.exists(directory):
                os.makedirs(directory)
            next_number = self.get_next_image_number(directory)
            file_extension = os.path.splitext(self.path_arquivo)[1][1:]
            file_name = f"image-{next_number}.{file_extension}"
            destination_path = os.path.join(directory, file_name)
            total_size = os.path.getsize(self.path_arquivo)
            with open(self.path_arquivo, 'rb') as file:
                self.progress_bar(destination_path, total_size)
            return destination_path
        except Exception as e:
            raise Exception(f"Erro ao salvar arquivo local: {e}")

    def save_image_from_base64(self):
        # Imagem em base64
        try:
            header, encoded = self.url.split(",", 1)
            file_extension = header.split("/")[1].split(";")[0]
            directory = "imagens"
            next_number = get_next_image_number(directory)
            file_name = f"image-{next_number}.{file_extension}"
            file_path = os.path.join(directory, file_name)
            
            self.progress_bar(destination_path, total_size)
                
            return file_path
        
        except Exception as e:
            raise Exception(f"Erro ao salvar imagem base64: {e}")