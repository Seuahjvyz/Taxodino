from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuración global de la aplicación"""
    
    # Base de datos
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/dbname")
    
    # APIs externas
    PALEODB_URL = "https://paleobiodb.org/data1.2"
    FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY", "")
    
    # User Agent para respetar términos de uso
    USER_AGENT = "TaxodinoApp/1.0 (https://github.com/tuusuario/taxodino; taxodino@ejemplo.com)"
    
    # Mapeo de países a códigos ISO para la API
    PAISES_API: Dict[str, str] = {
        "argentina": "AR",
        "usa": "US", 
        "estados unidos": "US",
        "china": "CN",
        "mongolia": "MN",
        "canada": "CA",
        "brasil": "BR",
        "australia": "AU",
        "sudafrica": "ZA",
        "egipto": "EG",
        "reino unido": "GB",
        "francia": "FR",
        "alemania": "DE",
        "españa": "ES",
        "italia": "IT",
        "mexico": "MX",
        "peru": "PE",
        "chile": "CL",
        "colombia": "CO",
        "uruguay": "UY",
        "venezuela": "VE",
        "bolivia": "BO",
        "paraguay": "PY",
        "ecuador": "EC"
    }
    
    # Coordenadas para el mapa mundial
    PAISES_COORDENADAS: Dict[str, Dict] = {
        "argentina": {"lat": -38.4161, "lng": -63.6167, "continente": "Sudamérica"},
        "usa": {"lat": 37.0902, "lng": -95.7129, "continente": "América del Norte"},
        "china": {"lat": 35.8617, "lng": 104.1954, "continente": "Asia"},
        "mongolia": {"lat": 46.8625, "lng": 103.8467, "continente": "Asia"},
        "canada": {"lat": 56.1304, "lng": -106.3468, "continente": "América del Norte"},
        "brasil": {"lat": -14.2350, "lng": -51.9253, "continente": "Sudamérica"},
        "australia": {"lat": -25.2744, "lng": 133.7751, "continente": "Oceanía"},
        "sudafrica": {"lat": -30.5595, "lng": 22.9375, "continente": "África"},
        "egipto": {"lat": 26.8206, "lng": 30.8025, "continente": "África"},
        "reino unido": {"lat": 55.3781, "lng": -3.4360, "continente": "Europa"},
        "francia": {"lat": 46.2276, "lng": 2.2137, "continente": "Europa"},
        "alemania": {"lat": 51.1657, "lng": 10.4515, "continente": "Europa"},
        "españa": {"lat": 40.4637, "lng": -3.7492, "continente": "Europa"},
        "mexico": {"lat": 23.6345, "lng": -102.5528, "continente": "América del Norte"},
        "peru": {"lat": -9.1900, "lng": -75.0152, "continente": "Sudamérica"},
        "chile": {"lat": -35.6751, "lng": -71.5430, "continente": "Sudamérica"},
        "colombia": {"lat": 4.5709, "lng": -74.2973, "continente": "Sudamérica"},
        "uruguay": {"lat": -32.5228, "lng": -55.7658, "continente": "Sudamérica"},
        "venezuela": {"lat": 6.4238, "lng": -66.5897, "continente": "Sudamérica"},
        "bolivia": {"lat": -16.2902, "lng": -63.5887, "continente": "Sudamérica"},
        "paraguay": {"lat": -23.4425, "lng": -58.4438, "continente": "Sudamérica"},
        "ecuador": {"lat": -1.8312, "lng": -78.1834, "continente": "Sudamérica"}
    }

settings = Settings()