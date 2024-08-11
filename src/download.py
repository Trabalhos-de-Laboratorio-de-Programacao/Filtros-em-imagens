import requests
import os
import base64
import re
from tqdm import tqdm

class Download:
    def __init__(self, url=None, path_arquivo=None):
        self.url = url
        self.path_arquivo = path_arquivo
        self.callback = None  # Function to be called for progress updates

    def set_callback(self, callback):
        self.callback = callback

    def executa(self):
        if self.url:
            if self.url.startswith("http://") or self.url.startswith("https://"):
                return self.download_from_url()
            elif self.url.startswith("data:image/"):
                return self.save_image_from_base64()
        elif self.path_arquivo:
            return self.save_local_file()
        else:
            raise Exception("Nenhuma URL ou caminho de arquivo fornecido.")

    def download_from_url(self):
        try:
            print('Aguarde...')
            response = requests.get(self.url, stream=True)  # Habilita streaming para progresso
            response.raise_for_status()  # Verifica se houve algum erro na requisição
            total_size = int(response.headers.get('content-length', 0))  # Tamanho total do arquivo
            with open(self.path_arquivo, 'wb') as file:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=self.path_arquivo) as pbar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
                            if self.callback:
                                self.callback(total_size, pbar.n)  # Chama o callback com o tamanho total e o progresso atual
            print(f"Download completo. Tamanho: {total_size}, Arquivo salvo em: {self.path_arquivo}")
            return self.url
        except requests.exceptions.MissingSchema:
            print("URL inválida. Certifique-se de fornecer uma URL válida.")
            raise Exception('URL inválida. Certifique-se de fornecer uma URL válida.')
        except requests.exceptions.RequestException as e:
            print(f"Erro na conexão: {e}")
            raise Exception(f"Erro na conexão: {e}")
        
    def get_next_image_number(self, directory):
        existing_files = os.listdir(directory)
        image_number = 0
        for f in existing_files: # Percorre os arquivos do diretório imagens
            match = re.search(r'image-(\d+)', f)
            if match: # Verifica apenas os arquivos iniciados por "image-"
                image_number += 1
        return image_number + 1

    def save_local_file(self):
        try:
            directory = "imagens"
            if not os.path.exists(directory):
                os.makedirs(directory)
            next_number = self.get_next_image_number(directory)
            file_extension = os.path.splitext(self.path_arquivo)[1][1:]
            file_name = f"image-{next_number}.{file_extension}"
            destination_path = os.path.join(directory, file_name)
            with open(self.path_arquivo, 'rb') as file:
                with open(destination_path, 'wb') as new_file:
                    new_file.write(file.read())
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
            
            with open(file_path, 'wb') as file:
                file.write(base64.b64decode(encoded))
                
            return file_path
        
        except Exception as e:
            raise Exception(f"Erro ao salvar imagem base64: {e}")