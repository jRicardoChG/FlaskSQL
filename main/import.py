import os
import csv

from flask              import Flask, session,render_template,request
from flask_sqlalchemy   import SQLAlchemy
from sqlalchemy         import create_engine
from sqlalchemy.orm     import scoped_session, sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ricardo:Theendworld1220@localhost:5432/proyect1edx'
engine = create_engine('postgresql://ricardo:Theendworld1220@localhost:5432/proyect1edx')
db = scoped_session(sessionmaker(bind=engine))

query = db.execute("SELECT * FROM usuarios").fetchall()

print(query)
variable = []

with open('books.csv') as csvfile:
   archivocsv = csv.reader(csvfile, delimiter=',')
   for row in archivocsv:
       variable[len(variable):] = [row]       

db.execute("INSERT INTO libros (isbn,titulo,autor,years) VALUES {}")