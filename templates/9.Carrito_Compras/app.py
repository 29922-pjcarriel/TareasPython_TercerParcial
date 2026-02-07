# app.py (Launcher-proof, sin redirect(), sin rutas absolutas)
import os
import base64
import urllib.parse
from flask import Flask, request, send_from_directory

from db import conectar
from config import PORT

from clases9.producto import Producto
from clases9.cliente import Cliente
from clases9.pedido import Pedido

app = Flask(__name__)

# =========================
# Paths
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images", "productos")
os.makedirs(IMG_DIR, exist_ok=True)

# =========================
# DB + clases
# =========================
cn = conectar()
producto = Producto(cn, IMG_DIR)
cliente = Cliente(cn)
pedido = Pedido(cn)

# =========================
# Helpers
# =========================
def b64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")

def b64d(text: str) -> str:
    return base64.b64decode(text.encode("utf-8")).decode("utf-8")

def U(op: str) -> str:
    """
    🔥 URL RELATIVA: mantiene el navegador en /9.Carrito_Compras/app.py
    y evita que el launcher te saque al menú.
    """
    return f"?d={b64(op)}"

def IMG(filename: str) -> str:
    """
    🔥 Imágenes por query en la MISMA ruta: evita /images/... que el launcher no reenvía.
    """
    return f"?img={urllib.parse.quote(filename)}"

# =========================
# Layout base
# =========================
def render_page(content: str) -> str:
    return f"""
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Carrito CRUD</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">

      <nav class="navbar navbar-dark bg-dark px-4">
        <span class="navbar-brand">Carrito CRUD</span>
        <div class="d-flex gap-2">
          <a class="btn btn-outline-light btn-sm" href="{U("olist/0")}">Pedidos</a>
          <a class="btn btn-outline-light btn-sm" href="{U("plist/0")}">Productos</a>
          <a class="btn btn-outline-light btn-sm" href="{U("clist/0")}">Clientes</a>
        </div>
      </nav>

      <main class="container py-4">
        {content}
      </main>

    </body>
    </html>
    """

# =========================
# Única ruta (tu launcher llama siempre a "/")
# =========================
@app.route("/", methods=["GET", "POST"])
def index():

    # =========================
    # 1) SERVIR IMÁGENES: ?img=xxx.jpg
    # =========================
    img = request.args.get("img")
    if img:
        img = os.path.basename(img)  # seguridad básica
        return send_from_directory(IMG_DIR, img)

    # =========================
    # 2) POST (SIN redirect)
    # =========================
    if request.method == "POST":
        op = request.form.get("op", "")

        # ---- PRODUCTOS ----
        if op == "pnew":
            return render_page(producto.save(U))
        if op == "pupdate":
            return render_page(producto.update(U))

        # ---- CLIENTES ----
        if op == "cnew":
            return render_page(cliente.save(U))
        if op == "cupdate":
            return render_page(cliente.update(U))

        # ---- PEDIDOS ----
        # Nuevo pedido: seleccionar cliente -> guardar -> entrar a escoger productos
        if op == "osave":
            new_id = pedido.save_pedido()
            return render_page(pedido.get_items(U, IMG, new_id))

        # Actualizar cantidades carrito (en la pantalla de productos del pedido)
        if op == "oitems_update":
            pid = pedido.update_qty()
            return render_page(pedido.get_items(U, IMG, pid))

        # fallback
        return render_page(pedido.get_list(U))

    # =========================
    # 3) GET (router d=base64) SIN redirect
    # =========================
    d = request.args.get("d", "")
    if not d:
        return render_page(pedido.get_list(U))

    try:
        decoded = b64d(d)
    except Exception:
        return render_page("<div class='alert alert-danger'>Parámetro inválido.</div>")

    parts = decoded.split("/")
    action = parts[0]
    id1 = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    id2 = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0

    # =========================
    # PRODUCTOS
    # =========================
    if action == "plist":
        return render_page(producto.get_list(U, IMG))

    if action == "pnew":
        return render_page(producto.get_form(U, IMG))

    if action == "pact":
        return render_page(producto.get_form(U, IMG, id1))

    if action == "pdet":
        return render_page(producto.get_detail(U, IMG, id1))

    if action == "pdel":
        return render_page(producto.delete(U, id1))

    # =========================
    # CLIENTES
    # =========================
    if action == "clist":
        return render_page(cliente.get_list(U))

    if action == "cnew":
        return render_page(cliente.get_form(U))

    if action == "cact":
        return render_page(cliente.get_form(U, id1))

    if action == "cdet":
        return render_page(cliente.get_detail(U, id1))

    if action == "cdel":
        return render_page(cliente.delete(U, id1))

    # =========================
    # PEDIDOS
    # =========================
    if action == "olist":
        return render_page(pedido.get_list(U))

    if action == "onew":
        return render_page(pedido.get_form(U))

    if action == "odel":
        pedido.delete_pedido(id1)
        return render_page(pedido.get_list(U))

    if action == "odet":
        return render_page(pedido.get_detail(U, IMG, id1))

    if action == "oitems":
        return render_page(pedido.get_items(U, IMG, id1))

    # carrito ops (SIN redirect)
    if action == "oadd":
        pedido.add_item(id1, id2)
        return render_page(pedido.get_items(U, IMG, id1))

    if action == "orm":
        pedido.rm_item(id1, id2)
        return render_page(pedido.get_items(U, IMG, id1))

    if action == "oclear":
        pedido.clear_items(id1)
        return render_page(pedido.get_items(U, IMG, id1))

    if action == "opay":
        return render_page(pedido.pay(U, id1))

    return render_page("<div class='alert alert-danger'>Operación no válida.</div>")

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
