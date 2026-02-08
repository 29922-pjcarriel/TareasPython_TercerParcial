# app.py - EXAMEN CRUD (INICIO / VEHICULO / MATRICULA / MARCA)

import os
import sys
import base64
import mysql.connector
from flask import Flask, request

# =========================
# RUTA BASE DEL PROYECTO
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# (Opcional pero útil con tu lanzador y carpetas)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# =========================
# FLASK APP (STATIC)
# =========================
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path="/static"
)

# =========================
# IMPORTS DEL PROYECTO
# =========================
from constants import SERVER, USER, PASS, BD, PORT
from clases8.vehiculo import Vehiculo
from clases8.matricula import Matricula
from clases8.marca import Marca

# ===========================
# CONEXIÓN
# ===========================
def conectar():
    return mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        port=PORT
    )


# ===========================
# NAV (RUTAS RELATIVAS)
# ===========================
def nav_html(mod):
    def active(m):
        return "fw-bold text-decoration-underline" if mod == m else ""

    # OJO: links relativos "app.py?mod=..."
    return f"""
    <nav class="container-fluid nav-area box-border mt-2">
      <div class="container py-2">
        <ul class="nav justify-content-center gap-4">
          <li class="nav-item">
            <a class="nav-link text-dark fw-semibold {active('inicio')}" href="app.py?mod=inicio">INICIO</a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-dark fw-semibold {active('vehiculo')}" href="app.py?mod=vehiculo">VEHICULO</a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-dark fw-semibold {active('matricula')}" href="app.py?mod=matricula">MATRICULA</a>
          </li>
          <li class="nav-item">
            <a class="nav-link text-dark fw-semibold {active('marca')}" href="app.py?mod=marca">MARCA</a>
          </li>
        </ul>
      </div>
    </nav>
    """


# ===========================
# PAGE (HTML COMPLETO)
# ===========================
def page(mod, body_html):
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <title>EXAMEN</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
      <style>
        .box-border {{ border: 4px solid #6c757d; border-radius: 12px; }}
        .header-area {{ background: #18e7ea; }}
        .nav-area {{ background: #fff200; }}
        .footer-area {{ background: #fff200; }}
        .h-hero {{ min-height: 310px; }}
        .video-box {{ padding: 0; overflow: hidden; }}
        .video-box iframe {{ width:100%; height:100%; border:0; }}
      </style>
    </head>

    <body style="background:#f8f9fa;">

      <header class="container-fluid py-4 header-area box-border">
        <div class="d-flex justify-content-center align-items-center">
          <img src="static/images/logo_ESPE.png" alt="ESPE" class="img-fluid" style="max-height:95px;">
        </div>
      </header>

      {nav_html(mod)}

      {body_html}

      <footer class="container-fluid footer-area box-border mt-3">
        <div class="container py-3 text-center">
          <p class="mb-0 fw-semibold">Contacto</p>
        </div>
      </footer>

      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """


# ===========================
# RUTA PRINCIPAL
# ===========================
@app.route("/", methods=["GET", "POST"])
def index():
    mod = request.args.get("mod", "inicio").strip().lower()
    if mod == "marcas":
        mod = "marca"

    cn = conectar()
    obj = None

    if mod == "vehiculo":
        obj = Vehiculo(cn)
    elif mod == "matricula":
        obj = Matricula(cn)
    elif mod == "marca":
        obj = Marca(cn)
    else:
        mod = "inicio"

    # --------- INICIO ----------
    if mod == "inicio":
        body = """
        <main class="container-fluid mt-3">
          <div class="container">
            <div class="row g-3 align-items-stretch">

              <div class="col-12 col-lg-3">
                <div class="box-border bg-white h-hero d-flex flex-column justify-content-center p-3 text-center">
                  <h5 class="fw-bold mb-2">¡Bienvenidos al CRUD!</h5>
                  <p class="mb-2">Desde el menú superior podrás gestionar:</p>
                  <div class="d-grid gap-2">
                    <span class="btn btn-primary">Vehículo</span>
                    <span class="btn btn-warning text-dark">Matrícula</span>
                    <span class="btn btn-dark">Marca</span>
                  </div>
                  <hr class="my-3">
                  <small class="text-muted">
                    Usa <b>NUEVO</b> para registrar y <b>Detalle</b> para ver información completa.
                  </small>
                </div>
              </div>

              <div class="col-12 col-lg-5">
                <div class="box-border h-hero d-flex flex-column justify-content-center text-center" style="background:#2f8f2f;">
                  <h2 class="text-white fw-bold mb-3">Aplicación de aplicaciones WEB</h2>
                  <p class="text-dark fs-5 mb-1">Integrantes: Pamela Carriel, Karla Molina, Josue Tapia</p>
                  <p class="text-dark fs-5 mb-1">NRC: 29922</p>
                  <p class="text-dark fs-5 mb-0">Fecha: 2026</p>
                </div>
              </div>

              <div class="col-12 col-lg-4">
                <div class="box-border bg-dark h-hero video-box">
                  <div class="ratio ratio-16x9 h-100">
                    <iframe src="https://www.youtube.com/embed/B03ff1xSMoQ" title="YouTube video" allowfullscreen></iframe>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </main>
        """
        cn.close()
        return page(mod, body)

    # --------- CRUD ----------
    body = """
    <main class="container-fluid mt-3">
      <div class="container">
        <div class="box-border bg-white p-3">
    """

    # POST: new/update
    if request.method == "POST" and "op" in request.form:
        opPost = request.form["op"]

        if mod == "vehiculo":
            if opPost == "new":
                body += obj.save_vehiculo()
            elif opPost == "update":
                body += obj.update_vehiculo()

        elif mod == "matricula":
            if opPost == "new":
                body += obj.save_matricula()
            elif opPost == "update":
                body += obj.update_matricula()

        elif mod == "marca":
            if opPost == "new":
                body += obj.save_marca()
            elif opPost == "update":
                body += obj.update_marca()

    # GET: d (new/act/det/del) o lista
    else:
        d = request.args.get("d")
        if d:
            op, id_str = base64.b64decode(d).decode("utf-8").split("/")
            id_val = int(id_str)

            if op == "new":
                body += obj.get_form(None)
            elif op == "act":
                body += obj.get_form(id_val)
            elif op == "det":
                if mod == "vehiculo":
                    body += obj.get_detail_vehiculo(id_val)
                elif mod == "matricula":
                    body += obj.get_detail_matricula(id_val)
                else:
                    body += obj.get_detail_marca(id_val)
            elif op == "del":
                if mod == "vehiculo":
                    body += obj.delete_vehiculo(id_val)
                elif mod == "matricula":
                    body += obj.delete_matricula(id_val)
                else:
                    body += obj.delete_marca(id_val)
            else:
                body += obj.get_list()
        else:
            body += obj.get_list()

    body += """
        </div>
      </div>
    </main>
    """

    cn.close()
    return page(mod, body)


if __name__ == "__main__":
    app.run(debug=True)
