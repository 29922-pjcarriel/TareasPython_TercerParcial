# 10.Sesion/app.py
import os
import sys
from flask import Flask, render_template, request, session, redirect

# ✅ Para que pueda importar Notebook.py aunque lo ejecute el Script_Backend_Py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from Notebook import NotebookCatalog  # Notebook.py en la misma carpeta

# ✅ IMPORTANTE: template_folder debe apuntar a 10.Sesion/templates
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = "dev-secret-key"

catalog = NotebookCatalog()


@app.route("/", methods=["GET"])
def home():
    # Muestra home.html (tu plantilla)
    return render_template("home.html")


# ✅ soporta GET y POST para que el form con action="" funcione
@app.route("/sesiones", methods=["GET", "POST"])
def index():
    notebooks = catalog.get_all()

    # Si el form viene con action="" se postea a /sesiones.
    # En tu HTML te puse __post_to=verNotebook para reconocerlo.
    if request.method == "POST":
        if request.form.get("__post_to") == "verNotebook":
            return ver_notebook()  # llama al handler real

    return render_template("index.html", notebooks=notebooks)


@app.route("/verNotebook", methods=["POST"])
def ver_notebook():
    notebooks = catalog.get_all()
    marca = request.form.get("op", "").strip()

    obj = catalog.get_by_marca(marca)

    # Guardar en session (misma lógica)
    session["marca_seleccionada"] = marca

    # Mostrar datos para debug como tú lo pusiste
    session_data = dict(session)
    post_data = dict(request.form)

    return render_template(
        "verNotebook.html",
        obj=obj,
        session_data=session_data,
        post_data=post_data
    )


@app.route("/cerrar", methods=["GET"])
def cerrar():
    session.clear()

    # 🔥 Redirección en cliente (NO HTTP redirect)
    return """
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Cerrando sesión...</title>
        <script>
            // redirección real en el navegador
            window.location.href = "/10.Sesion/app.py/sesiones";
        </script>
    </head>
    <body>
        <p>Cerrando sesión...</p>
    </body>
    </html>
    """


# Si lo corres directo (sin Script_Backend_Py)
if __name__ == "__main__":
    app.run(debug=True)
