from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Dinosaurio(Base):
    __tablename__ = "dinosaurios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, index=True)
    nombre_cientifico = Column(String(200), nullable=True)
    periodo = Column(String(50), nullable=True)
    dieta = Column(String(50), nullable=True)
    descripcion = Column(Text, nullable=True)
    imagen_url = Column(String(500), nullable=True)
    altura = Column(Float, nullable=True)
    peso = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    
    # Relación con registros fósiles (comentada temporalmente)
    # registros_fosiles = relationship("RegistroFosil", back_populates="dinosaurio")