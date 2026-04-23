import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, '/app')

from app.core.database import engine, Base
from sqlalchemy import text

def fix_table():
    print("🔧 Reparando tabla registros_fosiles...")
    
    with engine.connect() as conn:
        # Verificar si la tabla existe
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'registros_fosiles'
            )
        """))
        exists = result.scalar()
        
        if exists:
            print("  📦 Tabla registros_fosiles existe, eliminando...")
            conn.execute(text("DROP TABLE registros_fosiles CASCADE"))
            conn.commit()
            print("  ✅ Tabla eliminada")
    
    # Recrear la tabla
    from app.models.registro_fosil import RegistroFosil
    Base.metadata.create_all(bind=engine)
    print("  ✅ Tabla recreada correctamente")
    
    print("🎉 Reparación completada!")

if __name__ == "__main__":
    fix_table()
