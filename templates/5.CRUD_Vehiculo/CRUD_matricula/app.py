from flask import Flask, request
import mysql.connector
import base64
import os
import sys
import importlib.util

app = Flask(__name__)

# ============================
# UBICACIÓN REAL DEL app.py
# ============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Intentar encontrar la carpeta "class" (o "Class") dentro del proyecto
POSSIBLE_CLASS_DIRS = ["class", "Class", "clase", "Clases", "classes", "Classes"]
CLASS_DIR = None

for name in POSSIBLE_CLASS_DIRS:
    candidate = os.path.join(BASE_DIR, name)
    if os.path.isdir(candidate):
        CLASS_DIR = candidate
        break

if CLASS_DIR is None:
    raise Exception(
        f"No encuentro la carpeta de clases dentro de: {BASE_DIR}\n"
        f"Busca una carpeta llamada 'class' (recomendado) y que contenga constantes.py y class_matricula.py"
    )

# ============================
# CARGAR constantes.py A LA FUERZA
# ============================
const_path = os.path.join(CLASS_DIR, "constantes.py")
if not os.path.exists(const_path):
    # Mostrar qué archivos hay para que veas el nombre real
    raise Exception(
        f"No encuentro constantes.py en: {CLASS_DIR}\n"
        f"Archivos encontrados: {os.listdir(CLASS_DIR)}\n"
        f"✅ Asegúrate que el archivo se llame EXACTO: constantes.py"
    )

spec_const = importlib.util.spec_from_file_location("constantes", const_path)
constantes = importlib.util.module_from_spec(spec_const)
spec_const.loader.exec_module(constantes)

SERVER = constantes.SERVER
USER = constantes.USER
PASS = constantes.PASS
BD = constantes.BD

# ============================
# CARGAR class_matricula.py A LA FUERZA
# ============================
mat_path = os.path.join(CLASS_DIR, "class_matricula.py")
if not os.path.exists(mat_path):
    # Tal vez en PHP se llama class.matricula.php -> aquí debe ser .py
    alt = os.path.join(CLASS_DIR, "class.matricula.py")
    if os.path.exists(alt):
        mat_path = alt
    else:
        raise Exception(
            f"No encuentro class_matricula.py en: {CLASS_DIR}\n"
            f"Archivos encontrados: {os.listdir(CLASS_DIR)}\n"
            f"✅ Asegúrate que el archivo se llame EXACTO: class_matricula.py"
        )

spec_mat = importlib.util.spec_from_file_location("class_matricula", mat_path)
mod_mat = importlib.util.module_from_spec(spec_mat)
spec_mat.loader.exec_module(mod_mat)

Matricula = mod_mat.Matricula

# ============================
# CONEXIÓN BD
# ============================
def conectar():
    return mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD
    )

# ============================
# RUTA PRINCIPAL
# ============================
@app.route("/", methods=["GET", "POST"])
def index():
    cn = conectar()
    m = Matricula(cn)

    # GET con base64
    if "d" in request.args:
        try:
            dato = base64.b64decode(request.args["d"]).decode("utf-8")
            op, id_str = dato.split("/")
            id_val = int(id_str)

            if op == "det":
                out = m.get_detail_matricula(id_val)
            elif op == "del":
                out = m.delete_matricula(id_val)
            elif op == "act":
                out = m.get_form(id_val)
            elif op == "new":
                out = m.get_form()
            else:
                out = m.get_list()

            cn.close()
            return out

        except Exception as e:
            cn.close()
            return f"<h3>Error en GET</h3><pre>{e}</pre>"

    # POST
    if request.method == "POST":
        # Aquí mantengo tu lógica “tal cual” (sin añadir métodos)
        print("PETICION POST:", dict(request.form))
        cn.close()
        return '<a href="/">Regresar</a>'

    # Default
    out = m.get_list()
    cn.close()
    return out


if __name__ == "__main__":
    app.run(debug=True, port=5000)
