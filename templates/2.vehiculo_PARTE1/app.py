# app.py
import os
import uuid
import pymysql
from flask import Flask, request, redirect, send_from_directory

from vehiculo import Vehiculo

app = Flask(__name__)

# ======= carpeta images (como pediste) =======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# ======= conexión igual a tu conectar() =======
def conectar():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123",
        database="matriculacionfinal",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )

# ======= servir imágenes =======
@app.get("/images/<path:filename>")
def images(filename):
    return send_from_directory(IMAGES_DIR, filename)

def page_wrap(inner_html: str) -> str:
    return f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>Matriculas Vehículos PARTE I</title>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
</head>
<body>
{inner_html}
</body>
</html>"""

@app.route("/", methods=["GET", "POST"])
def index():
    con = conectar()
    obj = Vehiculo(con)

    try:
        # ===================== POST (GUARDAR) =====================
        if request.method == "POST":
            placa = (request.form.get("placa") or "").strip()
            marca = (request.form.get("marcaCMB") or "").strip()
            motor = (request.form.get("motor") or "").strip()
            chasis = (request.form.get("chasis") or "").strip()
            combustible = (request.form.get("combustibleRBT") or "").strip()
            anio = (request.form.get("anio") or "").strip()
            color = (request.form.get("colorCMB") or "").strip()
            avaluo = (request.form.get("avaluo") or "").strip()

            # foto a /images
            foto_file = request.files.get("foto")
            filename = ""
            if foto_file and foto_file.filename:
                ext = os.path.splitext(foto_file.filename)[1].lower()
                filename = f"{uuid.uuid4().hex}{ext}"
                foto_file.save(os.path.join(IMAGES_DIR, filename))

            ok = obj.insertar({
                "placa": placa,
                "marca": marca,
                "motor": motor,
                "chasis": chasis,
                "combustible": combustible,
                "anio": anio,
                "color": color,
                "foto": filename,
                "avaluo": avaluo,
            })

            con.close()
            return redirect("/") if ok else page_wrap(obj._message_error("guardar"))

        # ===================== GET (MISMA LÓGICA d=C/1) =====================
        d = request.args.get("d", "")
        if d:
            tmp = d.split("/")
            op = tmp[0] if len(tmp) > 0 else ""
            _id = tmp[1] if len(tmp) > 1 else ""

            if op == "C":
                html = obj.get_form(_id)
                con.close()
                return page_wrap(html)

            # (R/U/D quedan como en tu PHP: vacíos o por implementar)
            # Si quieres, luego los completamos igual que el CRUD vehiculo grande.
            html = obj._message_error("operación")
            con.close()
            return page_wrap(html)

        # default: listado
        html = obj.get_list()
        con.close()
        return page_wrap(html)

    except Exception:
        try:
            con.close()
        except Exception:
            pass
        return page_wrap("<h3>Error inesperado</h3>")

if __name__ == "__main__":
    app.run(debug=True)
