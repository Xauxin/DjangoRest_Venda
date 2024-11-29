from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import pathlib

def redimensionar_imagem(imagem, codigo):
        imagem = pathlib.Path(imagem)
        imgs = {}
        img = Image.open(imagem)
        tamanhos = [60, 120, 240]
        for tamanho in tamanhos:
            img_resize = img.resize((tamanho, tamanho))
            buffer = BytesIO()
            img_resize.save(buffer, format='PNG')
            imgs[f'x{str(tamanho)}'] = ContentFile(buffer.getvalue(), name=f"{codigo}_{tamanho}.png")
        return imgs