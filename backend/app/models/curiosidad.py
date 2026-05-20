from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class Curiosidad(Base):
    __tablename__ = "curiosidades"
    
    id = Column(Integer, primary_key=True, index=True)
    dinosaurio_id = Column(Integer, ForeignKey("dinosaurs.id", ondelete="CASCADE"))
    texto_curiosidad = Column(Text, nullable=False)
    tipo = Column(String(50))