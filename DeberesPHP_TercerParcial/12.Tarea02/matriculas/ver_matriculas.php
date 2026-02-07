<?php
// =====================================================
// ver_matriculas.php
// CONSULTA DE MATRÍCULAS POR SESIÓN
// SOLO AGENTE (rol = R)
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "R") {
    die("Acceso denegado.");
}

// -----------------------------------------------------
// Validar vehículo en sesión
// -----------------------------------------------------
if (!isset($_SESSION["vehiculo_id"])) {
    die("No se ha seleccionado ningún vehículo.");
}

$vehiculo_id = $_SESSION["vehiculo_id"];

require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

// -----------------------------------------------------
// Información COMPLETA del vehículo
// -----------------------------------------------------
$sqlVehiculo = "
SELECT 
    v.placa,
    m.descripcion AS marca,
    v.motor,
    v.chasis,
    v.combustible,
    v.anio,
    c.descripcion AS color,
    v.avaluo,
    v.foto
FROM vehiculo v
JOIN marca m ON v.marca = m.id
JOIN color c ON v.color = c.id
WHERE v.id = ?
";

$stmtVeh = $cnMatriculacion->prepare($sqlVehiculo);
$stmtVeh->execute([$vehiculo_id]);
$vehiculo = $stmtVeh->fetch();

if (!$vehiculo) {
    die("Vehículo no encontrado.");
}

// -----------------------------------------------------
// Matrículas (solo años matriculados)
// -----------------------------------------------------
$sqlMatriculas = "
SELECT 
    m.anio,
    m.fecha,
    a.descripcion AS agencia
FROM matricula m
JOIN agencia a ON m.agencia = a.id
WHERE m.vehiculo = ?
ORDER BY m.anio
";

$stmtMat = $cnMatriculacion->prepare($sqlMatriculas);
$stmtMat->execute([$vehiculo_id]);
$matriculas = $stmtMat->fetchAll();
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Consulta de Matrículas</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

<div class="container" style="margin-top:30px; max-width:1000px;">

    <div class="panel panel-success">
        <div class="panel-heading">
            <h3 class="panel-title">Consulta de Matrículas</h3>
        </div>

        <div class="panel-body">

            <!-- VEHÍCULO -->
            <h4>Información del Vehículo</h4>

            <div class="row">
                <div class="col-sm-4 text-center">
                    <?php if ($vehiculo["foto"]): ?>
                        <img src="../Recursos/img/<?= htmlspecialchars($vehiculo["foto"]) ?>"
                             class="img-thumbnail"
                             style="max-width:100%;">
                    <?php else: ?>
                        <img src="../Recursos/img/no-image.png"
                             class="img-thumbnail"
                             style="max-width:100%;">
                    <?php endif; ?>
                </div>

                <div class="col-sm-8">
                    <table class="table table-bordered">
                        <tr><th>Placa</th><td><?= $vehiculo["placa"] ?></td></tr>
                        <tr><th>Marca</th><td><?= $vehiculo["marca"] ?></td></tr>
                        <tr><th>Motor</th><td><?= $vehiculo["motor"] ?></td></tr>
                        <tr><th>Chasis</th><td><?= $vehiculo["chasis"] ?></td></tr>
                        <tr><th>Combustible</th><td><?= $vehiculo["combustible"] ?></td></tr>
                        <tr><th>Año</th><td><?= $vehiculo["anio"] ?></td></tr>
                        <tr><th>Color</th><td><?= $vehiculo["color"] ?></td></tr>
                        <tr><th>Avalúo</th><td>$ <?= number_format($vehiculo["avaluo"], 2) ?></td></tr>
                    </table>
                </div>
            </div>

            <hr>

            <!-- MATRÍCULAS -->
            <h4>Historial de Matrículas</h4>

            <?php if (count($matriculas) === 0): ?>
                <div class="alert alert-warning">
                    Este vehículo no registra matrículas.
                </div>
            <?php else: ?>
                <table class="table table-striped table-bordered">
                    <thead class="bg-success">
                        <tr>
                            <th>Año</th>
                            <th>Fecha</th>
                            <th>Agencia</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($matriculas as $m): ?>
                            <tr>
                                <td><?= $m["anio"] ?></td>
                                <td><?= $m["fecha"] ?></td>
                                <td><?= $m["agencia"] ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>

            <hr>

            <a href="../vehiculos/vehiculos.php" class="btn btn-default">
                Volver a Vehículos
            </a>
            <a href="../index.php" class="btn btn-primary">
                Inicio
            </a>

        </div>
    </div>

</div>

</body>
</html>
