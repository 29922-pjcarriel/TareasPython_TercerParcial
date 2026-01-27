# app.py
# Matriculas Vehículos - PARTE II

import base64
import mysql.connector
from flask import Flask, request

from constantes import SERVER, USER, PASS, BD, PORT
from clases.vehiculo import Vehiculo

app = Flask(__name__)

#*******************************************************
def conectar():
    print("\n CONEXION A LA BASE DE DATOS")
    cn = mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        port=PORT
    )
    print("La conexión tuvo éxito .......\n")
    return cn
#**********************************************************

def page(title, body_html):
    # Bootstrap wrapper (solo para que se vea bonito)
    return f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>{title}</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
      <nav class="navbar navbar-dark bg-dark">
        <div class="container">
          <span class="navbar-brand fw-bold">Matriculas Vehículos - PARTE II</span>
        </div>
      </nav>

      {body_html}
    </body>
    </html>
    """

@app.route("/", methods=["GET", "POST"])
def index():
    cn = conectar()
    v = Vehiculo(cn)
    #vehiculo::MetodoEstatico();

    # Codigo necesario para realizar pruebas.
    if "d" in request.args:
        print("\nPETICION GET\n")
        print(dict(request.args))

        # 2.2 DETALLE id
        dato = base64.b64decode(request.args.get("d")).decode("utf-8")
        tmp = dato.split("/")

        print("\nVARIABLE TEMP\n")
        print(tmp)

        op = tmp[0]
        id = int(tmp[1])

        if op == "det":
            html = v.get_detail_vehiculo(id)
        elif op == "act":
            html = v.get_form(id)
        elif op == "new":
            html = v.get_form()
        elif op == "del":
            html = v.delete_vehiculo(id)  # BORRAR TODOS LOS REGISTROS DE LA BASE DE DATOS
        else:
            html = "<div class='container my-4 alert alert-danger'>Operación no válida</div>"

        cn.close()
        return page("Vehículo - Parte II", html)

    else:
        if request.method == "POST" and "Guardar" in request.form:
            print("\nPETICION POST ......\n")
            print(dict(request.form))

        # PARTE III
        if request.method == "POST" and "Guardar" in request.form and request.form.get("placa"):
            html = """
            <div class="container my-4">
              <div class="alert alert-info">
                <b>GRABAR VEHICULO - PARTE III</b><br><br>
                (Aquí iría el save_vehiculo() en la Parte III)
              </div>
              <a class="btn btn-outline-secondary" href="index.py">Regresar</a>
            </div>
            """
            # $v->save_vehiculo();
        else:
            html = v.get_list()

        cn.close()
        return page("Vehículo - Parte II", html)

# IMPORTANTE:
# Tu lanzador llama la app como archivo .py, así que debes entrar como:
# /4. vehiculo PARTE II (listar, detalle y borrar)/app.py
