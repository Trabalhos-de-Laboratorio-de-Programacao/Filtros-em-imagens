import requests
import os
import base64
import re

def download_image(url):
    def get_next_image_number(directory):
        existing_files = os.listdir(directory)
        image_number = 0
        for f in existing_files: # Percorre os arquivos do diretório imagens
            match = re.search(r'image-(\d+)', f)
            if match: # Verifica apenas os arquivos iniciados por "image-"
                image_number += 1
        return image_number + 1

    if url.startswith("data:image/"):
        # Handle base64 image
        header, encoded = url.split(",", 1)
        file_extension = header.split("/")[1].split(";")[0]
        directory = "imagens"
        next_number = get_next_image_number(directory)
        file_name = f"image-{next_number}.{file_extension}"
        file_path = os.path.join(directory, file_name)
        
        with open(file_path, 'wb') as file:
            file.write(base64.b64decode(encoded))
        return file_path