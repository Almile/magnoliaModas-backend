import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
load_dotenv()

def initialize_firebase():
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "app/core/serviceAccountKey.json")
    
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        
        return firestore.client()
    except Exception as e:
        print(f"Erro ao conectar ao Firebase: {e}")
        return None

db = initialize_firebase()