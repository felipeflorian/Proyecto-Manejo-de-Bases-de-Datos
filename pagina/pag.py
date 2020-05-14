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


def cambioEstado(est, pla):

    if est == "SI":

        try:
          # conectar usando el método connect de pyscopg2
          print('Connecting to the PostgreSQL database...')
          DBConnection = psycopg2.connect(**parametrosDict)

          # crear un cursor para ejecutar comandos dentro de la D
          cursorDB = DBConnection.cursor()
          query = "CALL pago('" + pla + "');"
          plac = "'" + pla  + "'"
          #cursorDB.callproc('pago', (plac,))
          cursorDB.execute(query)

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
        return "Estado nuevo de la placa: " + pla + "pagado."

    else:
        return "No hay cambios en el estado para la placa " + pla + "."

@app.route('/',methods=['GET'])
def paginaInicial():
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
    return app.send_static_file("busquedaPorFechaDepartamento.html")

@app.route('/multasPorFechaDep', methods = ['GET','POST'])
def multasPorFecha():
    dep = request.values.get("Departamento")
    f1 = request.values.get("f1")
    f2 = request.values.get("f2")
    query = "SELECT * FROM numeroMultasTiempo_departamento('" + f1 + "','" + f2 + "','" + dep + "')"
    contenido = queryComoDataFrame(query)
    return "<p>" + contenido.to_html() + "</p>"

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

@app.route('/MultasMenores18', methods = ['GET'])
def multas_menores():
    query = "SELECT * FROM multasMenoresDe('18')"
    contenido = queryComoDataFrame(query)
    return "<p>" + contenido.to_html() + "</p>"

@app.route('/MultasMayores60', methods = ['GET'])
def multas_mayores():
    query = "SELECT * FROM multasMayoresDe('60')"
    contenido = queryComoDataFrame(query)
    return "<p>" + contenido.to_html() + "</p>"

@app.route('/actualizacionMultas', methods = ['GET'])
def actualizacion_multas():
    return app.send_static_file('actualizacionMultas.html')

@app.route('/estadoMulta', methods = ['GET','POST'])
def nuevo_estado_multa():
    placa = request.values.get("placa")
    print("placa")
    valor = request.values.get("estado")
    valor = valor.upper()
    if valor == 'SI':
        return cambioEstado(valor,placa)
    else:
        return "No se realizaron cambios de estado a la placa " + placa + "."


if __name__ == "__main__":
    app.run()
