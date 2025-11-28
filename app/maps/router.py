from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List, Dict
from app.maps.service import listar_mapas, get_map_by_uuid

router = APIRouter(prefix="/maps", tags=["Mapas"])

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