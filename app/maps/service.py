from app.database.connection import query
from typing import List, Dict
from uuid import UUID
from fastapi import HTTPException

def listar_mapas() -> List[Dict]:
    sql = """
        SELECT 
            m.uuid,
            m.focus_question,
            m.created,
            t.name AS central_topic_name
        FROM maps m
        LEFT JOIN topics t ON t.id = m.topic_id_central
        ORDER BY m.created DESC
    """
    return query(sql)


def get_map_by_uuid(map_uuid: UUID) -> Dict:
    # 1. Busca o mapa
    mapa = query(
        """
        SELECT 
            m.id,
            m.uuid,
            m.focus_question,
            m.created,
            m.topic_id_central,
            tc.name AS central_topic_name
        FROM maps m
        LEFT JOIN topics tc ON tc.id = m.topic_id_central
        WHERE m.uuid = %s
        """,
        [str(map_uuid)],
        fetch_one=True
    )

    if not mapa:
        raise HTTPException(status_code=404, detail="Mapa não encontrado")

    map_id = mapa["id"]

    # 2. Todos os tópicos deste mapa
    nodes = query(
        "SELECT id, name FROM topics WHERE map_id = %s ORDER BY id",
        [map_id]
    )

    # 3. Todas as proposições deste mapa
    links = query(
        """
        SELECT 
            p.id,
            p.topic_id_origin AS source,
            p.topic_id_destination AS target,
            p.text AS label
        FROM propositions p
        WHERE p.map_id = %s
        """,
        [map_id]
    )

    return {
        "map": {
            "uuid": str(mapa["uuid"]),
            "focus_question": mapa["focus_question"],
            "created": mapa["created"].isoformat() if mapa["created"] else None,
            "central_topic": {
                "id": mapa["topic_id_central"],
                "name": mapa["central_topic_name"]
            } if mapa["topic_id_central"] else None
        },
        "nodes": [{"id": n["id"], "name": n["name"]} for n in nodes],
        "links": [
            {
                "id": l["id"],
                "source": l["source"],
                "target": l["target"],
                "label": l["label"]
            }
            for l in links
        ]
    }