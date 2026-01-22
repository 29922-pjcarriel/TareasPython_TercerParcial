import base64

class Matricula:

    def __init__(self, cn):
        self.con = cn

    # ==================================================
    # LISTAR MATRÍCULAS
    # ==================================================
    def get_list(self):

        html = """
        <table border="1" align="center" cellpadding="5">
            <tr>
                <th colspan="7">Lista de Matrículas</th>
            </tr>
            <tr>
                <th colspan="7">
                    <a href="?d={nuevo}">Nuevo</a>
                </th>
            </tr>
            <tr>
                <th>Fecha</th>
                <th>Vehículo</th>
                <th>Agencia</th>
                <th>Año</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        d_new = base64.b64encode("new/0".encode()).decode()
        html = html.format(nuevo=d_new)

        sql = """
        SELECT m.id,
               m.fecha,
               v.placa AS vehiculo,
               a.descripcion AS agencia,
               m.anio
        FROM matricula m
        JOIN vehiculo v ON m.vehiculo = v.id
        JOIN agencia a ON m.agencia = a.id
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)

        for r in cur.fetchall():
            id = r["id"]

            d_del = base64.b64encode(f"del/{id}".encode()).decode()
            d_act = base64.b64encode(f"act/{id}".encode()).decode()
            d_det = base64.b64encode(f"det/{id}".encode()).decode()

            html += f"""
            <tr>
                <td>{r['fecha']}</td>
                <td>{r['vehiculo']}</td>
                <td>{r['agencia']}</td>
                <td>{r['anio']}</td>
                <td><a href="?d={d_del}">Borrar</a></td>
                <td><a href="?d={d_act}">Actualizar</a></td>
                <td><a href="?d={d_det}">Detalle</a></td>
            </tr>
            """

        html += "</table>"
        cur.close()
        return html

    # ==================================================
    # BORRAR
    # ==================================================
    def delete_matricula(self, id):
        cur = self.con.cursor()
        cur.execute("DELETE FROM matricula WHERE id=%s", (id,))
        self.con.commit()
        cur.close()
        return '<script>location.href="/"</script>'

    # ==================================================
    # DETALLE
    # ==================================================
    def get_detail_matricula(self, id):
        cur = self.con.cursor(dictionary=True)
        cur.execute("""
            SELECT m.fecha,
                   v.placa,
                   a.descripcion AS agencia,
                   m.anio
            FROM matricula m
            JOIN vehiculo v ON m.vehiculo = v.id
            JOIN agencia a ON m.agencia = a.id
            WHERE m.id=%s
        """, (id,))
        r = cur.fetchone()
        cur.close()

        return f"""
        <table border="1" align="center" cellpadding="5">
            <tr><th colspan="2">DETALLE MATRÍCULA</th></tr>
            <tr><td>Fecha</td><td>{r['fecha']}</td></tr>
            <tr><td>Vehículo</td><td>{r['placa']}</td></tr>
            <tr><td>Agencia</td><td>{r['agencia']}</td></tr>
            <tr><td>Año</td><td>{r['anio']}</td></tr>
            <tr><td colspan="2" align="center"><a href="/">Regresar</a></td></tr>
        </table>
        """

    # ==================================================
    # FORMULARIO (NUEVO / ACTUALIZAR)
    # ==================================================
    def get_form(self, id=None):

        cur = self.con.cursor(dictionary=True)

        fecha = ""
        vehiculo_id = ""
        agencia_id = ""
        anio = ""

        if id:
            cur.execute("""
                SELECT fecha, vehiculo, agencia, anio
                FROM matricula
                WHERE id=%s
            """, (id,))
            r = cur.fetchone()
            fecha = r["fecha"]
            vehiculo_id = r["vehiculo"]
            agencia_id = r["agencia"]
            anio = r["anio"]

        cur.execute("SELECT id, placa FROM vehiculo")
        vehiculos = cur.fetchall()

        cur.execute("SELECT id, descripcion FROM agencia")
        agencias = cur.fetchall()

        cur.close()

        html = """
        <form method="post">
        <table border="1" align="center" cellpadding="5">
            <tr>
                <th colspan="2">DATOS MATRÍCULA</th>
            </tr>

            <tr>
                <td>Fecha</td>
                <td><input type="date" name="fecha" value="{fecha}"></td>
            </tr>

            <tr>
                <td>Vehículo</td>
                <td>
                    <select name="vehiculo">
        """.format(fecha=fecha)

        for v in vehiculos:
            sel = "selected" if v["id"] == vehiculo_id else ""
            html += f'<option value="{v["id"]}" {sel}>{v["placa"]}</option>'

        html += """
                    </select>
                </td>
            </tr>

            <tr>
                <td>Agencia</td>
                <td>
                    <select name="agencia">
        """

        for a in agencias:
            sel = "selected" if a["id"] == agencia_id else ""
            html += f'<option value="{a["id"]}" {sel}>{a["descripcion"]}</option>'

        html += f"""
                    </select>
                </td>
            </tr>

            <tr>
                <td>Año</td>
                <td><input type="number" name="anio" value="{anio}"></td>
            </tr>

            <tr>
                <td colspan="2" align="center">
                    <input type="submit" name="Guardar" value="GUARDAR">
                </td>
            </tr>
        </table>
        </form>
        """

        return html

    # ==================================================
    # GUARDAR (POST)
    # ==================================================
    def save(self, data, id=None):

        cur = self.con.cursor()

        if id:
            cur.execute("""
                UPDATE matricula
                SET fecha=%s, vehiculo=%s, agencia=%s, anio=%s
                WHERE id=%s
            """, (
                data["fecha"],
                data["vehiculo"],
                data["agencia"],
                data["anio"],
                id
            ))
        else:
            cur.execute("""
                INSERT INTO matricula (fecha, vehiculo, agencia, anio)
                VALUES (%s, %s, %s, %s)
            """, (
                data["fecha"],
                data["vehiculo"],
                data["agencia"],
                data["anio"]
            ))

        self.con.commit()
        cur.close()
        return '<script>location.href="/"</script>'
