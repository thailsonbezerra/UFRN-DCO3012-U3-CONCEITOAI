from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List, Dict

from app.maps.schemas import CreateMapSchema, CreateTopicSchema, UpdateTopicSchema, CreatePropositionSchema, UpdatePropositionSchema
from app.maps.service import (
    listar_mapas,
    get_map_by_uuid,
    create_map,
    create_topic,
    update_topic,
    delete_topic,
    create_proposition,
    update_proposition,
    delete_proposition
)

router = APIRouter(prefix="/maps", tags=["Mapas"])

### MAPAS ###
@router.post("/", summary="Cria um novo mapa conceitual")
def criar_mapa(data: CreateMapSchema):
    try:
        return create_map(
            focus_question=data.focus_question,
            central_topic_name=data.central_topic
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar mapa: {str(e)}")


@router.get("/", summary="Lista todos os mapas criados")
def listar() -> List[Dict]:
    return listar_mapas()


@router.get("/{map_uuid}", summary="Busca mapa completo (nós + proposições)")
def buscar_mapa(map_uuid: UUID):
    try:
        return get_map_by_uuid(map_uuid)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao buscar mapa")


### TÓPICOS ###
@router.post("/{map_uuid}/topics", summary="Cria um novo tópico dentro do mapa")
def criar_topico(map_uuid: UUID, data: CreateTopicSchema):
    try:
        return create_topic(map_uuid, data.name)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao criar tópico")


@router.put("/{map_uuid}/topics/{topic_id}", summary="Atualiza um tópico")
def atualizar_topico(map_uuid: UUID, topic_id: int, data: UpdateTopicSchema):
    try:
        return update_topic(map_uuid, topic_id, data.name)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao atualizar tópico")


@router.delete("/{map_uuid}/topics/{topic_id}", summary="Remove um tópico do mapa")
def remover_topico(map_uuid: UUID, topic_id: int):
    try:
        return delete_topic(map_uuid, topic_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao deletar tópico")

### PROPOSIÇÕES ###
@router.post("/{map_uuid}/propositions", summary="Cria uma proposição entre dois tópicos")
def criar_proposicao(map_uuid: UUID, data: CreatePropositionSchema):
    try:
        return create_proposition(map_uuid, data.source, data.target, data.label)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao criar proposição")


@router.put("/{map_uuid}/propositions/{prop_id}", summary="Atualiza a proposição")
def atualizar_proposicao(map_uuid: UUID, prop_id: int, data: UpdatePropositionSchema):
    try:
        return update_proposition(map_uuid, prop_id, data.label)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao atualizar proposição")


@router.delete("/{map_uuid}/propositions/{prop_id}", summary="Remove uma proposição")
def remover_proposicao(map_uuid: UUID, prop_id: int):
    try:
        return delete_proposition(map_uuid, prop_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao deletar proposição")
