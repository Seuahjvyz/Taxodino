import httpx
import os
import json  # ← AGREGAR ESTA LÍNEA
from typing import Optional, Dict, Any, List

class FreepikService:
    BASE_URL = "https://api.freepik.com/v1"
    
    def __init__(self):
        self.api_key = os.getenv("FREEPIK_API_KEY")
    
    async def buscar_imagenes(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Busca imágenes de dinosaurios en Freepik"""
        
        if not self.api_key:
            print("FREEPIK_API_KEY no configurada")
            return []
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.BASE_URL}/resources",
                    params={
                        "term": query,
                        "limit": limit,
                        "order": "relevance"
                    },
                    headers={
                        "x-api-key": self.api_key,
                        "Accept": "application/json"
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    imagenes = []
                    
                    # Adapta según la respuesta real de Freepik
                    if "data" in data:
                        for item in data.get("data", []):
                            imagenes.append({
                                "url_imagen": item.get("image", {}).get("url", ""),
                                "url_miniatura": item.get("image", {}).get("thumbnail", ""),
                                "atribucion": item.get("attribution", ""),
                                "ancho": item.get("width", 0),
                                "alto": item.get("height", 0)
                            })
                    
                    return imagenes if imagenes else self._get_placeholder(query)
                    
            except Exception as e:
                print(f"Error en Freepik: {e}")
        
        return self._get_placeholder(query)
    
    def _get_placeholder(self, query: str) -> List[Dict[str, Any]]:
        """Retorna imágenes placeholder"""
        return [
            {
                "url_imagen": f"https://placehold.co/600x400/2D4A22/white?text={query.replace(' ', '+')}",
                "url_miniatura": f"https://placehold.co/300x200/2D4A22/white?text={query.replace(' ', '+')}",
                "atribucion": "Placeholder image",
                "ancho": 600,
                "alto": 400
            }
        ]