<?php
// =====================================================
// mi_vehiculo.php
// SOLO DUEÑO DEL VEHÍCULO
// - username = placa
// - solo lectura
// - solo sus matrículas (años)
// =====================================================

session_start();

// -----------------------------------------------------
// Validar sesión
// -----------------------------------------------------
if (!isset($_SESSION["rol"], $_SESSION["username"])) {
    header("Location: ../index.php");
    exit;
}

// -----------------------------------------------------
// Validar que sea R (Read)
// -----------------------------------------------------
if ($_SESSION["rol"] !== "R") {
    header("Location: ../index.php");
    exit;
}

$placa = trim($_SESSION["username"]);

// -----------------------------------------------------
// Conexión BD matriculación
// -----------------------------------------------------
require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

// -----------------------------------------------------
// Obtener VEHÍCULO del dueño
// -----------------------------------------------------
$sqlVehiculo = "
    SELECT 
        v.id,
        v.placa,
        m.descripcion AS marca,
        v.motor,
        v.chasis,
        v.combustible,
        v.anio,
        c.descripcion AS color,
        v.avaluo
    FROM vehiculo v
    JOIN marca m ON v.marca = m.id
    JOIN color c ON v.color = c.id
    WHERE v.placa = ?
";

$stmtVeh = $cnMatriculacion->prepare($sqlVehiculo);
$stmtVeh->execute([$placa]);
$vehiculo = $stmtVeh->fetch(PDO::FETCH_ASSOC);

// -----------------------------------------------------
// Si no tiene vehículo asignado
// -----------------------------------------------------
if (!$vehiculo) {
    die("No existe un vehículo asignado a este usuario.");
}

// -----------------------------------------------------
// Obtener AÑOS matriculados
// -----------------------------------------------------
$sqlMatriculas = "
    SELECT DISTINCT anio
    FROM matricula
    WHERE vehiculo = ?
    ORDER BY anio
";

$stmtMat = $cnMatriculacion->prepare($sqlMatriculas);
$stmtMat->execute([$vehiculo["id"]]);
$anios = $stmtMat->fetchAll(PDO::FETCH_COLUMN);
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Mi Vehículo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

<div class="container" style="margin-top:30px; max-width:900px;">

    <h2 class="text-center">Mi Vehículo</h2>
    <p class="text-center">
        Usuario: <strong><?= htmlspecialchars($placa) ?></strong> |
        Rol: <strong>DUEÑO DEL VEHÍCULO</strong>
    </p>
    <hr>

    <!-- INFORMACIÓN DEL VEHÍCULO -->
    <div class="panel panel-success">
        <div class="panel-heading">
            <h4 class="panel-title">Información del Vehículo</h4>
        </div>
        <div class="panel-body">

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
                    <th>Motor</th>
                    <td><?= htmlspecialchars($vehiculo["motor"]) ?></td>
                </tr>
                <tr>
                    <th>Chasis</th>
                    <td><?= htmlspecialchars($vehiculo["chasis"]) ?></td>
                </tr>
                <tr>
                    <th>Combustible</th>
                    <td><?= htmlspecialchars($vehiculo["combustible"]) ?></td>
                </tr>
                <tr>
                    <th>Año</th>
                    <td><?= $vehiculo["anio"] ?></td>
                </tr>
                <tr>
                    <th>Color</th>
                    <td><?= htmlspecialchars($vehiculo["color"]) ?></td>
                </tr>
                <tr>
                    <th>Avalúo</th>
                    <td>$ <?= number_format($vehiculo["avaluo"], 2) ?></td>
                </tr>
            </table>

        </div>
    </div>

    <!-- MATRÍCULAS -->
    <div class="panel panel-info">
        <div class="panel-heading">
            <h4 class="panel-title">Años Matriculados</h4>
        </div>
        <div class="panel-body">

            <?php if (count($anios) === 0): ?>
                <div class="alert alert-warning">
                    Este vehículo no registra matrículas.
                </div>
            <?php else: ?>
                <ul>
                    <?php foreach ($anios as $a): ?>
                        <li><?= $a ?></li>
                    <?php endforeach; ?>
                </ul>
            <?php endif; ?>

        </div>
    </div>

    <div class="text-center">
        <a href="../index.php" class="btn btn-default">
            Volver al Inicio
        </a>
    </div>

</div>

</body>
</html>
