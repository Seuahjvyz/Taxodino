from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from app.core.config import settings
from app.models.dinosaurio import Dinosaurio
from app.models.registro_fosil import RegistroFosil
from app.schemas.dinosaurio import DinosaurioResponse, DinosaurioCreate
from app.services.local_dinosaur_data import (
    get_all_local_dinosaurs,
    get_local_dinosaur_by_id,
    search_local_dinosaurs,
)
from app.services.paleodb_service import PaleoDBService

router = APIRouter()

# Servicios
paleo_service = PaleoDBService()


def _build_dinosaur_key(nombre: Optional[str], nombre_cientifico: Optional[str]) -> str:
    primary = (nombre or "").strip().lower()
    secondary = (nombre_cientifico or "").strip().lower()
    return primary or secondary


def _serialize_db_dinosaur(
    dinosaurio: Dinosaurio,
    ubicaciones_por_dino: Dict[int, List[Dict[str, Any]]]
) -> Dict[str, Any]:
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
        "ubicaciones": ubicaciones_por_dino.get(dinosaurio.id) or _resolve_known_locations(dinosaurio)
    }


def _merge_dinosaur_sources(
    db_dinosaurios: List[Dict[str, Any]],
    local_dinosaurios: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    combinados: Dict[str, Dict[str, Any]] = {}

    for dinosaurio in local_dinosaurios:
        key = _build_dinosaur_key(
            dinosaurio.get("nombre"),
            dinosaurio.get("nombre_cientifico")
        )
        if key:
            combinados[key] = dinosaurio

    for dinosaurio in db_dinosaurios:
        key = _build_dinosaur_key(
            dinosaurio.get("nombre"),
            dinosaurio.get("nombre_cientifico")
        )
        if key:
            combinados[key] = dinosaurio

    return sorted(
        combinados.values(),
        key=lambda dinosaurio: (dinosaurio.get("nombre") or "").lower()
    )


def _resolve_known_locations(dinosaurio: Dinosaurio) -> List[Dict[str, Any]]:
    nombres = [
        (dinosaurio.nombre or "").strip().lower(),
        (dinosaurio.nombre_cientifico or "").strip().lower()
    ]
    paises = []
    for nombre in nombres:
        paises.extend(settings.DINOSAURIO_UBICACIONES_CONOCIDAS.get(nombre, []))

    ubicaciones = []
    for pais in dict.fromkeys(paises):
        coordenadas = settings.PAISES_COORDENADAS.get(pais)
        if not coordenadas:
            continue
        ubicaciones.append({
            "pais": settings.PAISES_LABELS.get(pais, pais.capitalize()),
            "clave": pais,
            "latitud": coordenadas["lat"],
            "longitud": coordenadas["lng"],
            "continente": coordenadas.get("continente", "Desconocido"),
            "fuente": "Referencia conocida"
        })
    return ubicaciones


def _group_locations_by_dinosaur(db: Session, dinosaurio_ids: List[int]) -> Dict[int, List[Dict[str, Any]]]:
    if not dinosaurio_ids:
        return {}

    registros = db.query(RegistroFosil).filter(
        RegistroFosil.dinosaurio_id.in_(dinosaurio_ids)
    ).all()

    ubicaciones_por_dino: Dict[int, List[Dict[str, Any]]] = {}
    vistos = set()

    for registro in registros:
        if not registro.dinosaurio_id or not registro.pais:
            continue

        pais = settings.normalize_country_key(registro.pais)
        clave = (registro.dinosaurio_id, pais)
        if clave in vistos:
            continue
        vistos.add(clave)

        coordenadas = settings.PAISES_COORDENADAS.get(pais, {})
        ubicaciones_por_dino.setdefault(registro.dinosaurio_id, []).append({
            "pais": settings.PAISES_LABELS.get(pais, registro.pais.capitalize()),
            "clave": pais,
            "latitud": registro.latitud if registro.latitud is not None else coordenadas.get("lat"),
            "longitud": registro.longitud if registro.longitud is not None else coordenadas.get("lng"),
            "continente": coordenadas.get("continente", "Desconocido"),
            "fuente": "Registro fósil local",
            "formacion": registro.formacion,
            "edad_ma": registro.edad_ma
        })

    return ubicaciones_por_dino

@router.get("/")
async def get_all_dinosaurs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener todos los dinosaurios (formato para frontend)"""
    try:
        dinosaurios_db = db.query(Dinosaurio).all()
        ubicaciones_por_dino = _group_locations_by_dinosaur(db, [d.id for d in dinosaurios_db])
        data_db = [
            _serialize_db_dinosaur(dinosaurio, ubicaciones_por_dino)
            for dinosaurio in dinosaurios_db
        ]
        local_data = get_all_local_dinosaurs()
        combined_data = _merge_dinosaur_sources(data_db, local_data)

        return {
            "data": combined_data[skip:skip + limit],
            "total": len(combined_data),
            "message": "Success"
        }
    except Exception as e:
        print(f"Error en get_all_dinosaurs: {e}")
        local_data = get_all_local_dinosaurs()
        return {
            "data": local_data[skip:skip + limit],
            "total": len(local_data),
            "message": f"Fallback local: {str(e)}"
        }

@router.get("/search/")
async def search_dinosaurs(
    query: str,
    db: Session = Depends(get_db)
):
    """Buscar dinosaurios por nombre (formato para frontend)"""
    try:
        dinosaurios_db = db.query(Dinosaurio).filter(
            (Dinosaurio.nombre.ilike(f"%{query}%")) |
            (Dinosaurio.nombre_cientifico.ilike(f"%{query}%")) |
            (Dinosaurio.periodo.ilike(f"%{query}%")) |
            (Dinosaurio.dieta.ilike(f"%{query}%")) |
            (Dinosaurio.descripcion.ilike(f"%{query}%"))
        ).all()

        ubicaciones_por_dino = _group_locations_by_dinosaur(db, [d.id for d in dinosaurios_db])
        data_db = [
            _serialize_db_dinosaur(dinosaurio, ubicaciones_por_dino)
            for dinosaurio in dinosaurios_db
        ]
        local_results = search_local_dinosaurs(query)
        combined_results = _merge_dinosaur_sources(data_db, local_results)

        if combined_results:
            return {
                "data": combined_results,
                "total": len(combined_results),
                "message": f"Encontrados {len(combined_results)} dinosaurios"
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
        local_results = search_local_dinosaurs(query)
        return {
            "data": local_results,
            "total": len(local_results),
            "message": f"Fallback local: {str(e)}"
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
            local_dinosaur = get_local_dinosaur_by_id(dinosaurio_id)
            if local_dinosaur:
                return local_dinosaur
            raise HTTPException(status_code=404, detail="Dinosaurio no encontrado")

        ubicaciones = _group_locations_by_dinosaur(db, [dinosaurio.id]).get(dinosaurio.id) or _resolve_known_locations(dinosaurio)

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
            "curiosidades": [],
            "ubicaciones": ubicaciones
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en get_dinosaur: {e}")
        local_dinosaur = get_local_dinosaur_by_id(dinosaurio_id)
        if local_dinosaur:
            return local_dinosaur
        raise HTTPException(status_code=500, detail=str(e))

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
