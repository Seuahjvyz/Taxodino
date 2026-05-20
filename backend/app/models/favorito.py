from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Favorito(Base):
    __tablename__ = "favoritos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)
    dinosaurio_id = Column(Integer, ForeignKey("dinosaurs.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now())