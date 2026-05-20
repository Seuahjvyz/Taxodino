from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.favorito import Favorito
from app.models.dinosaurio import Dinosaurio
from pydantic import BaseModel

router = APIRouter()

class FavoritoCreate(BaseModel):
    usuario_id: int
    dinosaurio_id: int

class FavoritoResponse(BaseModel):
    id: int
    usuario_id: int
    dinosaurio_id: int
    dinosaurio_nombre: str

@router.post("/", response_model=FavoritoResponse)
async def crear_favorito(
    favorito: FavoritoCreate,
    db: Session = Depends(get_db)
):
    """Agrega un dinosaurio a favoritos"""
    # Verificar si el dinosaurio existe
    dinosaurio = db.query(Dinosaurio).filter(Dinosaurio.id == favorito.dinosaurio_id).first()
    if not dinosaurio:
        raise HTTPException(status_code=404, detail="Dinosaurio no encontrado")
    
    # Verificar si ya existe
    existing = db.query(Favorito).filter(
        Favorito.usuario_id == favorito.usuario_id,
        Favorito.dinosaurio_id == favorito.dinosaurio_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Ya está en favoritos")
    
    db_favorito = Favorito(**favorito.dict())
    db.add(db_favorito)
    db.commit()
    db.refresh(db_favorito)
    
    return FavoritoResponse(
        id=db_favorito.id,
        usuario_id=db_favorito.usuario_id,
        dinosaurio_id=db_favorito.dinosaurio_id,
        dinosaurio_nombre=dinosaurio.nombre
    )

@router.delete("/{usuario_id}/{dinosaurio_id}")
async def eliminar_favorito(
    usuario_id: int,
    dinosaurio_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un dinosaurio de favoritos"""
    favorito = db.query(Favorito).filter(
        Favorito.usuario_id == usuario_id,
        Favorito.dinosaurio_id == dinosaurio_id
    ).first()
    
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito no encontrado")
    
    db.delete(favorito)
    db.commit()
    
    return {"message": "Eliminado de favoritos"}

@router.get("/{usuario_id}", response_model=List[FavoritoResponse])
async def get_favoritos(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene todos los favoritos de un usuario"""
    favoritos = db.query(Favorito).filter(Favorito.usuario_id == usuario_id).all()
    
    result = []
    for fav in favoritos:
        dino = db.query(Dinosaurio).filter(Dinosaurio.id == fav.dinosaurio_id).first()
        if dino:
            result.append(FavoritoResponse(
                id=fav.id,
                usuario_id=fav.usuario_id,
                dinosaurio_id=fav.dinosaurio_id,
                dinosaurio_nombre=dino.nombre
            ))
    
    return result