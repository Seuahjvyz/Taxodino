from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from app.core.database import Base

class Imagen(Base):
    __tablename__ = "imagenes"
    
    id = Column(Integer, primary_key=True, index=True)
    dinosaurio_id = Column(Integer, ForeignKey("dinosaurs.id", ondelete="CASCADE"))
    url_imagen = Column(Text, nullable=False)
    url_miniatura = Column(Text)
    atribucion = Column(String(255))
    es_principal = Column(Boolean, default=False)