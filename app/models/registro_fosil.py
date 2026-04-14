from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class RegistroFosil(Base):
    __tablename__ = "registros_fosiles"
    
    id = Column(Integer, primary_key=True, index=True)
    dinosaurio_id = Column(Integer, ForeignKey("dinosaurs.id", ondelete="CASCADE"))
    ubicacion = Column(String(200))
    coordenadas_lat = Column(Float)
    coordenadas_lng = Column(Float)
    edad_geologica = Column(String(100))
    formacion_rocosa = Column(String(150))
    museo_codigo = Column(String(100))
    fecha_descubrimiento = Column(Integer)