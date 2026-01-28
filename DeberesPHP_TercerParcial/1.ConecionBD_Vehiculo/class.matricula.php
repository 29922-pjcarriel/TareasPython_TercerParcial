<?php
class matricula
{
    private $id;
    private $fecha;
    private $vehiculo;
    private $agencia;
    private $anio;
    private $con;

    function __construct($cn)
    {
        $this->con = $cn;
    }

    public function get_list()
    {
        $html = '
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
            </tr>';

        $sql = "SELECT 
                    m.id, 
                    m.fecha, 
                    m.anio, 
                    v.placa as vehiculo, 
                    a.descripcion as agencia 
                FROM matricula m, vehiculo v, agencia a 
                WHERE m.vehiculo=v.id AND m.agencia=a.id;";

        $res = $this->con->query($sql);

        // Verificar error de consulta
        if (!$res) {
            return $this->_message_error("consultar matrículas: " . $this->con->error);
        }

        while ($row = $res->fetch_assoc()) {
            $html .= '
            <tr>
                <td>' . $row['fecha'] . '</td>
                <td>' . $row['vehiculo'] . '</td>
                <td>' . $row['agencia'] . '</td>
                <td>' . $row['anio'] . '</td>
                <td class="text-danger">BORRAR</td>
                <td class="text-warning">ACTUALIZAR</td>
                <td class="text-info">DETALLE</td>
            </tr>';
        }

        $html .= '
        </table>
        </div>';

        return $html;
    }

    private function _message_error($tipo)
    {
        $html = '
        <div class="container mt-5">
            <div class="alert alert-danger text-center">
                Error al ' . $tipo . '. Favor contactar a soporte.
                <br><br>
                <a href="index.php" class="btn btn-primary">Regresar</a>
            </div>
        </div>';
        return $html;
    }
}
?>
