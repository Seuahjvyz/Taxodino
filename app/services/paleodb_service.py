import httpx
from typing import Optional, Dict, Any, List

class PaleoDBService:
    BASE_URL = "https://paleobiodb.org/data1.2"
    
    @staticmethod
    async def buscar_fosiles(nombre_cientifico: str) -> List[Dict[str, Any]]:
        """Busca registros fósiles en Paleobiology Database"""
        
        if not nombre_cientifico or len(nombre_cientifico) < 3:
            return []
        
        async with httpx.AsyncClient() as client:
            try:
                # Limpiar nombre para la búsqueda
                nombre_busqueda = nombre_cientifico.split()[0] if " " in nombre_cientifico else nombre_cientifico
                
                response = await client.get(
                    f"{PaleoDBService.BASE_URL}/occs/list.json",
                    params={
                        "base_name": nombre_busqueda,
                        "show": "attr,loc,geo,coords",
                        "limit": "10"
                    },
                    timeout=30.0,
                    headers={"User-Agent": "Taxodino/1.0"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    records = data.get("records", [])
                    
                    if records:
                        print(f"✅ PaleoDB: {len(records)} registros fósiles encontrados")
                    else:
                        print(f"⚠️ PaleoDB: no se encontraron fósiles para {nombre_busqueda}")
                    
                    fosiles = []
                    for record in records[:5]:
                        fosiles.append(PaleoDBService._parse_fosil_record(record))
                    
                    return fosiles
                    
            except Exception as e:
                print(f"❌ Error en PaleoDB: {e}")
        return []
    
    @staticmethod
    def _parse_fosil_record(record: Dict) -> Dict:
        return {
            "ubicacion": record.get("loc", "Ubicación desconocida"),
            "coordenadas_lat": float(record.get("lat", 0)) if record.get("lat") else None,
            "coordenadas_lng": float(record.get("lng", 0)) if record.get("lng") else None,
            "edad_geologica": record.get("early_interval", "Desconocida"),
            "formacion_rocosa": record.get("formation", "No especificada"),
            "museo_codigo": record.get("collection_name", "")[:100]
        }