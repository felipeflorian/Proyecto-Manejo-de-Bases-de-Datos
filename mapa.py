import psycopg2
import folium
import pandas as pd


localizaciones = []

#Parametros para la conexion
hostname = 'drona.db.elephantsql.com'
username = 'kopfshah'
password = 'jdOtVcae5OU8yNxMldLT3iVW3TdllYaX'
database = 'kopfshah'

try:
  # conectar usando el método connect de pyscopg2
  print('Connecting to the PostgreSQL database...')
  DBConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

  # crear un cursor para ejecutar comandos dentro de la DB
  cursorDB = DBConnection.cursor()
  query = "select latitud, longitud, direccion from equipo"
  busqueda = cursorDB.execute(query)
  localizaciones = cursorDB.fetchall()
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

m = folium.Map(
    location=[4.570868, -74.2973328]
)

for i in localizaciones:
    lat = i[0]
    lon = i[1]
    dir = i[2]
    folium.Marker([lat,lon],popup=dir).add_to(m)

#folium.Marker([40.965, -5.664], popup='Plaza Mayor', tooltip=tooltip).add_to(m)
m.save("MapaFotoMultas.html")
