import requests
from tqdm import tqdm  # progress bar
import os

class Download:
    def __init__(self, url, path_arquivo):
        self.url = url
        self.path_arquivo = path_arquivo
        self.callback = None # Function to be called for progress updates

    def set_callback(self, callback):
        self.callback = callback

    def executa(self):
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