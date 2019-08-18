# funciones apra mantner codigo limpio

from sqlalchemy         import create_engine, exc
from sqlalchemy.orm     import scoped_session, sessionmaker 

engine = create_engine('postgresql://ricardo:Theendworld1220@localhost:5432/miprimeradb')
db = scoped_session(sessionmaker(bind=engine))

#registrar usuario
def registrar(nombre,email,contra):
    try:
        db.execute("INSERT INTO usuarios (usuario,email,passwords) VALUES (:nom,:em,:pass);",{"nom":nombre,"em":email,"pass":contra})
        db.commit()
        print("usuario registrado saltisfactoriamente")
    except exc.SQLAlchemyError as e:
        if "psycopg2.errors.UniqueViolation" in str(e):
            return "yaexiste"

#verificar si usuario existe y contraseña correcta
def verificar(nomEmal,verPass):
        consulta = db.execute("SELECT * FROM usuarios WHERE usuario=:esto;",{"esto":nomEmal}).fetchall()
        print(consulta)
        if consulta==[]:
            return "Noexiste"
        if verPass!=consulta[0][3]:
            return "malaPass"