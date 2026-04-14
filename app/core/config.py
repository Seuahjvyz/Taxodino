from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    FREEPIK_API_KEY: str = os.getenv("FREEPIK_API_KEY", "")
    
    # URLs de APIs externas
    WIKIDATA_SPARQL_URL: str = "https://query.wikidata.org/sparql"
    PALEOBIO_BASE_URL: str = "https://paleobiodb.org/data1.2"
    DINOSAUR_FACTS_URL: str = "https://dinosaur-facts-api.shultzlab.com"
    FREEPIK_BASE_URL: str = "https://api.freepik.com/v1"
    
    class Config:
        env_file = ".env"

settings = Settings()