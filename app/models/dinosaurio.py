from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Dinosaurio(Base):
    __tablename__ = "dinosaurs"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre_comun = Column(String(100), nullable=False)
    nombre_cientifico = Column(String(150), unique=True, nullable=False)
    dieta = Column(String(50))
    periodo = Column(String(50))
    longitud_metros = Column(Float)
    peso_kg = Column(Float)
    altura_metros = Column(Float)
    descripcion_general = Column(Text)
    imagen_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())