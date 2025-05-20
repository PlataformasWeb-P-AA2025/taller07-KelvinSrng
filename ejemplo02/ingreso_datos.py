from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importamos las clases Club y Jugador
from genera_tablas import Club, Jugador

from configuracion import cadena_base_datos

# Creamos el motor (engine) que se conecta a la base de datos
engine = create_engine(cadena_base_datos)

# Creamos la clase Session que nos permitirá iniciar una sesión
Session = sessionmaker(bind=engine)

# Instanciamos una sesión (es como abrir una conexión a la base de datos)
session = Session()

# Creamos un diccionario para almacenar los clubes
# Esto nos servirá para asignar jugadores a los clubes más adelante
clubes_dict = {}

# Abrimos el archivo de clubes que está en la carpeta 'data'
# Usamos modo lectura ('r') y codificación UTF-8
archivo_clubs = open('data/datos_clubs.txt', 'r', encoding='utf-8')

# Recorremos cada línea del archivo
for linea in archivo_clubs:
    # Quitamos saltos de línea y espacios innecesarios
    # Luego separamos los valores usando el delimitador ';'
    nombre, deporte, fundacion = linea.strip().split(';')
    
    # Creamos un objeto de tipo Club con los datos leídos
    club = Club(nombre=nombre, deporte=deporte, fundacion=int(fundacion))
    
    # Agregamos el club a la sesión para su posterior guardado
    session.add(club)
    
    # Guardamos el club en el diccionario usando su nombre como clave
    clubes_dict[nombre] = club

# Cerramos el archivo de clubes
archivo_clubs.close()

# Guardamos los clubes en la base de datos (se hace antes de agregar jugadores)
session.commit()

# Abrimos el archivo de jugadores
archivo_jugadores = open('data/datos_jugadores.txt', 'r', encoding='utf-8')

# Recorremos cada línea del archivo de jugadores
for linea in archivo_jugadores:
    # Separamos los valores de la línea
    nombre, dorsal, posicion, nombre_club = linea.strip().split(';')
    
    # Creamos un objeto de tipo Jugador con los datos leídos
    # Asociamos el jugador al club correspondiente usando el diccionario
    jugador = Jugador(
        nombre=nombre,
        dorsal=int(dorsal),
        posicion=posicion,
        club=clubes_dict[nombre_club]
    )
    
    # Agregamos el jugador a la sesión
    session.add(jugador)

# Cerramos el archivo de jugadores
archivo_jugadores.close()

# Guardamos todos los jugadores en la base de datos
session.commit()
