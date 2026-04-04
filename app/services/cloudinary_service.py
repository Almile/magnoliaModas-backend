import cloudinary
import cloudinary.uploader
from fastapi import UploadFile

cloudinary.config( 
  cloud_name = "dkmbs6lyk", 
  api_key = "866228495147311", 
  api_secret = "aKD81AXGYcQBbzoSgwckjehm7CA",
  secure = True
)

async def upload_imagem_cloudinary(arquivo: UploadFile):
    try:
        resultado = cloudinary.uploader.upload(arquivo.file, folder="magnolia_produtos")
        
        return resultado.get("secure_url")
    except Exception as e:
        print(f"Erro no Cloudinary: {e}")
        return None