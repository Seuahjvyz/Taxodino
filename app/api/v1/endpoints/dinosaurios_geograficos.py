from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.config import settings
from app.services.dinosaur_geography_service import DinosaurGeographyService
from app.models.registro_fosil import RegistroFosil
from app.models.dinosaurio import Dinosaurio

router = APIRouter()
geo_service = DinosaurGeographyService()

@router.get("/paises")
async def get_paises():
    """Retorna lista de países disponibles en el mapa"""
    paises = sorted([p.capitalize() for p in settings.PAISES_API.keys()])
    return paises

@router.get("/dinosaurios/{pais}")
async def get_dinosaurios_por_pais(
    pais: str, 
    db: Session = Depends(get_db)
):
    """
    Obtiene dinosaurios encontrados en un país específico
    """
    pais_lower = pais.lower()
    
    # Verificar si el país existe
    if pais_lower not in settings.PAISES_API:
        raise HTTPException(status_code=404, detail=f"País '{pais}' no encontrado")
    
    # Primero buscar en base de datos local
    registros = db.query(RegistroFosil).filter(
        RegistroFosil.pais == pais_lower
    ).all()
    
    if registros:
        dinosaurios_ids = [r.dinosaurio_id for r in registros]
        dinosaurios = db.query(Dinosaurio).filter(
            Dinosaurio.id.in_(dinosaurios_ids)
        ).all()
        
        coordenadas = settings.PAISES_COORDENADAS.get(pais_lower, {
            "lat": 0, "lng": 0, "continente": "Desconocido"
        })
        
        return {
            "pais": pais.capitalize(),
            "coordenadas": coordenadas,
            "dinosaurios": [
                {
                    "id": d.id,
                    "nombre": d.nombre,
                    "nombre_cientifico": d.nombre_cientifico,
                    "periodo": d.periodo,
                    "dieta": d.dieta,
                    "descripcion": d.descripcion[:200] if d.descripcion else ""
                }
                for d in dinosaurios
            ],
            "fuente": "Base de datos local",
            "total": len(dinosaurios)
        }
    
    # Si no hay datos locales, usar API externa (PaleoDB)
    try:
        resultado = await geo_service.get_dinosaurs_by_country(pais_lower)
        return resultado
    except Exception as e:
        # Si falla la API externa, devolver mensaje amigable
        return {
            "pais": pais.capitalize(),
            "coordenadas": settings.PAISES_COORDENADAS.get(pais_lower, {
                "lat": 0, "lng": 0, "continente": "Desconocido"
            }),
            "dinosaurios": [],
            "fuente": "No hay datos disponibles",
            "total": 0,
            "mensaje": f"No se encontraron registros fósiles en {pais.capitalize()} aún. ¡Pronto agregaremos más información!"
        }