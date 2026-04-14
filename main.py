from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

# Importar rutas de API
from app.api.v1.endpoints import dinosaurios
from app.core.database import engine, Base

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Taxodino API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (CSS, JS, imágenes)
static_path = Path("static")
if static_path.exists():
    app.mount("/static", StaticFiles(directory="static"), name="static")
else:
    print("⚠️ Carpeta 'static' no encontrada")
    static_path.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates_path = Path("templates")
if not templates_path.exists():
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


@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon"}

# ============================================
# RUTAS DE API
# ============================================

app.include_router(dinosaurios.router, prefix="/api/v1/dinosaurs", tags=["dinosaurs"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando Taxodino API...")
    print("📁 Archivos estáticos:", "static/" if Path("static").exists() else "No encontrada")
    print("📁 Templates:", "templates/" if Path("templates").exists() else "No encontrada")
    print("🌐 Visita: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)