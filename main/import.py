# import os y csv para modificar archivos de csv y comandos de os
import os
import csv

# todos son necesarios
from sqlalchemy         import create_engine
from sqlalchemy.orm     import scoped_session, sessionmaker

# realizo mi conexion con la base de datos
engine = create_engine('postgresql://ricardo:Theendworld1220@localhost:5432/miprimeradb')
db = scoped_session(sessionmaker(bind=engine))

# creo una varialbe para guardar los valores fuera del archivo csv para no tneer que leerlo siempre
variable = []
# leo el archivo csv y lo guardo en variable
with open('books.csv') as csvfile:
   archivocsv = csv.reader(csvfile, delimiter=',')
   for row in archivocsv:
       variable[len(variable):] = [row]  
#elimino los titilos del archivo dado que los años vienen en str y necesito guardarlos en entero, porque asi diseñe la base de datos
variable.pop(0)

#guardo las filas en la base de datos y guardo todo con db.commit(), si no se hace, no se guardan y quedan en ram
for isbn,title,autor,year in variable:
    db.execute("INSERT INTO libros (isbn,titulo,autor,years) VALUES (:isbn,:title,:autor,:year);",{"isbn":isbn,"title":title,"autor":autor,"year":int(year)})
db.commit()

