<?php
// =====================================================
// routes/class_vehiculo.php
// CRUD VEHÍCULO COMPLETO – VERSIÓN FINAL
// Compatible con index.php (Front Controller)
// =====================================================

class Vehiculo
{

    private $con;

    // =====================================================
    // CONSTRUCTOR
    // =====================================================
    public function __construct($cn)
    {
        $this->con = $cn;
    }

    // =====================================================
    // BASE64 PARA ?d=
    // =====================================================
    private function _b64($txt)
    {
        return urlencode(base64_encode($txt));
    }

    // =====================================================
    // FORMULARIO (NEW / UPDATE)
    // =====================================================
    public function get_form($id = 0)
    {

        if ($id == 0) {
            $row = [
                "placa" => "",
                "marca" => "",
                "motor" => "",
                "chasis" => "",
                "combustible" => "",
                "anio" => "",
                "color" => "",
                "foto" => "",
                "avaluo" => ""
            ];
            $op = "new";
            $titulo = "Nuevo Vehículo";
        } else {

            $res = $this->con->query("SELECT * FROM vehiculo WHERE id=$id");
            if ($res->num_rows == 0) {
                return $this->_message_error("actualizar el vehículo");
            }
            $row = $res->fetch_assoc();
            $op = "update";
            $titulo = "Actualizar Vehículo";
        }

        $combustibles = ["Gasolina", "Diesel", "Eléctrico"];

        ob_start(); ?>
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white d-flex justify-content-between">
                    <div>
                        <h4 class="mb-0"><i class="bi bi-car-front-fill"></i> <?= $titulo ?></h4>
                        <small class="opacity-75">Formulario</small>
                    </div>
                    <a href="index.php?mod=vehiculo" class="btn btn-light">
                        <i class="bi bi-arrow-left"></i> Regresar
                    </a>
                </div>

                <div class="card-body">
                    <form method="POST" enctype="multipart/form-data">

                        <input type="hidden" name="op" value="<?= $op ?>">
                        <input type="hidden" name="id" value="<?= $id ?>">
                        <input type="hidden" name="foto_actual" value="<?= htmlspecialchars($row['foto']) ?>">

                        <div class="row g-3">

                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Placa</label>
                                <input type="text" class="form-control"
                                    name="placa" value="<?= htmlspecialchars($row['placa']) ?>" required>
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Marca</label>
                                <?= $this->_combo_db("marca", "id", "descripcion", "marca", $row['marca']) ?>
                            </div>

                            <div class="col-md-4">
                                <label class="form-label fw-semibold">Color</label>
                                <?= $this->_combo_db("color", "id", "descripcion", "color", $row['color']) ?>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Motor</label>
                                <input type="text" class="form-control"
                                    name="motor" value="<?= htmlspecialchars($row['motor']) ?>">
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Chasis</label>
                                <input type="text" class="form-control"
                                    name="chasis" value="<?= htmlspecialchars($row['chasis']) ?>">
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold d-block">Combustible</label>
                                <?= $this->_radio($combustibles, "combustible", $row['combustible']) ?>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Año</label>
                                <?= $this->_combo_anio("anio", 1950, $row['anio']) ?>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Foto</label>
                                <input type="file" class="form-control" name="foto">
                                <div class="form-text">
                                    Actual: <?= $row['foto'] ? $row['foto'] : "Sin foto" ?>
                                </div>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label fw-semibold">Avalúo</label>
                                <input type="number" step="0.01" class="form-control"
                                    name="avaluo" value="<?= $row['avaluo'] ?>" required>
                            </div>

                        </div>

                        <div class="mt-4 text-end">
                            <button type="submit" name="Guardar"
                                class="btn btn-success px-4">
                                GUARDAR
                            </button>
                            <a href="index.php?mod=vehiculo"
                                class="btn btn-secondary ms-2">
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
    public function save_vehiculo()
    {

        $foto = isset($_POST["foto_actual"]) ? $_POST["foto_actual"] : "";

        if (!empty($_FILES["foto"]["name"])) {
            $nombre = basename($_FILES["foto"]["name"]);
            move_uploaded_file($_FILES["foto"]["tmp_name"], "images/" . $nombre);
            $foto = $nombre;
        }

        if ($_POST["op"] === "new") {

            $sql = "INSERT INTO vehiculo
            (placa, marca, motor, chasis, combustible, anio, color, foto, avaluo)
            VALUES (
              '{$_POST['placa']}','{$_POST['marca']}','{$_POST['motor']}',
              '{$_POST['chasis']}','{$_POST['combustible']}',
              '{$_POST['anio']}','{$_POST['color']}',
              '$foto','{$_POST['avaluo']}'
            )";

            return $this->con->query($sql)
                ? $this->_message_ok("insertó")
                : $this->_message_error("insertar el vehículo");
        }

        if ($_POST["op"] === "update") {

            $sql = "UPDATE vehiculo SET
              placa='{$_POST['placa']}',
              marca='{$_POST['marca']}',
              motor='{$_POST['motor']}',
              chasis='{$_POST['chasis']}',
              combustible='{$_POST['combustible']}',
              anio='{$_POST['anio']}',
              color='{$_POST['color']}',
              foto='$foto',
              avaluo='{$_POST['avaluo']}'
            WHERE id={$_POST['id']}";

            return $this->con->query($sql)
                ? $this->_message_ok("actualizó")
                : $this->_message_error("actualizar el vehículo");
        }

        return $this->_message_error("guardar el vehículo");
    }

    // =====================================================
    // LISTA
    // =====================================================
    public function get_list()
    {

        $res = $this->con->query("
            SELECT v.id, v.placa,
                   m.descripcion AS marca,
                   c.descripcion AS color,
                   v.anio, v.avaluo
            FROM vehiculo v, marca m, color c
            WHERE v.marca=m.id AND v.color=c.id
        ");

        ob_start(); ?>
        <div class="container py-4">
            <div class="card shadow-lg">
                <div class="card-header bg-primary text-white d-flex justify-content-between">
                    <h4 class="mb-0">
                        <i class="bi bi-car-front-fill"></i> Lista de Vehículos
                    </h4>
                    <a href="index.php?mod=vehiculo&d=<?= $this->_b64("new/0") ?>"
                        class="btn btn-light">
                        <i class="bi bi-plus-circle"></i> Nuevo
                    </a>
                </div>

                <div class="table-responsive">
                    <table class="table table-striped table-hover text-center mb-0">
                        <thead class="table-dark">
                            <tr>
                                <th>Placa</th>
                                <th>Marca</th>
                                <th>Color</th>
                                <th>Año</th>
                                <th>Avalúo</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php while ($r = $res->fetch_assoc()): ?>
                                <tr>
                                    <td><?= $r['placa'] ?></td>
                                    <td><?= $r['marca'] ?></td>
                                    <td><?= $r['color'] ?></td>
                                    <td><?= $r['anio'] ?></td>
                                    <td>$<?= $r['avaluo'] ?></td>
                                    <td class="text-center">
                                        <a class="btn btn-sm btn-outline-primary me-1"
                                            href="index.php?mod=vehiculo&d=<?= $this->_b64("det/" . $r['id']) ?>">
                                            <i class="bi bi-eye"></i> Detalle
                                        </a>

                                        <a class="btn btn-sm btn-warning me-1"
                                            href="index.php?mod=vehiculo&d=<?= $this->_b64("act/" . $r['id']) ?>">
                                            <i class="bi bi-pencil"></i> Editar
                                        </a>

                                        <a class="btn btn-sm btn-danger"
                                            href="index.php?mod=vehiculo&d=<?= $this->_b64("del/" . $r['id']) ?>"
                                            onclick="return confirm('¿Desea eliminar este vehículo?')">
                                            <i class="bi bi-trash"></i> Borrar
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

    // =====================================================
    // DETALLE
    // =====================================================
    public function get_detail_vehiculo($id)
    {
        $res = $this->con->query("
        SELECT v.placa, m.descripcion AS marca,
               v.motor, v.chasis, v.combustible,
               v.anio, c.descripcion AS color,
               v.foto, v.avaluo
        FROM vehiculo v, marca m, color c
        WHERE v.id=$id 
          AND v.marca=m.id 
          AND v.color=c.id
    ");

        if ($res->num_rows == 0) {
            return $this->_message_error("mostrar el detalle del vehículo");
        }

        $r = $res->fetch_assoc();
        $matricula = number_format($r['avaluo'] * 0.10, 2);

        // ================= IMAGEN =================
        $img = (!empty($r['foto']) && file_exists("images/" . $r['foto']))
            ? "images/" . $r['foto']
            : "images/no-image.png";

        ob_start(); ?>

        <style>
            /* ===============================
           DETALLE VEHÍCULO – ESTILO PRO
        ================================ */
            .vehicle-detail-card {
                border-radius: 16px;
                overflow: hidden;
                background: #ffffff;
            }

            .vehicle-detail-header {
                background: linear-gradient(135deg, #0d6efd, #0a58ca);
                color: #fff;
                padding: 1rem 1.25rem;
            }

            .vehicle-detail-header h4 {
                margin: 0;
                font-weight: 600;
            }

            .vehicle-detail-header .btn-back {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                font-weight: 500;
            }

            .vehicle-image-box img {
                max-height: 260px;
                width: 100%;
                object-fit: contain;
                border-radius: 14px;
                background: #f8f9fa;
                padding: 12px;
                box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
            }

            .vehicle-detail-table th {
                width: 35%;
                background: #f1f3f5;
                font-weight: 600;
            }

            .vehicle-price {
                font-size: 1.1rem;
                font-weight: 600;
                color: #198754;
            }

            .vehicle-matricula {
                font-size: 1.1rem;
                font-weight: 600;
                color: #dc3545;
            }

            @media (max-width: 768px) {
                .vehicle-detail-header {
                    flex-direction: column;
                    gap: 10px;
                    text-align: center;
                }
            }
        </style>

        <div class="container py-4">
            <div class="card shadow-lg vehicle-detail-card">

                <!-- HEADER -->
                <div class="card-header vehicle-detail-header d-flex justify-content-between align-items-center">
                    <h4><i class="bi bi-car-front-fill"></i> Detalle Vehículo</h4>
                    <a href="index.php?mod=vehiculo" class="btn btn-light btn-back">
                        <i class="bi bi-arrow-left"></i> Regresar
                    </a>
                </div>

                <!-- BODY -->
                <div class="card-body">
                    <div class="row g-4 align-items-center">

                        <!-- IMAGEN -->
                        <div class="col-md-4 text-center">
                            <div class="vehicle-image-box">
                                <img src="<?= $img ?>" alt="Imagen del vehículo">
                            </div>
                        </div>

                        <!-- DATOS -->
                        <div class="col-md-8">
                            <table class="table table-bordered vehicle-detail-table mb-0">
                                <tr>
                                    <th>Placa</th>
                                    <td><?= $r['placa'] ?></td>
                                </tr>
                                <tr>
                                    <th>Marca</th>
                                    <td><?= $r['marca'] ?></td>
                                </tr>
                                <tr>
                                    <th>Motor</th>
                                    <td><?= $r['motor'] ?></td>
                                </tr>
                                <tr>
                                    <th>Chasis</th>
                                    <td><?= $r['chasis'] ?></td>
                                </tr>
                                <tr>
                                    <th>Combustible</th>
                                    <td><?= $r['combustible'] ?></td>
                                </tr>
                                <tr>
                                    <th>Año</th>
                                    <td><?= $r['anio'] ?></td>
                                </tr>
                                <tr>
                                    <th>Color</th>
                                    <td><?= $r['color'] ?></td>
                                </tr>
                                <tr>
                                    <th>Avalúo</th>
                                    <td class="vehicle-price">$<?= $r['avaluo'] ?></td>
                                </tr>
                                <tr>
                                    <th>Valor Matrícula</th>
                                    <td class="vehicle-matricula">$<?= $matricula ?></td>
                                </tr>
                            </table>
                        </div>

                    </div>
                </div>

            </div>
        </div>

<?php
        return ob_get_clean();
    }


    // =====================================================
    // BORRAR
    // =====================================================
    public function delete_vehiculo($id)
    {

        return $this->con->query("DELETE FROM vehiculo WHERE id=$id")
            ? $this->_message_ok("eliminó")
            : $this->_message_error("eliminar el vehículo");
    }

    // =====================================================
    // UTILIDADES
    // =====================================================
    private function _combo_db($tabla, $valor, $texto, $name, $defecto)
    {
        $html = "<select class='form-select' name='$name'>";
        $res = $this->con->query("SELECT $valor,$texto FROM $tabla");
        while ($r = $res->fetch_assoc()) {
            $sel = ($r[$valor] == $defecto) ? "selected" : "";
            $html .= "<option value='{$r[$valor]}' $sel>{$r[$texto]}</option>";
        }
        return $html . "</select>";
    }

    private function _combo_anio($name, $inicio, $defecto)
    {
        $html = "<select class='form-select' name='$name'>";
        for ($i = $inicio; $i <= date("Y"); $i++) {
            $sel = ($i == $defecto) ? "selected" : "";
            $html .= "<option value='$i' $sel>$i</option>";
        }
        return $html . "</select>";
    }

    private function _radio($arr, $name, $defecto)
    {
        $html = "";
        foreach ($arr as $v) {
            $chk = ($v == $defecto) ? "checked" : "";
            $html .= "
            <div class='form-check form-check-inline'>
                <input class='form-check-input' type='radio'
                       name='$name' value='$v' $chk required>
                <label class='form-check-label'>$v</label>
            </div>";
        }
        return $html;
    }

    // =====================================================
    // MENSAJES
    // =====================================================
    private function _message_ok($txt)
    {
        return "
        <div class='container mt-4 text-center'>
            <div class='alert alert-success'>
                El registro se $txt correctamente
            </div>
            <a href='index.php?mod=vehiculo'
               class='btn btn-primary'>
               Regresar a la lista
            </a>
        </div>";
    }

    private function _message_error($txt)
    {
        return "
        <div class='container mt-4 text-center'>
            <div class='alert alert-danger'>
                Error al $txt
            </div>
            <a href='index.php?mod=vehiculo'
               class='btn btn-secondary'>
               Regresar
            </a>
        </div>";
    }
}
?>