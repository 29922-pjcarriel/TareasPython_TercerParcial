from flask import Flask, request, session, send_from_directory
import os
import mysql.connector

from clases11.notebook import Notebook

# =========================
# RUTA BASE DEL PROYECTO
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAGINAS_DIR = os.path.join(BASE_DIR, "paginas")

# =========================
# FLASK APP (STATIC)
# =========================
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)
app.secret_key = "123"  # para sesiones


def leer_pagina(nombre_archivo: str) -> str:
    ruta = os.path.join(PAGINAS_DIR, nombre_archivo)
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def crear_lista_notebooks():
    chronos = Notebook(2, "Samsung", 5900)
    acer = Notebook(1, "Acer", 3500.50)
    compaq = Notebook(3, "Compaq", 2600.33)
    lenovo = Notebook(4, "Lenovo", 1555.00)

    notebooks = {
        "Acer": {"id": acer.id, "marca": acer.getMarca(), "precio": acer.getPrecio()},
        "Samsung": {"id": chronos.id, "marca": chronos.getMarca(), "precio": chronos.getPrecio()},
        "Compaq": {"id": compaq.id, "marca": compaq.getMarca(), "precio": compaq.getPrecio()},
        "Lenovo": {"id": lenovo.id, "marca": lenovo.getMarca(), "precio": lenovo.getPrecio()},
    }
    return notebooks


def validar_usuario_mysql(usuario: str, clave: str) -> bool:
    cn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="sesionesbd"
    )
    cur = cn.cursor()
    cur.execute("SELECT 1 FROM usuarios WHERE usuario=%s AND clave=%s LIMIT 1", (usuario, clave))
    row = cur.fetchone()
    cur.close()
    cn.close()
    return row is not None


@app.route("/")
def index():
    return leer_pagina("index.html")


@app.route("/home")
def home():
    session["listaNote"] = crear_lista_notebooks()
    return leer_pagina("home.html")


@app.route("/login")
def login():
    if "listaNote" not in session:
        session["listaNote"] = crear_lista_notebooks()
    return leer_pagina("login.html")



@app.route("/validar", methods=["POST"])
def validar():
    usuario = request.form.get("usuario", "").strip()
    clave = request.form.get("clave", "").strip()

    # ✅ SIN redirect: devolvemos la página final directo
    if validar_usuario_mysql(usuario, clave):
        session["usuario"] = usuario
        session["login"] = True

        # Mostrar notebook directamente (sin redirect)
        return _render_notebook(usuario)

    else:
        return leer_pagina("error.html")


def _render_notebook(op: str):
    # Validaciones como antes
    if "listaNote" not in session:
        session["listaNote"] = crear_lista_notebooks()

    notes = session["listaNote"]

    if not op or op not in notes:
        # si no existe, volvemos al home (sin redirect)
        return leer_pagina("home.html")

    obj = notes[op]

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Bienvenida</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">

            <div class="text-center mb-4">
                <h2 class="fw-bold">BIENVENIDOS !!!!</h2>
            </div>

            <div class="card shadow mx-auto mb-4" style="max-width: 600px;">
                <div class="card-body text-center">
                    <h1 class="fw-bold mb-3">{obj['marca']}</h1>
                    <p class="fs-4 mb-4">
                        Precio: <span class="fw-bold">${obj['precio']}</span>
                    </p>
                    <a href="home" class="btn btn-primary">Continuar</a>
                </div>
            </div>

            <div class="card shadow mx-auto" style="max-width: 600px;">
                <div class="card-body">
                    <h5 class="fw-bold">VARIABLE SESSION:</h5>
                    <pre class="bg-light border rounded p-3 mb-0">{dict(session)}</pre>
                </div>
            </div>

        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """


@app.route("/verNotebook", methods=["GET", "POST"])
def ver_notebook():
    # ✅ SIN redirect: obtenemos op y renderizamos
    op = request.form.get("op") if request.method == "POST" else request.args.get("op")
    return _render_notebook(op)


@app.route("/error")
def error():
    return leer_pagina("error.html")


@app.route("/paginas/<path:nombre>")
def paginas(nombre):
    return send_from_directory(PAGINAS_DIR, nombre)


if __name__ == "__main__":
    app.run(debug=True)
