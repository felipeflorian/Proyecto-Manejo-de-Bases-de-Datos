import psycopg2
import folium

#Parametros para la conexion
hostname = 'drona.db.elephantsql.com'
username = 'kopfshah'
password = 'jdOtVcae5OU8yNxMldLT3iVW3TdllYaX'
database = 'kopfshah'

datos_camara = []

#vamos a intentar hacer la conexión usando un bloque try catch:
DBConnection = None
try:
  # conectar usando el método connect de pyscopg2
  print('Connecting to the PostgreSQL database...')
  DBConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

  # crear un cursor para ejecutar comandos dentro de la DB
  cursorDB = DBConnection.cursor()
  cursorDB = DBConnection.cursor()
  query = "select * from camara"
  busqueda = cursorDB.execute(query)
  datos_camara = cursorDB.fetchall()
  #almacenar en la variable resultado todo el contenido del query
  DBConnection.commit();
  # cerrar la conexión a la base de datos
  DBConnection.close()
#si hay un error en la conexión informar
except (Exception, psycopg2.DatabaseError) as error:
        print('Error encontrado:',error)
#si algo no ha sido cubierto en los casos anteriores, cerrar la conexión a la base de datos
finally:
  if DBConnection is not None:
    DBConnection.close()
    print('en caso finally: cerrando la conexión a la DB.')
