import httpx
from typing import Optional, Dict, Any, List
import random

class DinosaurFactsService:
    BASE_URL = "https://dinosaur-facts-api.shultzlab.com"
    
    # Cache para no llamar a la API cada vez
    _todos_dinosaurios_cache = None
    
    @staticmethod
    async def obtener_todos_dinosaurios() -> List[Dict[str, Any]]:
        """Obtiene lista completa de dinosaurios con caché"""
        if DinosaurFactsService._todos_dinosaurios_cache is not None:
            return DinosaurFactsService._todos_dinosaurios_cache
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{DinosaurFactsService.BASE_URL}/dinosaurs", timeout=30.0)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Dinosaur Facts: {len(data)} dinosaurios cargados")
                    # Mostrar algunos nombres como ejemplo
                    nombres = [d.get("name", "") for d in data[:10]]
                    print(f"📝 Ejemplos de nombres: {nombres}")
                    DinosaurFactsService._todos_dinosaurios_cache = data
                    return data
            except Exception as e:
                print(f"❌ Error en Dinosaur Facts: {e}")
        return []
    
    @staticmethod
    async def buscar_por_nombre(nombre: str) -> Optional[Dict[str, Any]]:
        """Busca un dinosaurio por nombre con coincidencia flexible"""
        todos = await DinosaurFactsService.obtener_todos_dinosaurios()
        
        nombre_lower = nombre.lower().strip()
        
        # Diferentes estrategias de búsqueda
        for dino in todos:
            dino_name = dino.get("name", "").lower().strip()
            
            # Coincidencia exacta
            if nombre_lower == dino_name:
                print(f"✅ Coincidencia exacta: {dino.get('name')}")
                return dino
            
            # El nombre contiene el buscado
            if nombre_lower in dino_name:
                print(f"✅ Coincidencia parcial (nombre contiene): {dino.get('name')}")
                return dino
            
            # El buscado contiene el nombre
            if dino_name in nombre_lower and len(dino_name) > 3:
                print(f"✅ Coincidencia parcial (dino en nombre): {dino.get('name')}")
                return dino
        
        print(f"⚠️ No encontrado en Dinosaur Facts: {nombre}")
        return None