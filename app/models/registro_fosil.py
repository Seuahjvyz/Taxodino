from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class RegistroFosil(Base):
    __tablename__ = "registros_fosiles"
    
    id = Column(Integer, primary_key=True, index=True)
    dinosaurio_id = Column(Integer, ForeignKey("dinosaurios.id"), nullable=True)  # Hacer nullable por ahora
    pais = Column(String(100), index=True)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    formacion = Column(String(200), nullable=True)
    edad_ma = Column(String(50), nullable=True)
    descripcion = Column(Text, nullable=True)
    
    # Relación (comentada temporalmente)
    # dinosaurio = relationship("Dinosaurio", back_populates="registros_fosiles")