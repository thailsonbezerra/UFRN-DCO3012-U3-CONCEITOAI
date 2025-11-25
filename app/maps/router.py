from fastapi import APIRouter
from typing import List, Dict
from app.maps.service import listar_mapas

router = APIRouter(prefix="/maps", tags=["Mapas"])

@router.get("/", response_model=List[Dict])
def listar():
    return listar_mapas()