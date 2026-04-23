from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from app.models.dinosaurio import Dinosaurio
from app.schemas.dinosaurio import DinosaurioResponse, DinosaurioCreate
from app.services.paleodb_service import PaleoDBService

router = APIRouter()

# Servicios
paleo_service = PaleoDBService()

@router.get("/")
async def get_all_dinosaurs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los dinosaurios (formato para frontend)"""
    try:
        dinosaurios = db.query(Dinosaurio).offset(skip).limit(limit).all()
        total = db.query(Dinosaurio).count()
        
        # Formato que espera el frontend
        return {
            "data": [
                {
                    "id": d.id,
                    "nombre": d.nombre,
                    "nombre_cientifico": d.nombre_cientifico,
                    "periodo": d.periodo,
                    "dieta": d.dieta,
                    "descripcion": d.descripcion,
                    "imagen_url": d.imagen_url,
                    "longitud_metros": d.longitud,
                    "peso_kg": d.peso
                }
                for d in dinosaurios
            ],
            "total": total,
            "message": "Success"
        }
    except Exception as e:
        print(f"Error en get_all_dinosaurs: {e}")
        return {
            "data": [],
            "total": 0,
            "message": f"Error: {str(e)}"
        }

@router.get("/{dinosaurio_id}")
async def get_dinosaur(
    dinosaurio_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un dinosaurio por ID (formato para frontend)"""
    try:
        dinosaurio = db.query(Dinosaurio).filter(Dinosaurio.id == dinosaurio_id).first()
        if not dinosaurio:
            raise HTTPException(status_code=404, detail="Dinosaurio no encontrado")
        
        # Formato que espera el frontend
        return {
            "id": dinosaurio.id,
            "nombre": dinosaurio.nombre,
            "nombre_cientifico": dinosaurio.nombre_cientifico,
            "periodo": dinosaurio.periodo,
            "dieta": dinosaurio.dieta,
            "descripcion": dinosaurio.descripcion,
            "imagen_url": dinosaurio.imagen_url,
            "longitud_metros": dinosaurio.longitud,
            "peso_kg": dinosaurio.peso,
            "curiosidades": []
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_dinosaur: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/")
async def search_dinosaurs(
    query: str,
    db: Session = Depends(get_db)
):
    """Buscar dinosaurios por nombre (formato para frontend)"""
    try:
        # Buscar en base de datos local - CORREGIDO: usar 'nombre' en lugar de 'nombre_comun'
        dinosaurios = db.query(Dinosaurio).filter(
            (Dinosaurio.nombre.ilike(f"%{query}%")) |
            (Dinosaurio.nombre_cientifico.ilike(f"%{query}%"))
        ).all()
        
        if dinosaurios:
            return {
                "data": [
                    {
                        "id": d.id,
                        "nombre": d.nombre,
                        "nombre_cientifico": d.nombre_cientifico,
                        "periodo": d.periodo,
                        "dieta": d.dieta,
                        "descripcion": d.descripcion,
                        "imagen_url": d.imagen_url,
                        "longitud_metros": d.longitud,
                        "peso_kg": d.peso
                    }
                    for d in dinosaurios
                ],
                "total": len(dinosaurios),
                "message": f"Encontrados {len(dinosaurios)} dinosaurios"
            }
        
        # Si no hay en local, buscar en PaleoDB
        fosiles = await paleo_service.buscar_fosiles(query)
        
        return {
            "data": fosiles,
            "total": len(fosiles),
            "message": f"Búsqueda en PaleoDB: {len(fosiles)} resultados"
        }
        
    except Exception as e:
        print(f"Error en search_dinosaurs: {e}")
        return {
            "data": [],
            "total": 0,
            "message": f"Error: {str(e)}"
        }

@router.post("/")
async def create_dinosaur(
    nombre: str,
    nombre_cientifico: str = None,
    periodo: str = None,
    dieta: str = None,
    descripcion: str = None,
    db: Session = Depends(get_db)
):
    """Crear un nuevo dinosaurio"""
    try:
        nuevo_dino = Dinosaurio(
            nombre=nombre,
            nombre_cientifico=nombre_cientifico,
            periodo=periodo,
            dieta=dieta,
            descripcion=descripcion
        )
        db.add(nuevo_dino)
        db.commit()
        db.refresh(nuevo_dino)
        
        return {
            "id": nuevo_dino.id,
            "nombre": nuevo_dino.nombre,
            "message": "Dinosaurio creado exitosamente"
        }
    except Exception as e:
        print(f"Error en create_dinosaur: {e}")
        raise HTTPException(status_code=500, detail=str(e))