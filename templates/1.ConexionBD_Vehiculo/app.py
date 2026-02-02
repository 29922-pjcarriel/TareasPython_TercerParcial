from flask import Flask
import mysql.connector
from routes.class_vehiculo1 import Vehiculo

app = Flask(__name__)

# -------------------------------
# FUNCIÓN DE CONEXIÓN A LA BD
# -------------------------------
def conectar():
    server = "localhost"
    user = "root"
    password = "123"
    database = "matriculacionfinal"

    c = mysql.connector.connect(
        host=server,
        user=user,
        password=password,
        database=database
    )

    c.set_charset_collation(charset='utf8')
    return c


# -------------------------------
# RUTA PRINCIPAL
# -------------------------------
@app.route("/")
def index():

    cn = conectar()
    objetoVehiculo = Vehiculo(cn)

    # -------------------------------
    # HTML BASE + BOOTSTRAP (AQUÍ ESTABA EL ERROR)
    # -------------------------------
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Matriculación Vehicular</title>

        <!-- BOOTSTRAP 5 -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    </head>

    <body class="bg-light">
    """

    # CONTENIDO
    html += objetoVehiculo.get_list()

    # CIERRE HTML
    html += """
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

    cn.close()
    return html


# -------------------------------
# EJECUCIÓN DE LA APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
