from flask import Flask
import mysql.connector
import os
import sys

# ===============================
# CONFIGURACIÓN DE RUTAS
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Rutas a los proyectos
RUTA_VEHICULO = os.path.join(BASE_DIR, "Vehiculo", "routes")
RUTA_MATRICULA = os.path.join(BASE_DIR, "Matricula", "routes")


# Agregar rutas al sys.path
if RUTA_VEHICULO not in sys.path:
    sys.path.append(RUTA_VEHICULO)

if RUTA_MATRICULA not in sys.path:
    sys.path.append(RUTA_MATRICULA)

# Imports CORRECTOS
from class_vehiculo import Vehiculo
from class_matricula import Matricula

# ===============================
# APP FLASK (HIJA DEL LANZADOR)
# ===============================
app = Flask(__name__)

# ===============================
# CONEXIÓN A BD
# ===============================
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="matriculacionfinal"
    )

# ===============================
# RUTAS
# ===============================
@app.route("/")
def inicio():
    cn = conectar()
    vehiculo = Vehiculo(cn)
    html = layout(vehiculo.get_list(), activo="vehiculo")
    cn.close()
    return html

@app.route("/vehiculo")
def ver_vehiculo():
    cn = conectar()
    vehiculo = Vehiculo(cn)
    html = layout(vehiculo.get_list(), activo="vehiculo")
    cn.close()
    return html

@app.route("/matricula")
def ver_matricula():
    cn = conectar()
    matricula = Matricula(cn)
    html = layout(matricula.get_list(), activo="matricula")
    cn.close()
    return html

# ===============================
# LAYOUT CON NAVBAR
# ===============================
def layout(contenido, activo):
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Sistema Matriculación</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>

<nav class="navbar navbar-dark bg-dark px-4">
    <span class="navbar-brand fw-bold">Sistema Matriculación</span>
    <div class="ms-auto">
        <a href="/3.ConexionBD_V&M/app.py/vehiculo"
           class="btn btn-outline-light me-2 {'active' if activo=='vehiculo' else ''}">
           🚗 Vehículo
        </a>
        <a href="/3.ConexionBD_V&M/app.py/matricula"
           class="btn btn-outline-light {'active' if activo=='matricula' else ''}">
           📄 Matrícula
        </a>
    </div>
</nav>

<div class="container mt-4">
    {contenido}
</div>

</body>
</html>
"""
