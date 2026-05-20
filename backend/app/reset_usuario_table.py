from app.core.database import engine
from sqlalchemy import text

def reset_table():
    print("🔄 Eliminando tabla usuarios...")
    with engine.connect() as conn:
        # Eliminar la tabla si existe
        conn.execute(text("DROP TABLE IF EXISTS usuarios CASCADE"))
        conn.commit()
        print("  ✅ Tabla eliminada")
    
    print("📝 Recreando tabla usuarios...")
    from app.models.usuario import Usuario
    from app.core.database import Base
    Base.metadata.create_all(bind=engine)
    print("  ✅ Tabla recreada correctamente")
    
    # Verificar columnas
    with engine.connect() as conn:
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'usuarios'"))
        print("\n📋 Columnas creadas:")
        for row in result:
            print(f"  - {row[0]}")

if __name__ == "__main__":
    reset_table()