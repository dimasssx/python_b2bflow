import os 
import logging

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def BuscarContatos(supabase:Client):
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
    contatos = BuscarContatos(supabase)
    print(contatos)

if __name__ == "__main__":    main()