import pandas as pd
import psycopg2

#Funciones para la insercion de los datos
def Insert_Equipo(tip, lat, lon, dir, dep, mun):
    instruccion = "insert into Equipo(tipo_equipo,latitud,longitud,direccion,departamento,municipio) values('" + str(tip) + "','" + str(lat) + "','" + str(lon) + "','" + str(dir) + "','" + str(dep) + "','" + str(mun) + "');"
    return instruccion

def count(l):
    count = 0
    for i in l:
        if i == '.':
            count += 1

    if count == 2:
        return True
    else:
        return False

def quitar(l):
    x = ""
    count = 0
    for i in l:
        if i != '.':
            x += i
        if i == '.':
            count += 1
        if count == 1:
            x += i
    return x


#Se cargan los archivos con la información de las camaras de fotomultas.
data_set = pd.read_csv('Equipos_de_Fotodeteccion.csv',sep=';',encoding='latin1').fillna('-')

Multa = []
tipoMulta = []
Equipo = []

for (index, datos) in data_set.iterrows():
    x = datos['Latitud']
    y = datos['Longitud']
    if count(x)==True:
        x = quitar(x)
    if count(y)==True:
        y = quitar(y)
    Equipo.append(Insert_Equipo(datos['Tipo Equipo'],x,y,datos['Direccion'],datos['Departamento'],datos['Municipio']))

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
