import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import Generator
from dotenv import load_dotenv

load_dotenv()  # ← lê o .env

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("FALHA AO CARREGAR DATABASE_URL DA VARIÁVEL DE AMBIENTE")

def get_db() -> Generator:
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

# Função auxiliar pra usar direto (mais simples no começo)
def query(sql: str, params=None, fetch_one=False):
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                if fetch_one:
                    return cur.fetchone()
                return cur.fetchall()
    except Exception as e:
        raise RuntimeError(f"Erro no banco: {e}")