from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class WikidataInfo(Base):
    __tablename__ = "wikidata_info"
    
    id = Column(Integer, primary_key=True, index=True)
    dinosaurio_id = Column(Integer, ForeignKey("dinosaurs.id", ondelete="CASCADE"))
    wikidata_id = Column(String(50), unique=True)
    descubridor = Column(String(150))
    año_descubrimiento = Column(Integer)
    lugar_descubrimiento = Column(String(200))
    habitat = Column(String(100))
    caracteristicas = Column(Text)