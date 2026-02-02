# ===============================
# HEADER CON BOOTSTRAP (PYTHON)
# ===============================
def cargar_bootstrap():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gestión Vehicular</title>

        <!-- BOOTSTRAP 5 -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css" rel="stylesheet">
    </head>
    <body class="bg-light">
    """


def cerrar_html():
    return """
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """


# ===============================
# CLASE VEHICULO
# ===============================
class Vehiculo:

    def __init__(self, cn):
        self.__id = None
        self.__placa = None
        self.__marca = None
        self.__motor = None
        self.__chasis = None
        self.__combustible = None
        self.__anio = None
        self.__color = None
        self.__foto = None
        self.__avaluo = None

        self.con = cn

    # -------------------------------
    # LISTAR VEHÍCULOS
    # -------------------------------
    def get_list(self):

            # -------------------------------
            # CONSULTA
            # -------------------------------
            sql = """
            SELECT v.id, v.placa, m.descripcion AS marca,
                c.descripcion AS color, v.anio, v.avaluo
            FROM vehiculo v, color c, marca m
            WHERE v.marca = m.id AND v.color = c.id
            """

            cursor = self.con.cursor(dictionary=True)
            cursor.execute(sql)

            rows = cursor.fetchall()

            # -------------------------------
            # HTML INICIAL (CENTRADO REAL)
            # -------------------------------
            html = """
            <div class="container-fluid mt-5">
                <div class="d-flex justify-content-center">
                    <div class="col-lg-10 col-xl-9">
            """

            # -------------------------------
            # PRINT_R GENERAL (UNA SOLA VEZ)
            # -------------------------------
            html += """
            <div class="card mb-4 shadow-sm">
                <div class="card-header bg-secondary text-white">
                    🔎 Datos internos (print_r)
                </div>
                <div class="card-body">
                    <pre class="bg-light border rounded p-3 small">
            """

            for row in rows:
                html += print_r_py(row) + "\n"

            html += """
                    </pre>
                </div>
            </div>
            """

            # -------------------------------
            # TABLA BONITA
            # -------------------------------
            html += """
            <div class="card shadow-lg border-0">
                <div class="card-header bg-primary text-white text-center">
                    <h4 class="mb-0">🚗 Lista de Vehículos</h4>
                </div>

                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover align-middle text-center">
                            <thead class="table-dark">
                                <tr>
                                    <th>Placa</th>
                                    <th>Marca</th>
                                    <th>Color</th>
                                    <th>Año</th>
                                    <th>Avalúo</th>
                                    <th colspan="3">Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
            """

            for row in rows:
                html += f"""
                <tr>
                    <td class="fw-bold">{row['placa']}</td>
                    <td>{row['marca']}</td>
                    <td>
                        <span class="badge bg-info text-dark px-3">
                            {row['color']}
                        </span>
                    </td>
                    <td>{row['anio']}</td>
                    <td class="fw-semibold text-success">
                        ${row['avaluo']}
                    </td>
                    <td><span class="btn btn-sm btn-outline-danger">BORRAR</span></td>
                    <td><span class="btn btn-sm btn-outline-warning">ACTUALIZAR</span></td>
                    <td><span class="btn btn-sm btn-outline-primary">DETALLE</span></td>
                </tr>
                """

            html += """
                            </tbody>
                        </table>
                    </div>
                </div>

                <div class="card-footer text-center text-muted small">
                    Sistema de Gestión Vehicular
                </div>
            </div>

                    </div>
                </div>
            </div>
            """

            cursor.close()
            return html


# ===============================
# print_r TIPO PHP
# ===============================
def print_r_py(diccionario):
    salida = "Array\n(\n"
    for clave, valor in diccionario.items():
        salida += f"    [{clave}] => {valor}\n"
    salida += ")\n"
    return salida
