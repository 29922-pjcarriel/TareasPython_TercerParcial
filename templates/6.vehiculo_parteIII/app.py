# app.py
from flask import current_app
from flask import Flask, request, Response
import base64
import mysql.connector

from routes.constantes import SERVER, USER, PASS, BD
from routes.class_vehiculo import Vehiculo

app = Flask(__name__, static_url_path="", static_folder="")  # para /images/
def base_path():
    # Si corre dentro del menú, usa esa ruta
    return current_app.config.get("BASE_PATH", "")


# *******************************************************
def conectar():
    print("<br> CONEXION A LA BASE DE DATOS<br>")

    cn = mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        port=3306,     # <-- si tu MySQL usa otro puerto cámbialo aquí
        charset="utf8"
    )

    print("La conexión tuvo éxito .......<br><br>")
    cur = cn.cursor()
    cur.execute("SET NAMES utf8;")
    cur.close()
    return cn
# **********************************************************


@app.route("/", methods=["GET", "POST"])
def index():

    cn = conectar()
    v = Vehiculo(cn)

    # ==========================
    # PETICION GET
    # ==========================
    if request.args.get("d") is not None:
        d_raw = request.args.get("d", "")

        # ✅ FIX: si venía base64 con +, Flask lo pudo convertir en espacio
        d_raw = d_raw.replace(" ", "+")

        try:
            dato = base64.b64decode(d_raw).decode("utf-8")
        except Exception:
            return v._message_error("decodificar la URL (base64 inválido)<br>")

        tmp = dato.split("/")
        if len(tmp) < 2:
            return v._message_error("procesar la URL (formato inválido)<br>")

        op = tmp[0]
        try:
            id_ = int(tmp[1])
        except Exception:
            id_ = 0

        if op == "det":
            return v.get_detail_vehiculo(id_)
        elif op == "act":
            return v.get_form(id_)
        elif op == "new":
            return v.get_form()
        elif op == "del":
            return v.delete_vehiculo(id_)

        return v._message_error("procesar la operación GET<br>")

    # ==========================
    # PETICION POST
    # ==========================
    if request.method == "POST":
        # PARTE III (igual al PHP: NO guardamos aún porque tu PHP lo tiene comentado)
        if request.form.get("Guardar") is not None and request.form.get("placa"):
            html = """
            <br>GRABAR VEHICULO - PARTE III<br><br><br>
            <th colspan="2"><a href="/">Regresar</a></th>
            """
            return html

        return v.get_list()

    return v.get_list()


@app.errorhandler(Exception)
def handle_error(e):
    return Response(f"<h2>ERROR EN FLASK</h2><pre>{repr(e)}</pre>", status=500, mimetype="text/html")


if __name__ == "__main__":
    app.run(debug=True)
