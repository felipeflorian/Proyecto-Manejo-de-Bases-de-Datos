#inclusiones de liberías y demás
import flask #para hacer la API
from flask import Flask,redirect,url_for,request,render_template #especiales para escribir más fácilmente
import pandas as Pandas #para recibir los datos
import psycopg2 #para hacer la conexión a la Base de Datos

#vamos a crear una aplicación servidor en Flask
#vamos a crear una app de prueba que no hace nada
app = flask.Flask(__name__) #la app va tener nombre
app.config["DEBUG"] = True #esta app se puede debuggear


parametrosDict = {
    "host":"drona.db.elephantsql.com",
    "database":"kopfshah",
    "user":"kopfshah",
    "password":"jdOtVcae5OU8yNxMldLT3iVW3TdllYaX"
}


def queryComoDataFrame(Query):
  DBConnection = None #conexion a db
  resultDataFrame = None #dataframe vacio.
  try:

    print('Connecting to the PostgreSQL database...')
    DBConnection = psycopg2.connect(**parametrosDict)
    #se recibe el comando por medio de pandas
    resultDataFrame = Pandas.read_sql_query(Query, DBConnection)
    DBConnection.close()

    return resultDataFrame
  except (Exception, psycopg2.DatabaseError) as error:
    print('Error en el Query:',error)
    return None
  #si algo no ha sido cubierto en los casos anteriores, cerrar la conexión a la base de datos
  finally:
    if DBConnection is not None:
      DBConnection.close()
    print('en caso finally: query ejecutado, resultados en un data frame.')

#---------------------------------------------------------------------------------------------
#métodos para extraer información de la Base de datos
#---------------------------------------------------------------------------------------------
def bitacoraIncidentesLocalidadMesAno(loc,ano,mes):
    query = "SELECT * FROM incidentesMesAnoLocalidad('"+loc+"',"+str(ano)+","+str(mes)+")"
    print(query)
    dataFrameMesLocalidad = queryComoDataFrame(query);
    return dataFrameMesLocalidad
def informacionDelitosMensual(ano):
    query = "SELECT * FROM delitosTipoMesAno("+str(2010)+")"
    dataFrameMeses = queryComoDataFrame(query)
    return dataFrameMeses
