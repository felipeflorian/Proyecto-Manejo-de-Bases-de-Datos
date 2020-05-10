import random as rng
import pandas as pd
import psycopg2

def Insert_Multa(edad, pl, fecha, cod, lat, lon):
    instruccion = "insert into Multa(edad, placa, fecha,codigo_multa,latitud,longitud) values('"+ str(edad) + "','" + str(pl) + "','" + str(fecha) + "','" + str(cod) + "','" + str(lat) + "','" + str(lon) + "');"
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

tipo1 = ["C29","D04","C02","D10"]
tipo2 = ["D03","D06","C29"]


multasTipo1 = pd.read_csv('tipo1.csv',sep=';',encoding='latin1')
multasTipo2 = pd.read_csv('tipo2.csv',sep=";",encoding='latin1')


lat_lon1 = []
lat_lon2 = []

for (index, datos) in multasTipo1.iterrows():
        x = datos['Latitud']
        y = datos['Longitud']
        if count(x)==True:
            x = quitar(x)
        if count(y)==True:
            y = quitar(y)
        l = [x,y]
        lat_lon1.append(l)

for (index, datos) in multasTipo2.iterrows():
            x = datos['Latitud']
            y = datos['Longitud']
            if count(x)==True:
                x = quitar(x)
            if count(y)==True:
                y = quitar(y)
            l = [x,y]
            lat_lon2.append(l)

In_multas = []
letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i in range(200):
    placa = ""
    for i in range(3):
        l1 = rng.randrange(26)
        placa += letras[l1]
    for i in range(3):
        l2 = rng.randrange(0,9)
        placa += str(l2)
    edad = rng.randrange(16,80)
    dia = rng.randrange(30)
    mes = rng.randrange(12)
    a = "2019"
    fecha = str(dia) + "/" + str(mes) + "/" + a
    t1 = rng.choice(tipo1)
    a1 = rng.randrange(0,len(lat_lon1))
    a2 = rng.randrange(0,len(lat_lon2))
    f1 = lat_lon1[a1]
    f2 = lat_lon2[a2]
    in1 = Insert_Multa(edad, placa, fecha,t1,f1[0],f1[1])
    In_multas.append(in1)


for i in range(200):
    placa = ""
    for i in range(3):
        l1 = rng.randrange(26)
        placa += letras[l1]
    for i in range(3):
        l2 = rng.randrange(0,9)
        placa += str(l2)
    edad = rng.randrange(16,80)
    dia = rng.randrange(30)
    mes = rng.randrange(12)
    fech =   str(mes) + "/" + str(dia) + "/" + "2019"
    t2 = rng.choice(tipo2)
    a1 = rng.randrange(1,len(lat_lon1))
    a2 = rng.randrange(1,len(lat_lon2))
    f1 = lat_lon1[a1]
    f2 = lat_lon2[a2]
    in1 = Insert_Multa(edad, placa, fech,t2,f1[0],f1[1])
    In_multas.append(in1)



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
  for i in In_multas:
      cursorDB.execute(i)

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
