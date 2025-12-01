from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List, Dict
from app.maps.schemas import CreateMapSchema
from app.maps.service import listar_mapas, get_map_by_uuid, create_map

router = APIRouter(prefix="/maps", tags=["Mapas"])

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

@router.get("/{map_uuid}", summary="Busca mapa completo com grafo (nós + arestas)")
def buscar_mapa(map_uuid: UUID):
    try:
        return get_map_by_uuid(map_uuid)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno ao buscar mapa")