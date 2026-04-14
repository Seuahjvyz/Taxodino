from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio

from app.core.database import get_db
from app.models import Dinosaurio, Imagen, WikidataInfo, RegistroFosil, Curiosidad
from app.services.dinosaurio_service import DinosaurioService

router = APIRouter()

@router.get("/")
async def get_all_dinosaurs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtiene todos los dinosaurios paginados"""
    
    dinosaurios = db.query(Dinosaurio).offset(skip).limit(limit).all()
    
    return {
        "total": db.query(Dinosaurio).count(),
        "data": [
            {
                "id": d.id,
                "nombre": d.nombre_comun,
                "nombre_cientifico": d.nombre_cientifico,
                "dieta": d.dieta,
                "periodo": d.periodo,
                "imagen_url": d.imagen_url or f"https://placehold.co/600x400/2D4A22/white?text={d.nombre_comun.replace(' ', '+')}",
                "descripcion": d.descripcion_general or f"Información sobre {d.nombre_comun}"
            }
            for d in dinosaurios
        ]
    }

@router.get("/search")
async def search_dinosaurs(
    query: str = Query(..., min_length=1, description="Nombre del dinosaurio a buscar"),
    db: Session = Depends(get_db)
):
    """Busca dinosaurios por nombre común o científico"""
    
    # 1. Buscar en BD local
    resultados = db.query(Dinosaurio).filter(
        (Dinosaurio.nombre_comun.ilike(f"%{query}%")) |
        (Dinosaurio.nombre_cientifico.ilike(f"%{query}%"))
    ).all()
    
    if resultados:
        return {
            "source": "database",
            "count": len(resultados),
            "data": [
                {
                    "id": d.id,
                    "nombre": d.nombre_comun,
                    "nombre_cientifico": d.nombre_cientifico,
                    "dieta": d.dieta,
                    "periodo": d.periodo,
                    "imagen_url": d.imagen_url or f"https://placehold.co/600x400/2D4A22/white?text={d.nombre_comun.replace(' ', '+')}",
                    "descripcion": d.descripcion_general
                }
                for d in resultados
            ]
        }
    
    # 2. Si no está en BD, buscar en APIs externas (solo para nombres válidos)
    # Lista de palabras que no son dinosaurios reales
    palabras_invalidas = ["carnivoro", "herbivoro", "omnivoro", "carnívoro", "herbívoro", "omnívoro", "dinosaurio", "dinosaur"]
    
    if query.lower() in palabras_invalidas:
        return {
            "source": "none",
            "count": 0,
            "data": [],
            "message": f"'{query}' es un tipo de dieta, no un dinosaurio específico. Busca nombres como 'Tiranosaurio Rex' o 'Velociraptor'."
        }
    
    # Buscar en APIs externas
    service = DinosaurioService(db)
    result = await service.buscar_o_crear(query)
    
    return result

@router.get("/{dino_id}")
async def get_dinosaur_by_id(
    dino_id: int,
    db: Session = Depends(get_db)
):
    """Obtiene un dinosaurio por su ID con toda la información"""
    
    dino = db.query(Dinosaurio).filter(Dinosaurio.id == dino_id).first()
    
    if not dino:
        raise HTTPException(status_code=404, detail="Dinosaurio no encontrado")
    
    # Obtener información relacionada
    imagenes = db.query(Imagen).filter(Imagen.dinosaurio_id == dino_id).all()
    wikidata_info = db.query(WikidataInfo).filter(WikidataInfo.dinosaurio_id == dino_id).first()
    registros_fosiles = db.query(RegistroFosil).filter(RegistroFosil.dinosaurio_id == dino_id).all()
    curiosidades = db.query(Curiosidad).filter(Curiosidad.dinosaurio_id == dino_id).all()
    
    return {
        "id": dino.id,
        "nombre": dino.nombre_comun,
        "nombre_cientifico": dino.nombre_cientifico,
        "dieta": dino.dieta,
        "periodo": dino.periodo,
        "longitud_metros": dino.longitud_metros,
        "peso_kg": dino.peso_kg,
        "altura_metros": dino.altura_metros,
        "descripcion": dino.descripcion_general,
        "imagen_url": dino.imagen_url,
        "imagenes": [
            {
                "url": img.url_imagen,
                "miniatura": img.url_miniatura,
                "principal": img.es_principal
            } for img in imagenes
        ] if imagenes else [],
        "wikidata": {
            "descubridor": wikidata_info.descubridor if wikidata_info else None,
            "año_descubrimiento": wikidata_info.año_descubrimiento if wikidata_info else None,
            "habitat": wikidata_info.habitat if wikidata_info else None
        } if wikidata_info else None,
        "registros_fosiles": [
            {
                "ubicacion": r.ubicacion,
                "edad_geologica": r.edad_geologica,
                "formacion_rocosa": r.formacion_rocosa
            } for r in registros_fosiles
        ] if registros_fosiles else [],
        "curiosidades": [c.texto_curiosidad for c in curiosidades] if curiosidades else [
            f"¡El {dino.nombre_comun} es un dinosaurio fascinante!",
            f"Vivió durante el período {dino.periodo or 'desconocido'}.",
            f"Era un dinosaurio {dino.dieta or 'desconocido'}."
        ]
    }