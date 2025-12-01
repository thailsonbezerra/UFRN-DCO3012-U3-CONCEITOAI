import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import Generator
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("FALHA AO CARREGAR DATABASE_URL DA VARIÁVEL DE AMBIENTE")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def query(sql: str, params=None, fetch_one=False):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                if fetch_one:
                    return cur.fetchone()
                return cur.fetchall()
    except Exception as e:
        raise RuntimeError(f"Erro no banco: {e}")

class Transaction:
    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    def execute(self, sql, params=None, fetch_one=False):
        self.cur.execute(sql, params or ())
        if fetch_one:
            return self.cur.fetchone()
        return None

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()


def transaction() -> Transaction:
    return Transaction()
