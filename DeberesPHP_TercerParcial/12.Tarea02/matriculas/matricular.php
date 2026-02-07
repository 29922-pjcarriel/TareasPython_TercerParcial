<?php
// =====================================================
// matriculas/matricular.php
// REGISTRO DE MATRÍCULAS
// SOLO AGENTE (rol = R)
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso (solo AGENTE)
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "R") {
    header("Location: ../index.php");
    exit;
}

// -----------------------------------------------------
// Validar ID de vehículo recibido
// -----------------------------------------------------
if (!isset($_GET["id"]) || !is_numeric($_GET["id"])) {
    header("Location: ../vehiculos/vehiculos.php");
    exit;
}

$vehiculo_id = (int) $_GET["id"];

// -----------------------------------------------------
// Guardar vehículo en sesión
// -----------------------------------------------------
$_SESSION["vehiculo_id"] = $vehiculo_id;

// -----------------------------------------------------
// Conexión BD matriculacionfinal
// -----------------------------------------------------
require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

$mensaje = "";
$error   = "";

// -----------------------------------------------------
// Obtener datos del vehículo
// -----------------------------------------------------
$sqlVehiculo = "
    SELECT 
        v.placa,
        m.descripcion AS marca,
        v.anio
    FROM vehiculo v
    JOIN marca m ON v.marca = m.id
    WHERE v.id = ?
";
$stmtVeh = $cnMatriculacion->prepare($sqlVehiculo);
$stmtVeh->execute([$vehiculo_id]);
$vehiculo = $stmtVeh->fetch();

if (!$vehiculo) {
    die("Vehículo no encontrado.");
}

// -----------------------------------------------------
// Obtener agencias
// -----------------------------------------------------
$sqlAgencias = "SELECT id, descripcion FROM agencia ORDER BY descripcion";
$stmtAg = $cnMatriculacion->prepare($sqlAgencias);
$stmtAg->execute();
$agencias = $stmtAg->fetchAll();

// -----------------------------------------------------
// PROCESAR MATRÍCULA
// -----------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $anio     = $_POST["anio"] ?? "";
    $fecha    = $_POST["fecha"] ?? "";
    $agencia  = $_POST["agencia"] ?? "";

    if ($anio === "" || $fecha === "" || $agencia === "") {
        $error = "Todos los campos son obligatorios.";
    } else {

        // Verificar que NO se repita la matrícula del mismo año
        $sqlCheck = "
            SELECT COUNT(*) 
            FROM matricula 
            WHERE vehiculo = ? AND anio = ?
        ";
        $stmtCheck = $cnMatriculacion->prepare($sqlCheck);
        $stmtCheck->execute([$vehiculo_id, $anio]);

        if ($stmtCheck->fetchColumn() > 0) {
            $error = "Este vehículo ya está matriculado en ese año.";
        } else {

            // INSERT matrícula
            $sqlInsert = "
                INSERT INTO matricula (anio, fecha, agencia, vehiculo)
                VALUES (?, ?, ?, ?)
            ";
            $stmtInsert = $cnMatriculacion->prepare($sqlInsert);
            $stmtInsert->execute([
                $anio,
                $fecha,
                $agencia,
                $vehiculo_id
            ]);

            $mensaje = "Matrícula registrada correctamente.";
        }
    }
}
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Matricular Vehículo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- Estilos -->
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

<div class="container" style="margin-top:30px; max-width:700px;">

    <div class="panel panel-success">
        <div class="panel-heading">
            <h3 class="panel-title">Matricular Vehículo</h3>
        </div>

        <div class="panel-body">

            <!-- MENSAJES -->
            <?php if ($error): ?>
                <div class="alert alert-danger"><?= htmlspecialchars($error) ?></div>
            <?php endif; ?>

            <?php if ($mensaje): ?>
                <div class="alert alert-success"><?= htmlspecialchars($mensaje) ?></div>
            <?php endif; ?>

            <!-- INFO VEHÍCULO -->
            <h4>Vehículo</h4>
            <table class="table table-bordered">
                <tr>
                    <th>Placa</th>
                    <td><?= htmlspecialchars($vehiculo["placa"]) ?></td>
                </tr>
                <tr>
                    <th>Marca</th>
                    <td><?= htmlspecialchars($vehiculo["marca"]) ?></td>
                </tr>
                <tr>
                    <th>Año</th>
                    <td><?= $vehiculo["anio"] ?></td>
                </tr>
            </table>

            <hr>

            <!-- FORMULARIO MATRÍCULA -->
            <form method="post">

                <div class="form-group">
                    <label>Año de Matrícula</label>
                    <input type="number"
                           name="anio"
                           class="form-control"
                           placeholder="Ej: 2025"
                           required>
                </div>

                <div class="form-group">
                    <label>Fecha</label>
                    <input type="date"
                           name="fecha"
                           class="form-control"
                           required>
                </div>

                <div class="form-group">
                    <label>Agencia</label>
                    <select name="agencia" class="form-control" required>
                        <option value="">-- Seleccione --</option>
                        <?php foreach ($agencias as $a): ?>
                            <option value="<?= $a["id"] ?>">
                                <?= htmlspecialchars($a["descripcion"]) ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </div>

                <button class="btn btn-success">
                    <span class="glyphicon glyphicon-check"></span>
                    Registrar Matrícula
                </button>

                <a href="../vehiculos/vehiculos.php"
                   class="btn btn-default">
                    Cancelar
                </a>

            </form>

        </div>
    </div>

</div>

</body>
</html>
