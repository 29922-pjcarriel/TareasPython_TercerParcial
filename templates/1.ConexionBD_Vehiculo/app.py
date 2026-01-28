# app.py  (APP HIJA para Script_Backend_Py.py)
from flask import Flask, request
import mysql.connector

from routes.class_vehiculo import Vehiculo
from routes.class_matricula import Matricula

app = Flask(__name__)

# ======================================================
# CONEXIÓN BD (igual a tu PHP)
# ======================================================
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="matriculacionfinal",
        charset="utf8"
    )

# ======================================================
# INDEX (equivalente a index.php)
# IMPORTANTE: usamos links RELATIVOS ?m=V / ?m=M
# para que NO se salga del prefijo /carpeta/app.py
# ======================================================
@app.route("/", methods=["GET", "POST"])
def index():
    db = conectar()
    objVehiculo = Vehiculo(db)
    objMatricula = Matricula(db)

    modo = request.args.get("m", "V")  # V por defecto

    if modo == "M":
        contenido = objMatricula.get_list()
        titulo = "CRUD Matrículas"
    else:
        contenido = objVehiculo.get_list()
        titulo = "CRUD Vehículos"

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>{titulo}</title>

        <!-- Bootstrap CDN -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    </head>

    <body class="bg-light">

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <span class="navbar-brand">CRUD</span>

                <!-- LINKS RELATIVOS: se quedan en /carpeta/app.py -->
                <div class="navbar-nav">
                    <a class="nav-link" href="?m=V">Vehículos</a>
                    <a class="nav-link" href="?m=M">Matrículas</a>
                </div>
            </div>
        </nav>

        {contenido}

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

    return html
