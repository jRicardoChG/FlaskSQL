#######################################SETUP################################################
import requests
import os
import json

from funciones          import registrar,verificar,realBusqueda
from flask              import Flask, session,render_template,request
from flask_session      import Session
from flask_sqlalchemy   import SQLAlchemy
from sqlalchemy         import create_engine
from sqlalchemy.orm     import scoped_session, sessionmaker

# configurar la base de datos, hago conexion con base de datos en posgres con usuario ricardo y mi app flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ricardo:Theendworld1220@localhost:5432/miprimeradb'
engine = create_engine('postgresql://ricardo:Theendworld1220@localhost:5432/miprimeradb')
db = scoped_session(sessionmaker(bind=engine))

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

###########################################APP####################################################
#variablesglobales 

##################################################################################################

@app.route("/Home.html",methods=["GET"])
def home():
    return render_template("Home.html",logueadoHtml=session.get("logueado"),userHtml=session.get("userid"))

@app.route("/Login.html",methods=["GET"])
def login():
    return render_template("Login.html")

@app.route("/Foro.html",methods=["GET"])
def foro():
    return render_template("Foro.html",logueadoHtml=session.get("logueado"),userHtml=session["userid"])

@app.route("/Noticias.html",methods=["GET"])
def noticias():
    return render_template("Noticias.html",logueadoHtml=session.get("logueado"),userHtml=session["userid"])


@app.route("/Registro.html",methods=["GET","POST"])
def registro():
    if request.method == "POST":
        esto = registrar(request.form.get("rNombreUser"),request.form.get("rEmailUser"),request.form.get("rPasswordUser"))
        if esto=="yaexiste":
            return render_template("/Registro.html",errorHtml=esto)
        return render_template("Registrado.html")
    elif request.method == "GET":
        return render_template("Registro.html") 

@app.route("/LogOut.html",methods=["POST"])
def logout():
    if(session.get("logueado")):
        session["userid"]=None
        session["passworduser"]=None
        session["logueado"]=None
    return render_template("LogOut.html")

@app.route("/Landing.html",methods=["GET","POST"])
def landing():
    if request.method == "POST":
        verificado = verificar(request.form.get("usuarioid"),request.form.get("passworduser"))
        if(verificado=="Noexiste" or verificado=="malaPass"):
            return render_template("Login.html",noExisteHtml=verificado)
        else:    
            session["userid"] = request.form.get("usuarioid")
            session["passworduser"] = request.form.get("passworduser")
            session["logueado"]=True
    return render_template("Landing.html",userHtml=session["userid"],passwordUserHtml=session["passworduser"],logueadoHtml=session["logueado"])

@app.route("/ResultadoBusqueda.html",methods=["POST"])
def resultado():
    if request.method=="POST":
        busqueda = realBusqueda(request.form.get("bISBN"),request.form.get("bTitulo"),request.form.get("bAutor"))
    return render_template("ResultadoBusqueda.html",logueadoHtml=session.get("logueado"))
###################################################################################################

