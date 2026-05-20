from typing import Dict
import os
import unicodedata
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
        "japon": "JP",
        "india": "IN",
        "niger": "NE",
        "portugal": "PT",
        "mexico": "MX",
        "peru": "PE",
        "chile": "CL",
        "colombia": "CO",
        "uruguay": "UY",
        "venezuela": "VE",
        "bolivia": "BO",
        "paraguay": "PY",
        "ecuador": "EC",
        "marruecos": "MA",
        "tanzania": "TZ"
    }

    PAISES_LABELS: Dict[str, str] = {
        "argentina": "Argentina",
        "usa": "Estados Unidos",
        "estados unidos": "Estados Unidos",
        "china": "China",
        "mongolia": "Mongolia",
        "canada": "Canadá",
        "brasil": "Brasil",
        "australia": "Australia",
        "sudafrica": "Sudáfrica",
        "egipto": "Egipto",
        "reino unido": "Reino Unido",
        "francia": "Francia",
        "alemania": "Alemania",
        "españa": "España",
        "italia": "Italia",
        "japon": "Japón",
        "india": "India",
        "niger": "Níger",
        "portugal": "Portugal",
        "mexico": "México",
        "peru": "Perú",
        "chile": "Chile",
        "colombia": "Colombia",
        "uruguay": "Uruguay",
        "venezuela": "Venezuela",
        "bolivia": "Bolivia",
        "paraguay": "Paraguay",
        "ecuador": "Ecuador",
        "marruecos": "Marruecos",
        "tanzania": "Tanzania"
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
        "italia": {"lat": 41.8719, "lng": 12.5674, "continente": "Europa"},
        "japon": {"lat": 36.2048, "lng": 138.2529, "continente": "Asia"},
        "india": {"lat": 20.5937, "lng": 78.9629, "continente": "Asia"},
        "niger": {"lat": 17.6078, "lng": 8.0817, "continente": "África"},
        "portugal": {"lat": 39.3999, "lng": -8.2245, "continente": "Europa"},
        "mexico": {"lat": 23.6345, "lng": -102.5528, "continente": "América del Norte"},
        "peru": {"lat": -9.1900, "lng": -75.0152, "continente": "Sudamérica"},
        "chile": {"lat": -35.6751, "lng": -71.5430, "continente": "Sudamérica"},
        "colombia": {"lat": 4.5709, "lng": -74.2973, "continente": "Sudamérica"},
        "uruguay": {"lat": -32.5228, "lng": -55.7658, "continente": "Sudamérica"},
        "venezuela": {"lat": 6.4238, "lng": -66.5897, "continente": "Sudamérica"},
        "bolivia": {"lat": -16.2902, "lng": -63.5887, "continente": "Sudamérica"},
        "paraguay": {"lat": -23.4425, "lng": -58.4438, "continente": "Sudamérica"},
        "ecuador": {"lat": -1.8312, "lng": -78.1834, "continente": "Sudamérica"},
        "marruecos": {"lat": 31.7917, "lng": -7.0926, "continente": "África"},
        "tanzania": {"lat": -6.3690, "lng": 34.8888, "continente": "África"}
    }

    DINOSAURIO_UBICACIONES_CONOCIDAS: Dict[str, list] = {
        "tiranosaurio rex": ["usa", "canada"],
        "tyrannosaurus rex": ["usa", "canada"],
        "triceratops": ["usa", "canada"],
        "triceratops horridus": ["usa", "canada"],
        "velociraptor": ["mongolia", "china"],
        "velociraptor mongoliensis": ["mongolia", "china"],
        "brachiosaurio": ["usa", "tanzania"],
        "brachiosaurus altithorax": ["usa", "tanzania"],
        "estegosaurio": ["usa", "portugal"],
        "stegosaurus stenops": ["usa", "portugal"],
        "espinosaurio": ["egipto", "marruecos"],
        "spinosaurus aegyptiacus": ["egipto", "marruecos"],
        "diplodocus": ["usa"],
        "diplodocus carnegii": ["usa"],
        "anquilosaurio": ["usa", "canada"],
        "ankylosaurus magniventris": ["usa", "canada"],
        "parasaurolofo": ["usa", "canada"],
        "parasaurolophus walkeri": ["usa", "canada"],
        "carnotaurus": ["argentina"],
        "carnotaurus sastrei": ["argentina"],
        "giganotosaurus": ["argentina"],
        "giganotosaurus carolinii": ["argentina"],
        "argentinosaurus": ["argentina"],
        "argentinosaurus huinculensis": ["argentina"],
        "microraptor": ["china"],
        "microraptor zhaoianus": ["china"],
        "iguanodon": ["reino unido", "alemania"],
        "iguanodon bernissartensis": ["reino unido", "alemania"],
        "plateosaurus": ["alemania"],
        "plateosaurus engelhardti": ["alemania"],
        "dilophosaurus": ["usa"],
        "dilophosaurus wetherilli": ["usa"],
        "protoceratops": ["mongolia"],
        "protoceratops andrewsi": ["mongolia"],
        "concavenator": ["españa"],
        "concavenator corcovatus": ["españa"],
        "amargasaurus": ["argentina"],
        "amargasaurus cazaui": ["argentina"],
        "leaellynasaura": ["australia"],
        "leaellynasaura amicagraphica": ["australia"],
        "oxalaia": ["brasil"],
        "oxalaia quilombensis": ["brasil"],
        "arcovenator": ["francia"],
        "arcovenator escotae": ["francia"],
        "labocania": ["mexico"],
        "labocania anomala": ["mexico"]
    }

    _COUNTRY_ALIASES: Dict[str, str] = {
        "estados unidos": "usa",
        "eeuu": "usa",
        "united states": "usa",
        "united states of america": "usa",
        "u s a": "usa",
        "sudafrica": "sudafrica",
        "sudáfrica": "sudafrica",
        "mexico": "mexico",
        "méxico": "mexico",
        "canada": "canada",
        "canadá": "canada",
        "peru": "peru",
        "perú": "peru",
        "japon": "japon",
        "japón": "japon",
        "niger": "niger",
        "níger": "niger",
        "espana": "españa",
        "españa": "españa",
    }

    @staticmethod
    def _strip_accents(value: str) -> str:
        normalized = unicodedata.normalize("NFKD", value or "")
        return "".join(char for char in normalized if not unicodedata.combining(char))

    def normalize_country_key(self, value: str) -> str:
        raw = " ".join((value or "").strip().lower().split())
        if not raw:
            return ""

        alias = self._COUNTRY_ALIASES.get(raw)
        if alias:
            return alias

        stripped = self._strip_accents(raw)
        alias = self._COUNTRY_ALIASES.get(stripped)
        if alias:
            return alias

        for key in self.PAISES_API.keys():
            if raw == key or stripped == self._strip_accents(key):
                return key

        for key in self.PAISES_COORDENADAS.keys():
            if raw == key or stripped == self._strip_accents(key):
                return key

        return stripped

    def get_country_label(self, value: str) -> str:
        key = self.normalize_country_key(value)
        if not key:
            return ""
        return self.PAISES_LABELS.get(key, key.capitalize())

settings = Settings()
