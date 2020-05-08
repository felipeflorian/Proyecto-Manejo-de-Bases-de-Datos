import pandas as pd
import psycopg2
#geopandas

#Funciones para la insercion de los datos
def Insert_Equipo(tip, lat, lon, dir, dep, mun):
    instruccion = "insert into Equipo(tipo_equipo,latitud,longitud,direccion,departamento,municipio) values('" + str(tip) + "','" + str(lat) + "','" + str(lon) + "','" + str(dir) + "','" + str(dep) + "','" + str(mun) + "');"
    return instruccion

def Insert_tipoMulta(cod,tip):
    instruccion = "insert into tipoMulta values('" + str(cod) + "','" + str(tip) +"');"
    return instruccion

def Insert_Multa(cod, lat, lon):
    instruccion = "insert into Multa values('" + str(cod) + "','" + str(lat) + "','" + str(lon) + "');"
    return instruccion

#Se cargan los archivos con la información de las camaras de fotomultas.
data_set = pd.read_csv('Equipos_de_Fotodeteccion.csv',sep=';',encoding='latin1').fillna('-')
multas = pd.read_csv('tipoMultas.csv',sep=';', encoding='latin1')

Multa = []
tipoMulta = []
Equipo = []

for (index, datos) in data_set.iterrows():
    Equipo.append(Insert_Equipo(datos['Tipo Equipo'],datos['Latitud'],datos['Longitud'],datos['Direccion'],datos['Departamento'],datos['Municipio']))

for (index, datos) in multas.iterrows():
    tipoMulta.append(Insert_tipoMulta(datos['Codigo'],datos['Descripcion']))

#Parametros para la conexion
hostname = 'drona.db.elephantsql.com'
username = 'kopfshah'
password = 'jdOtVcae5OU8yNxMldLT3iVW3TdllYaX'
database = 'kopfshah'

#vamos a intentar hacer la conexión usando un bloque try catch:
DBConnection = None
try:
  # conectar usando el método connect de pyscopg2
  print('Connecting to the PostgreSQL database...')
  DBConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

  # crear un cursor para ejecutar comandos dentro de la DB
  cursorDB = DBConnection.cursor()

	# ejecutar un comando SQL en la base de datos
  for i in range(len(Equipo)):
      cursorDB.execute(Equipo[i])

  for j in range(len(tipoMulta)):
      cursorDB.execute(tipoMulta[j])

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
