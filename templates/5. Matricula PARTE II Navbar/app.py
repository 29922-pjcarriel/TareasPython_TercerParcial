# app.py
# Matriculas Vehículos - PARTE II (Vehiculo + Matricula)

import base64
import mysql.connector
from flask import Flask, request

from constantes import SERVER, USER, PASS, BD, PORT
from clases.vehiculo import Vehiculo
from clases.matricula import Matricula

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

def page(title, body_html, activo="vehiculo"):
    # Navbar igual a tu imagen: Vehículo / Matrícula
    # activo = "vehiculo" o "matricula"
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
      <nav class="navbar navbar-dark bg-dark px-4">
        <span class="navbar-brand fw-bold">Sistema Matriculación</span>

        <div class="ms-auto d-flex gap-2">
          <a href="app.py?mod=vehiculo"
             class="btn btn-outline-light {'active' if activo=='vehiculo' else ''}">
             🚗 Vehículo
          </a>
          <a href="app.py?mod=matricula"
             class="btn btn-outline-light {'active' if activo=='matricula' else ''}">
             📄 Matrícula
          </a>
        </div>
      </nav>

      {body_html}
    </body>
    </html>
    """

@app.route("/", methods=["GET", "POST"])
def index():
    cn = conectar()

    # módulo actual (por defecto vehiculo)
    mod = request.args.get("mod", "vehiculo").lower().strip()

    v = Vehiculo(cn)
    m = Matricula(cn)

    # ---------------------------
    # Codigo necesario para realizar pruebas. (igual que PHP)
    # ---------------------------
    if "d" in request.args:
        print("\nPETICION GET\n")
        print(dict(request.args))

        dato = base64.b64decode(request.args.get("d")).decode("utf-8")
        tmp = dato.split("/")

        print("\nVARIABLE TEMP\n")
        print(tmp)

        op = tmp[0]
        id = int(tmp[1])

        # seleccionar clase según mod
        if mod == "matricula":
            if op == "det":
                html = m.get_detail_matricula(id)
            elif op == "del":
                html = m.delete_matricula(id)
            elif op in ("act", "new"):
                # Deshabilitado en Parte II
                html = """
                <div class="container my-4">
                  <div class="alert alert-warning">
                    Esta opción está deshabilitada en la PARTE II (solo listar, detalle y borrar).
                  </div>
                  <a class="btn btn-outline-secondary" href="app.py?mod=matricula">Regresar</a>
                </div>
                """
            else:
                html = "<div class='container my-4 alert alert-danger'>Operación no válida</div>"

            cn.close()
            return page("Matrícula - Parte II", html, activo="matricula")

        else:
            # vehiculo (por defecto)
            if op == "det":
                html = v.get_detail_vehiculo(id)
            elif op == "del":
                html = v.delete_vehiculo(id)
            elif op in ("act", "new"):
                # Deshabilitado en Parte II
                html = """
                <div class="container my-4">
                  <div class="alert alert-warning">
                    Esta opción está deshabilitada en la PARTE II (solo listar, detalle y borrar).
                  </div>
                  <a class="btn btn-outline-secondary" href="app.py?mod=vehiculo">Regresar</a>
                </div>
                """
            else:
                html = "<div class='container my-4 alert alert-danger'>Operación no válida</div>"

            cn.close()
            return page("Vehículo - Parte II", html, activo="vehiculo")

    # ---------------------------
    # LISTAS (sin d)
    # ---------------------------
    if mod == "matricula":
        html = m.get_list()
        cn.close()
        return page("Matrícula - Parte II", html, activo="matricula")

    # default: vehiculo
    html = v.get_list()
    cn.close()
    return page("Vehículo - Parte II", html, activo="vehiculo")
