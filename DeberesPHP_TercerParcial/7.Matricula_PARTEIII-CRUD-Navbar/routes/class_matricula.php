<?php
// =====================================================
// CLASE MATRÍCULA – CRUD COMPLETO
// USADO DESDE index.php ÚNICO (Front Controller)
// =====================================================

class Matricula {

    private $con;

    // =====================================================
    // CONSTRUCTOR
    // =====================================================
    public function __construct($cn) {
        $this->con = $cn;
    }

    // =====================================================
    // FORMULARIO (NEW / UPDATE)
    // =====================================================
    public function get_form($id = 0) {

        if ($id == 0) {
            $row = [
                "fecha" => "",
                "vehiculo" => "",
                "agencia" => "",
                "anio" => ""
            ];
            $op = "new";
            $titulo = "Nueva Matrícula";
        } else {
            $res = $this->con->query("SELECT * FROM matricula WHERE id=$id");
            if ($res->num_rows == 0) {
                return $this->_message_error("actualizar la matrícula");
            }
            $row = $res->fetch_assoc();
            $op = "update";
            $titulo = "Actualizar Matrícula";
        }

        ob_start(); ?>
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-success text-white d-flex justify-content-between">
                    <h4><?= $titulo ?></h4>
                    <a href="index.php?mod=matricula" class="btn btn-light">Regresar</a>
                </div>

                <div class="card-body">
                    <form method="POST">
                        <input type="hidden" name="op" value="<?= $op ?>">
                        <input type="hidden" name="id" value="<?= $id ?>">

                        <div class="row g-3">

                            <div class="col-md-4">
                                <label class="form-label">Fecha</label>
                                <input type="date" class="form-control"
                                       name="fecha" value="<?= $row['fecha'] ?>" required>
                            </div>

                            <div class="col-md-4">
                                <label class="form-label">Vehículo</label>
                                <?= $this->_combo_vehiculo("vehiculo", $row['vehiculo']) ?>
                            </div>

                            <div class="col-md-4">
                                <label class="form-label">Agencia</label>
                                <?= $this->_combo_agencia("agencia", $row['agencia']) ?>
                            </div>

                            <div class="col-md-4">
                                <label class="form-label">Año</label>
                                <?= $this->_combo_anio("anio", 2000, $row['anio']) ?>
                            </div>

                        </div>

                        <div class="mt-4 text-end">
                            <button type="submit" name="Guardar" class="btn btn-success">
                                GUARDAR
                            </button>
                            <a href="index.php?mod=matricula" class="btn btn-secondary">
                                Cancelar
                            </a>
                        </div>

                    </form>
                </div>
            </div>
        </div>
        <?php
        return ob_get_clean();
    }

    // =====================================================
    // GUARDAR (INSERT / UPDATE)
    // =====================================================
    public function save_matricula() {

        if ($_POST['op'] === 'new') {
            $sql = "INSERT INTO matricula
                (fecha, vehiculo, agencia, anio)
                VALUES (
                    '{$_POST['fecha']}',
                    '{$_POST['vehiculo']}',
                    '{$_POST['agencia']}',
                    '{$_POST['anio']}'
                )";
            $this->con->query($sql);
            return $this->_message_ok("insertó");
        }

        if ($_POST['op'] === 'update') {
            $sql = "UPDATE matricula SET
                fecha='{$_POST['fecha']}',
                vehiculo='{$_POST['vehiculo']}',
                agencia='{$_POST['agencia']}',
                anio='{$_POST['anio']}'
                WHERE id={$_POST['id']}";
            $this->con->query($sql);
            return $this->_message_ok("actualizó");
        }
    }

    // =====================================================
    // LISTA
    // =====================================================
    public function get_list() {

        $res = $this->con->query("
            SELECT m.id, m.fecha,
                   v.placa AS vehiculo,
                   a.descripcion AS agencia,
                   m.anio
            FROM matricula m
            JOIN vehiculo v ON m.vehiculo=v.id
            JOIN agencia a ON m.agencia=a.id
        ");

        ob_start(); ?>
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-success text-white d-flex justify-content-between">
                    <h4>Lista de Matrículas</h4>
                    <a href="index.php?mod=matricula&d=<?= base64_encode('new/0') ?>"
                       class="btn btn-light">
                        Nueva
                    </a>
                </div>

                <div class="table-responsive">
                    <table class="table table-striped table-hover text-center mb-0">
                        <thead class="table-dark">
                        <tr>
                            <th>Fecha</th>
                            <th>Vehículo</th>
                            <th>Agencia</th>
                            <th>Año</th>
                            <th>Acciones</th>
                        </tr>
                        </thead>
                        <tbody>
                        <?php while ($r = $res->fetch_assoc()): ?>
                            <tr>
                                <td><?= $r['fecha'] ?></td>
                                <td><?= $r['vehiculo'] ?></td>
                                <td><?= $r['agencia'] ?></td>
                                <td><?= $r['anio'] ?></td>
                                <td>
                                    <a class="btn btn-sm btn-info"
                                       href="index.php?mod=matricula&d=<?= base64_encode("det/{$r['id']}") ?>">
                                        Detalle
                                    </a>
                                    <a class="btn btn-sm btn-warning"
                                       href="index.php?mod=matricula&d=<?= base64_encode("act/{$r['id']}") ?>">
                                        Editar
                                    </a>
                                    <a class="btn btn-sm btn-danger"
                                       href="index.php?mod=matricula&d=<?= base64_encode("del/{$r['id']}") ?>">
                                        Borrar
                                    </a>
                                </td>
                            </tr>
                        <?php endwhile; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <?php
        return ob_get_clean();
    }

    // =====================================================
    // DETALLE
    // =====================================================
    public function get_detail_matricula($id) {

        $res = $this->con->query("
            SELECT m.fecha,
                   v.placa AS vehiculo,
                   a.descripcion AS agencia,
                   m.anio
            FROM matricula m
            JOIN vehiculo v ON m.vehiculo=v.id
            JOIN agencia a ON m.agencia=a.id
            WHERE m.id=$id
        ");

        if ($res->num_rows == 0) {
            return $this->_message_error("mostrar detalle");
        }

        $r = $res->fetch_assoc();

        ob_start(); ?>
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-info text-white">
                    Detalle Matrícula
                </div>
                <div class="card-body">
                    <table class="table table-bordered">
                        <tr><th>Fecha</th><td><?= $r['fecha'] ?></td></tr>
                        <tr><th>Vehículo</th><td><?= $r['vehiculo'] ?></td></tr>
                        <tr><th>Agencia</th><td><?= $r['agencia'] ?></td></tr>
                        <tr><th>Año</th><td><?= $r['anio'] ?></td></tr>
                    </table>
                    <a href="index.php?mod=matricula" class="btn btn-secondary">
                        Regresar
                    </a>
                </div>
            </div>
        </div>
        <?php
        return ob_get_clean();
    }

    // =====================================================
    // BORRAR
    // =====================================================
    public function delete_matricula($id) {
        $this->con->query("DELETE FROM matricula WHERE id=$id");
        return $this->_message_ok("eliminó");
    }

    // =====================================================
    // COMBOS
    // =====================================================
    private function _combo_vehiculo($name, $defecto) {
        $html = "<select class='form-select' name='$name' required>";
        $res = $this->con->query("SELECT id, placa FROM vehiculo");
        while ($r = $res->fetch_assoc()) {
            $sel = ($r['id'] == $defecto) ? "selected" : "";
            $html .= "<option value='{$r['id']}' $sel>{$r['placa']}</option>";
        }
        return $html . "</select>";
    }

    private function _combo_agencia($name, $defecto) {
        $html = "<select class='form-select' name='$name' required>";
        $res = $this->con->query("SELECT id, descripcion FROM agencia");
        while ($r = $res->fetch_assoc()) {
            $sel = ($r['id'] == $defecto) ? "selected" : "";
            $html .= "<option value='{$r['id']}' $sel>{$r['descripcion']}</option>";
        }
        return $html . "</select>";
    }

    private function _combo_anio($name, $inicio, $defecto) {
        $html = "<select class='form-select' name='$name'>";
        $actual = date("Y");
        for ($i = $inicio; $i <= $actual; $i++) {
            $sel = ($i == $defecto) ? "selected" : "";
            $html .= "<option value='$i' $sel>$i</option>";
        }
        return $html . "</select>";
    }

    // =====================================================
    // MENSAJES
    // =====================================================
    private function _message_ok($txt) {
        return "
        <div class='container mt-4'>
            <div class='alert alert-success text-center'>
                El registro se $txt correctamente
            </div>
            <div class='text-center'>
                <a href='index.php?mod=matricula' class='btn btn-primary'>
                    Regresar a la lista
                </a>
            </div>
        </div>";
    }

    private function _message_error($txt) {
        return "
        <div class='container mt-4'>
            <div class='alert alert-danger text-center'>
                Error al $txt
            </div>
            <div class='text-center'>
                <a href='index.php?mod=matricula' class='btn btn-secondary'>
                    Regresar
                </a>
            </div>
        </div>";
    }
}
?>
