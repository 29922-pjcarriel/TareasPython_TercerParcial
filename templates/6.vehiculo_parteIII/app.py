# app.py  --- CRUD VEHICULO (PARTE III FUNCIONAL)

from flask import Flask, request, Response
import base64
import mysql.connector

from routes.constantes import SERVER, USER, PASS, BD
from routes.class_vehiculo6 import Vehiculo

# =====================================================
# APP
# =====================================================
app = Flask(__name__)

# =====================================================
# CONEXIÓN A LA BASE DE DATOS
# =====================================================
def conectar():
    print("<br> CONEXION A LA BASE DE DATOS<br>")

    cn = mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        port=3306,
        charset="utf8"
    )

    print("La conexión tuvo éxito .......<br><br>")
    return cn


# =====================================================
# INDEX (EQUIVALENTE A index.php)
# =====================================================
@app.route("/", methods=["GET", "POST"])
def index():

    cn = conectar()
    v = Vehiculo(cn)

    # =================================================
    # POST → GUARDAR (NEW / UPDATE)
    # =================================================
    if request.method == "POST" and request.form.get("Guardar"):

        op = request.form.get("op")

        # INSERT
        if op == "new":
            cur = cn.cursor()
            cur.execute("""
                INSERT INTO vehiculo
                (placa, marca, motor, chasis, combustible, anio, color, avaluo)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                request.form.get("placa"),
                request.form.get("marca"),
                request.form.get("motor"),
                request.form.get("chasis"),
                request.form.get("combustible"),
                request.form.get("anio"),
                request.form.get("color"),
                request.form.get("avaluo")
            ))
            cn.commit()
            return v._message_ok("insertó")

        # UPDATE
        elif op == "update":
            cur = cn.cursor()
            cur.execute("""
                UPDATE vehiculo
                SET placa=%s, marca=%s, motor=%s, chasis=%s,
                    combustible=%s, anio=%s, color=%s, avaluo=%s
                WHERE id=%s
            """, (
                request.form.get("placa"),
                request.form.get("marca"),
                request.form.get("motor"),
                request.form.get("chasis"),
                request.form.get("combustible"),
                request.form.get("anio"),
                request.form.get("color"),
                request.form.get("avaluo"),
                request.form.get("id")
            ))
            cn.commit()
            return v._message_ok("actualizó")

    # =================================================
    # GET → OPERACIONES (?d=...)
    # =================================================
    if request.args.get("d"):

        d_raw = request.args.get("d").replace(" ", "+")
        try:
            dato = base64.b64decode(d_raw).decode("utf-8")
        except Exception:
            return v._message_error("decodificar la URL<br>")

        tmp = dato.split("/")
        if len(tmp) < 2:
            return v._message_error("procesar la URL<br>")

        op = tmp[0]
        try:
            id_ = int(tmp[1])
        except Exception:
            id_ = 0

        if op == "new":
            return v.get_form()

        elif op == "act":
            return v.get_form(id_)

        elif op == "det":
            return v.get_detail_vehiculo(id_)

        elif op == "del":
            return v.delete_vehiculo(id_)

        else:
            return v._message_error("procesar la operación<br>")

    # =================================================
    # DEFAULT → LISTA
    # =================================================
    return v.get_list()


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
