import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.dinosaurio import Dinosaurio

def populate_dinosaurs():
    print("🦕 Conectando a la base de datos...")
    
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Verificar si ya hay datos
    count = db.query(Dinosaurio).count()
    if count > 0:
        print(f"⚠️ Ya existen {count} dinosaurios en la base de datos")
        respuesta = input("¿Deseas agregar más? (s/n): ")
        if respuesta.lower() != 's':
            db.close()
            return
    
    dinosaurios_ejemplo = [
        Dinosaurio(
            nombre="Tiranosaurio Rex",
            nombre_cientifico="Tyrannosaurus rex",
            periodo="Cretácico Superior",
            dieta="Carnívoro",
            descripcion="El Tyrannosaurus rex fue uno de los depredadores más grandes que caminaron sobre la Tierra. Con una longitud de hasta 12 metros y una mordida increíblemente poderosa, dominaba su ecosistema.",
            longitud=12.3,
            peso=8000
        ),
        Dinosaurio(
            nombre="Triceratops",
            nombre_cientifico="Triceratops horridus",
            periodo="Cretácico Superior",
            dieta="Herbívoro",
            descripcion="El Triceratops es fácilmente reconocible por sus tres cuernos y su gran gola ósea. Era un herbívoro que vivía en manadas.",
            longitud=9.0,
            peso=6000
        ),
        Dinosaurio(
            nombre="Velociraptor",
            nombre_cientifico="Velociraptor mongoliensis",
            periodo="Cretácico Superior",
            dieta="Carnívoro",
            descripcion="El Velociraptor era un cazador ágil con una garra en forma de hoz.",
            longitud=2.0,
            peso=15
        ),
        Dinosaurio(
            nombre="Brachiosaurio",
            nombre_cientifico="Brachiosaurus altithorax",
            periodo="Jurásico Superior",
            dieta="Herbívoro",
            descripcion="Uno de los dinosaurios más altos que existieron.",
            longitud=25.0,
            peso=56000
        ),
        Dinosaurio(
            nombre="Estegosaurio",
            nombre_cientifico="Stegosaurus stenops",
            periodo="Jurásico Superior",
            dieta="Herbívoro",
            descripcion="Famoso por las placas óseas en su espalda.",
            longitud=9.0,
            peso=5000
        ),
        Dinosaurio(
            nombre="Espinosaurio",
            nombre_cientifico="Spinosaurus aegyptiacus",
            periodo="Cretácico Superior",
            dieta="Carnívoro",
            descripcion="El Spinosaurus era más grande que el T-Rex, con una distintiva vela en su espalda.",
            longitud=15.0,
            peso=7000
        ),
        Dinosaurio(
            nombre="Diplodocus",
            nombre_cientifico="Diplodocus carnegii",
            periodo="Jurásico Superior",
            dieta="Herbívoro",
            descripcion="Uno de los dinosaurios más largos.",
            longitud=27.0,
            peso=15000
        ),
        Dinosaurio(
            nombre="Anquilosaurio",
            nombre_cientifico="Ankylosaurus magniventris",
            periodo="Cretácico Superior",
            dieta="Herbívoro",
            descripcion="El 'tanque viviente' del Cretácico.",
            longitud=8.0,
            peso=6000
        ),
        Dinosaurio(
            nombre="Parasaurolofo",
            nombre_cientifico="Parasaurolophus walkeri",
            periodo="Cretácico Superior",
            dieta="Herbívoro",
            descripcion="Conocido por su larga cresta hueca en la cabeza.",
            longitud=9.5,
            peso=2500
        )
    ]
    
    print("\n📝 Agregando dinosaurios...")
    for dino in dinosaurios_ejemplo:
        existing = db.query(Dinosaurio).filter(Dinosaurio.nombre == dino.nombre).first()
        if not existing:
            db.add(dino)
            print(f"  ✅ Agregado: {dino.nombre}")
        else:
            print(f"  ⏭️ Ya existe: {dino.nombre}")
    
    db.commit()
    
    final_count = db.query(Dinosaurio).count()
    print(f"\n🎉 Total de dinosaurios en la base de datos: {final_count}")
    
    db.close()

if __name__ == "__main__":
    populate_dinosaurs()