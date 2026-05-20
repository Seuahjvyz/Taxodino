from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.services.dinosaur_geography_service import DinosaurGeographyService
from app.services.local_dinosaur_data import get_local_dinosaurs_by_country
from app.models.registro_fosil import RegistroFosil
from app.models.dinosaurio import Dinosaurio

router = APIRouter()
geo_service = DinosaurGeographyService()

@router.get("/paises")
async def get_paises():
    """Retorna lista de países disponibles en el mapa"""
    paises = sorted({
        settings.get_country_label(pais)
        for pais in settings.PAISES_COORDENADAS.keys()
    })
    return paises

@router.get("/paises-detalle")
async def get_paises_detalle():
    """Retorna países con coordenadas para dibujar el mapa mundial"""
    return [
        {
            "clave": pais,
            "nombre": settings.get_country_label(pais),
            "coordenadas": coordenadas
        }
        for pais, coordenadas in sorted(settings.PAISES_COORDENADAS.items())
    ]

@router.get("/dinosaurios/{pais}")
async def get_dinosaurios_por_pais(
    pais: str, 
    db: Session = Depends(get_db)
):
    """
    Obtiene dinosaurios encontrados en un país específico
    """
    pais_key = settings.normalize_country_key(pais)

    if not pais_key:
        raise HTTPException(status_code=400, detail="Debes indicar un país válido")
    
    # Primero buscar en base de datos local
    registros = db.query(RegistroFosil).filter(
        RegistroFosil.pais == pais_key
    ).all()
    
    if registros:
        dinosaurios_ids = list(dict.fromkeys(
            r.dinosaurio_id for r in registros if r.dinosaurio_id is not None
        ))
        dinosaurios = []
        if dinosaurios_ids:
            dinosaurios = db.query(Dinosaurio).filter(
                Dinosaurio.id.in_(dinosaurios_ids)
            ).all()
        
        coordenadas = settings.PAISES_COORDENADAS.get(pais_key, {
            "lat": 0, "lng": 0, "continente": "Desconocido"
        })
        
        return {
            "pais": settings.get_country_label(pais_key),
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

    local_resultado = get_local_dinosaurs_by_country(pais_key)
    if local_resultado["total"] > 0:
        return local_resultado
    
    # Si no hay datos locales, usar API externa (PaleoDB)
    try:
        resultado = await geo_service.get_dinosaurs_by_country(pais_key)
        return resultado
    except Exception as e:
        # Si falla la API externa, devolver mensaje amigable
        return {
            "pais": settings.get_country_label(pais_key),
            "coordenadas": settings.PAISES_COORDENADAS.get(pais_key, {
                "lat": 0, "lng": 0, "continente": "Desconocido"
            }),
            "dinosaurios": [],
            "fuente": "No hay datos disponibles",
            "total": 0,
            "mensaje": f"No se encontraron registros fósiles en {settings.get_country_label(pais_key)} aún. ¡Pronto agregaremos más información!"
        }
