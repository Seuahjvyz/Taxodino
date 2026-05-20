import httpx
from typing import List, Dict, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class DinosaurGeographyService:
    def __init__(self):
        self.paleodb_url = "https://paleobiodb.org/data1.2"
    
    async def get_dinosaurs_by_country(self, country_name: str) -> Dict:
        """
        Obtiene dinosaurios por país desde PaleoDB
        """
        country_lower = country_name.lower()
        
        # Obtener código ISO del país
        codigo_pais = settings.PAISES_API.get(country_lower)
        
        if not codigo_pais:
            return {
                "pais": country_name.capitalize(),
                "dinosaurios": [],
                "error": f"País '{country_name}' no soportado",
                "total": 0
            }
        
        # Consultar PaleoDB
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    f"{self.paleodb_url}/occs/list.json",
                    params={
                        "cc": codigo_pais,
                        "taxon_name": "Dinosauria",
                        "show": "coords,attr,loc",
                        "limit": 20
                    },
                    headers={"User-Agent": settings.USER_AGENT}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    records = data.get("records", [])
                    
                    dinosaurios = []
                    for record in records:
                        nombre_taxon = record.get("taxon_name", "")
                        if nombre_taxon:
                            dino = {
                                "nombre": nombre_taxon.split()[-1] if nombre_taxon else "Desconocido",
                                "nombre_cientifico": nombre_taxon,
                                "periodo": record.get("early_interval", "Desconocido"),
                                "dieta": self._guess_diet(nombre_taxon),
                                "descripcion": f"Fósil encontrado en {record.get('formation', 'formación rocosa')}, "
                                              f"período {record.get('early_interval', 'desconocido')}"
                            }
                            dinosaurios.append(dino)
                    
                    coordenadas = settings.PAISES_COORDENADAS.get(country_lower, {
                        "lat": 0, "lng": 0, "continente": "Desconocido"
                    })
                    
                    return {
                        "pais": country_name.capitalize(),
                        "coordenadas": coordenadas,
                        "dinosaurios": dinosaurios,
                        "fuente": "Paleobiology Database",
                        "total": len(dinosaurios)
                    }
                else:
                    return {
                        "pais": country_name.capitalize(),
                        "dinosaurios": [],
                        "fuente": "Error en la API",
                        "total": 0
                    }
                    
            except Exception as e:
                logger.error(f"Error en PaleoDB: {e}")
                return {
                    "pais": country_name.capitalize(),
                    "dinosaurios": [],
                    "fuente": "Error de conexión",
                    "total": 0,
                    "error": str(e)
                }
    
    def _guess_diet(self, nombre: str) -> str:
        """Adivina la dieta basado en el nombre"""
        nombre_lower = nombre.lower()
        if any(x in nombre_lower for x in ["raptor", "rex", "tirano", "carn", "megal", "spino"]):
            return "Carnívoro"
        if any(x in nombre_lower for x in ["ceratops", "saurus", "brachio", "diplo", "bronto", "stego"]):
            return "Herbívoro"
        return "Desconocida"