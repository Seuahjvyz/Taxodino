import httpx
from typing import Optional, Dict, Any, List
import random

class DinosaurFactsService:
    BASE_URL = "https://dinosaur-facts-api.shultzlab.com"
    
    @staticmethod
    async def obtener_todos_dinosaurios() -> List[Dict[str, Any]]:
        """Obtiene lista completa de dinosaurios"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{DinosaurFactsService.BASE_URL}/dinosaurs", timeout=30.0)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Dinosaur Facts: {len(data)} dinosaurios cargados")
                    return data
            except Exception as e:
                print(f"❌ Error en Dinosaur Facts: {e}")
        return []
    
    @staticmethod
    async def buscar_por_nombre(nombre: str) -> Optional[Dict[str, Any]]:
        """Busca un dinosaurio por nombre"""
        todos = await DinosaurFactsService.obtener_todos_dinosaurios()
        
        # Búsqueda más precisa
        nombre_lower = nombre.lower()
        for dino in todos:
            dino_name = dino.get("name", "").lower()
            # Buscar coincidencia exacta o que contenga
            if nombre_lower == dino_name or nombre_lower in dino_name or dino_name in nombre_lower:
                print(f"✅ Encontrado en Dinosaur Facts: {dino.get('name')}")
                return dino
        
        print(f"⚠️ No encontrado en Dinosaur Facts: {nombre}")
        return None
    
    @staticmethod
    async def obtener_curiosidades(nombre: str, cantidad: int = 3) -> List[str]:
        """Obtiene curiosidades de un dinosaurio"""
        dino_data = await DinosaurFactsService.buscar_por_nombre(nombre)
        
        if dino_data and "description" in dino_data:
            descripcion = dino_data.get("description", "")
            curiosidades = [
                descripcion[:200] + "..." if len(descripcion) > 200 else descripcion,
                f"El {dino_data.get('name', nombre)} habitó la Tierra hace millones de años.",
                f"Este dinosaurio es uno de los más estudiados por los paleontólogos."
            ]
            return curiosidades[:cantidad]
        
        return [
            f"¡El {nombre} es un dinosaurio fascinante!",
            f"Aprende más sobre el increíble {nombre}.",
            f"Los dinosaurios como el {nombre} dominaron la Tierra durante millones de años."
        ]