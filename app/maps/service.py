# app/maps/service.py
from app.database.connection import query
from typing import List, Dict

def listar_mapas() -> List[Dict]:
    sql = """
        SELECT m.uuid, m.focus_question, m.created,
               t.name AS topic_central_name
        FROM maps m
        JOIN topics t ON t.id = m.topic_id_central
        ORDER BY m.created DESC
    """
    return query(sql)