class Matricula:
    def __init__(self, con):
        self.con = con

    def get_list(self):
        cur = self.con.cursor(dictionary=True)
        sql = """
        SELECT m.id, m.fecha, m.anio,
               v.placa AS vehiculo,
               a.descripcion AS agencia
        FROM matricula m, vehiculo v, agencia a
        WHERE m.vehiculo=v.id AND m.agencia=a.id;
        """
        cur.execute(sql)
        rows = cur.fetchall()

        html = """
        <div class="container mt-4">
        <table class="table table-bordered table-hover text-center align-middle">
            <tr class="table-dark">
                <th colspan="7">Lista de Matrículas</th>
            </tr>
            <tr class="table-secondary">
                <th>Fecha</th>
                <th>Vehículo</th>
                <th>Agencia</th>
                <th>Año</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        for r in rows:
            html += f"""
            <tr>
                <td>{r['fecha']}</td>
                <td>{r['vehiculo']}</td>
                <td>{r['agencia']}</td>
                <td>{r['anio']}</td>
                <td class="text-danger">BORRAR</td>
                <td class="text-warning">ACTUALIZAR</td>
                <td class="text-info">DETALLE</td>
            </tr>
            """

        html += "</table></div>"
        return html
