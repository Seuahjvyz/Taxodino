import httpx
from typing import Optional, Dict, Any, List
from app.core.config import settings  # Importamos configuración

class PaleoDBService:
    BASE_URL = "https://paleobiodb.org/data1.2"
    
    # ============================================
    # MÉTODOS EXISTENTES (TU CÓDIGO)
    # ============================================
    
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
    
    # ============================================
    # NUEVOS MÉTODOS PARA EL MAPA MUNDIAL
    # ============================================
    
    @staticmethod
    async def buscar_por_pais(codigo_pais: str) -> List[Dict[str, Any]]:
        """
        Busca dinosaurios por país (NUEVO para el mapa mundial)
        
        Args:
            codigo_pais: Código ISO del país (AR, US, CN, etc.)
        
        Returns:
            Lista de dinosaurios encontrados en ese país
        """
        if not codigo_pais:
            return []
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{PaleoDBService.BASE_URL}/occs/list.json",
                    params={
                        "cc": codigo_pais,  # Código de país
                        "taxon_name": "Dinosauria",  # Solo dinosaurios
                        "show": "coords,attr,loc,classext",
                        "limit": 50  # Límite para no saturar
                    },
                    timeout=30.0,
                    headers={"User-Agent": "Taxodino/1.0"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    records = data.get("records", [])
                    
                    if records:
                        print(f"✅ PaleoDB: {len(records)} dinosaurios encontrados en {codigo_pais}")
                    
                    # Procesar resultados
                    dinosaurios = []
                    for record in records:
                        dino = PaleoDBService._parse_dinosaurio_por_pais(record, codigo_pais)
                        if dino and dino.get("nombre"):
                            dinosaurios.append(dino)
                    
                    return dinosaurios
                    
            except Exception as e:
                print(f"❌ Error en PaleoDB (búsqueda por país): {e}")
        
        return []
    
    @staticmethod
    def _parse_dinosaurio_por_pais(record: Dict, codigo_pais: str) -> Dict:
        """
        Parsea un registro de dinosaurio para el mapa mundial
        """
        nombre_taxon = record.get("taxon_name", "")
        
        # Extraer nombre común del nombre científico
        nombre_comun = nombre_taxon.split()[-1] if nombre_taxon else "Desconocido"
        
        # Determinar dieta basada en el nombre
        dieta = "Desconocida"
        nombre_lower = nombre_taxon.lower()
        if any(x in nombre_lower for x in ["raptor", "rex", "tirano", "carn", "megal"]):
            dieta = "Carnívoro"
        elif any(x in nombre_lower for x in ["ceratops", "saurus", "brachio", "diplo", "long", "bronto"]):
            dieta = "Herbívoro"
        elif any(x in nombre_lower for x in ["mimus", "oviraptor", "therizino"]):
            dieta = "Omnívoro"
        
        return {
            "nombre": nombre_comun,
            "nombre_cientifico": nombre_taxon,
            "periodo": record.get("early_interval", "Desconocido"),
            "dieta": dieta,
            "latitud": float(record.get("lat", 0)) if record.get("lat") else None,
            "longitud": float(record.get("lng", 0)) if record.get("lng") else None,
            "formacion": record.get("formation", "No especificada"),
            "edad_ma": f"{record.get('min_ma', '?')} - {record.get('max_ma', '?')} MA",
            "descripcion": f"Fósil encontrado en {record.get('formation', 'formación rocosa')}, "
                          f"período {record.get('early_interval', 'desconocido')}"
        }
    
    @staticmethod
    async def buscar_por_continente(continente: str) -> List[Dict[str, Any]]:
        """
        Busca dinosaurios por continente (NUEVO)
        
        Args:
            continente: Nombre del continente (Sudamérica, América del Norte, etc.)
        """
        # Mapeo de continentes a códigos de país aproximados
        continente_paises = {
            "sudamerica": ["AR", "BR", "CL", "PE", "CO", "VE", "BO", "UY", "PY", "EC"],
            "america del norte": ["US", "CA", "MX"],
            "europa": ["GB", "FR", "DE", "ES", "IT", "PT"],
            "asia": ["CN", "MN", "IN", "JP", "RU"],
            "africa": ["ZA", "EG", "MA", "NG", "KE"],
            "oceania": ["AU", "NZ"]
        }
        
        paises = continente_paises.get(continente.lower(), [])
        todos_dinosaurios = []
        
        for pais in paises[:3]:  # Limitar a 3 países para no saturar
            dinosaurios = await PaleoDBService.buscar_por_pais(pais)
            todos_dinosaurios.extend(dinosaurios)
        
        # Eliminar duplicados por nombre científico
        vistos = set()
        unicos = []
        for dino in todos_dinosaurios:
            if dino["nombre_cientifico"] not in vistos:
                vistos.add(dino["nombre_cientifico"])
                unicos.append(dino)
        
        return unicos[:20]  # Limitar a 20 resultados
    
    @staticmethod
    async def obtener_estadisticas_por_pais() -> Dict[str, Any]:
        """
        Obtiene estadísticas de cantidad de fósiles por país (NUEVO)
        """
        paises_principales = ["AR", "US", "CN", "MN", "CA", "BR", "AU", "ZA", "EG", "GB"]
        estadisticas = {}
        
        for pais in paises_principales:
            dinosaurios = await PaleoDBService.buscar_por_pais(pais)
            estadisticas[pais] = len(dinosaurios)
        
        return estadisticas