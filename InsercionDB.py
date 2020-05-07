import pandas as pd
import psycopg2

def Insert_solicitante(sol, mun, dep):
    instruccion = "insert into Solicitante values('"  +str(sol)+ "','" + str(mun) + "','" + str(dep) + "');"
    return instruccion

def Insert_solicitud(soli, sol, est, f):
    instruccion = "insert into Solicitud(solicitud,solicitante,estado,fecha) values('"  + str(soli) + "','" + str(sol) + "','" + str(est) + "','" + str(f) + "');"
    return instruccion

def Insert_camara(tip, lat, lon, dir, est, sol):
    instruccion = "insert into Camara(tipo_equipo,latitud,longitud,direccion,estado_solicitud,solicitud) values('" + str(tip) + "','" + str(lat) + "','" + str(lon) + "','" + str(dir) + "','" + str(est) + "','" + str(sol) + "');"
    return instruccion
#Se cargan los archivos con la información de las camaras de fotomultas.
data_set = pd.read_csv('Equipos_de_Fotodeteccion.csv',sep=';',encoding='latin1').fillna('-')

In_solicitante = []
In_solicitud = []
Camara = []
s = []

for (index, datos) in data_set.iterrows():
    in1 = Insert_solicitante(datos['Solicitante'],datos['Municipio'],datos['Departamento'])
    in2 = Insert_solicitud(datos['Solicitud'],datos['Solicitante'],datos['Estado Solicitud'], datos['Fecha Radicado'])
    in3 = Insert_camara(datos['Tipo Equipo'],datos['Latitud'],datos['Longitud'],datos['Direccion'],datos['Estado Ubicacion'],datos['Solicitud'])
    In_solicitante.append(in1)
    In_solicitud.append(in2)
    Camara.append(in3)


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
  for i in range(len(In_solicitud)):
      #cursorDB.execute(In_solicitud[i])
      #cursorDB.execute(In_solicitante[i])
      cursorDB.execute(Camara[i])
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
