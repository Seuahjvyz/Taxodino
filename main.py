from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
from dotenv import load_dotenv
from app.api.v1.endpoints import auth

# Cargar variables de entorno
load_dotenv()

# Importar rutas de API existentes
from app.api.v1.endpoints import dinosaurios

# Importar nuevas rutas geográficas
from app.api.v1.endpoints.dinosaurios_geograficos import router as geografia_router

# Intentar importar favoritos (si existe)
try:
    from app.api.v1.endpoints import favoritos
    HAS_FAVORITOS = hasattr(favoritos, 'router')
except ImportError:
    HAS_FAVORITOS = False
    print("⚠️ Módulo de favoritos no encontrado")

# Importar configuración de base de datos
from app.core.database import engine, Base

# Crear tablas en la base de datos (Neon PostgreSQL)
print("🔌 Conectando a la base de datos...")
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas/verificadas exitosamente")
except Exception as e:
    print(f"⚠️ Error conectando a la base de datos: {e}")
    print("💡 Asegúrate de tener configurado el archivo .env con DATABASE_URL")

# Inicializar FastAPI
app = FastAPI(
    title="Taxodino API", 
    version="1.0.0",
    description="API de dinosaurios con mapa mundial interactivo y base de datos en Neon PostgreSQL"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

# ============================================
# SERVIDOR DE ARCHIVOS ESTÁTICOS
# ============================================

static_path = Path("static")
if static_path.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    print("📁 Archivos estáticos montados desde:", static_path.absolute())
else:
    print("⚠️ Carpeta 'static' no encontrada, creándola...")
    static_path.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")

# ============================================
# CONFIGURACIÓN DE TEMPLATES
# ============================================

templates_path = Path("templates")
if not templates_path.exists():
    print("⚠️ Carpeta 'templates' no encontrada, creándola...")
    templates_path.mkdir(exist_ok=True)

templates = Jinja2Templates(directory="templates")

# ============================================
# RUTAS PARA VISTAS (PÁGINAS HTML)
# ============================================

@app.get("/")
async def home(request: Request):
    """Página principal"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    """Página de inicio de sesión"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/registro")
async def registro_page(request: Request):
    """Página de registro"""
    return templates.TemplateResponse("registro.html", {"request": request})

@app.get("/perfil")
async def perfil_page(request: Request):
    """Página de perfil de usuario"""
    return templates.TemplateResponse("perfil.html", {"request": request})

@app.get("/favoritos")
async def favoritos_page(request: Request):
    """Página de favoritos"""
    return templates.TemplateResponse("favoritos.html", {"request": request})

@app.get("/mapa")
async def mapa_mundial_page(request: Request):
    """🌍 Página del mapa mundial de dinosaurios"""
    return templates.TemplateResponse("mapa_dinosaurios.html", {"request": request})

# ============================================
# RUTAS DE API
# ============================================

# APIs existentes
app.include_router(dinosaurios.router, prefix="/api/v1/dinosaurs", tags=["dinosaurs"])

# NUEVA API GEOGRÁFICA (Mapa mundial)
app.include_router(geografia_router, prefix="/api/v1/geografia", tags=["geography"])

# API de favoritos (solo si existe)
if HAS_FAVORITOS:
    app.include_router(favoritos.router, prefix="/api/v1/favorites", tags=["favorites"])
    print("✅ API de favoritos habilitada")
else:
    print("⚠️ API de favoritos no disponible (archivo no encontrado o sin router)")

# ============================================
# ENDPOINTS ADICIONALES
# ============================================

@app.get("/health")
async def health_check():
    """Verificar estado de la API y base de datos"""
    db_status = "connected"
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "api_version": "1.0.0",
        "features": ["dinosaurios", "mapa_mundial", "favoritos" if HAS_FAVORITOS else "no"]
    }

@app.get("/api-info")
async def api_info():
    """Información de los endpoints disponibles"""
    endpoints = {
        "dinosaurios": "/api/v1/dinosaurs",
        "geografia": {
            "paises": "/api/v1/geografia/paises",
            "dinosaurios_por_pais": "/api/v1/geografia/dinosaurios/{pais}"
        },
        "health": "/health"
    }
    
    if HAS_FAVORITOS:
        endpoints["favoritos"] = "/api/v1/favorites"
    
    return {
        "endpoints": endpoints,
        "documentacion": "/docs",
        "redoc": "/redoc"
    }

# ============================================
# INICIALIZACIÓN DE LA APLICACIÓN
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*50)
    print("🦕 TAXODINO API - Servidor de Dinosaurios")
    print("="*50)
    print(f"📁 Archivos estáticos: {'✅' if static_path.exists() else '❌'}")
    print(f"📁 Templates: {'✅' if templates_path.exists() else '❌'}")
    print(f"🗄️  Base de datos: {'🌩️ Neon PostgreSQL' if 'neon.tech' in os.getenv('DATABASE_URL', '') else 'SQLite/local'}")
    print(f"🌍 Mapa mundial: ✅ Activado")
    print(f"⭐ Favoritos: {'✅ Activado' if HAS_FAVORITOS else '❌ No disponible'}")
    print("\n📌 Endpoints disponibles:")
    print("   - 🌐 http://localhost:8000/")
    print("   - 🗺️  http://localhost:8000/mapa")
    print("   - 📚 http://localhost:8000/docs")
    print("   - 💚 http://localhost:8000/health")
    print("\n🚀 Iniciando servidor...")
    print("="*50 + "\n")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )