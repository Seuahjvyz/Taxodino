from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DinosaurioBase(BaseModel):
    nombre_comun: str
    nombre_cientifico: str
    dieta: Optional[str] = None
    periodo: Optional[str] = None
    longitud_metros: Optional[float] = None
    peso_kg: Optional[float] = None
    descripcion_general: Optional[str] = None

class DinosaurioCreate(DinosaurioBase):
    pass

class DinosaurioResponse(DinosaurioBase):
    id: int
    imagen_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class DinosaurioDetalleResponse(DinosaurioResponse):
    wikidata: Optional[dict] = None
    registros_fosiles: List[dict] = []
    curiosidades: List[str] = []
    imagenes: List[dict] = []