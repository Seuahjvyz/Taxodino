from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario import Usuario
import hashlib
import re

router = APIRouter()

class RegistroRequest(BaseModel):
    nombre: str
    username: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(request: RegistroRequest, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    
    # Validar que el username no exista
    existing_user = db.query(Usuario).filter(Usuario.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    
    # Validar que el email no exista
    existing_email = db.query(Usuario).filter(Usuario.email == request.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    
    # Validar fortaleza de contraseña
    if not validate_password(request.password):
        raise HTTPException(status_code=400, detail="La contraseña no cumple con los requisitos de seguridad")
    
    # Hashear contraseña
    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()
    
    # Crear usuario
    nuevo_usuario = Usuario(
        nombre=request.nombre,
        username=request.username,
        email=request.email,
        password_hash=hashed_password
    )
    
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    return {
        "message": "Usuario registrado exitosamente",
        "id": nuevo_usuario.id,
        "username": nuevo_usuario.username
    }

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Iniciar sesión"""
    
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()
    
    if usuario.password_hash != hashed_password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    return {
        "message": "Login exitoso",
        "id": usuario.id,
        "nombre": usuario.nombre,
        "username": usuario.username,
        "email": usuario.email
    }

def validate_password(password: str) -> bool:
    """Validar que la contraseña cumpla con los requisitos"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True