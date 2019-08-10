#Para que funcione hay que:
#instalalr postgresql
#se crea el usuario postgres en el Os linux
#si se desea usar otro usuario par laa base de datos, este debe ser un usuario nativo linux
# se necesita logearse con con el usuario posrtgres al sistema operativ
# sudo -i -u postgres
# desde aca se peuden ya crear ususarios y tablas, para entrar a postgres se usa el comnado psql
# se crea la tabla en psql 
# deben estar isntaladas todas las lirberias aca mensionadas
# psycopg2 debe instlaalrse asi: sudo pip install psycopg2-binary
# ya se puede usar la base de datos unida a flask

import os

from funciones      import primera,admBD
from flask          import Flask, session,render_template
from flask_session  import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy     import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable

# if not os.getenv('postgresql://ricardo:Theendworld1220@localhost:5432/var/run/postgres/miprimeradb.db'):


# Configure session to use filesystem
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

# configurar la base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ricardo:Theendworld1220@localhost:5432/miprimeradb'
engine = create_engine('postgresql://ricardo:Theendworld1220@localhost:5432/miprimeradb')
# Set up database
#db = SQLAlchemy(app)
db = scoped_session(sessionmaker(bind=engine))

#empieza codigo de mi backend
query = db.execute('SELECT id,name,lastname FROM idusuario').fetchall()
for valores in query:
    print("hola id: ",valores.id,"name: ",valores.name,"lastname: ",valores.lastname)

objeto = primera("hola","mundo")

@app.route('/')
def index():
    return render_template("index.html",variablehtml=objeto.funcion1())
