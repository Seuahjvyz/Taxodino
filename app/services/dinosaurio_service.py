from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
import asyncio
from app.models import Dinosaurio, WikidataInfo, RegistroFosil, Curiosidad, Imagen
from app.services.wikidata_service import WikidataService
from app.services.paleodb_service import PaleoDBService
from app.services.dinosaurfacts_service import DinosaurFactsService
from app.services.freepik_service import FreepikService

class DinosaurioService:
    
    def __init__(self, db: Session):
        self.db = db
        self.freepik_service = FreepikService()
    
    async def buscar_o_crear(self, query: str) -> Dict[str, Any]:
        """Busca en BD local o crea desde APIs externas"""
        
        # 1. Buscar en BD local
        dino_local = self.db.query(Dinosaurio).filter(
            (Dinosaurio.nombre_comun.ilike(f"%{query}%")) |
            (Dinosaurio.nombre_cientifico.ilike(f"%{query}%"))
        ).first()
        
        if dino_local:
            return {"source": "database", "data": self._to_dict(dino_local)}
        
        # 2. Consultar APIs externas
        wikidata_data, fosiles_data, facts_data, images_data = await asyncio.gather(
            WikidataService.buscar_dinosaurio(query),
            PaleoDBService.buscar_fosiles(query),
            DinosaurFactsService.buscar_por_nombre(query),
            self.freepik_service.buscar_imagenes(f"{query} dinosaurio", limit=3)
        )
        
        # 3. Crear en BD (manejando None correctamente)
        nuevo_dino = await self._crear_dinosaurio(
            query, wikidata_data, facts_data, images_data
        )
        
        # 4. Guardar relaciones (manejando None correctamente)
        await self._guardar_relaciones(nuevo_dino.id, wikidata_data, fosiles_data, facts_data, images_data)
        
        return {"source": "external_apis", "data": self._to_dict(nuevo_dino)}
    
    async def _crear_dinosaurio(self, query: str, wikidata_data, facts_data, images_data) -> Dinosaurio:
        # Manejar caso donde facts_data es None
        nombre_comun = query
        if facts_data and isinstance(facts_data, dict):
            nombre_comun = facts_data.get("name", query)
        
        nombre_cientifico = query
        if wikidata_data and isinstance(wikidata_data, dict):
            nombre_cientifico = wikidata_data.get("nombre_cientifico", query)
        
        longitud = 0
        if wikidata_data and isinstance(wikidata_data, dict):
            longitud = wikidata_data.get("longitud_metros", 0) or 0
        
        peso = 0
        if wikidata_data and isinstance(wikidata_data, dict):
            peso = wikidata_data.get("peso_kg", 0) or 0
        
        descripcion = f"Información sobre {nombre_comun}"
        if facts_data and isinstance(facts_data, dict):
            descripcion = facts_data.get("description", descripcion)
        
        imagen = None
        if images_data and len(images_data) > 0:
            imagen = images_data[0].get("url_imagen")
        
        dino = Dinosaurio(
            nombre_comun=nombre_comun,
            nombre_cientifico=nombre_cientifico,
            longitud_metros=longitud,
            peso_kg=peso,
            descripcion_general=descripcion,
            imagen_url=imagen
        )
        self.db.add(dino)
        self.db.flush()
        return dino
    
    async def _guardar_relaciones(self, dino_id: int, wikidata_data, fosiles_data, facts_data, images_data):
        # Guardar Wikidata
        if wikidata_data and isinstance(wikidata_data, dict):
            wikidata_info = WikidataInfo(
                dinosaurio_id=dino_id,
                wikidata_id=wikidata_data.get("wikidata_id"),
                descubridor=wikidata_data.get("descubridor"),
                año_descubrimiento=wikidata_data.get("año_descubrimiento"),
                habitat=wikidata_data.get("habitat"),
                caracteristicas=wikidata_data.get("caracteristicas", "")
            )
            self.db.add(wikidata_info)
        
        # Guardar fósiles
        if fosiles_data and isinstance(fosiles_data, list):
            for fosil in fosiles_data[:3]:
                registro = RegistroFosil(
                    dinosaurio_id=dino_id,
                    ubicacion=fosil.get("ubicacion"),
                    coordenadas_lat=fosil.get("coordenadas_lat"),
                    coordenadas_lng=fosil.get("coordenadas_lng"),
                    edad_geologica=fosil.get("edad_geologica"),
                    formacion_rocosa=fosil.get("formacion_rocosa"),
                    museo_codigo=fosil.get("museo_codigo")
                )
                self.db.add(registro)
        
        # Guardar curiosidades (manejando None)
        nombre_dino = ""
        if facts_data and isinstance(facts_data, dict):
            nombre_dino = facts_data.get("name", "")
        
        curiosidades_textos = await DinosaurFactsService.obtener_curiosidades(nombre_dino if nombre_dino else "dinosaurio", 3)
        for texto in curiosidades_textos:
            curiosidad = Curiosidad(
                dinosaurio_id=dino_id,
                texto_curiosidad=texto,
                tipo="general"
            )
            self.db.add(curiosidad)
        
        # Guardar imágenes
        if images_data and isinstance(images_data, list):
            for i, img in enumerate(images_data):
                imagen = Imagen(
                    dinosaurio_id=dino_id,
                    url_imagen=img.get("url_imagen", ""),
                    url_miniatura=img.get("url_miniatura"),
                    atribucion=img.get("atribucion"),
                    es_principal=(i == 0)
                )
                self.db.add(imagen)
        
        self.db.commit()
    
    def _to_dict(self, dino: Dinosaurio) -> dict:
        return {
            "id": dino.id,
            "nombre": dino.nombre_comun,
            "nombre_cientifico": dino.nombre_cientifico,
            "dieta": dino.dieta,
            "periodo": dino.periodo,
            "imagen_url": dino.imagen_url,
            "descripcion": dino.descripcion_general
        }