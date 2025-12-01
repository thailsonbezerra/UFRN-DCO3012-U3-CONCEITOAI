from app.database.connection import query, transaction
from typing import List, Dict
from uuid import UUID
from fastapi import HTTPException

def create_map(focus_question: str, central_topic_name: str) -> dict:
    tx = transaction()
    try:
        # 1. Criar mapa e retornar tudo que vamos usar
        mapa = tx.execute(
            """
            INSERT INTO maps (focus_question)
            VALUES (%s)
            RETURNING id, uuid, created, focus_question
            """,
            (focus_question,),
            fetch_one=True
        )
        map_id = mapa["id"]
        map_uuid = mapa["uuid"]

        # 2. Criar tópico central
        topic = tx.execute(
            """
            INSERT INTO topics (map_id, name)
            VALUES (%s, %s)
            RETURNING id, name
            """,
            (map_id, central_topic_name.strip().capitalize()),
            fetch_one=True
        )
        topic_id = topic["id"]

        # 3. Associar tópico central ao mapa
        tx.execute(
            "UPDATE maps SET topic_id_central = %s WHERE id = %s",
            (topic_id, map_id)
        )

        # 4. Commit
        tx.commit()

        # 5. Retorno limpo e completo
        return {
            "map": {
                "uuid": str(map_uuid),
                "focus_question": mapa["focus_question"],
                "created": mapa["created"].isoformat(),
                "central_topic": {
                    "id": topic["id"],
                    "name": topic["name"]
                }
            },
            "nodes": [
                {"id": topic["id"], "name": topic["name"]}
            ],
            "links": []
        }

    except Exception as e:
        tx.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar mapa: {str(e)}")
    finally:
        tx.close()

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
    
def create_topic(map_uuid: UUID, name: str) -> dict:
    # Validar mapa
    mapa = query(
        "SELECT id FROM maps WHERE uuid = %s",
        [str(map_uuid)],
        fetch_one=True
    )
    if not mapa:
        raise HTTPException(404, "Mapa não encontrado")

    map_id = mapa["id"]

    # Criar tópico
    topic = query(
        """
        INSERT INTO topics (map_id, name)
        VALUES (%s, %s)
        RETURNING id, name
        """,
        [map_id, name.strip()],
        fetch_one=True
    )

    return {"id": topic["id"], "name": topic["name"]}

def update_topic(map_uuid: UUID, topic_id: int, name: str):
    result = query(
        """
        UPDATE topics
        SET name = %s
        WHERE id = %s AND map_id = (SELECT id FROM maps WHERE uuid = %s)
        RETURNING id
        """,
        [name.strip(), topic_id, str(map_uuid)],
        fetch_one=True
    )

    if not result:
        raise HTTPException(404, "Tópico não encontrado")
    
    return {"id": topic_id, "name": name}

def delete_topic(map_uuid: UUID, topic_id: int):
    tx = transaction()
    try:
        # Remover tópico central se for ele
        tx.execute(
            """
            UPDATE maps
            SET topic_id_central = NULL
            WHERE uuid = %s AND topic_id_central = %s
            """,
            [str(map_uuid), topic_id]
        )

        # Deletar tópico (proposições caem pela FK)
        deleted = tx.execute(
            """
            DELETE FROM topics
            WHERE id = %s 
              AND map_id = (SELECT id FROM maps WHERE uuid = %s)
            RETURNING id
            """,
            [topic_id, str(map_uuid)],
            fetch_one=True
        )

        if not deleted:
            tx.rollback()
            raise HTTPException(404, "Tópico não encontrado")

        tx.commit()
        return {"deleted": topic_id}
    except:
        tx.rollback()
        raise

def create_proposition(map_uuid: UUID, source: int, target: int, label: str):
    mapa = query(
        "SELECT id FROM maps WHERE uuid = %s",
        [str(map_uuid)],
        fetch_one=True
    )
    if not mapa:
        raise HTTPException(404, "Mapa não encontrado")

    map_id = mapa["id"]

    prop = query(
        """
        INSERT INTO propositions (map_id, topic_id_origin, topic_id_destination, text)
        VALUES (%s, %s, %s, %s)
        RETURNING id, text
        """,
        [map_id, source, target, label],
        fetch_one=True
    )

    return {
        "id": prop["id"],
        "source": source,
        "target": target,
        "label": prop["text"]
    }

def update_proposition(map_uuid: UUID, prop_id: int, label: str):
    updated = query(
        """
        UPDATE propositions
        SET text = %s
        WHERE id = %s
          AND map_id = (SELECT id FROM maps WHERE uuid = %s)
        RETURNING id
        """,
        [label.strip(), prop_id, str(map_uuid)],
        fetch_one=True
    )

    if not updated:
        raise HTTPException(404, "Proposição não encontrada")

    return {"id": prop_id, "label": label}

def delete_proposition(map_uuid: UUID, prop_id: int):
    deleted = query(
        """
        DELETE FROM propositions
        WHERE id = %s
          AND map_id = (SELECT id FROM maps WHERE uuid = %s)
        RETURNING id
        """,
        [prop_id, str(map_uuid)],
        fetch_one=True
    )

    if not deleted:
        raise HTTPException(404, "Proposição não encontrada")

    return {"deleted": prop_id}
