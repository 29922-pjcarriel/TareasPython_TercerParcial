from flask import Flask, request
import constantes

from clases.vehiculo import Vehiculo

app = Flask(__name__)

# =========================
# CONEXIÓN (igual que conectar() en PHP)
# =========================
def conectar():
    try:
        import mysql.connector
        return mysql.connector.connect(
            host=constantes.DB_HOST,
            user=constantes.DB_USER,
            password=constantes.DB_PASS,
            database=constantes.DB_NAME,
            charset="utf8"
        )
    except Exception:
        import pymysql
        return pymysql.connect(
            host=constantes.DB_HOST,
            user=constantes.DB_USER,
            password=constantes.DB_PASS,
            database=constantes.DB_NAME,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )

# =========================
# NAVBAR (SIN MATRÍCULA)
# =========================
def navbar():
    return """
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand fw-semibold" href="app.py">Vehículos</a>
      </div>
    </nav>
    """

# =========================
# LAYOUT
# =========================
def page(title, module_title, body_html, debug_html=""):
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

{navbar()}

<div class="container py-4">
  <h4 class="mb-3">{module_title}</h4>

  <div class="card shadow-sm">
    <div class="card-body">
      {debug_html}
      {body_html}
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

<script>
document.querySelectorAll("table").forEach(t=>{{
  t.classList.add("table","table-bordered","table-hover","align-middle");
}});
document.querySelectorAll('input[type="submit"]').forEach(b=>{{
  b.classList.add("btn","btn-success");
}});
</script>

</body>
</html>"""


def debug_block(data):
    import html
    return f"<pre>{html.escape(str(data))}</pre>"

# =========================
# ÚNICA RUTA (IGUAL QUE TU PHP)
# =========================
@app.route("/", methods=["GET", "POST"])
def main():

    cn = conectar()
    try:
        obj = Vehiculo(cn)

        if "d" in request.args:
            d = request.args.get("d", "")
            tmp = d.split("/")
            op = tmp[0] if len(tmp) > 0 else ""
            _id = tmp[1] if len(tmp) > 1 else ""

            debug_html = debug_block(dict(request.args))

            if op == "C":
                body = obj.get_form(_id)
            else:
                body = ""

        else:
            debug_html = debug_block(dict(request.form))
            body = obj.get_list()

        return page(
            title="Vehículos",
            module_title="Módulo Vehículo",
            body_html=body,
            debug_html=debug_html
        )

    finally:
        try:
            cn.close()
        except Exception:
            pass

if __name__ == "__main__":
    app.run(debug=True)
