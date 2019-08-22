#######################################SETUP################################################
import requests
import os
import json

from funciones          import queryISBN,registrar,verificar,realBusqueda,registrarReview,queryReviews,borrarReview,queryPersonal
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
Sel={}
##################################################################################################

@app.route("/api/<string:algo>",methods=["GET"])
def Api(algo):
        try:
            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "O3iEdmNy0enR3tZi4CmjQ", "isbns":algo})
            ApiR = res.json()
            print(ApiR)
        except:
            ApiR = {}
            return 404
        try:
            ApiT = queryISBN(algo)
            print(ApiT)
        except:
            return 404
        dic = {}
        dic["titulo"] = ApiT[0]["titulo"]
        dic["autor"] = ApiT[0]["autor"]
        dic["years"] = ApiT[0]["years"]
        dic["isbn"] = ApiR["books"][0]["isbn"]
        dic["reviews_count"] = ApiR["books"][0]["reviews_count"]
        dic["average_rating"] = ApiR["books"][0]["average_rating"]
        return dic
 
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

@app.route("/esto",methods=["GET"])
def seleccion():
    return "hola mundo"
    
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
        for key in session:
            session[key]=None
    return render_template("LogOut.html")

@app.route("/borrarReview.html",methods=["GET","POST"])
def borrar():
    print("llegue aca")
    if request.method == "POST" and session.get("reviews"):
        session["estrellas"]=None
        session["txtreview"]=None
        print("voy a borrar")
        borrarReview(session.get("idIngresado"),session.get("reviews")[0][4])
        print("reviewBorrada")
        session["reviews"]=queryReviews(session.get("titulo").lower())
        session["qPersonal"]=queryPersonal(session.get("userid"),session.get("titulo").lower())
        return render_template("Seleccionado.html",reviewsHtmlpersonal=session.get("qPersonal"),logueadoHtml=session.get("logueado"),ApiHtml=session.get("res2")["books"],selHtml=session,userHtml=session.get("userid"),reviewsHtml=session["reviews"])
    if request.method == "POST" and not session.get("reviews"):
        session["estrellas"]=None
        session["txtreview"]=None
        session["reviews"]=queryReviews(session.get("titulo").lower())
        session["qPersonal"]=queryPersonal(session.get("userid"),session.get("titulo").lower())
        return render_template("Seleccionado.html",reviewsHtmlpersonal=session.get("qPersonal"),logueadoHtml=session.get("logueado"),ApiHtml=session.get("res2")["books"],selHtml=session,userHtml=session.get("userid"),reviewsHtml=session["reviews"])
    if request.method == "GET":
        session["estrellas"]=None
        session["txtreview"]=None
        session["reviews"]=queryReviews(session.get("titulo").lower())
        session["qPersonal"]=queryPersonal(session.get("userid"),session.get("titulo").lower())
        return render_template("Seleccionado.html",reviewsHtmlpersonal=session.get("qPersonal"),logueadoHtml=session.get("logueado"),ApiHtml=session.get("res2")["books"],selHtml=session,userHtml=session.get("userid"),reviewsHtml=session["reviews"])

    
@app.route("/Landing.html",methods=["GET","POST"])
def landing():
    if request.method == "POST":
        verificado = verificar(request.form.get("usuarioid"),request.form.get("passworduser"))
        if(verificado=="Noexiste" or verificado=="malaPass"):
            return render_template("Login.html",noExisteHtml=verificado)
        else:
            session["idIngresado"]= verificado[0][0]   
            session["userid"] = request.form.get("usuarioid")
            session["passworduser"] = request.form.get("passworduser")
            session["logueado"]=True
    return render_template("Landing.html",userHtml=session["userid"],passwordUserHtml=session["passworduser"],logueadoHtml=session["logueado"])

@app.route("/ResultadoBusqueda.html",methods=["POST"])
def resultado():
    if request.method=="POST":
        busqueda = realBusqueda(request.form.get("bISBN"),request.form.get("bTitulo"),request.form.get("bAutor"))    
    return render_template("ResultadoBusqueda.html",logueadoHtml=session.get("logueado"),userHtml=session.get("userid"),consultaUserHtml=busqueda)

@app.route("/Seleccionado.html",methods=["GET","POST"])
def seleccionado():
    if request.method=="GET" and request.args.get("ibsnSel"):
        session["isbn"] = request.args.get("ibsnSel")
        session["titulo"] = request.args.get("tituloSel")
        session["autor"] = request.args.get("autorSel")
        session["anio"] = request.args.get("anioSel")
        session["titulo"]=request.args.get("tituloSel")
        session["idlibro"]=request.args.get("idSel")
        session["estrellas"]=None
        session["txtreview"]=None
        #peticion a URL goodReads tomo un unico valor de la peticion
        try:
            res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "O3iEdmNy0enR3tZi4CmjQ", "isbns":session["isbn"]})
            session["res2"] = res.json()
            print(session["res2"])
        except:
            session["res2"] = {}

    if request.method=="POST" and not session.get("estrellas"):
        if request.form.get("radio")==None or request.form.get("reviewUser")==None:
            reviews=queryReviews(session.get("titulo").lower())
            session["qPersonal"]=queryPersonal(session.get("userid"),session.get("titulo").lower())
            session["reviews"]=reviews
            return render_template("Seleccionado.html",logueadoHtml=session.get("logueado"),ApiHtml=session.get("res2")["books"],userHtml=session.get("userid"),selHtml=session,reviewsHtmlpersonal=session.get("qPersonal"),reviewsHtml=reviews,errorHtmlest=True)
        session["estrellas"]=request.form.get("radio")
        session["txtreview"]=request.form.get("reviewUser")
        registrarReview(session.get("idIngresado"),session.get("idlibro"),session["estrellas"],session["txtreview"])
    reviews=queryReviews(session.get("titulo").lower())
    session["qPersonal"]=queryPersonal(session.get("userid"),session.get("titulo").lower())
    session["reviews"]=reviews
    print("resultaqdo query de reviews: ",reviews)
    return render_template("Seleccionado.html",reviewsHtmlpersonal=session.get("qPersonal"),logueadoHtml=session.get("logueado"),ApiHtml=session.get("res2")["books"],userHtml=session.get("userid"),selHtml=session,reviewsHtml=reviews)

###################################################################################################

