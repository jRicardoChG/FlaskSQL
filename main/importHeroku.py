# import os y csv para modificar archivos de csv y comandos de os
import os
import csv

# todos son necesarios
from sqlalchemy         import create_engine, exc
from sqlalchemy.orm     import scoped_session, sessionmaker

# realizo mi conexion con la base de datos
engine = create_engine('postgres://gpoyfyitqdntzv:67f826c7ba2729a8f8e0b73ff6280b0332dff516d589a4d064426a0484fff1c2@ec2-54-83-55-125.compute-1.amazonaws.com:5432/d9p3vo3kqndk4i',convert_unicode=True)
db= scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))

# creo una varialbe para guardar los valores fuera del archivo csv para no tneer que leerlo siempre
variable = []

# leo el archivo csv y lo guardo en variable
with open('books.csv') as csvfile:
   archivocsv = csv.reader(csvfile, delimiter=',')
   for row in archivocsv:
       variable[len(variable):] = [row]  

#elimino los titilos del archivo dado que los años vienen en str y necesito guardarlos en entero, porque asi diseñe la base de datos
variable.pop(0)
#convierto todos los elementos de la base de datos a minuscula para facilitar su procesamiento

#guardo las filas en la base de datos y guardo todo con db.commit(), si no se hace, no se guardan y quedan en ram

for isbn,title,autor,year in variable:
    title = title.lower()
    autor = autor.lower()
    #db().execute("insert into libros (isbn,titulo,autor,years) VALUES ('1','1','1','1');")
    db().execute("INSERT INTO libros (isbn,titulo,autor,years) VALUES (:isbn,:title,:autor,:year);",{"isbn":isbn,"title":title,"autor":autor,"year":int(year)})
db().commit()
print("todo ha sido insertado correctamente")


