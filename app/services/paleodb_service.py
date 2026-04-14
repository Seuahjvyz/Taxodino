import httpx
from typing import Optional, Dict, Any, List

class PaleoDBService:
    BASE_URL = "https://paleobiodb.org/data1.2"
    
    @staticmethod
    async def buscar_fosiles(nombre_cientifico: str) -> List[Dict[str, Any]]:
        """Busca registros fósiles en Paleobiology Database"""
        
        async with httpx.AsyncClient() as client:
            try:
                # Endpoint para ocurrencias
                response = await client.get(
                    f"{PaleoDBService.BASE_URL}/occs/list.json",
                    params={
                        "base_name": nombre_cientifico,
                        "show": "attr,loc,geo,coords",
                        "limit": "all"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    records = data.get("records", [])
                    
                    # Procesar registros únicos (sin duplicados por ubicación)
                    fosiles = []
                    seen_locations = set()
                    
                    for record in records:
                        ubicacion = record.get("loc", "")
                        if ubicacion not in seen_locations:
                            seen_locations.add(ubicacion)
                            fosiles.append(PaleoDBService._parse_fosil_record(record))
                    
                    return fosiles[:5]  # Limitamos a 5 ubicaciones únicas
            except Exception as e:
                print(f"Error en PaleoDB: {e}")
        return []
    
    @staticmethod
    def _parse_fosil_record(record: Dict) -> Dict:
        """Parsea un registro fósil"""
        return {
            "ubicacion": record.get("loc", ""),
            "coordenadas_lat": float(record.get("lat", 0)) if record.get("lat") else None,
            "coordenadas_lng": float(record.get("lng", 0)) if record.get("lng") else None,
            "edad_geologica": record.get("early_interval", ""),
            "formacion_rocosa": record.get("formation", ""),
            "museo_codigo": record.get("collection_name", "")[:100]
        }