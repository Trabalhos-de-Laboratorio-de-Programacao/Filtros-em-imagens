import requests
import os
import base64
import re

def save_image(caminho, online):
    def get_next_image_number(directory):
        existing_files = os.listdir(directory)
        image_number = 0
        for f in existing_files: # Percorre os arquivos do diretório imagens
            match = re.search(r'image-(\d+)', f)
            if match: # Verifica apenas os arquivos iniciados por "image-"
                image_number += 1
        return image_number + 1

    if online:
        if caminho.startswith("data:image/"):
            # Imagem em base64
            header, encoded = caminho.split(",", 1)
            file_extension = header.split("/")[1].split(";")[0]
            directory = "imagens"
            next_number = get_next_image_number(directory)
            file_name = f"image-{next_number}.{file_extension}"
            file_path = os.path.join(directory, file_name)
            
            with open(file_path, 'wb') as file:
                file.write(base64.b64decode(encoded))
            return file_path
        else:
            # Imagem online
            response = requests.get(caminho)
            if response.status_code == 200:
                directory = "imagens"
                next_number = get_next_image_number(directory)
                file_extension = caminho.split(".")[-1]
                file_name = f"image-{next_number}.{file_extension}"
                file_path = os.path.join(directory, file_name)
                
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                return file_path
            else:
                return None
    elif not online:
        # Imagem local
        directory = "imagens"
        next_number = get_next_image_number(directory)
        file_name = f"image-{next_number}.png"
        file_path = os.path.join(directory, file_name)
        
        with open(caminho, 'rb') as file:
            with open(file_path, 'wb') as new_file:
                new_file.write(file.read())
        return file_path