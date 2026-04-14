import httpx
from typing import Optional, Dict, Any

class WikidataService:
    
    @staticmethod
    async def buscar_dinosaurio(nombre: str) -> Optional[Dict[str, Any]]:
        """Busca un dinosaurio en Wikidata"""
        
        # Lista de nombres de dinosaurios conocidos para búsqueda
        nombres_busqueda = [
            nombre,
            nombre.capitalize(),
            nombre.title(),
            f"{nombre} rex" if "rex" not in nombre.lower() else nombre,
            nombre.replace(" ", "_")
        ]
        
        for search_name in nombres_busqueda[:3]:
            sparql_query = f"""
            SELECT ?item ?itemLabel ?scientificName ?weight ?length WHERE {{
              ?item wdt:P31 wd:Q430;
                     rdfs:label ?itemLabel.
              ?item wdt:P225 ?scientificName.
              OPTIONAL {{ ?item wdt:P2067 ?weight. }}
              OPTIONAL {{ ?item wdt:P2043 ?length. }}
              FILTER(CONTAINS(LCASE(?itemLabel), LCASE("{search_name}")))
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "es". }}
            }}
            LIMIT 1
            """
            
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        "https://query.wikidata.org/sparql",
                        params={"format": "json", "query": sparql_query},
                        timeout=30.0
                    )
                    if response.status_code == 200:
                        data = response.json()
                        results = data.get("results", {}).get("bindings", [])
                        if results:
                            print(f"✅ Encontrado en Wikidata: {search_name}")
                            return WikidataService._parse_result(results[0])
                except Exception as e:
                    print(f"Error en Wikidata: {e}")
        
        print(f"⚠️ No encontrado en Wikidata: {nombre}")
        return None
    
    @staticmethod
    def _parse_result(result: Dict) -> Dict:
        return {
            "nombre_cientifico": result.get("scientificName", {}).get("value", ""),
            "peso_kg": float(result.get("weight", {}).get("value", 0)) if result.get("weight") else None,
            "longitud_metros": float(result.get("length", {}).get("value", 0)) if result.get("length") else None,
            "wikidata_id": result.get("item", {}).get("value", "").split("/")[-1] if result.get("item") else None,
        }