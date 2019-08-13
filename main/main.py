#Para que funcione hay que:
#instalalr postgresql
#se crea el usuario postgres en el Os linux
#si se desea usar otro usuario par laa base de datos, este debe ser un usuario nativo linux
# se necesita logearse con con el usuario posrtgres al sistema operativ
# sudo -i -u postgres
# desde aca se peuden ya crear ususarios y tablas, para entrar a postgres se usa el comnado psql
# se crea la tabla en psql 
# deben estar isntaladas todas las librerias aca mencionadas
# psycopg2 debe instlaalrse asi: sudo pip install psycopg2-binary
# ya se puede usar la base de datos unida a flask
# Good Reads key
# key: O3iEdmNy0enR3tZi4CmjQ
# secret: SYGiLDMUmFWVtVyhSpqU5b7CYnOPzCHzHhAOGjW7w


import requests
import os
import json

from funciones          import primera,admBD
from flask              import Flask, session,render_template,request
from flask_session      import Session
from flask_sqlalchemy   import SQLAlchemy
from sqlalchemy         import create_engine
from sqlalchemy.orm     import scoped_session, sessionmaker

# Check for environment variable

# if not os.getenv('postgresql://ricardo:Theendworld1220@localhost:5432/var/run/postgres/miprimeradb.db'):

# peticion a URL goodReads tomo un unico valor de la peticion
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "O3iEdmNy0enR3tZi4CmjQ", "isbns": "0380795272"})
res2 = res.json()
print(res2['books'][0]['average_rating'])

# configurar la base de datos, hago conexion con base de datos en posgres con usuario ricardo y mi app flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ricardo:Theendworld1220@localhost:5432/miprimeradb'
engine = create_engine('postgresql://ricardo:Theendworld1220@localhost:5432/miprimeradb')
db = scoped_session(sessionmaker(bind=engine))

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#empieza codigo de mi backend
query = db.execute('SELECT id,name,lastname FROM idusuario').fetchall()
for valores in query:
    print("hola id: ",valores.id,"name: ",valores.name,"lastname: ",valores.lastname)

objeto = primera("hola","mundo")
# pagina principal de la aplciacion actual
@app.route('/',methods=['GET'])
def index():
    return render_template("index.html",variablehtml=objeto.funcion1())

# realizo un get con un formuario con method get y obtengo el parametro d ela peticion 
@app.route("/landing",methods=["GET"])
def landing():
    variable1 = request.args.get("texto1")
    return render_template("index.html",variablehtml=objeto.funcion1(),resultadohtml=variable1)

# mi app responde segun lo que escribe el usuario en la URL y muestro lo que escribio en el DOM
@app.route("/<string:name>")
def isbn(name):
    variable2 = name
    return render_template("index.html",variablehtml=objeto.funcion1(),resultadohtml2=variable2)

# realizo un post con los datos del usuario y los muestro en el DOM
@app.route("/logueado",methods=["POST"])
def logueado():
    session["datosUser"]=None
    if session.get("datosUser")==None:
        session["datosUser"]=[]
    if request.method == "POST":
        var1 = request.form.get("usuarioid")
        var2 = request.form.get("passworduser")
        session["datosUser"][len(session["datosUser"]):]=[var1]
        session["datosUser"][len(session["datosUser"]):]=[var2]
    print(session["datosUser"])
    return render_template("index.html",passwordhtml=session["datosUser"][1],userhtml=session["datosUser"][0])

