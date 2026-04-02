import firebase_admin
from firebase_admin import auth, credentials
import os
from dotenv import load_dotenv

load_dotenv()

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "app/core/serviceAccountKey.json")
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def promover_pelo_email(email):
    try:
        user = auth.get_user_by_email(email)
        
        auth.set_custom_user_claims(user.uid, {'role': 'admin'})
        
        print(f"✅ SUCESSO: O usuário {email} agora é oficialmente ADMIN no Firebase Auth!")
        print("⚠️ IMPORTANTE: Você precisa fazer um NOVO LOGIN para gerar um token atualizado.")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    promover_pelo_email("magnolia@gmail.com")