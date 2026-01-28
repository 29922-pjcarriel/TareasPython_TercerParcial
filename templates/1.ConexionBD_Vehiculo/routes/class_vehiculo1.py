class Vehiculo:
    def __init__(self, con):
        self.con = con

    def get_list(self):
        cur = self.con.cursor(dictionary=True)
        sql = """
        SELECT v.id, v.placa,
               m.descripcion AS marca,
               c.descripcion AS color,
               v.anio, v.avaluo
        FROM vehiculo v, marca m, color c
        WHERE v.marca=m.id AND v.color=c.id;
        """
        cur.execute(sql)
        rows = cur.fetchall()

        html = """
        <div class="container mt-4">
        <table class="table table-bordered table-hover text-center align-middle">
            <tr class="table-dark">
                <th colspan="8">Lista de Vehículos</th>
            </tr>
            <tr class="table-secondary">
                <th>Placa</th>
                <th>Marca</th>
                <th>Color</th>
                <th>Año</th>
                <th>Avalúo</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        for r in rows:
            html += f"""
            <tr>
                <td>{r['placa']}</td>
                <td>{r['marca']}</td>
                <td>{r['color']}</td>
                <td>{r['anio']}</td>
                <td>{r['avaluo']}</td>
                <td class="text-danger">BORRAR</td>
                <td class="text-warning">ACTUALIZAR</td>
                <td class="text-info">DETALLE</td>
            </tr>
            """

        html += "</table></div>"
        return html
