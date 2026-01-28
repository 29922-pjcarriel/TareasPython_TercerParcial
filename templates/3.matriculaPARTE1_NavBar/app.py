# app.py
from flask import Flask, request
import constantes

from clases.vehiculo import Vehiculo
from clases.matricula import Matricula

app = Flask(__name__)

# =========================
# CONEXIÓN (igual que conectar() en PHP)
# =========================
def conectar():
    """
    Devuelve una conexión a MySQL.
    - Intenta mysql-connector-python primero
    - Si no existe, intenta pymysql
    """
    try:
        import mysql.connector  # type: ignore
        cn = mysql.connector.connect(
            host=constantes.DB_HOST,
            user=constantes.DB_USER,
            password=constantes.DB_PASS,
            database=constantes.DB_NAME,
            charset="utf8"
        )
        return cn
    except Exception:
        import pymysql  # type: ignore
        cn = pymysql.connect(
            host=constantes.DB_HOST,
            user=constantes.DB_USER,
            password=constantes.DB_PASS,
            database=constantes.DB_NAME,
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        return cn


# =========================
# NAVBAR (compatible con SCRIPT)
# - NO usar /matricula
# - usar app.py?mod=...
# =========================
def navbar(actual: str) -> str:
    def active(mod_: str) -> str:
        return "active" if mod_ == actual else ""

    # Importante: usar enlaces RELATIVOS "app.py?mod=..."
    # Cuando lo corres directo, también funciona (mismo archivo app.py).
    return f"""
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <a class="navbar-brand fw-semibold" href="app.py?mod=vehiculo">Matriculación</a>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menu">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="menu">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link {active('vehiculo')}" href="app.py?mod=vehiculo">Vehículo</a>
            </li>
            <li class="nav-item">
              <a class="nav-link {active('matricula')}" href="app.py?mod=matricula">Matrícula</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    """


# =========================
# LAYOUT
# =========================
def page(title: str, module_title: str, body_html: str, actual: str, debug_html: str = "") -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">

{navbar(actual)}

<div class="container py-4">
  <div class="d-flex align-items-center justify-content-between mb-3">
    <h4 class="mb-0">{module_title}</h4>
  </div>

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


def debug_block(data: dict) -> str:
    import html as _html
    safe = _html.escape(str(data))
    return f"<pre>{safe}</pre>"


# =========================
# ÚNICA RUTA (compatible con SCRIPT)
# - Módulo por ?mod=vehiculo|matricula
# - Acción por ?d=C/id  (igual tu lógica)
# =========================
@app.route("/", methods=["GET", "POST"])
def main():
    mod = request.args.get("mod", "vehiculo").lower().strip()

    cn = conectar()
    try:
        if mod == "matricula":
            obj = Matricula(cn)
            actual = "matricula"
            title = "Matrícula PARTE I"
            module_title = "Módulo Matrícula"

            if "d" in request.args:
                d = request.args.get("d", "")
                debug_html = debug_block(dict(request.args))
                tmp = d.split("/")
                op = tmp[0] if len(tmp) > 0 else ""
                _id = tmp[1] if len(tmp) > 1 else ""

                if op == "C":
                    body = obj.get_form(_id)
                else:
                    body = ""  # igual que tu PHP (no hay R/U/D)
            else:
                debug_html = debug_block(dict(request.form))
                body = obj.get_list()

            return page(title=title, module_title=module_title, body_html=body, actual=actual, debug_html=debug_html)

        # ====== VEHICULO (default) ======
        obj = Vehiculo(cn)
        actual = "vehiculo"
        title = "Matriculas Vehículos PARTE I"
        module_title = "Módulo Vehículo"

        if "d" in request.args:
            d = request.args.get("d", "")
            debug_html = debug_block(dict(request.args))
            tmp = d.split("/")
            op = tmp[0] if len(tmp) > 0 else ""
            _id = tmp[1] if len(tmp) > 1 else ""

            if op == "C":
                body = obj.get_form(_id)
            else:
                body = ""  # igual que tu PHP (no hay R/U/D)
        else:
            debug_html = debug_block(dict(request.form))
            body = obj.get_list()

        return page(title=title, module_title=module_title, body_html=body, actual=actual, debug_html=debug_html)

    finally:
        try:
            cn.close()
        except Exception:
            pass


if __name__ == "__main__":
    app.run(debug=True)
