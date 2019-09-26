# funciones apra mantner codigo limpio

from sqlalchemy         import create_engine, exc
from sqlalchemy.orm     import scoped_session, sessionmaker 

engine = create_engine('postgres://gpoyfyitqdntzv:67f826c7ba2729a8f8e0b73ff6280b0332dff516d589a4d064426a0484fff1c2@ec2-54-83-55-125.compute-1.amazonaws.com:5432/d9p3vo3kqndk4i')
#engine = create_engine('postgresql://ricardo:Theendworld1220@localhost:5432/miprimeradb')
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
        # print(consulta)
        if consulta==[]:
            return "Noexiste"
        if verPass!=consulta[0][3]:
            return "malaPass"
        else:
            return consulta

# crear consulta con filtros por parte del usuario
def realBusqueda(ISBN,titulo,Autor):
    if ISBN==None or ISBN=="":
        ISBN = ""
        andISBN = ""
    else:
        andISBN = "and isbn like "    
        ISBN = list(ISBN.lower())
        while ISBN != None and ISBN!=[]:
            if ISBN[0]==" ":
                ISBN.pop(0)
            else:
                break
        ISBN = "'%"+"".join(ISBN)+"%'"

    if titulo==None or titulo=="":
        titulo = ""
        andTitulo = ""
    else:
        andTitulo = "and titulo like "    
        titulo = list(titulo.lower())
        while (titulo!=None and titulo!=[]):
            if titulo[0]==" ":
                titulo.pop(0)
            else:
                break
        titulo = "'%"+"".join(titulo)+"%'"

    if Autor==None or Autor=="":
        Autor = ""
        andTitulo = "titulo like "
        if titulo =="":
            andISBN = "isbn like "
            andTitulo = ""
        if ISBN =="":
            andISBN = ""
    else:
        Autor = list(Autor.lower())
        while Autor!=None and Autor!=[]:
            if Autor[0]==" ":
                Autor.pop(0)
            else:
                break
        Autor = "autor like "+"'%"+"".join(Autor)+"%'"

    if((titulo==[]or titulo=="") and (Autor=="" or Autor==[]) and (ISBN =="" or ISBN==[])):
        return "no_hay_consulta"
    else:
        consultaUser = db.execute("select * from libros where "+Autor+andTitulo+titulo+andISBN+ISBN+" limit 30;").fetchall()
        print("asi quedo la consulta:","select * from libros where "+Autor+andTitulo+titulo+andISBN+ISBN)
        for i in range(0,len(consultaUser)):
            consultaUser[i]=list(consultaUser[i])
            consultaUser[i][2]=consultaUser[i][2].capitalize()
            consultaUser[i][3] = consultaUser[i][3].split(" ")
            for j in range(0,len(consultaUser[i][3])):
                consultaUser[i][3][j] = consultaUser[i][3][j].capitalize()
            consultaUser[i][3] = " ".join(consultaUser[i][3])
        return consultaUser

# registrar la review del usuario con method post 
def registrarReview(idUsuario,idLibro,estrellas,review):
    db.execute("INSERT INTO reviews (id_usuario,id_libro,review,estrellas) VALUES (:idusuario,:idlibro,:review,:estrellas);",{"idusuario":idUsuario,"idlibro":idLibro,"review":review,"estrellas":estrellas})
    db.commit()
    print("herecibido para registrar:",idUsuario,idLibro,estrellas,review)

# realizar Querys de Reviews 
def queryReviews(libro):
    libro=list(libro)
    print(libro)
    for i in range(0,len(libro)):
        if libro[i] == "'":
            libro[i] = "''"
    libro2 = "".join(libro)
    query = db.execute("SELECT reviews.review,reviews.estrellas,usuarios.usuario,reviews.id_usuario,reviews.id_libro FROM reviews JOIN usuarios ON reviews.id_usuario=usuarios.id_usuario JOIN libros ON libros.id_libro=reviews.id_libro WHERE libros.titulo = "+"'"+libro2+"'").fetchall()
    print("esto fue lo que recibio la query:",libro2)
    return query

def queryPersonal(idUser,titulo):
    titulo=list(titulo)
    print(titulo)
    for i in range(0,len(titulo)):
        if titulo[i] == "'":
            titulo[i] = "''"
    titulo2 = "".join(titulo)
    query = db.execute("SELECT reviews.review,reviews.estrellas,usuarios.usuario,reviews.id_usuario,reviews.id_libro FROM reviews JOIN usuarios ON reviews.id_usuario=usuarios.id_usuario JOIN libros ON libros.id_libro=reviews.id_libro WHERE usuarios.usuario = "+"'"+idUser+"'"+ " and libros.titulo = "+"'"+titulo2+"'").fetchall()
    return query

#borrar review
def borrarReview(idusuario,idlibro):
    db.execute("DELETE from reviews where id_usuario = :id_usuario and id_libro = :id_libro;",{"id_usuario":idusuario,"id_libro":idlibro})
    db.commit()

def queryISBN(isbn):
    query = db.execute("SELECT titulo,autor,years from libros where isbn = :isbn;",{"isbn":isbn}).fetchall()
    return query