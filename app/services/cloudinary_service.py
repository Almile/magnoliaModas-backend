import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

cloudinary.config( 
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
    api_key = os.getenv("CLOUDINARY_API_KEY"), 
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure = True
)

async def upload_imagem_cloudinary(arquivo: UploadFile):
    try:
        resultado = cloudinary.uploader.upload(arquivo.file, folder="magnolia_produtos")
        return resultado.get("secure_url")
    except Exception as e:
        print(f"Erro no Cloudinary: {e}")
        return None