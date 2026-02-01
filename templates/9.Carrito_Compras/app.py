# app.py
import base64, os
import pymysql
from pymysql.cursors import DictCursor
from flask import Flask, request, redirect

from constantes import DB_HOST, DB_USER, DB_PASS, DB_NAME, SECRET_KEY, UPLOAD_FOLDER
from clases9.producto import Producto
from clases9.cliente import Cliente
from clases9.pedido import Pedido

app = Flask(__name__)
app.secret_key = SECRET_KEY

def get_conn():
    return pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME,
        charset="utf8mb4", cursorclass=DictCursor, autocommit=True
    )

def b64_decode(s: str) -> str:
    return base64.b64decode(s.encode("utf-8")).decode("utf-8")

def b64_encode(s: str) -> str:
    return base64.b64encode(s.encode("utf-8")).decode("utf-8")

@app.route("/", methods=["GET", "POST"])
def index():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    conn = get_conn()

    pro = Producto(conn, UPLOAD_FOLDER)
    cli = Cliente(conn)
    ped = Pedido(conn)

    # ============ GET ROUTER (d=base64(op/id/id2)) ============
    if request.method == "GET" and request.args.get("d"):
        dato = b64_decode(request.args["d"])
        tmp = dato.split("/")
        op = tmp[0]
        id1 = int(tmp[1]) if len(tmp) > 1 and tmp[1].isdigit() else 0
        id2 = int(tmp[2]) if len(tmp) > 2 and tmp[2].isdigit() else 0

        # PRODUCTOS
        if op == "plist": return pro.html_list()
        if op == "pnew":  return pro.html_form_new()
        if op == "pact":  return pro.html_form_update(id1)
        if op == "pdet":  return pro.html_detail(id1)
        if op == "pdel":
            pro.delete(id1)
            return redirect("/?d=" + b64_encode("plist/0"))

        # CLIENTES
        if op == "clist": return cli.html_list()
        if op == "cnew":  return cli.html_form_new()
        if op == "cact":  return cli.html_form_update(id1)
        if op == "cdet":  return cli.html_detail(id1)
        if op == "cdel":
            cli.delete(id1)
            return redirect("/?d=" + b64_encode("clist/0"))

        # PEDIDOS
        if op == "olist": return ped.html_list()
        if op == "onew":  return ped.html_form_new(cli.list())
        if op == "oact":  return ped.html_form_update(id1, cli.list())
        if op == "odel":
            ped.delete(id1)
            return redirect("/?d=" + b64_encode("olist/0"))
        if op == "odet":  return ped.html_detail(id1)

        # ITEMS / CARRITO
        if op == "oitems":
            return ped.html_items(id1, pro.list())
        if op == "oadd":
            ped.add_item(id1, id2)
            return redirect("/?d=" + b64_encode(f"oitems/{id1}"))
        if op == "orm":
            ped.rm_item(id1, id2)
            return redirect("/?d=" + b64_encode(f"oitems/{id1}"))
        if op == "oclear":
            ped.clear_items(id1)
            return redirect("/?d=" + b64_encode(f"oitems/{id1}"))

        # default
        return redirect("/?d=" + b64_encode("olist/0"))

    # ============ POST (op como en PHP) ============
    if request.method == "POST":
        op = request.form.get("op", "")

        # PRODUCTOS
        if request.form.get("Guardar") and op == "pnew":
            pro.save(request)
            return redirect("/?d=" + b64_encode("plist/0"))

        if request.form.get("Guardar") and op == "pupdate":
            pro.update(request)
            return redirect("/?d=" + b64_encode("plist/0"))

        # CLIENTES
        if request.form.get("Guardar") and op == "cnew":
            cli.save(request.form)
            return redirect("/?d=" + b64_encode("clist/0"))

        if request.form.get("Guardar") and op == "cupdate":
            cli.update(request.form)
            return redirect("/?d=" + b64_encode("clist/0"))

        # PEDIDOS
        if request.form.get("Guardar") and op == "osave":
            new_id = ped.save(request.form)
            return redirect("/?d=" + b64_encode(f"oitems/{new_id}"))

        if request.form.get("Guardar") and op == "oupdate":
            ped.update(request.form)
            return redirect("/?d=" + b64_encode("olist/0"))

        if request.form.get("Actualizar") and op == "oitems_update":
            pedido_id = ped.update_qty(request.form)
            return redirect("/?d=" + b64_encode(f"oitems/{pedido_id}"))

    # inicio
    return redirect("/?d=" + b64_encode("olist/0"))

if __name__ == "__main__":
    app.run(debug=True)
