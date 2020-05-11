import flask
from flask import Flask, redirect, url_for, request, render_template
import pandas as Pandas
import psycopg2

app = flask.Flask(__name__)
app.config["DEBUG"] = True


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


@app.route('/',methods=['GET'])
def paginaInicial():
    #c= <a href="prueba.html">prueba</a>
    return render_template('hipervinculos.html')

@app.route('/tipoMultas',methods=['GET'])
def tiposDeMultas():
    tipomultas = queryComoDataFrame("SELECT  * from tipomulta")
    contenido = "<h1>Fotomultas</h1>"
    contenido += """<h2>Tipo de multas.
                     </h2>"""
    contenido += "<p>"+tipomultas.to_html()+"</p>"
    return contenido


@app.route('/multasDepartamentoRangoTiempo', methods = ['GET'])
def MultasRangoTiempo():
    return "HOLA"

@app.route('/multasEnElDepartamento', methods = ['GET'])
def Departamento():
    return app.send_static_file('busquedaDepartamento.html')

@app.route('/ResultadosDepartamento', methods = ['GET','POST'])
def resultadosDepartamento():
    valor = request.values.get("Departamento")
    query = "SELECT * FROM multasPorDepartamento('" + valor + "')"
    contenido = queryComoDataFrame(query)
    return "<p>" + contenido.to_html() + "</p>"


@app.route('/multasDepartamento', methods=['GET'])
def multasEnDepartamento():
    #multas = queryComoDataFrame("SELECT * FROM ")
    return render_template('departamento.html')

@app.route('/BusquedaMultas', methods = ['GET'])
def BusquedaMultas():
    return app.send_static_file('busquedaMultas.html')

@app.route('/ResultadoBusqueda', methods = ["POST",'GET'])
def resultado():
    valor = request.values.get("Placa")
    query = "SELECT * FROM busquedaPorPlaca('" + valor + "')"
    contenido = queryComoDataFrame(query)
    return "<p>" + contenido.to_html() + "</p>"

if __name__ == "__main__":
    app.run()
