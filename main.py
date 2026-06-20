import os 
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client, Client


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_KEY = os.getenv("ZAPI_KEY")

def validar_variaveis_ambiente():
    variaveis_necessarias = {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY": SUPABASE_KEY,
        "ZAPI_INSTANCE": ZAPI_INSTANCE,
        "ZAPI_TOKEN": ZAPI_TOKEN,
        "ZAPI_KEY": ZAPI_KEY
    }
    faltando = [nome for nome, valor in variaveis_necessarias.items() if not valor]
    if faltando:
        logger.error(f"Variáveis de ambiente faltando: {', '.join(faltando)}. Verifique o arquivo .env.")
        raise ValueError(f"Variáveis de ambiente faltando: {', '.join(faltando)}.")


def enviar_mensagem(numero: str, mensagem: str):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"
    payload = {
    "phone": numero,
    "message": mensagem
     }
    headers = {
    "Client-Token": ZAPI_KEY,
    "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers,timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar mensagem: {e}")
        return False
    
def buscar_contatos(supabase:Client):
   try:
        response = supabase.table("contatos").select("*").limit(3).execute()
        if not response.data:
            logger.info("Nenhum contato encontrado.")
            return []
        return response.data
   except Exception as e:
        logger.error(f"Erro ao buscar contatos: {e}")
        return []
   

def main():
    
    try:
        validar_variaveis_ambiente()
    except ValueError:
        return

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    contatos = buscar_contatos(supabase)

    if not contatos:
        logger.info("Nenhum contato encontrado.")
        return
    
    for contato in contatos:
        nome_contato = contato.get("nome", "")
        numero_contato = contato.get("contato", "")     
        if enviar_mensagem(numero_contato, f"Olá, {nome_contato} tudo bem com você?"):
            logger.info(f"Mensagem enviada para {nome_contato}")
        else:
            logger.error(f"Falha ao enviar mensagem para {nome_contato}")

        

if __name__ == "__main__":   
    main()


