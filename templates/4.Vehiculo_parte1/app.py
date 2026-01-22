from flask import Flask, request
import mysql.connector
from routes.class_vehiculo import vehiculo

app = Flask(__name__)

# =====================================================
# CONEXIÓN (equivalente a conectar() en index.php)
# =====================================================
def conectar():
    cn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="matriculacionfinal"
    )
    return cn


# =====================================================
# CONTROLADOR PRINCIPAL (equivale a index.php)
# =====================================================
@app.route("/", methods=["GET", "POST"])
def index():

    db = conectar()
    obj = vehiculo(db)

    salida = ""

    # =================================================
    # CASO 1: GET con parámetro d  (?d=C/1)
    # =================================================
    if "d" in request.args:

        # Equivalente a print_r($_GET)
        salida += f"<pre>{dict(request.args)}</pre>"

        tmp = request.args["d"].split("/")
        salida += f"<pre>{tmp}</pre>"

        op = tmp[0]
        id = tmp[1] if len(tmp) > 1 else None

        salida += f"op = {op}<br>"
        salida += f"id = {id}<br>"

        if op == "C":
            # CREATE → mostrar formulario
            salida += obj.get_form(id)

        elif op == "R":
            # READ (no usado todavía)
            salida += obj.get_list()

        elif op == "U":
            # UPDATE (pendiente)
            salida += "<h3>ACTUALIZAR (pendiente)</h3>"

        elif op == "D":
            # DELETE (pendiente)
            salida += "<h3>BORRAR (pendiente)</h3>"

    # =================================================
    # CASO 2: POST → GUARDAR (equivalente a $_POST)
    # =================================================
    elif request.method == "POST":

        # Equivalente a print_r($_POST)
        salida += f"<pre>{dict(request.form)}</pre>"

        try:
            cursor = db.cursor()

            sql = """
            INSERT INTO vehiculo
            (placa, marca, motor, chasis, combustible, anio, color, avaluo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            datos = (
                request.form.get("placa"),
                request.form.get("marcaCMB"),
                request.form.get("motor"),
                request.form.get("chasis"),
                request.form.get("combustibleRBT"),
                request.form.get("anio"),
                request.form.get("colorCMB"),
                request.form.get("avaluo")
            )

            cursor.execute(sql, datos)
            db.commit()
            cursor.close()

            salida += "<h3>Vehículo guardado correctamente</h3>"

        except Exception as e:
            salida += f"<h3>Error al guardar</h3><pre>{e}</pre>"

        # Luego de guardar → lista
        salida += obj.get_list()

    # =================================================
    # CASO 3: DEFAULT → LISTADO
    # =================================================
    else:
        salida += obj.get_list()

    db.close()
    return salida


# =====================================================
# MAIN
# =====================================================
if __name__ == "__main__":
    app.run(debug=True)
