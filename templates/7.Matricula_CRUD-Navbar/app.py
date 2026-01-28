# app.py  --- NAVBAR CRUD (VEHICULO + MATRÍCULA)
# FUNCIONA CON templates/base.html EXPLÍCITO

import os
import base64
import mysql.connector
from flask import Flask, request, render_template, Response

from routes.constantes import SERVER, USER, PASS, BD
from routes.class_vehiculo import Vehiculo
from routes.class_matricula import Matricula

# =====================================================
# RUTAS BASE (SOLUCIÓN DEFINITIVA A TemplateNotFound)
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# =====================================================
# CONEXIÓN A LA BASE DE DATOS
# =====================================================
def conectar():
    return mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        port=3306,
        charset="utf8"
    )

# =====================================================
# INDEX (EQUIVALENTE A index.php)
# =====================================================
@app.route("/", methods=["GET", "POST"])
def index():

    cn = conectar()

    # -----------------------------
    # MODULO ACTIVO
    # -----------------------------
    modulo = request.args.get("mod", "vehiculo")

    if modulo == "matricula":
        obj = Matricula(cn)
    else:
        modulo = "vehiculo"
        obj = Vehiculo(cn)

    contenido = ""

    # =================================================
    # POST → GUARDAR
    # =================================================
    if request.method == "POST" and request.form.get("Guardar"):
        try:
            if modulo == "vehiculo":
                contenido = obj.save_vehiculo(request.form, request.files)
            else:
                contenido = obj.save_matricula(request.form)
        except Exception as e:
            contenido = obj._message_error(str(e))

        return render_template(
            "base.html",
            contenido=contenido,
            modulo=modulo
        )

    # =================================================
    # GET → ?d=base64(op/id)
    # =================================================
    if request.args.get("d"):

        d_raw = request.args.get("d").replace(" ", "+")
        try:
            dato = base64.b64decode(d_raw).decode("utf-8")
        except Exception:
            contenido = obj._message_error("decodificar la URL<br>")
            return render_template("base.html", contenido=contenido, modulo=modulo)

        tmp = dato.split("/")
        if len(tmp) < 2:
            contenido = obj._message_error("procesar la URL<br>")
            return render_template("base.html", contenido=contenido, modulo=modulo)

        op = tmp[0]
        try:
            id_ = int(tmp[1])
        except:
            id_ = 0

        if op == "new":
            contenido = obj.get_form()

        elif op == "act":
            contenido = obj.get_form(id_)

        elif op == "det":
            if modulo == "vehiculo":
                contenido = obj.get_detail_vehiculo(id_)
            else:
                contenido = obj.get_detail_matricula(id_)

        elif op == "del":
            if modulo == "vehiculo":
                contenido = obj.delete_vehiculo(id_)
            else:
                contenido = obj.delete_matricula(id_)

        else:
            contenido = obj._message_error("procesar la operación<br>")

        return render_template(
            "base.html",
            contenido=contenido,
            modulo=modulo
        )

    # =================================================
    # DEFAULT → LISTA
    # =================================================
    contenido = obj.get_list()

    return render_template(
        "base.html",
        contenido=contenido,
        modulo=modulo
    )

# =====================================================
# ERROR GLOBAL
# =====================================================
@app.errorhandler(Exception)
def error_general(e):
    return Response(
        f"<h2>ERROR EN FLASK</h2><pre>{repr(e)}</pre>",
        mimetype="text/html",
        status=500
    )

# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
