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

# crear consulta con filtros por parte del usuario
def realBusqueda(ISBN,titulo,Autor):
    limpTitulo = []
    limpISBN = []
    limpAutor = []

    if(ISBN== None or ISBN=="" or ISBN==" "):
        consISBN = ""
        andISBN = ""
    else:
        andISBN = " and "
        consISBN = "isbn like " 
        limpISBN = ISBN.split(" ")
        while limpISBN[0] == "":
            limpISBN.pop(0)
        for i in range(0,len(limpAutor)):
            if(i==0):
                consISBN+="'%"+limpAutor[i]+"%'"
            else:
                consISBN+=" and autor like "+"'%"+limpAutor[i]+"%'"

    
    if(titulo== None or titulo=="" or titulo==" "):
        consTitulo = ""
        andTitulo = ""
        andISBN = ""
    else:
        andTitulo = " and "
        consTitulo = "titulo like " 
        limpTitulo = titulo.split(" ")
        while limpTitulo[0] == "":
            limpTitulo.pop(0)
        for i in range(0,len(limpTitulo)):
            if(i==0):
                consTitulo+="'%"+limpTitulo[i]+"%'"
            else:
                consTitulo+=" and titulo like "+"'%"+limpTitulo[i]+"%'"


    if(Autor== None or Autor=="" or Autor==" "):
        consAutor = ""
        andTitulo = ""
    else:
        consAutor = "autor like " 
        limpAutor = Autor.split(" ")
        while limpAutor[0] == "":
            limpAutor.pop(0)
        for i in range(0,len(limpAutor)):
            if(i==0):
                consAutor+="'%"+limpAutor[i]+"%'"
            else:
                consAutor+=" and autor like "+"'%"+limpAutor[i]+"%'"
    
    consultaUser = db.execute("select * from libros where "+consAutor+andTitulo+consTitulo+andISBN+consISBN).fetchall()
    print("asi quedo la consulta:","select * from libros where "+consAutor+andTitulo+consTitulo+andISBN+consISBN)
    print("RESULTADO:",consultaUser)

