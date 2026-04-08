from google import genai
from google.genai import types
import os
import json
from PIL import Image
import io
from fastapi import HTTPException

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def analisar_roupa_com_ia(imagem_bytes):
    try:
        img = Image.open(io.BytesIO(imagem_bytes))
        
        prompt = """
            Analise a roupa nesta imagem para a loja 'Magnólia Modas'.
            Retorne um JSON com: nome, categoria, estacao, descricao, preco_sugerido.
            Responda APENAS o JSON puro.
        """

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=[prompt, img],
            config=types.GenerateContentConfig  (
                response_mime_type="application/json"
            )
        )

        if not response.text:
            raise Exception("A IA não conseguiu processar a imagem.")

        return json.loads(response.text)

    except Exception as e:
        print(f"Erro no Gemini: {str(e)}")
        if "API_KEY_INVALID" in str(e):
             raise HTTPException(status_code=401, detail="Chave do Gemini está incorreta no .env")
        raise HTTPException(status_code=500, detail=f"Erro na IA: {str(e)}")