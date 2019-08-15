####################################SETUP################################################
import requests
import os
import json

from funciones          import primera,admBD
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
userid = ""
passworduser = ""
##################################################################################################

@app.route("/Home.html",methods=["GET"])
def home():
    return render_template("Home.html")

@app.route("/Login.html",methods=["GET"])
def login():
    return render_template("Login.html")

@app.route("/Foro.html",methods=["GET"])
def foro():
    return render_template("Foro.html")

@app.route("/Noticias.html",methods=["GET"])
def noticias():
    return render_template("Noticias.html")

@app.route("/Landing.html",methods=["POST"])
def landing():
    if request.method == "POST":
        userid = request.form.get("usuarioid")
        passworduser = request.form.get("passworduser")
    return render_template("Landing.html",userHtml=userid,passwordUserHtml=passworduser)

##################################################################################################

# if __name__ == '__main__':
#     app.run(port=8080, debug=True)