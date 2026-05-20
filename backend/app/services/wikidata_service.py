import httpx
from typing import Optional, Dict, Any

class WikidataService:
    
    @staticmethod
    async def buscar_dinosaurio(nombre: str) -> Optional[Dict[str, Any]]:
        """Busca un dinosaurio en Wikidata con múltiples estrategias"""
        
        nombre_limpio = nombre.strip()
        
        # Estrategia 1: Búsqueda directa por nombre
        query_directa = f"""
        SELECT ?item ?itemLabel ?scientificName ?weight ?length WHERE {{
          ?item wdt:P31 wd:Q430;
                 rdfs:label ?itemLabel.
          ?item wdt:P225 ?scientificName.
          OPTIONAL {{ ?item wdt:P2067 ?weight. }}
          OPTIONAL {{ ?item wdt:P2043 ?length. }}
          FILTER(LCASE(?itemLabel) = LCASE("{nombre_limpio}"))
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "es,en". }}
        }}
        LIMIT 1
        """
        
        result = await WikidataService._ejecutar_query(query_directa)
        if result:
            print(f"✅ Wikidata: encontrado por nombre exacto: {nombre_limpio}")
            return result
        
        # Estrategia 2: Búsqueda por coincidencia parcial
        query_parcial = f"""
        SELECT ?item ?itemLabel ?scientificName ?weight ?length WHERE {{
          ?item wdt:P31 wd:Q430;
                 rdfs:label ?itemLabel.
          ?item wdt:P225 ?scientificName.
          OPTIONAL {{ ?item wdt:P2067 ?weight. }}
          OPTIONAL {{ ?item wdt:P2043 ?length. }}
          FILTER(CONTAINS(LCASE(?itemLabel), LCASE("{nombre_limpio}")))
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "es,en". }}
        }}
        LIMIT 1
        """
        
        result = await WikidataService._ejecutar_query(query_parcial)
        if result:
            print(f"✅ Wikidata: encontrado por coincidencia parcial: {nombre_limpio}")
            return result
        
        # Estrategia 3: Si tiene dos palabras, buscar por nombre científico
        if " " in nombre_limpio:
            query_cientifico = f"""
            SELECT ?item ?itemLabel ?scientificName ?weight ?length WHERE {{
              ?item wdt:P31 wd:Q430;
                    wdt:P225 ?scientificName.
              FILTER(CONTAINS(LCASE(?scientificName), LCASE("{nombre_limpio}")))
              OPTIONAL {{ ?item wdt:P2067 ?weight. }}
              OPTIONAL {{ ?item wdt:P2043 ?length. }}
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "es,en". }}
            }}
            LIMIT 1
            """
            result = await WikidataService._ejecutar_query(query_cientifico)
            if result:
                print(f"✅ Wikidata: encontrado por nombre científico: {nombre_limpio}")
                return result
        
        print(f"⚠️ Wikidata: no encontrado: {nombre_limpio}")
        return None
    
    @staticmethod
    async def _ejecutar_query(query: str) -> Optional[Dict[str, Any]]:
        """Ejecuta una consulta SPARQL y parsea el resultado"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "https://query.wikidata.org/sparql",
                    params={"format": "json", "query": query},
                    timeout=30.0,
                    headers={"User-Agent": "Taxodino/1.0 (https://taxodino.com)"}
                )
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", {}).get("bindings", [])
                    if results:
                        return WikidataService._parse_result(results[0])
            except Exception as e:
                print(f"❌ Error en Wikidata: {e}")
        return None
    
    @staticmethod
    def _parse_result(result: Dict) -> Dict:
        return {
            "nombre_cientifico": result.get("scientificName", {}).get("value", ""),
            "peso_kg": float(result.get("weight", {}).get("value", 0)) if result.get("weight") else None,
            "longitud_metros": float(result.get("length", {}).get("value", 0)) if result.get("length") else None,
            "wikidata_id": result.get("item", {}).get("value", "").split("/")[-1] if result.get("item") else None,
        }