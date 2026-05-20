from typing import Any, Dict, List, Optional

from app.core.config import settings
from populate_dinosaurs import DINOSAURIOS_EJEMPLO, REGISTROS_FOSILES_EJEMPLO


LOCAL_ID_OFFSET = 10000


def _build_lookup() -> Dict[int, Dict[str, Any]]:
    lookup: Dict[int, Dict[str, Any]] = {}
    for index, dinosaurio in enumerate(DINOSAURIOS_EJEMPLO, start=1):
        record = dict(dinosaurio)
        record["id"] = LOCAL_ID_OFFSET + index
        lookup[record["id"]] = record
    return lookup


LOCAL_DINOSAURS_BY_ID = _build_lookup()


def _serialize_locations(nombre: str) -> List[Dict[str, Any]]:
    ubicaciones = []
    vistos = set()
    for registro in REGISTROS_FOSILES_EJEMPLO.get(nombre, []):
        pais = settings.normalize_country_key(registro.get("pais", ""))
        if not pais or pais in vistos:
            continue
        vistos.add(pais)
        coordenadas = settings.PAISES_COORDENADAS.get(pais, {})
        ubicaciones.append({
            "pais": settings.get_country_label(pais),
            "clave": pais,
            "latitud": registro.get("latitud", coordenadas.get("lat")),
            "longitud": registro.get("longitud", coordenadas.get("lng")),
            "continente": coordenadas.get("continente", "Desconocido"),
            "fuente": "Catálogo local",
            "formacion": registro.get("formacion"),
            "edad_ma": registro.get("edad_ma"),
        })
    return ubicaciones


def serialize_local_dinosaur(record: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": record["id"],
        "nombre": record["nombre"],
        "nombre_cientifico": record.get("nombre_cientifico"),
        "periodo": record.get("periodo"),
        "dieta": record.get("dieta"),
        "descripcion": record.get("descripcion"),
        "imagen_url": record.get("imagen_url"),
        "longitud_metros": record.get("longitud"),
        "peso_kg": record.get("peso"),
        "ubicaciones": _serialize_locations(record["nombre"]),
    }


def get_all_local_dinosaurs() -> List[Dict[str, Any]]:
    return [
        serialize_local_dinosaur(record)
        for record in LOCAL_DINOSAURS_BY_ID.values()
    ]


def search_local_dinosaurs(query: str) -> List[Dict[str, Any]]:
    needle = (query or "").strip().lower()
    if not needle:
        return get_all_local_dinosaurs()

    matches = []
    for record in LOCAL_DINOSAURS_BY_ID.values():
        haystack = " ".join([
            str(record.get("nombre", "")),
            str(record.get("nombre_cientifico", "")),
            str(record.get("periodo", "")),
            str(record.get("dieta", "")),
            str(record.get("descripcion", "")),
        ]).lower()
        if needle in haystack:
            matches.append(serialize_local_dinosaur(record))
    return matches


def get_local_dinosaur_by_id(dinosaurio_id: int) -> Optional[Dict[str, Any]]:
    record = LOCAL_DINOSAURS_BY_ID.get(dinosaurio_id)
    if not record:
        return None

    data = serialize_local_dinosaur(record)
    data["curiosidades"] = []
    return data


def get_local_dinosaurs_by_country(country: str) -> Dict[str, Any]:
    country_key = settings.normalize_country_key(country)
    dinosaurios = []

    for record in LOCAL_DINOSAURS_BY_ID.values():
        registros = REGISTROS_FOSILES_EJEMPLO.get(record["nombre"], [])
        if any(settings.normalize_country_key(item.get("pais", "")) == country_key for item in registros):
            dinosaurios.append({
                "id": record["id"],
                "nombre": record["nombre"],
                "nombre_cientifico": record.get("nombre_cientifico"),
                "periodo": record.get("periodo"),
                "dieta": record.get("dieta"),
                "descripcion": (record.get("descripcion") or "")[:200],
            })

    return {
        "pais": settings.get_country_label(country_key),
        "coordenadas": settings.PAISES_COORDENADAS.get(country_key, {
            "lat": 0,
            "lng": 0,
            "continente": "Desconocido",
        }),
        "dinosaurios": dinosaurios,
        "fuente": "Catálogo local",
        "total": len(dinosaurios),
        "mensaje": (
            f"No se encontraron registros fósiles en {settings.get_country_label(country_key)} aún."
            if not dinosaurios else None
        ),
    }
