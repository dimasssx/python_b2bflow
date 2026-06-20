import os 
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_KEY = os.getenv("ZAPI_KEY")

def enviar_mensagem(numero: str, mensagem: str):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-messages"
    payload = {
    "phone": numero,
    "message": mensagem
     }
    headers = {
    "Client-Token": ZAPI_KEY,
    "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())

def buscar_contatos(supabase:Client):
   try:
        response = supabase.table("contatos").select("*").execute()
        if not response.data:
            logging.info("Nenhum contato encontrado.")
            return []
        return response.data
   except Exception as e:
        logging.error(f"Erro ao buscar contatos: {e}")
        return []
   

def main():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    contatos = buscar_contatos(supabase)

    for contato in contatos:
        print(contato)
        nome_contato = contato.get("nome", "")
        numero_contato = contato.get("contato", "")
        if nome_contato == "eu":
            enviar_mensagem(numero_contato, f"Olá, {nome_contato} tudo bem com você?")

if __name__ == "__main__":    main()


