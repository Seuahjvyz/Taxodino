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
        """
        Busca un dinosaurio en BD local o lo crea desde APIs externas.
        """
        print(f"\n{'='*50}")
        print(f"🔍 Buscando dinosaurio: '{query}'")
        print(f"{'='*50}")
        
        # 1. Buscar en BD local (coincidencia flexible)
        dino_local = self.db.query(Dinosaurio).filter(
            (Dinosaurio.nombre_comun.ilike(f"%{query}%")) |
            (Dinosaurio.nombre_cientifico.ilike(f"%{query}%"))
        ).first()
        
        if dino_local:
            print(f"✅ Encontrado en BD local: {dino_local.nombre_comun} (ID: {dino_local.id})")
            return {"source": "database", "data": self._to_dict(dino_local)}
        
        # 2. Consultar APIs externas en paralelo
        print("🌐 Consultando APIs externas...")
        
        wikidata_data, fosiles_data, facts_data, images_data = await asyncio.gather(
            WikidataService.buscar_dinosaurio(query),
            PaleoDBService.buscar_fosiles(query),
            DinosaurFactsService.buscar_por_nombre(query),
            self.freepik_service.buscar_imagenes(f"{query} dinosaur", limit=3)
        )
        
        # Mostrar resultados de las APIs
        print(f"\n📊 Resultados de APIs externas:")
        print(f"  ├─ Wikidata: {'✅ Encontrado' if wikidata_data else '❌ No encontrado'}")
        print(f"  ├─ PaleoDB: {len(fosiles_data) if fosiles_data else 0} registros fósiles")
        print(f"  ├─ Dinosaur Facts: {'✅ Encontrado' if facts_data else '❌ No encontrado'}")
        print(f"  └─ Freepik: {len(images_data) if images_data else 0} imágenes")
        
        # 3. Si no se encuentra en ninguna API, devolver error
        if not wikidata_data and not facts_data:
            print(f"❌ No se encontró información para '{query}' en ninguna API")
            return {
                "source": "none",
                "data": None,
                "message": f"No se encontró información para '{query}'. Intenta con otro nombre."
            }
        
        # 4. Crear nuevo dinosaurio en BD
        nuevo_dino = await self._crear_dinosaurio(
            query, wikidata_data, facts_data, images_data
        )
        
        print(f"✅ Dinosaurio creado en BD: {nuevo_dino.nombre_comun} (ID: {nuevo_dino.id})")
        
        # 5. Guardar relaciones (datos adicionales)
        await self._guardar_relaciones(
            nuevo_dino.id, 
            wikidata_data, 
            fosiles_data, 
            facts_data, 
            images_data,
            query
        )
        
        print(f"✅ Todos los datos guardados correctamente")
        print(f"{'='*50}\n")
        
        return {"source": "external_apis", "data": self._to_dict(nuevo_dino)}
    
    async def _crear_dinosaurio(
        self, 
        query: str, 
        wikidata_data: Optional[Dict], 
        facts_data: Optional[Dict], 
        images_data: List[Dict]
    ) -> Dinosaurio:
        """Crea un nuevo dinosaurio en la base de datos"""
        
        # Determinar el nombre común
        nombre_comun = query
        if facts_data and isinstance(facts_data, dict):
            nombre_comun = facts_data.get("name", query)
        elif wikidata_data and isinstance(wikidata_data, dict):
            # Intentar obtener el nombre de Wikidata
            pass
        
        # Determinar el nombre científico
        nombre_cientifico = None
        if wikidata_data and isinstance(wikidata_data, dict):
            nombre_cientifico = wikidata_data.get("nombre_cientifico")
        if not nombre_cientifico and facts_data and isinstance(facts_data, dict):
            nombre_cientifico = facts_data.get("name", query)
        if not nombre_cientifico:
            nombre_cientifico = query
        
        # Determinar la dieta (si se puede inferir)
        dieta = None
        if facts_data and isinstance(facts_data, dict):
            # Intentar inferir dieta de la descripción
            desc = facts_data.get("description", "").lower()
            if "carnivor" in desc or "meat" in desc or "hunter" in desc:
                dieta = "Carnívoro"
            elif "herbivor" in desc or "plant" in desc:
                dieta = "Herbívoro"
            elif "omnivor" in desc:
                dieta = "Omnívoro"
        
        # Determinar el período
        periodo = None
        if facts_data and isinstance(facts_data, dict):
            desc = facts_data.get("description", "").lower()
            if "cretaceous" in desc or "cretácico" in desc:
                periodo = "Cretácico"
            elif "jurassic" in desc or "jurásico" in desc:
                periodo = "Jurásico"
            elif "triassic" in desc or "triásico" in desc:
                periodo = "Triásico"
        
        # Obtener medidas
        longitud = 0
        if wikidata_data and isinstance(wikidata_data, dict):
            longitud = wikidata_data.get("longitud_metros", 0) or 0
        
        peso = 0
        if wikidata_data and isinstance(wikidata_data, dict):
            peso = wikidata_data.get("peso_kg", 0) or 0
        
        # Descripción general
        descripcion = f"Información sobre {nombre_comun}"
        if facts_data and isinstance(facts_data, dict):
            descripcion = facts_data.get("description", descripcion)
        
        # Imagen principal
        imagen_url = None
        if images_data and len(images_data) > 0:
            imagen_url = images_data[0].get("url_imagen")
        
        # Crear el dinosaurio
        dino = Dinosaurio(
            nombre_comun=nombre_comun,
            nombre_cientifico=nombre_cientifico,
            dieta=dieta,
            periodo=periodo,
            longitud_metros=longitud,
            peso_kg=peso,
            descripcion_general=descripcion,
            imagen_url=imagen_url
        )
        
        self.db.add(dino)
        self.db.flush()  # Para obtener el ID
        return dino
    
    async def _guardar_relaciones(
        self, 
        dino_id: int, 
        wikidata_data: Optional[Dict], 
        fosiles_data: List[Dict], 
        facts_data: Optional[Dict], 
        images_data: List[Dict],
        query: str
    ):
        """Guarda las relaciones del dinosaurio (Wikidata, fósiles, curiosidades, imágenes)"""
        
        # 1. Guardar datos de Wikidata
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
            print(f"  ├─ Wikidata: Información guardada")
        
        # 2. Guardar registros fósiles
        if fosiles_data and isinstance(fosiles_data, list):
            for fosil in fosiles_data[:3]:
                if fosil.get("ubicacion"):  # Solo guardar si tiene ubicación
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
            print(f"  ├─ PaleoDB: {len([f for f in fosiles_data if f.get('ubicacion')])} registros guardados")
        
        # 3. Guardar curiosidades
        nombre_dino = query
        if facts_data and isinstance(facts_data, dict):
            nombre_dino = facts_data.get("name", query)
        
        curiosidades = await self._generar_curiosidades(nombre_dino, facts_data, wikidata_data)
        
        for texto in curiosidades:
            curiosidad = Curiosidad(
                dinosaurio_id=dino_id,
                texto_curiosidad=texto,
                tipo="general"
            )
            self.db.add(curiosidad)
        print(f"  ├─ Curiosidades: {len(curiosidades)} generadas")
        
        # 4. Guardar imágenes
        if images_data and isinstance(images_data, list):
            for i, img in enumerate(images_data):
                if img.get("url_imagen"):
                    imagen = Imagen(
                        dinosaurio_id=dino_id,
                        url_imagen=img.get("url_imagen", ""),
                        url_miniatura=img.get("url_miniatura"),
                        atribucion=img.get("atribucion"),
                        es_principal=(i == 0)
                    )
                    self.db.add(imagen)
            print(f"  └─ Imágenes: {len([i for i in images_data if i.get('url_imagen')])} guardadas")
        
        # Commit final
        self.db.commit()
    
    async def _generar_curiosidades(
        self, 
        nombre: str, 
        facts_data: Optional[Dict], 
        wikidata_data: Optional[Dict]
    ) -> List[str]:
        """Genera curiosidades personalizadas para el dinosaurio"""
        
        curiosidades = []
        
        # Curiosidad 1: Basada en la descripción de Dinosaur Facts
        if facts_data and isinstance(facts_data, dict):
            descripcion = facts_data.get("description", "")
            if descripcion and len(descripcion) > 50:
                # Tomar la primera oración o parte de la descripción
                primer_punto = descripcion.find(".")
                if primer_punto > 0:
                    curiosidad1 = descripcion[:primer_punto + 1]
                else:
                    curiosidad1 = descripcion[:200] + "..."
                curiosidades.append(curiosidad1)
            else:
                curiosidades.append(f"¡El {nombre} es uno de los dinosaurios más fascinantes del período!")
        else:
            curiosidades.append(f"¡El {nombre} es un dinosaurio fascinante que vivió hace millones de años!")
        
        # Curiosidad 2: Basada en datos de Wikidata
        if wikidata_data and isinstance(wikidata_data, dict):
            peso = wikidata_data.get("peso_kg")
            longitud = wikidata_data.get("longitud_metros")
            
            if peso and peso > 0:
                curiosidades.append(f"El {nombre} podía pesar hasta {int(peso):,} kg, ¡el equivalente a {int(peso/500)} autos pequeños!")
            elif longitud and longitud > 0:
                curiosidades.append(f"El {nombre} medía aproximadamente {longitud} metros de largo, ¡como {int(longitud/2)} autos estacionados en fila!")
            else:
                curiosidades.append(f"El {nombre} dominó su ecosistema durante el período en que vivió.")
        else:
            curiosidades.append(f"Los científicos continúan descubriendo nuevos datos fascinantes sobre el {nombre}.")
        
        # Curiosidad 3: Hecho general
        curiosidades.append(f"El nombre '{nombre}' proviene del griego y significa algo relacionado con sus características únicas.")
        
        return curiosidades[:3]  # Máximo 3 curiosidades
    
    def _to_dict(self, dino: Dinosaurio) -> dict:
        """Convierte un objeto Dinosaurio a diccionario para la respuesta JSON"""
        return {
            "id": dino.id,
            "nombre": dino.nombre_comun,
            "nombre_cientifico": dino.nombre_cientifico,
            "dieta": dino.dieta,
            "periodo": dino.periodo,
            "longitud_metros": dino.longitud_metros,
            "peso_kg": dino.peso_kg,
            "altura_metros": dino.altura_metros,
            "descripcion": dino.descripcion_general,
            "imagen_url": dino.imagen_url
        }
    
    async def obtener_detalle_completo(self, dino_id: int) -> Dict[str, Any]:
        """Obtiene el detalle completo de un dinosaurio con toda su información relacionada"""
        
        dino = self.db.query(Dinosaurio).filter(Dinosaurio.id == dino_id).first()
        
        if not dino:
            return None
        
        # Obtener información relacionada
        wikidata_info = self.db.query(WikidataInfo).filter(WikidataInfo.dinosaurio_id == dino_id).first()
        registros_fosiles = self.db.query(RegistroFosil).filter(RegistroFosil.dinosaurio_id == dino_id).all()
        curiosidades = self.db.query(Curiosidad).filter(Curiosidad.dinosaurio_id == dino_id).all()
        imagenes = self.db.query(Imagen).filter(Imagen.dinosaurio_id == dino_id).all()
        
        return {
            "id": dino.id,
            "nombre": dino.nombre_comun,
            "nombre_cientifico": dino.nombre_cientifico,
            "dieta": dino.dieta,
            "periodo": dino.periodo,
            "longitud_metros": dino.longitud_metros,
            "peso_kg": dino.peso_kg,
            "altura_metros": dino.altura_metros,
            "descripcion": dino.descripcion_general,
            "imagen_url": dino.imagen_url,
            "wikidata": {
                "descubridor": wikidata_info.descubridor if wikidata_info else None,
                "año_descubrimiento": wikidata_info.año_descubrimiento if wikidata_info else None,
                "habitat": wikidata_info.habitat if wikidata_info else None,
                "caracteristicas": wikidata_info.caracteristicas if wikidata_info else None
            } if wikidata_info else None,
            "registros_fosiles": [
                {
                    "ubicacion": r.ubicacion,
                    "edad_geologica": r.edad_geologica,
                    "formacion_rocosa": r.formacion_rocosa,
                    "coordenadas": {"lat": r.coordenadas_lat, "lng": r.coordenadas_lng} if r.coordenadas_lat else None
                } for r in registros_fosiles
            ] if registros_fosiles else [],
            "curiosidades": [c.texto_curiosidad for c in curiosidades] if curiosidades else [],
            "imagenes": [
                {
                    "url": img.url_imagen,
                    "miniatura": img.url_miniatura,
                    "principal": img.es_principal,
                    "atribucion": img.atribucion
                } for img in imagenes
            ] if imagenes else []
        }