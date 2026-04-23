from app.core.database import engine, Base
from app.models import dinosaurio, registro_fosil, curiosidad, favorito, imagen, wikidata_info
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """Inicializa la base de datos creando todas las tablas"""
    logger.info("Creando tablas en Neon PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas exitosamente!")

if __name__ == "__main__":
    init_database()