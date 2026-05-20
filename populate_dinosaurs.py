import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import Base, SessionLocal, engine
from app.models.dinosaurio import Dinosaurio
from app.models.registro_fosil import RegistroFosil


def build_placeholder_url(nombre: str) -> str:
    return f"https://placehold.co/600x400/2D4A22/FFF4D6?text={nombre.replace(' ', '+')}"


DINOSAURIOS_EJEMPLO = [
    {
        "nombre": "Tiranosaurio Rex",
        "nombre_cientifico": "Tyrannosaurus rex",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Uno de los depredadores terrestres más famosos y poderosos del final del Cretácico.",
        "longitud": 12.3,
        "peso": 8000,
    },
    {
        "nombre": "Triceratops",
        "nombre_cientifico": "Triceratops horridus",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ceratopsio robusto con tres cuernos y una gran gola ósea defensiva.",
        "longitud": 9.0,
        "peso": 6000,
    },
    {
        "nombre": "Velociraptor",
        "nombre_cientifico": "Velociraptor mongoliensis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Pequeño dromeosáurido ágil, famoso por su garra en forma de hoz.",
        "longitud": 2.0,
        "peso": 15,
    },
    {
        "nombre": "Brachiosaurio",
        "nombre_cientifico": "Brachiosaurus altithorax",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo enorme de cuello largo y postura alta, adaptado para ramonear vegetación elevada.",
        "longitud": 25.0,
        "peso": 56000,
    },
    {
        "nombre": "Estegosaurio",
        "nombre_cientifico": "Stegosaurus stenops",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Conocido por sus placas dorsales y su cola con púas defensivas.",
        "longitud": 9.0,
        "peso": 5000,
    },
    {
        "nombre": "Espinosaurio",
        "nombre_cientifico": "Spinosaurus aegyptiacus",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Gran terópodo semiacuático con una distintiva vela sobre la espalda.",
        "longitud": 15.0,
        "peso": 7000,
    },
    {
        "nombre": "Diplodocus",
        "nombre_cientifico": "Diplodocus carnegii",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo extremadamente largo y ligero en comparación con otros gigantes.",
        "longitud": 27.0,
        "peso": 15000,
    },
    {
        "nombre": "Anquilosaurio",
        "nombre_cientifico": "Ankylosaurus magniventris",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Dinosaurio acorazado con una poderosa maza caudal para defenderse.",
        "longitud": 8.0,
        "peso": 6000,
    },
    {
        "nombre": "Parasaurolofo",
        "nombre_cientifico": "Parasaurolophus walkeri",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Hadrosaurio reconocido por su larga cresta craneal tubular.",
        "longitud": 9.5,
        "peso": 2500,
    },
    {
        "nombre": "Allosaurus",
        "nombre_cientifico": "Allosaurus fragilis",
        "periodo": "Jurásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Gran depredador norteamericano anterior al T. rex.",
        "longitud": 8.5,
        "peso": 2300,
    },
    {
        "nombre": "Carnotaurus",
        "nombre_cientifico": "Carnotaurus sastrei",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo sudamericano de brazos muy cortos y cuernos sobre los ojos.",
        "longitud": 8.0,
        "peso": 1500,
    },
    {
        "nombre": "Iguanodon",
        "nombre_cientifico": "Iguanodon bernissartensis",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Ornitópodo temprano famoso por la espina en el pulgar.",
        "longitud": 10.0,
        "peso": 3500,
    },
    {
        "nombre": "Pachycephalosaurus",
        "nombre_cientifico": "Pachycephalosaurus wyomingensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Dinosaurio bípedo con un domo craneal grueso y resistente.",
        "longitud": 4.5,
        "peso": 450,
    },
    {
        "nombre": "Giganotosaurus",
        "nombre_cientifico": "Giganotosaurus carolinii",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Uno de los mayores depredadores terrestres conocidos, hallado en Argentina.",
        "longitud": 13.0,
        "peso": 8000,
    },
    {
        "nombre": "Argentinosaurus",
        "nombre_cientifico": "Argentinosaurus huinculensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Gigante saurópodo sudamericano entre los animales terrestres más grandes conocidos.",
        "longitud": 30.0,
        "peso": 70000,
    },
    {
        "nombre": "Microraptor",
        "nombre_cientifico": "Microraptor zhaoianus",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Pequeño dromeosáurido con plumas en brazos y patas, relacionado con el vuelo temprano.",
        "longitud": 0.8,
        "peso": 1,
    },
    {
        "nombre": "Deinonychus",
        "nombre_cientifico": "Deinonychus antirrhopus",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Cazador ágil que ayudó a cambiar la imagen moderna de los dinosaurios.",
        "longitud": 3.4,
        "peso": 80,
    },
    {
        "nombre": "Coelophysis",
        "nombre_cientifico": "Coelophysis bauri",
        "periodo": "Triásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo esbelto y temprano, importante para estudiar la evolución inicial del grupo.",
        "longitud": 3.0,
        "peso": 25,
    },
    {
        "nombre": "Dilophosaurus",
        "nombre_cientifico": "Dilophosaurus wetherilli",
        "periodo": "Jurásico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo con dos crestas arqueadas sobre el cráneo.",
        "longitud": 7.0,
        "peso": 400,
    },
    {
        "nombre": "Apatosaurus",
        "nombre_cientifico": "Apatosaurus louisae",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo de cuerpo macizo y cuello largo, clásico de la Formación Morrison.",
        "longitud": 22.0,
        "peso": 23000,
    },
    {
        "nombre": "Styracosaurus",
        "nombre_cientifico": "Styracosaurus albertensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ceratopsio con una gola impresionante armada con largos cuernos.",
        "longitud": 5.5,
        "peso": 2700,
    },
    {
        "nombre": "Therizinosaurus",
        "nombre_cientifico": "Therizinosaurus cheloniformis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Dinosaurio de grandes garras, cuerpo voluminoso y probable dieta herbívora.",
        "longitud": 10.0,
        "peso": 5000,
    },
    {
        "nombre": "Oviraptor",
        "nombre_cientifico": "Oviraptor philoceratops",
        "periodo": "Cretácico Superior",
        "dieta": "Omnívoro",
        "descripcion": "Pequeño dinosaurio emplumado asociado a nidos y huevos fósiles.",
        "longitud": 2.0,
        "peso": 35,
    },
    {
        "nombre": "Maiasaura",
        "nombre_cientifico": "Maiasaura peeblesorum",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Hadrosaurio conocido por evidencias de cuidado parental en sus colonias de nido.",
        "longitud": 9.0,
        "peso": 2500,
    },
    {
        "nombre": "Corythosaurus",
        "nombre_cientifico": "Corythosaurus casuarius",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Hadrosaurio crestado con una cabeza similar a un casco.",
        "longitud": 8.0,
        "peso": 3000,
    },
    {
        "nombre": "Utahraptor",
        "nombre_cientifico": "Utahraptor ostrommaysorum",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Gran dromeosáurido norteamericano, más robusto que Velociraptor.",
        "longitud": 6.0,
        "peso": 500,
    },
    {
        "nombre": "Albertosaurus",
        "nombre_cientifico": "Albertosaurus sarcophagus",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Tiranosáurido esbelto de Norteamérica, pariente cercano del T. rex.",
        "longitud": 9.0,
        "peso": 2500,
    },
    {
        "nombre": "Ceratosaurus",
        "nombre_cientifico": "Ceratosaurus nasicornis",
        "periodo": "Jurásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo con un cuerno nasal prominente y cuerpo ágil.",
        "longitud": 6.0,
        "peso": 1000,
    },
    {
        "nombre": "Plateosaurus",
        "nombre_cientifico": "Plateosaurus engelhardti",
        "periodo": "Triásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Uno de los grandes dinosaurios tempranos más conocidos de Europa.",
        "longitud": 8.0,
        "peso": 4000,
    },
    {
        "nombre": "Protoceratops",
        "nombre_cientifico": "Protoceratops andrewsi",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Pequeño ceratopsio del desierto de Gobi, abundante en el registro fósil.",
        "longitud": 2.0,
        "peso": 180,
    },
    {
        "nombre": "Concavenator",
        "nombre_cientifico": "Concavenator corcovatus",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo ibérico con una joroba distintiva en la espalda, hallado en España.",
        "longitud": 6.0,
        "peso": 400,
    },
    {
        "nombre": "Labocania",
        "nombre_cientifico": "Labocania anomala",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo grande de Baja California conocido por restos fragmentarios.",
        "longitud": 7.0,
        "peso": 1200,
    },
    {
        "nombre": "Oxalaia",
        "nombre_cientifico": "Oxalaia quilombensis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Espinosáurido brasileño emparentado con Spinosaurus, encontrado en la Cuenca de Sao Luis.",
        "longitud": 12.0,
        "peso": 5000,
    },
    {
        "nombre": "Leaellynasaura",
        "nombre_cientifico": "Leaellynasaura amicagraphica",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Pequeño ornitópodo australiano adaptado a latitudes polares del Cretácico.",
        "longitud": 2.0,
        "peso": 30,
    },
    {
        "nombre": "Arcovenator",
        "nombre_cientifico": "Arcovenator escotae",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido europeo descubierto en el sur de Francia.",
        "longitud": 6.0,
        "peso": 500,
    },
    {
        "nombre": "Amargasaurus",
        "nombre_cientifico": "Amargasaurus cazaui",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo patagónico famoso por las largas espinas dobles de su cuello.",
        "longitud": 10.0,
        "peso": 2600,
    },
    {
        "nombre": "Acrocanthosaurus",
        "nombre_cientifico": "Acrocanthosaurus atokensis",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Gran terópodo norteamericano con altas espinas neurales a lo largo de la espalda.",
        "longitud": 11.5,
        "peso": 6200,
    },
    {
        "nombre": "Australovenator",
        "nombre_cientifico": "Australovenator wintonensis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Depredador australiano de complexión ligera hallado en la Formación Winton.",
        "longitud": 6.0,
        "peso": 500,
    },
    {
        "nombre": "Aucasaurus",
        "nombre_cientifico": "Aucasaurus garridoi",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido patagónico relacionado con Carnotaurus y de cráneo corto.",
        "longitud": 5.5,
        "peso": 700,
    },
    {
        "nombre": "Bajadasaurus",
        "nombre_cientifico": "Bajadasaurus pronuspinax",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Dicraeosáurido argentino conocido por sus largas espinas cervicales orientadas hacia delante.",
        "longitud": 12.0,
        "peso": 4000,
    },
    {
        "nombre": "Dreadnoughtus",
        "nombre_cientifico": "Dreadnoughtus schrani",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio gigante de Patagonia preservado con uno de los esqueletos más completos entre los colosos.",
        "longitud": 26.0,
        "peso": 49000,
    },
    {
        "nombre": "Europasaurus",
        "nombre_cientifico": "Europasaurus holgeri",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Pequeño saurópodo insular de Alemania, famoso por su caso de enanismo evolutivo.",
        "longitud": 6.2,
        "peso": 1000,
    },
    {
        "nombre": "Eustreptospondylus",
        "nombre_cientifico": "Eustreptospondylus oxoniensis",
        "periodo": "Jurásico Medio",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo jurásico británico conocido por restos relativamente completos para su época.",
        "longitud": 5.0,
        "peso": 300,
    },
    {
        "nombre": "Gasosaurus",
        "nombre_cientifico": "Gasosaurus constructus",
        "periodo": "Jurásico Medio",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo chino descubierto durante obras de una planta de gas, de ahí su peculiar nombre.",
        "longitud": 3.5,
        "peso": 150,
    },
    {
        "nombre": "Herrerasaurus",
        "nombre_cientifico": "Herrerasaurus ischigualastensis",
        "periodo": "Triásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Uno de los dinosaurios más antiguos y mejor conocidos del Triásico sudamericano.",
        "longitud": 6.0,
        "peso": 350,
    },
    {
        "nombre": "Irritator",
        "nombre_cientifico": "Irritator challengeri",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Espinosáurido brasileño descrito a partir de un cráneo alterado comercialmente.",
        "longitud": 8.0,
        "peso": 1000,
    },
    {
        "nombre": "Kentrosaurus",
        "nombre_cientifico": "Kentrosaurus aethiopicus",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Estegosaurio africano con hileras de espinas y placas distribuidas por el lomo y la cola.",
        "longitud": 5.0,
        "peso": 1000,
    },
    {
        "nombre": "Lusotitan",
        "nombre_cientifico": "Lusotitan atalaiensis",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Gran saurópodo portugués emparentado con Brachiosaurus.",
        "longitud": 17.0,
        "peso": 13000,
    },
    {
        "nombre": "Mamenchisaurus",
        "nombre_cientifico": "Mamenchisaurus youngi",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo chino célebre por su cuello extremadamente largo.",
        "longitud": 22.0,
        "peso": 25000,
    },
    {
        "nombre": "Mapusaurus",
        "nombre_cientifico": "Mapusaurus roseae",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Carcharodontosáurido argentino encontrado en un yacimiento con múltiples individuos.",
        "longitud": 12.0,
        "peso": 5000,
    },
    {
        "nombre": "Massospondylus",
        "nombre_cientifico": "Massospondylus carinatus",
        "periodo": "Jurásico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Prosaurópodo sudafricano abundante en el registro del Karoo.",
        "longitud": 4.5,
        "peso": 500,
    },
    {
        "nombre": "Megalosaurus",
        "nombre_cientifico": "Megalosaurus bucklandii",
        "periodo": "Jurásico Medio",
        "dieta": "Carnívoro",
        "descripcion": "Primer dinosaurio descrito formalmente en la historia de la paleontología.",
        "longitud": 6.0,
        "peso": 700,
    },
    {
        "nombre": "Minmi",
        "nombre_cientifico": "Minmi paravertebra",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Anquilosaurio australiano pequeño y bien adaptado a desplazarse cerca del suelo.",
        "longitud": 3.0,
        "peso": 300,
    },
    {
        "nombre": "Neovenator",
        "nombre_cientifico": "Neovenator salerii",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Allosauroide británico entre los grandes depredadores europeos mejor conocidos.",
        "longitud": 7.5,
        "peso": 1000,
    },
    {
        "nombre": "Shunosaurus",
        "nombre_cientifico": "Shunosaurus lii",
        "periodo": "Jurásico Medio",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo chino de cola armada con una maza ósea poco común entre sus parientes.",
        "longitud": 10.0,
        "peso": 3000,
    },
    {
        "nombre": "Tarbosaurus",
        "nombre_cientifico": "Tarbosaurus bataar",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Gran tiranosáurido asiático muy cercano a Tyrannosaurus.",
        "longitud": 10.0,
        "peso": 5000,
    },
    {
        "nombre": "Adasaurus",
        "nombre_cientifico": "Adasaurus mongoliensis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Dromeosáurido del desierto de Gobi conocido por sus patas posteriores especializadas.",
        "longitud": 2.4,
        "peso": 35,
    },
    {
        "nombre": "Agujaceratops",
        "nombre_cientifico": "Agujaceratops mariscalensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ceratopsio de Texas relacionado con Chasmosaurus y descubierto en la Formación Aguja.",
        "longitud": 4.3,
        "peso": 1500,
    },
    {
        "nombre": "Ampelosaurus",
        "nombre_cientifico": "Ampelosaurus atacis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio europeo con osteodermos hallado en el sur de Francia.",
        "longitud": 15.0,
        "peso": 8000,
    },
    {
        "nombre": "Bonitasaura",
        "nombre_cientifico": "Bonitasaura salgadoi",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio argentino con hocico cuadrado adaptado para cortar vegetación.",
        "longitud": 12.0,
        "peso": 7000,
    },
    {
        "nombre": "Camarasaurus",
        "nombre_cientifico": "Camarasaurus lentus",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo robusto y común en la Formación Morrison de Norteamérica.",
        "longitud": 18.0,
        "peso": 18000,
    },
    {
        "nombre": "Chialingosaurus",
        "nombre_cientifico": "Chialingosaurus kuani",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Estegosaurio chino entre los primeros miembros asiáticos bien reconocidos del grupo.",
        "longitud": 4.0,
        "peso": 1000,
    },
    {
        "nombre": "Chuandongocoelurus",
        "nombre_cientifico": "Chuandongocoelurus primitivus",
        "periodo": "Jurásico Medio",
        "dieta": "Carnívoro",
        "descripcion": "Pequeño terópodo chino conocido por restos fragmentarios de Sichuan.",
        "longitud": 2.8,
        "peso": 25,
    },
    {
        "nombre": "Draconyx",
        "nombre_cientifico": "Draconyx loureiroi",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ornitópodo portugués hallado en sedimentos de la cuenca de Lourinha.",
        "longitud": 3.5,
        "peso": 200,
    },
    {
        "nombre": "Gargoyleosaurus",
        "nombre_cientifico": "Gargoyleosaurus parkpinorum",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Anquilosaurio temprano de Norteamérica con armadura corporal bien desarrollada.",
        "longitud": 3.5,
        "peso": 1000,
    },
    {
        "nombre": "Huayangosaurus",
        "nombre_cientifico": "Huayangosaurus taibaii",
        "periodo": "Jurásico Medio",
        "dieta": "Herbívoro",
        "descripcion": "Estegosaurio basal chino con cráneo relativamente corto y placas mixtas.",
        "longitud": 4.5,
        "peso": 1500,
    },
    {
        "nombre": "Lourinhanosaurus",
        "nombre_cientifico": "Lourinhanosaurus antunesi",
        "periodo": "Jurásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo portugués conocido por restos de adultos y posibles nidadas.",
        "longitud": 4.5,
        "peso": 150,
    },
    {
        "nombre": "Mononykus",
        "nombre_cientifico": "Mononykus olecranus",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Pequeño alvarezsáurido mongol con brazos cortos y una sola gran garra funcional.",
        "longitud": 1.2,
        "peso": 3.5,
    },
    {
        "nombre": "Overosaurus",
        "nombre_cientifico": "Overosaurus paradasorum",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio argentino del grupo Aeolosaurini encontrado en Patagonia.",
        "longitud": 10.0,
        "peso": 5000,
    },
    {
        "nombre": "Pelecanimimus",
        "nombre_cientifico": "Pelecanimimus polyodon",
        "periodo": "Cretácico Inferior",
        "dieta": "Omnívoro",
        "descripcion": "Ornitomimosaurio español con un número excepcionalmente alto de dientes.",
        "longitud": 2.2,
        "peso": 25,
    },
    {
        "nombre": "Qiaowanlong",
        "nombre_cientifico": "Qiaowanlong kangxii",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo chino de cuello largo relacionado con los braquiosáuridos.",
        "longitud": 12.0,
        "peso": 6000,
    },
    {
        "nombre": "Rinconsaurus",
        "nombre_cientifico": "Rinconsaurus caudamirus",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio argentino de cola distintiva procedente de Neuquén.",
        "longitud": 11.0,
        "peso": 6000,
    },
    {
        "nombre": "Sinraptor",
        "nombre_cientifico": "Sinraptor dongi",
        "periodo": "Jurásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Gran depredador chino del Jurásico tardío, pese a su nombre no era un verdadero raptor.",
        "longitud": 7.5,
        "peso": 1000,
    },
    {
        "nombre": "Sonorasaurus",
        "nombre_cientifico": "Sonorasaurus thompsoni",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo de Arizona que representa a los gigantes del Cretácico temprano en Norteamérica.",
        "longitud": 15.0,
        "peso": 10000,
    },
    {
        "nombre": "Turiasaurus",
        "nombre_cientifico": "Turiasaurus riodevensis",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Enorme saurópodo ibérico, uno de los mayores dinosaurios descritos de Europa.",
        "longitud": 30.0,
        "peso": 40000,
    },
    {
        "nombre": "Xiongguanlong",
        "nombre_cientifico": "Xiongguanlong baimoensis",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Tiranosauroide chino que muestra rasgos intermedios antes de los gigantes tardíos.",
        "longitud": 5.0,
        "peso": 270,
    },
    {
        "nombre": "Achelousaurus",
        "nombre_cientifico": "Achelousaurus horneri",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ceratopsio norteamericano con jefes óseos sobre la nariz y los ojos en lugar de cuernos largos.",
        "longitud": 6.0,
        "peso": 3000,
    },
    {
        "nombre": "Alamosaurus",
        "nombre_cientifico": "Alamosaurus sanjuanensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Gran titanosaurio de Norteamérica, uno de los últimos saurópodos del continente.",
        "longitud": 21.0,
        "peso": 30000,
    },
    {
        "nombre": "Buitreraptor",
        "nombre_cientifico": "Buitreraptor gonzalezorum",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Pequeño dromeosáurido patagónico de hocico alargado y numerosos dientes pequeños.",
        "longitud": 1.5,
        "peso": 7,
    },
    {
        "nombre": "Chasmosaurus",
        "nombre_cientifico": "Chasmosaurus belli",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ceratopsio canadiense con gran gola alargada y cuernos faciales moderados.",
        "longitud": 4.8,
        "peso": 1500,
    },
    {
        "nombre": "Dicraeosaurus",
        "nombre_cientifico": "Dicraeosaurus hansemanni",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo africano de cuello relativamente corto y espinas neurales altas.",
        "longitud": 13.0,
        "peso": 12000,
    },
    {
        "nombre": "Dracorex",
        "nombre_cientifico": "Dracorex hogwartsia",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Paquicefalosaurio norteamericano con cráneo espinoso y aspecto de dragón.",
        "longitud": 4.0,
        "peso": 200,
    },
    {
        "nombre": "Einiosaurus",
        "nombre_cientifico": "Einiosaurus procurvicornis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ceratopsio de Montana famoso por su cuerno nasal curvado hacia delante.",
        "longitud": 4.5,
        "peso": 1300,
    },
    {
        "nombre": "Fukuiraptor",
        "nombre_cientifico": "Fukuiraptor kitadaniensis",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo japonés esbelto hallado en la cantera de Kitadani.",
        "longitud": 4.2,
        "peso": 300,
    },
    {
        "nombre": "Gallimimus",
        "nombre_cientifico": "Gallimimus bullatus",
        "periodo": "Cretácico Superior",
        "dieta": "Omnívoro",
        "descripcion": "Ornitomímido de largas patas conocido por su velocidad y su pico sin dientes.",
        "longitud": 6.0,
        "peso": 450,
    },
    {
        "nombre": "Hypsilophodon",
        "nombre_cientifico": "Hypsilophodon foxii",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Pequeño ornitópodo británico ágil y de gran importancia histórica.",
        "longitud": 2.3,
        "peso": 20,
    },
    {
        "nombre": "Jobaria",
        "nombre_cientifico": "Jobaria tiguidensis",
        "periodo": "Jurásico Medio",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo africano basal de gran tamaño descubierto en el desierto del Sahara.",
        "longitud": 18.0,
        "peso": 22000,
    },
    {
        "nombre": "Kaatedocus",
        "nombre_cientifico": "Kaatedocus siberi",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Diplodócido jurásico de Norteamérica conocido por un cráneo excepcionalmente bien preservado.",
        "longitud": 14.0,
        "peso": 9000,
    },
    {
        "nombre": "Latenivenatrix",
        "nombre_cientifico": "Latenivenatrix mcmasterae",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Troodóntido canadiense de gran tamaño descrito a partir de materiales de Alberta.",
        "longitud": 3.5,
        "peso": 40,
    },
    {
        "nombre": "Mussaurus",
        "nombre_cientifico": "Mussaurus patagonicus",
        "periodo": "Triásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Sauropodomorfo argentino famoso por sus nidadas y el cambio de postura con la edad.",
        "longitud": 6.0,
        "peso": 250,
    },
    {
        "nombre": "Nigersaurus",
        "nombre_cientifico": "Nigersaurus taqueti",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Rebaquisáurido africano de hocico ancho con cientos de dientes de reemplazo.",
        "longitud": 9.0,
        "peso": 4000,
    },
    {
        "nombre": "Ouranosaurus",
        "nombre_cientifico": "Ouranosaurus nigeriensis",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Ornitópodo africano con altas espinas dorsales que formaban una vela o joroba.",
        "longitud": 7.0,
        "peso": 2000,
    },
    {
        "nombre": "Rajasaurus",
        "nombre_cientifico": "Rajasaurus narmadensis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido indio con un prominente cuerno frontal.",
        "longitud": 7.0,
        "peso": 1200,
    },
    {
        "nombre": "Saltasaurus",
        "nombre_cientifico": "Saltasaurus loricatus",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio argentino relativamente pequeño y cubierto por osteodermos dérmicos.",
        "longitud": 12.5,
        "peso": 7000,
    },
    {
        "nombre": "Torvosaurus",
        "nombre_cientifico": "Torvosaurus tanneri",
        "periodo": "Jurásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Gran megalosáurido depredador de la Formación Morrison y de Portugal.",
        "longitud": 10.0,
        "peso": 2000,
    },
    {
        "nombre": "Zuniceratops",
        "nombre_cientifico": "Zuniceratops christopheri",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ceratopsio temprano del suroeste de Estados Unidos, intermedio en la evolución del grupo.",
        "longitud": 3.5,
        "peso": 300,
    },
    {
        "nombre": "Abelisaurus",
        "nombre_cientifico": "Abelisaurus comahuensis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido argentino que dio nombre a todo su grupo de depredadores sudamericanos.",
        "longitud": 8.5,
        "peso": 1800,
    },
    {
        "nombre": "Aerotitan",
        "nombre_cientifico": "Aerotitan sudamericanus",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Gran azdárquido sudamericano relacionado con los mayores reptiles voladores conocidos.",
        "longitud": 4.5,
        "peso": 40,
    },
    {
        "nombre": "Andesaurus",
        "nombre_cientifico": "Andesaurus delgadoi",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosauriforme argentino entre los saurópodos tempranos del grupo en Sudamérica.",
        "longitud": 15.0,
        "peso": 12000,
    },
    {
        "nombre": "Aratasaurus",
        "nombre_cientifico": "Aratasaurus museunacionali",
        "periodo": "Cretácico Inferior",
        "dieta": "Carnívoro",
        "descripcion": "Pequeño celurosaurio brasileño descrito a partir de un esqueleto parcial bien conservado.",
        "longitud": 3.0,
        "peso": 35,
    },
    {
        "nombre": "Barrosasaurus",
        "nombre_cientifico": "Barrosasaurus casamiquelai",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio patagónico de cuello largo descubierto en Neuquén.",
        "longitud": 18.0,
        "peso": 16000,
    },
    {
        "nombre": "Buriolestes",
        "nombre_cientifico": "Buriolestes schultzi",
        "periodo": "Triásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Dinosaurio brasileño muy temprano que ayuda a entender el origen de los saurópodomorfos.",
        "longitud": 1.8,
        "peso": 8,
    },
    {
        "nombre": "Chilesaurus",
        "nombre_cientifico": "Chilesaurus diegosuarezi",
        "periodo": "Jurásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Dinosaurio chileno de anatomía insólita que combina rasgos de varios grupos.",
        "longitud": 3.2,
        "peso": 120,
    },
    {
        "nombre": "Ekrixinatosaurus",
        "nombre_cientifico": "Ekrixinatosaurus novasi",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido argentino robusto, uno de los depredadores más grandes del grupo.",
        "longitud": 8.0,
        "peso": 1500,
    },
    {
        "nombre": "Futalognkosaurus",
        "nombre_cientifico": "Futalognkosaurus dukei",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio gigante de Argentina preservado junto a una fauna patagónica excepcional.",
        "longitud": 26.0,
        "peso": 50000,
    },
    {
        "nombre": "Gondwanatitan",
        "nombre_cientifico": "Gondwanatitan faustoi",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio brasileño del Grupo Bauru, representativo del interior de Gondwana.",
        "longitud": 14.0,
        "peso": 9000,
    },
    {
        "nombre": "Kurupi",
        "nombre_cientifico": "Kurupi itaata",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido paraguayo descrito a partir de vértebras y cadera de la Formación Presidente Hayes.",
        "longitud": 7.0,
        "peso": 1000,
    },
    {
        "nombre": "Lapampasaurus",
        "nombre_cientifico": "Lapampasaurus cholinoi",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Anquilosaurio sudamericano conocido por restos hallados en Patagonia argentina.",
        "longitud": 4.0,
        "peso": 600,
    },
    {
        "nombre": "Limaysaurus",
        "nombre_cientifico": "Limaysaurus tessonei",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Rebaquisáurido argentino de cuello largo y espinas neurales desarrolladas.",
        "longitud": 15.0,
        "peso": 7000,
    },
    {
        "nombre": "Megaraptor",
        "nombre_cientifico": "Megaraptor namunhuaiquii",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Gran depredador patagónico famoso por sus enormes garras manuales.",
        "longitud": 8.0,
        "peso": 1000,
    },
    {
        "nombre": "Notocolossus",
        "nombre_cientifico": "Notocolossus gonzalezparejasi",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio gigante argentino conocido por sus enormes extremidades y pies.",
        "longitud": 25.0,
        "peso": 45000,
    },
    {
        "nombre": "Oxalestes",
        "nombre_cientifico": "Oxalestes grandis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo brasileño poco conocido procedente del nordeste de Brasil.",
        "longitud": 4.0,
        "peso": 200,
    },
    {
        "nombre": "Padillasaurus",
        "nombre_cientifico": "Padillasaurus leivaensis",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo colombiano que amplía el registro de gigantes cretácicos en el norte de Sudamérica.",
        "longitud": 16.0,
        "peso": 12000,
    },
    {
        "nombre": "Perijasaurus",
        "nombre_cientifico": "Perijasaurus lapaz",
        "periodo": "Jurásico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodomorfo venezolano entre los dinosaurios jurásicos más importantes del norte de Sudamérica.",
        "longitud": 8.0,
        "peso": 1500,
    },
    {
        "nombre": "Thanos",
        "nombre_cientifico": "Thanos simonattoi",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido brasileño de tamaño mediano descrito en el estado de Sao Paulo.",
        "longitud": 5.5,
        "peso": 600,
    },
    {
        "nombre": "Yamanasaurus",
        "nombre_cientifico": "Yamanasaurus lojaensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio ecuatoriano que representa a los saurópodos tardíos de los Andes.",
        "longitud": 12.0,
        "peso": 6000,
    },
    {
        "nombre": "Aeolosaurus",
        "nombre_cientifico": "Aeolosaurus rionegrinus",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio argentino de cola alargada y muy representativo de la Patagonia tardía.",
        "longitud": 14.0,
        "peso": 10000,
    },
    {
        "nombre": "Agustinia",
        "nombre_cientifico": "Agustinia ligabuei",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo argentino famoso por sus espinas y placas dérmicas poco comunes.",
        "longitud": 16.0,
        "peso": 9000,
    },
    {
        "nombre": "Ahshislepelta",
        "nombre_cientifico": "Ahshislepelta minor",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Anquilosaurio mexicano hallado en sedimentos del norte del país.",
        "longitud": 3.5,
        "peso": 500,
    },
    {
        "nombre": "Alvarezsaurus",
        "nombre_cientifico": "Alvarezsaurus calvoi",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Pequeño terópodo argentino que dio nombre a los alvarezsáuridos.",
        "longitud": 2.0,
        "peso": 15,
    },
    {
        "nombre": "Anabisetia",
        "nombre_cientifico": "Anabisetia saldiviai",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ornitópodo argentino ligero y ágil procedente de la Patagonia.",
        "longitud": 2.0,
        "peso": 25,
    },
    {
        "nombre": "Aonikenk",
        "nombre_cientifico": "Aonikenk patagonicus",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Gran terópodo argentino emparentado con los carcarodontosáuridos.",
        "longitud": 7.0,
        "peso": 1200,
    },
    {
        "nombre": "Arackar",
        "nombre_cientifico": "Arackar licanantay",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio chileno descubierto en el desierto de Atacama.",
        "longitud": 6.5,
        "peso": 1000,
    },
    {
        "nombre": "Atacamatitan",
        "nombre_cientifico": "Atacamatitan chilensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo chileno del norte del país, conocido por restos vertebrales.",
        "longitud": 8.0,
        "peso": 2500,
    },
    {
        "nombre": "Bagualia",
        "nombre_cientifico": "Bagualia alba",
        "periodo": "Jurásico Temprano",
        "dieta": "Herbívoro",
        "descripcion": "Saurópodo temprano argentino clave para comprender el origen de los gigantes de cuello largo.",
        "longitud": 12.0,
        "peso": 4000,
    },
    {
        "nombre": "Bicentenaria",
        "nombre_cientifico": "Bicentenaria argentina",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Pequeño celurosaurio argentino conocido por varios individuos de distintas edades.",
        "longitud": 2.5,
        "peso": 40,
    },
    {
        "nombre": "Bonapartenykus",
        "nombre_cientifico": "Bonapartenykus ultimus",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Alvarezsáurido argentino del final del Cretácico de Patagonia.",
        "longitud": 2.2,
        "peso": 18,
    },
    {
        "nombre": "Bonapartesaurus",
        "nombre_cientifico": "Bonapartesaurus rionegrensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Hadrosaurio argentino descubierto en la provincia de Río Negro.",
        "longitud": 8.0,
        "peso": 2500,
    },
    {
        "nombre": "Bravasaurus",
        "nombre_cientifico": "Bravasaurus arrierosorum",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Pequeño titanosaurio argentino procedente del noroeste del país.",
        "longitud": 7.0,
        "peso": 1800,
    },
    {
        "nombre": "Brasilotitan",
        "nombre_cientifico": "Brasilotitan nemophagus",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio brasileño hallado en el interior de Sao Paulo.",
        "longitud": 12.0,
        "peso": 7000,
    },
    {
        "nombre": "Coahuilaceratops",
        "nombre_cientifico": "Coahuilaceratops magnacuerna",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Gran ceratopsio mexicano con cuernos supraorbitales especialmente largos.",
        "longitud": 6.0,
        "peso": 3000,
    },
    {
        "nombre": "Comahuesaurus",
        "nombre_cientifico": "Comahuesaurus windhauseni",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Rebaquisáurido argentino de Patagonia asociado a ambientes fluviales.",
        "longitud": 13.0,
        "peso": 6000,
    },
    {
        "nombre": "Drusilasaura",
        "nombre_cientifico": "Drusilasaura deseadensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosauriforme argentino de gran tamaño recuperado en Santa Cruz.",
        "longitud": 18.0,
        "peso": 14000,
    },
    {
        "nombre": "Eoabelisaurus",
        "nombre_cientifico": "Eoabelisaurus mefi",
        "periodo": "Jurásico Medio",
        "dieta": "Carnívoro",
        "descripcion": "Abelisauroide temprano de Argentina, importante para la historia evolutiva del grupo.",
        "longitud": 6.5,
        "peso": 700,
    },
    {
        "nombre": "Gasparinisaura",
        "nombre_cientifico": "Gasparinisaura cincosaltensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Pequeño ornitópodo argentino muy ágil, conocido por varios esqueletos parciales.",
        "longitud": 1.7,
        "peso": 13,
    },
    {
        "nombre": "Guaibasaurus",
        "nombre_cientifico": "Guaibasaurus candelariensis",
        "periodo": "Triásico Superior",
        "dieta": "Omnívoro",
        "descripcion": "Dinosaurio brasileño temprano que aporta datos sobre los primeros saurísquios.",
        "longitud": 1.8,
        "peso": 18,
    },
    {
        "nombre": "Ilokelesia",
        "nombre_cientifico": "Ilokelesia aguadagrandensis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido argentino del Cenomaniano-Turoniano patagónico.",
        "longitud": 5.0,
        "peso": 500,
    },
    {
        "nombre": "Ingentia",
        "nombre_cientifico": "Ingentia prima",
        "periodo": "Triásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Enorme sauropodomorfo argentino que anticipa el gigantismo de los saurópodos.",
        "longitud": 10.0,
        "peso": 10000,
    },
    {
        "nombre": "Isasicursor",
        "nombre_cientifico": "Isasicursor santacrucensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ornitópodo argentino pequeño del Maastrichtiense de Patagonia.",
        "longitud": 1.5,
        "peso": 10,
    },
    {
        "nombre": "Katepensaurus",
        "nombre_cientifico": "Katepensaurus goicoecheai",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Rebaquisáurido argentino de la provincia de Chubut.",
        "longitud": 14.0,
        "peso": 6500,
    },
    {
        "nombre": "Lavocatisaurus",
        "nombre_cientifico": "Lavocatisaurus agrioensis",
        "periodo": "Cretácico Inferior",
        "dieta": "Herbívoro",
        "descripcion": "Dicraeosáurido argentino relativamente pequeño hallado en la Formación Agrio.",
        "longitud": 12.0,
        "peso": 4500,
    },
    {
        "nombre": "Leonerasaurus",
        "nombre_cientifico": "Leonerasaurus taquetrensis",
        "periodo": "Jurásico Temprano",
        "dieta": "Herbívoro",
        "descripcion": "Sauropodomorfo argentino que muestra una transición anatómica hacia los saurópodos.",
        "longitud": 3.0,
        "peso": 35,
    },
    {
        "nombre": "Macrogryphosaurus",
        "nombre_cientifico": "Macrogryphosaurus gondwanicus",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ornitópodo argentino de cuello relativamente largo para su grupo.",
        "longitud": 6.0,
        "peso": 900,
    },
    {
        "nombre": "Maxakalisaurus",
        "nombre_cientifico": "Maxakalisaurus topai",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio brasileño descrito a partir de un esqueleto relativamente completo.",
        "longitud": 13.0,
        "peso": 9000,
    },
    {
        "nombre": "Mendozasaurus",
        "nombre_cientifico": "Mendozasaurus neguyelap",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Gran titanosaurio argentino emparentado con Futalognkosaurus.",
        "longitud": 22.0,
        "peso": 30000,
    },
    {
        "nombre": "Narambuenatitan",
        "nombre_cientifico": "Narambuenatitan palomoi",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio argentino de Patagonia austral descubierto en Santa Cruz.",
        "longitud": 12.0,
        "peso": 7000,
    },
    {
        "nombre": "Neuquensaurus",
        "nombre_cientifico": "Neuquensaurus australis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Pequeño titanosaurio acorazado del final del Cretácico argentino.",
        "longitud": 10.0,
        "peso": 5000,
    },
    {
        "nombre": "Noasaurus",
        "nombre_cientifico": "Noasaurus leali",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Pequeño terópodo argentino que dio nombre a los noasáuridos.",
        "longitud": 3.0,
        "peso": 30,
    },
    {
        "nombre": "Overoraptor",
        "nombre_cientifico": "Overoraptor chimentoi",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Paraviano argentino con mezcla de rasgos de aves tempranas y dromeosáuridos.",
        "longitud": 1.5,
        "peso": 5,
    },
    {
        "nombre": "Panamericansaurus",
        "nombre_cientifico": "Panamericansaurus schroederi",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio argentino hallado en sedimentos del norte de Patagonia.",
        "longitud": 11.0,
        "peso": 6000,
    },
    {
        "nombre": "Patagonykus",
        "nombre_cientifico": "Patagonykus puertai",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Alvarezsáurido argentino de patas largas y brazos muy reducidos.",
        "longitud": 2.0,
        "peso": 12,
    },
    {
        "nombre": "Patagotitan",
        "nombre_cientifico": "Patagotitan mayorum",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Titanosaurio gigante argentino entre los animales terrestres más grandes conocidos.",
        "longitud": 31.0,
        "peso": 57000,
    },
    {
        "nombre": "Piatnitzkysaurus",
        "nombre_cientifico": "Piatnitzkysaurus floresi",
        "periodo": "Jurásico Medio",
        "dieta": "Carnívoro",
        "descripcion": "Terópodo argentino clásico del Jurásico de Patagonia.",
        "longitud": 4.5,
        "peso": 350,
    },
    {
        "nombre": "Pycnonemosaurus",
        "nombre_cientifico": "Pycnonemosaurus nevesi",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido brasileño de gran tamaño procedente de Mato Grosso.",
        "longitud": 8.5,
        "peso": 1700,
    },
    {
        "nombre": "Riojasaurus",
        "nombre_cientifico": "Riojasaurus incertus",
        "periodo": "Triásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Sauropodomorfo argentino temprano conocido por esqueletos bastante completos.",
        "longitud": 8.0,
        "peso": 1000,
    },
    {
        "nombre": "Sacisaurus",
        "nombre_cientifico": "Sacisaurus agudoensis",
        "periodo": "Triásico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Pequeño silesáurido brasileño cercano a los orígenes de los dinosauriformes.",
        "longitud": 1.5,
        "peso": 10,
    },
    {
        "nombre": "Sanjuansaurus",
        "nombre_cientifico": "Sanjuansaurus gordilloi",
        "periodo": "Triásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Herrerasáurido argentino del famoso yacimiento de Ischigualasto.",
        "longitud": 3.0,
        "peso": 45,
    },
    {
        "nombre": "Skorpiovenator",
        "nombre_cientifico": "Skorpiovenator bustingorryi",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Abelisáurido argentino muy bien preservado de la Formación Huincul.",
        "longitud": 6.0,
        "peso": 600,
    },
    {
        "nombre": "Stegouros",
        "nombre_cientifico": "Stegouros elengassen",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Dinosaurio acorazado chileno con una cola armada inusual en forma de macuahuitl.",
        "longitud": 2.0,
        "peso": 150,
    },
    {
        "nombre": "Talenkauen",
        "nombre_cientifico": "Talenkauen santacrucensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Ornitópodo argentino mediano del sur de Patagonia.",
        "longitud": 4.0,
        "peso": 300,
    },
    {
        "nombre": "Teyuwasu",
        "nombre_cientifico": "Teyuwasu barberenai",
        "periodo": "Triásico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Dinosauriforme brasileño muy temprano del sur del país.",
        "longitud": 2.5,
        "peso": 30,
    },
    {
        "nombre": "Tlatolophus",
        "nombre_cientifico": "Tlatolophus galorum",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Hadrosaurio mexicano con una cresta alta y alargada.",
        "longitud": 8.0,
        "peso": 2500,
    },
    {
        "nombre": "Tototlmimus",
        "nombre_cientifico": "Tototlmimus packardensis",
        "periodo": "Cretácico Superior",
        "dieta": "Omnívoro",
        "descripcion": "Ornitomímido mexicano ligero y cursorial del norte del país.",
        "longitud": 4.0,
        "peso": 150,
    },
    {
        "nombre": "Unenlagia",
        "nombre_cientifico": "Unenlagia comahuensis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Paraviano argentino estrechamente relacionado con la evolución de las aves.",
        "longitud": 2.0,
        "peso": 20,
    },
    {
        "nombre": "Velafrons",
        "nombre_cientifico": "Velafrons coahuilensis",
        "periodo": "Cretácico Superior",
        "dieta": "Herbívoro",
        "descripcion": "Hadrosaurio crestado mexicano descubierto en Coahuila.",
        "longitud": 7.0,
        "peso": 2200,
    },
    {
        "nombre": "Vespersaurus",
        "nombre_cientifico": "Vespersaurus paranaensis",
        "periodo": "Cretácico Superior",
        "dieta": "Carnívoro",
        "descripcion": "Noasáurido brasileño adaptado a desplazarse sobre un pie muy especializado.",
        "longitud": 1.5,
        "peso": 8,
    },
]


REGISTROS_FOSILES_EJEMPLO = {
    "Tiranosaurio Rex": [
        {"pais": "usa", "latitud": 47.0, "longitud": -106.0, "formacion": "Hell Creek", "edad_ma": "68-66"},
        {"pais": "canada", "latitud": 49.6, "longitud": -112.8, "formacion": "Frenchman", "edad_ma": "68-66"},
    ],
    "Triceratops": [
        {"pais": "usa", "latitud": 45.0, "longitud": -103.0, "formacion": "Hell Creek", "edad_ma": "68-66"},
    ],
    "Velociraptor": [
        {"pais": "mongolia", "latitud": 43.5, "longitud": 104.2, "formacion": "Djadochta", "edad_ma": "75-71"},
    ],
    "Brachiosaurio": [
        {"pais": "usa", "latitud": 39.3, "longitud": -108.5, "formacion": "Morrison", "edad_ma": "154-150"},
    ],
    "Estegosaurio": [
        {"pais": "usa", "latitud": 40.4, "longitud": -105.6, "formacion": "Morrison", "edad_ma": "155-150"},
        {"pais": "portugal", "latitud": 39.6, "longitud": -9.0, "formacion": "Lourinha", "edad_ma": "152-145"},
    ],
    "Espinosaurio": [
        {"pais": "egipto", "latitud": 25.0, "longitud": 32.5, "formacion": "Bahariya", "edad_ma": "100-94"},
        {"pais": "marruecos", "latitud": 31.9, "longitud": -4.4, "formacion": "Kem Kem", "edad_ma": "100-94"},
    ],
    "Diplodocus": [
        {"pais": "usa", "latitud": 39.1, "longitud": -110.2, "formacion": "Morrison", "edad_ma": "154-152"},
    ],
    "Anquilosaurio": [
        {"pais": "canada", "latitud": 51.0, "longitud": -112.8, "formacion": "Scollard", "edad_ma": "68-66"},
    ],
    "Parasaurolofo": [
        {"pais": "canada", "latitud": 50.9, "longitud": -111.5, "formacion": "Dinosaur Park", "edad_ma": "76-74"},
        {"pais": "usa", "latitud": 36.1, "longitud": -107.9, "formacion": "Kirtland", "edad_ma": "76-73"},
    ],
    "Allosaurus": [
        {"pais": "usa", "latitud": 39.4, "longitud": -110.7, "formacion": "Morrison", "edad_ma": "155-145"},
    ],
    "Carnotaurus": [
        {"pais": "argentina", "latitud": -49.3, "longitud": -67.7, "formacion": "La Colonia", "edad_ma": "72-69"},
    ],
    "Iguanodon": [
        {"pais": "reino unido", "latitud": 50.7, "longitud": -1.1, "formacion": "Wealden", "edad_ma": "140-125"},
        {"pais": "alemania", "latitud": 52.1, "longitud": 8.6, "formacion": "Berriasian beds", "edad_ma": "145-140"},
    ],
    "Giganotosaurus": [
        {"pais": "argentina", "latitud": -38.7, "longitud": -68.1, "formacion": "Candeleros", "edad_ma": "99-97"},
    ],
    "Argentinosaurus": [
        {"pais": "argentina", "latitud": -38.6, "longitud": -68.5, "formacion": "Huincul", "edad_ma": "99-94"},
    ],
    "Microraptor": [
        {"pais": "china", "latitud": 41.0, "longitud": 120.5, "formacion": "Jiufotang", "edad_ma": "125-120"},
    ],
    "Dilophosaurus": [
        {"pais": "usa", "latitud": 36.4, "longitud": -110.8, "formacion": "Kayenta", "edad_ma": "196-183"},
    ],
    "Protoceratops": [
        {"pais": "mongolia", "latitud": 43.8, "longitud": 103.5, "formacion": "Djadochta", "edad_ma": "75-71"},
    ],
    "Concavenator": [
        {"pais": "españa", "latitud": 39.9, "longitud": -2.0, "formacion": "Las Hoyas", "edad_ma": "130-125"},
    ],
    "Labocania": [
        {"pais": "mexico", "latitud": 30.5, "longitud": -115.1, "formacion": "La Bocana Roja", "edad_ma": "73-72"},
    ],
    "Oxalaia": [
        {"pais": "brasil", "latitud": -2.5, "longitud": -44.3, "formacion": "Alcantara", "edad_ma": "100-94"},
    ],
    "Leaellynasaura": [
        {"pais": "australia", "latitud": -38.6, "longitud": 145.7, "formacion": "Wonthaggi", "edad_ma": "118-110"},
    ],
    "Arcovenator": [
        {"pais": "francia", "latitud": 43.4, "longitud": 6.3, "formacion": "Argiles rouges", "edad_ma": "72-70"},
    ],
    "Amargasaurus": [
        {"pais": "argentina", "latitud": -39.0, "longitud": -70.2, "formacion": "La Amarga", "edad_ma": "129-122"},
    ],
    "Acrocanthosaurus": [
        {"pais": "usa", "latitud": 32.7, "longitud": -94.7, "formacion": "Twin Mountains", "edad_ma": "113-110"},
    ],
    "Australovenator": [
        {"pais": "australia", "latitud": -22.3, "longitud": 143.1, "formacion": "Winton", "edad_ma": "98-95"},
    ],
    "Aucasaurus": [
        {"pais": "argentina", "latitud": -39.6, "longitud": -68.9, "formacion": "Anacleto", "edad_ma": "83-80"},
    ],
    "Bajadasaurus": [
        {"pais": "argentina", "latitud": -38.4, "longitud": -69.2, "formacion": "Bajada Colorada", "edad_ma": "140-134"},
    ],
    "Dreadnoughtus": [
        {"pais": "argentina", "latitud": -50.1, "longitud": -72.0, "formacion": "Cerro Fortaleza", "edad_ma": "77-75"},
    ],
    "Europasaurus": [
        {"pais": "alemania", "latitud": 52.0, "longitud": 10.6, "formacion": "Langenberg", "edad_ma": "154-151"},
    ],
    "Eustreptospondylus": [
        {"pais": "reino unido", "latitud": 51.8, "longitud": -1.3, "formacion": "Oxford Clay", "edad_ma": "166-164"},
    ],
    "Gasosaurus": [
        {"pais": "china", "latitud": 29.5, "longitud": 104.8, "formacion": "Shaximiao", "edad_ma": "168-161"},
    ],
    "Herrerasaurus": [
        {"pais": "argentina", "latitud": -30.0, "longitud": -68.2, "formacion": "Ischigualasto", "edad_ma": "231-229"},
    ],
    "Irritator": [
        {"pais": "brasil", "latitud": -7.2, "longitud": -39.7, "formacion": "Romualdo", "edad_ma": "113-110"},
    ],
    "Kentrosaurus": [
        {"pais": "tanzania", "latitud": -6.8, "longitud": 35.5, "formacion": "Tendaguru", "edad_ma": "154-150"},
    ],
    "Lusotitan": [
        {"pais": "portugal", "latitud": 39.3, "longitud": -9.3, "formacion": "Lourinha", "edad_ma": "152-145"},
    ],
    "Mamenchisaurus": [
        {"pais": "china", "latitud": 30.8, "longitud": 104.6, "formacion": "Shaximiao", "edad_ma": "162-159"},
    ],
    "Mapusaurus": [
        {"pais": "argentina", "latitud": -38.3, "longitud": -68.8, "formacion": "Huincul", "edad_ma": "97-93"},
    ],
    "Massospondylus": [
        {"pais": "sudafrica", "latitud": -30.6, "longitud": 25.0, "formacion": "Elliot", "edad_ma": "201-183"},
    ],
    "Megalosaurus": [
        {"pais": "reino unido", "latitud": 51.7, "longitud": -1.2, "formacion": "Taynton Limestone", "edad_ma": "168-166"},
    ],
    "Minmi": [
        {"pais": "australia", "latitud": -27.2, "longitud": 151.5, "formacion": "Allaru", "edad_ma": "112-105"},
    ],
    "Neovenator": [
        {"pais": "reino unido", "latitud": 50.7, "longitud": -1.1, "formacion": "Wessex", "edad_ma": "125-121"},
    ],
    "Shunosaurus": [
        {"pais": "china", "latitud": 29.9, "longitud": 104.5, "formacion": "Xiashaximiao", "edad_ma": "170-160"},
    ],
    "Tarbosaurus": [
        {"pais": "mongolia", "latitud": 43.6, "longitud": 101.9, "formacion": "Nemegt", "edad_ma": "70-66"},
    ],
    "Adasaurus": [
        {"pais": "mongolia", "latitud": 43.5, "longitud": 101.5, "formacion": "Nemegt", "edad_ma": "70-68"},
    ],
    "Agujaceratops": [
        {"pais": "usa", "latitud": 29.6, "longitud": -103.2, "formacion": "Aguja", "edad_ma": "80-77"},
    ],
    "Ampelosaurus": [
        {"pais": "francia", "latitud": 43.1, "longitud": 2.7, "formacion": "Marnes rouges inferieures", "edad_ma": "71-66"},
    ],
    "Bonitasaura": [
        {"pais": "argentina", "latitud": -39.2, "longitud": -68.4, "formacion": "Bajo de la Carpa", "edad_ma": "84-80"},
    ],
    "Camarasaurus": [
        {"pais": "usa", "latitud": 39.2, "longitud": -109.9, "formacion": "Morrison", "edad_ma": "155-145"},
    ],
    "Chialingosaurus": [
        {"pais": "china", "latitud": 29.3, "longitud": 104.2, "formacion": "Shaximiao", "edad_ma": "161-159"},
    ],
    "Chuandongocoelurus": [
        {"pais": "china", "latitud": 29.8, "longitud": 105.0, "formacion": "Xiashaximiao", "edad_ma": "170-168"},
    ],
    "Draconyx": [
        {"pais": "portugal", "latitud": 39.2, "longitud": -9.3, "formacion": "Lourinha", "edad_ma": "152-145"},
    ],
    "Gargoyleosaurus": [
        {"pais": "usa", "latitud": 44.6, "longitud": -106.8, "formacion": "Morrison", "edad_ma": "155-150"},
    ],
    "Huayangosaurus": [
        {"pais": "china", "latitud": 30.1, "longitud": 104.7, "formacion": "Lower Shaximiao", "edad_ma": "168-161"},
    ],
    "Lourinhanosaurus": [
        {"pais": "portugal", "latitud": 39.3, "longitud": -9.3, "formacion": "Lourinha", "edad_ma": "152-145"},
    ],
    "Mononykus": [
        {"pais": "mongolia", "latitud": 43.7, "longitud": 102.0, "formacion": "Nemegt", "edad_ma": "70-68"},
    ],
    "Overosaurus": [
        {"pais": "argentina", "latitud": -39.5, "longitud": -68.6, "formacion": "Allen", "edad_ma": "80-75"},
    ],
    "Pelecanimimus": [
        {"pais": "españa", "latitud": 39.9, "longitud": -2.0, "formacion": "Las Hoyas", "edad_ma": "130-125"},
    ],
    "Qiaowanlong": [
        {"pais": "china", "latitud": 40.6, "longitud": 95.4, "formacion": "Xinminbao", "edad_ma": "113-110"},
    ],
    "Rinconsaurus": [
        {"pais": "argentina", "latitud": -39.3, "longitud": -68.7, "formacion": "Bajo de la Carpa", "edad_ma": "84-80"},
    ],
    "Sinraptor": [
        {"pais": "china", "latitud": 44.8, "longitud": 88.1, "formacion": "Shishugou", "edad_ma": "161-156"},
    ],
    "Sonorasaurus": [
        {"pais": "usa", "latitud": 31.7, "longitud": -110.5, "formacion": "Turney Ranch", "edad_ma": "112-100"},
    ],
    "Turiasaurus": [
        {"pais": "españa", "latitud": 40.2, "longitud": -0.2, "formacion": "Villar del Arzobispo", "edad_ma": "150-145"},
    ],
    "Xiongguanlong": [
        {"pais": "china", "latitud": 39.8, "longitud": 98.2, "formacion": "Xinminbao", "edad_ma": "125-100"},
    ],
    "Achelousaurus": [
        {"pais": "usa", "latitud": 47.6, "longitud": -109.8, "formacion": "Two Medicine", "edad_ma": "74-72"},
    ],
    "Alamosaurus": [
        {"pais": "usa", "latitud": 31.2, "longitud": -104.7, "formacion": "Javelina", "edad_ma": "70-66"},
    ],
    "Buitreraptor": [
        {"pais": "argentina", "latitud": -40.1, "longitud": -66.1, "formacion": "Candeleros", "edad_ma": "99-97"},
    ],
    "Chasmosaurus": [
        {"pais": "canada", "latitud": 50.8, "longitud": -111.6, "formacion": "Dinosaur Park", "edad_ma": "77-75"},
    ],
    "Dicraeosaurus": [
        {"pais": "tanzania", "latitud": -10.0, "longitud": 39.0, "formacion": "Tendaguru", "edad_ma": "154-150"},
    ],
    "Dracorex": [
        {"pais": "usa", "latitud": 44.5, "longitud": -103.6, "formacion": "Hell Creek", "edad_ma": "68-66"},
    ],
    "Einiosaurus": [
        {"pais": "usa", "latitud": 47.4, "longitud": -109.4, "formacion": "Two Medicine", "edad_ma": "75-74"},
    ],
    "Fukuiraptor": [
        {"pais": "japon", "latitud": 36.1, "longitud": 136.5, "formacion": "Kitadani", "edad_ma": "127-115"},
    ],
    "Gallimimus": [
        {"pais": "mongolia", "latitud": 43.7, "longitud": 101.8, "formacion": "Nemegt", "edad_ma": "70-66"},
    ],
    "Hypsilophodon": [
        {"pais": "reino unido", "latitud": 50.7, "longitud": -1.2, "formacion": "Wessex", "edad_ma": "130-125"},
    ],
    "Jobaria": [
        {"pais": "niger", "latitud": 17.1, "longitud": 9.3, "formacion": "Tiouraren", "edad_ma": "170-160"},
    ],
    "Kaatedocus": [
        {"pais": "usa", "latitud": 44.5, "longitud": -106.7, "formacion": "Morrison", "edad_ma": "155-150"},
    ],
    "Latenivenatrix": [
        {"pais": "canada", "latitud": 50.9, "longitud": -111.5, "formacion": "Dinosaur Park", "edad_ma": "76-75"},
    ],
    "Mussaurus": [
        {"pais": "argentina", "latitud": -51.2, "longitud": -72.4, "formacion": "Laguna Colorada", "edad_ma": "215-203"},
    ],
    "Nigersaurus": [
        {"pais": "niger", "latitud": 18.0, "longitud": 8.8, "formacion": "Elrhaz", "edad_ma": "115-105"},
    ],
    "Ouranosaurus": [
        {"pais": "niger", "latitud": 18.2, "longitud": 8.7, "formacion": "Elrhaz", "edad_ma": "125-112"},
    ],
    "Rajasaurus": [
        {"pais": "india", "latitud": 22.7, "longitud": 72.7, "formacion": "Lameta", "edad_ma": "68-66"},
    ],
    "Saltasaurus": [
        {"pais": "argentina", "latitud": -24.8, "longitud": -65.4, "formacion": "Lecho", "edad_ma": "73-70"},
    ],
    "Torvosaurus": [
        {"pais": "portugal", "latitud": 39.3, "longitud": -9.3, "formacion": "Lourinha", "edad_ma": "152-145"},
        {"pais": "usa", "latitud": 39.6, "longitud": -110.4, "formacion": "Morrison", "edad_ma": "154-148"},
    ],
    "Zuniceratops": [
        {"pais": "usa", "latitud": 35.1, "longitud": -108.3, "formacion": "Moreno Hill", "edad_ma": "93-89"},
    ],
    "Abelisaurus": [
        {"pais": "argentina", "latitud": -39.1, "longitud": -68.7, "formacion": "Allen", "edad_ma": "80-70"},
    ],
    "Aerotitan": [
        {"pais": "argentina", "latitud": -50.0, "longitud": -72.1, "formacion": "Allen", "edad_ma": "83-66"},
    ],
    "Andesaurus": [
        {"pais": "argentina", "latitud": -38.8, "longitud": -68.4, "formacion": "Candeleros", "edad_ma": "100-96"},
    ],
    "Aratasaurus": [
        {"pais": "brasil", "latitud": -7.4, "longitud": -39.3, "formacion": "Romualdo", "edad_ma": "110-100"},
    ],
    "Barrosasaurus": [
        {"pais": "argentina", "latitud": -39.4, "longitud": -68.8, "formacion": "Anacleto", "edad_ma": "83-80"},
    ],
    "Buriolestes": [
        {"pais": "brasil", "latitud": -29.7, "longitud": -53.7, "formacion": "Santa Maria", "edad_ma": "233-228"},
    ],
    "Chilesaurus": [
        {"pais": "chile", "latitud": -46.6, "longitud": -72.6, "formacion": "Toqui", "edad_ma": "148-145"},
    ],
    "Ekrixinatosaurus": [
        {"pais": "argentina", "latitud": -38.2, "longitud": -69.1, "formacion": "Candeleros", "edad_ma": "100-97"},
    ],
    "Futalognkosaurus": [
        {"pais": "argentina", "latitud": -38.7, "longitud": -68.2, "formacion": "Portezuelo", "edad_ma": "87-84"},
    ],
    "Gondwanatitan": [
        {"pais": "brasil", "latitud": -20.1, "longitud": -48.7, "formacion": "Adamantina", "edad_ma": "90-83"},
    ],
    "Kurupi": [
        {"pais": "paraguay", "latitud": -23.0, "longitud": -58.2, "formacion": "Presidente Hayes", "edad_ma": "86-84"},
    ],
    "Lapampasaurus": [
        {"pais": "argentina", "latitud": -37.4, "longitud": -64.3, "formacion": "Allen", "edad_ma": "80-70"},
    ],
    "Limaysaurus": [
        {"pais": "argentina", "latitud": -38.5, "longitud": -68.9, "formacion": "Candeleros", "edad_ma": "100-97"},
    ],
    "Megaraptor": [
        {"pais": "argentina", "latitud": -38.6, "longitud": -68.6, "formacion": "Portezuelo", "edad_ma": "90-88"},
    ],
    "Notocolossus": [
        {"pais": "argentina", "latitud": -35.2, "longitud": -69.1, "formacion": "Plottier", "edad_ma": "86-84"},
    ],
    "Oxalestes": [
        {"pais": "brasil", "latitud": -2.6, "longitud": -44.2, "formacion": "Alcantara", "edad_ma": "95-93"},
    ],
    "Padillasaurus": [
        {"pais": "colombia", "latitud": 5.6, "longitud": -73.5, "formacion": "Paja", "edad_ma": "130-120"},
    ],
    "Perijasaurus": [
        {"pais": "venezuela", "latitud": 10.1, "longitud": -72.9, "formacion": "La Quinta", "edad_ma": "200-175"},
    ],
    "Thanos": [
        {"pais": "brasil", "latitud": -20.5, "longitud": -49.3, "formacion": "Sao Jose do Rio Preto", "edad_ma": "87-70"},
    ],
    "Yamanasaurus": [
        {"pais": "ecuador", "latitud": -3.9, "longitud": -79.2, "formacion": "Yamana", "edad_ma": "84-66"},
    ],
    "Aeolosaurus": [
        {"pais": "argentina", "latitud": -39.0, "longitud": -64.5, "formacion": "Allen", "edad_ma": "80-70"},
    ],
    "Agustinia": [
        {"pais": "argentina", "latitud": -39.2, "longitud": -70.1, "formacion": "Lohan Cura", "edad_ma": "116-108"},
    ],
    "Ahshislepelta": [
        {"pais": "mexico", "latitud": 26.9, "longitud": -102.1, "formacion": "Aguja", "edad_ma": "80-73"},
    ],
    "Alvarezsaurus": [
        {"pais": "argentina", "latitud": -39.5, "longitud": -68.7, "formacion": "Bajo de la Carpa", "edad_ma": "86-83"},
    ],
    "Anabisetia": [
        {"pais": "argentina", "latitud": -38.8, "longitud": -69.4, "formacion": "Candeleros", "edad_ma": "99-97"},
    ],
    "Aonikenk": [
        {"pais": "argentina", "latitud": -50.4, "longitud": -72.3, "formacion": "Mata Amarilla", "edad_ma": "96-90"},
    ],
    "Arackar": [
        {"pais": "chile", "latitud": -25.5, "longitud": -69.1, "formacion": "Hornitos", "edad_ma": "80-66"},
    ],
    "Atacamatitan": [
        {"pais": "chile", "latitud": -26.0, "longitud": -70.2, "formacion": "Tolar", "edad_ma": "80-70"},
    ],
    "Bagualia": [
        {"pais": "argentina", "latitud": -43.6, "longitud": -69.0, "formacion": "Canadon Asfalto", "edad_ma": "179-171"},
    ],
    "Bicentenaria": [
        {"pais": "argentina", "latitud": -38.5, "longitud": -68.9, "formacion": "Candeleros", "edad_ma": "99-97"},
    ],
    "Bonapartenykus": [
        {"pais": "argentina", "latitud": -39.3, "longitud": -68.8, "formacion": "Allen", "edad_ma": "80-70"},
    ],
    "Bonapartesaurus": [
        {"pais": "argentina", "latitud": -39.2, "longitud": -64.6, "formacion": "Allen", "edad_ma": "80-70"},
    ],
    "Bravasaurus": [
        {"pais": "argentina", "latitud": -28.7, "longitud": -67.0, "formacion": "Ciénaga del Río Huaco", "edad_ma": "75-70"},
    ],
    "Brasilotitan": [
        {"pais": "brasil", "latitud": -21.1, "longitud": -48.5, "formacion": "Adamantina", "edad_ma": "90-80"},
    ],
    "Coahuilaceratops": [
        {"pais": "mexico", "latitud": 28.6, "longitud": -102.4, "formacion": "Cerro del Pueblo", "edad_ma": "73-72"},
    ],
    "Comahuesaurus": [
        {"pais": "argentina", "latitud": -39.4, "longitud": -69.3, "formacion": "Lohan Cura", "edad_ma": "112-108"},
    ],
    "Drusilasaura": [
        {"pais": "argentina", "latitud": -47.0, "longitud": -68.7, "formacion": "Bajo Barreal", "edad_ma": "95-90"},
    ],
    "Eoabelisaurus": [
        {"pais": "argentina", "latitud": -43.7, "longitud": -69.2, "formacion": "Canadon Asfalto", "edad_ma": "170-165"},
    ],
    "Gasparinisaura": [
        {"pais": "argentina", "latitud": -38.8, "longitud": -68.9, "formacion": "Anacleto", "edad_ma": "83-80"},
    ],
    "Guaibasaurus": [
        {"pais": "brasil", "latitud": -29.8, "longitud": -53.8, "formacion": "Caturrita", "edad_ma": "225-220"},
    ],
    "Ilokelesia": [
        {"pais": "argentina", "latitud": -38.6, "longitud": -68.8, "formacion": "Huincul", "edad_ma": "97-93"},
    ],
    "Ingentia": [
        {"pais": "argentina", "latitud": -30.4, "longitud": -68.5, "formacion": "Quebrada del Barro", "edad_ma": "210-205"},
    ],
    "Isasicursor": [
        {"pais": "argentina", "latitud": -49.8, "longitud": -68.4, "formacion": "Chorrillo", "edad_ma": "72-66"},
    ],
    "Katepensaurus": [
        {"pais": "argentina", "latitud": -44.0, "longitud": -67.5, "formacion": "Bajo Barreal", "edad_ma": "95-90"},
    ],
    "Lavocatisaurus": [
        {"pais": "argentina", "latitud": -38.7, "longitud": -70.0, "formacion": "Agrio", "edad_ma": "130-121"},
    ],
    "Leonerasaurus": [
        {"pais": "argentina", "latitud": -43.3, "longitud": -69.5, "formacion": "Las Leoneras", "edad_ma": "190-180"},
    ],
    "Macrogryphosaurus": [
        {"pais": "argentina", "latitud": -39.4, "longitud": -69.0, "formacion": "Sierra Barrosa", "edad_ma": "90-88"},
    ],
    "Maxakalisaurus": [
        {"pais": "brasil", "latitud": -16.9, "longitud": -42.0, "formacion": "Adamantina", "edad_ma": "90-80"},
    ],
    "Mendozasaurus": [
        {"pais": "argentina", "latitud": -35.0, "longitud": -69.3, "formacion": "Plottier", "edad_ma": "86-84"},
    ],
    "Narambuenatitan": [
        {"pais": "argentina", "latitud": -47.7, "longitud": -69.1, "formacion": "Anita", "edad_ma": "75-72"},
    ],
    "Neuquensaurus": [
        {"pais": "argentina", "latitud": -39.1, "longitud": -68.8, "formacion": "Anacleto", "edad_ma": "83-80"},
    ],
    "Noasaurus": [
        {"pais": "argentina", "latitud": -25.0, "longitud": -65.5, "formacion": "Lecho", "edad_ma": "73-70"},
    ],
    "Overoraptor": [
        {"pais": "argentina", "latitud": -39.2, "longitud": -68.6, "formacion": "Huincul", "edad_ma": "97-93"},
    ],
    "Panamericansaurus": [
        {"pais": "argentina", "latitud": -39.4, "longitud": -68.5, "formacion": "Allen", "edad_ma": "80-70"},
    ],
    "Patagonykus": [
        {"pais": "argentina", "latitud": -39.0, "longitud": -68.4, "formacion": "Portezuelo", "edad_ma": "90-88"},
    ],
    "Patagotitan": [
        {"pais": "argentina", "latitud": -43.5, "longitud": -69.3, "formacion": "Cerro Barcino", "edad_ma": "101-99"},
    ],
    "Piatnitzkysaurus": [
        {"pais": "argentina", "latitud": -43.8, "longitud": -69.4, "formacion": "Canadon Asfalto", "edad_ma": "168-166"},
    ],
    "Pycnonemosaurus": [
        {"pais": "brasil", "latitud": -15.5, "longitud": -56.1, "formacion": "Cambambe", "edad_ma": "90-84"},
    ],
    "Riojasaurus": [
        {"pais": "argentina", "latitud": -30.5, "longitud": -68.3, "formacion": "Los Colorados", "edad_ma": "227-213"},
    ],
    "Sacisaurus": [
        {"pais": "brasil", "latitud": -29.5, "longitud": -53.4, "formacion": "Caturrita", "edad_ma": "225-220"},
    ],
    "Sanjuansaurus": [
        {"pais": "argentina", "latitud": -29.9, "longitud": -68.1, "formacion": "Ischigualasto", "edad_ma": "231-229"},
    ],
    "Skorpiovenator": [
        {"pais": "argentina", "latitud": -38.7, "longitud": -68.3, "formacion": "Huincul", "edad_ma": "97-93"},
    ],
    "Stegouros": [
        {"pais": "chile", "latitud": -48.6, "longitud": -72.0, "formacion": "Dorotea", "edad_ma": "74-71"},
    ],
    "Talenkauen": [
        {"pais": "argentina", "latitud": -49.6, "longitud": -71.8, "formacion": "Pari Aike", "edad_ma": "80-75"},
    ],
    "Teyuwasu": [
        {"pais": "brasil", "latitud": -29.7, "longitud": -53.6, "formacion": "Caturrita", "edad_ma": "225-220"},
    ],
    "Tlatolophus": [
        {"pais": "mexico", "latitud": 28.7, "longitud": -102.2, "formacion": "Cerro del Pueblo", "edad_ma": "73-72"},
    ],
    "Tototlmimus": [
        {"pais": "mexico", "latitud": 29.0, "longitud": -102.6, "formacion": "Javelina equivalent beds", "edad_ma": "72-69"},
    ],
    "Unenlagia": [
        {"pais": "argentina", "latitud": -38.9, "longitud": -68.7, "formacion": "Portezuelo", "edad_ma": "90-88"},
    ],
    "Velafrons": [
        {"pais": "mexico", "latitud": 28.5, "longitud": -102.0, "formacion": "Cerro del Pueblo", "edad_ma": "73-72"},
    ],
    "Vespersaurus": [
        {"pais": "brasil", "latitud": -23.4, "longitud": -51.9, "formacion": "Goio Ere", "edad_ma": "90-85"},
    ],
}


def upsert_dinosaurios(db):
    print("\n📝 Sincronizando dinosaurios con imágenes...")
    for data in DINOSAURIOS_EJEMPLO:
        payload = dict(data)
        payload["imagen_url"] = build_placeholder_url(data["nombre"])

        existing = db.query(Dinosaurio).filter(
            Dinosaurio.nombre == payload["nombre"]
        ).first()

        if existing:
            existing.nombre_cientifico = payload["nombre_cientifico"]
            existing.periodo = payload["periodo"]
            existing.dieta = payload["dieta"]
            existing.descripcion = payload["descripcion"]
            existing.longitud = payload["longitud"]
            existing.peso = payload["peso"]
            existing.imagen_url = payload["imagen_url"]
            print(f"  ♻️ Actualizado: {existing.nombre}")
            continue

        db.add(Dinosaurio(**payload))
        print(f"  ✅ Agregado: {payload['nombre']}")

    db.commit()


def upsert_registros_fosiles(db):
    print("\n🌍 Sincronizando registros fósiles...")
    dinosaurios_db = {d.nombre: d for d in db.query(Dinosaurio).all()}

    for nombre_dino, registros in REGISTROS_FOSILES_EJEMPLO.items():
        dinosaurio = dinosaurios_db.get(nombre_dino)
        if not dinosaurio:
            continue

        for registro_data in registros:
            existe = db.query(RegistroFosil).filter(
                RegistroFosil.dinosaurio_id == dinosaurio.id,
                RegistroFosil.pais == registro_data["pais"],
                RegistroFosil.formacion == registro_data["formacion"]
            ).first()

            if existe:
                existe.latitud = registro_data["latitud"]
                existe.longitud = registro_data["longitud"]
                existe.edad_ma = registro_data["edad_ma"]
                existe.descripcion = f"Registro fósil de {nombre_dino} en la formación {registro_data['formacion']}"
                print(f"  ♻️ Actualizado registro: {nombre_dino} en {registro_data['pais']}")
                continue

            db.add(RegistroFosil(
                dinosaurio_id=dinosaurio.id,
                pais=registro_data["pais"],
                latitud=registro_data["latitud"],
                longitud=registro_data["longitud"],
                formacion=registro_data["formacion"],
                edad_ma=registro_data["edad_ma"],
                descripcion=f"Registro fósil de {nombre_dino} en la formación {registro_data['formacion']}"
            ))
            print(f"  ✅ Registro fósil agregado: {nombre_dino} en {registro_data['pais']}")

    db.commit()


def populate_dinosaurs():
    print("🦕 Conectando a la base de datos...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        upsert_dinosaurios(db)
        upsert_registros_fosiles(db)
        total = db.query(Dinosaurio).count()
        print(f"\n🎉 Total de dinosaurios en la base de datos: {total}")
    finally:
        db.close()


if __name__ == "__main__":
    populate_dinosaurs()
