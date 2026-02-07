<?php
// =====================================================
// vehiculos.php
// SOLO AGENTE Y ADMIN
// =====================================================

session_start();

// -----------------------------------------------------
// Validar sesión
// -----------------------------------------------------
if (!isset($_SESSION["rol"], $_SESSION["username"])) {
    header("Location: ../index.php");
    exit;
}

$rolBD    = $_SESSION["rol"];      // R | CRUD
$username = trim($_SESSION["username"]);

// -----------------------------------------------------
// CONEXIÓN BD matriculación
// -----------------------------------------------------
require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

// -----------------------------------------------------
// DETERMINAR ROL REAL
// -----------------------------------------------------
if ($rolBD === "CRUD") {

    $rolReal = "ADM";

} elseif ($rolBD === "R") {

    // Si el username es una placa → ES DUEÑO → NO PUEDE ESTAR AQUÍ
    $sql = "SELECT COUNT(*) FROM vehiculo WHERE placa = ?";
    $stmt = $cnMatriculacion->prepare($sql);
    $stmt->execute([$username]);

    if ($stmt->fetchColumn() > 0) {
        // 🔒 Dueño NO puede entrar a este archivo
        header("Location: mi_vehiculo.php");
        exit;
    }

    $rolReal = "AGENTE";

} else {
    header("Location: ../index.php");
    exit;
}

// -----------------------------------------------------
// CONSULTA DE VEHÍCULOS (AGENTE y ADMIN)
// -----------------------------------------------------
$sql = "
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
    ORDER BY v.id
";

$stmt = $cnMatriculacion->prepare($sql);
$stmt->execute();
$vehiculos = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Vehículos</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

<div class="container-fluid" style="margin-top:20px;">

    <h2>Listado de Vehículos</h2>

    <p>
        Usuario: <strong><?= htmlspecialchars($username) ?></strong> |
        Rol:
        <strong><?= ($rolReal === "ADM") ? "ADMINISTRADOR" : "AGENTE" ?></strong>
    </p>
    <hr>

    <!-- BOTÓN CREAR SOLO ADMIN -->
    <?php if ($rolReal === "ADM"): ?>
        <a href="vehiculo_form.php" class="btn btn-success">
            <span class="glyphicon glyphicon-plus"></span>
            Nuevo Vehículo
        </a>
        <br><br>
    <?php endif; ?>

    <div class="table-responsive">
        <table class="table table-bordered table-striped table-hover">

            <thead class="bg-success">
                <tr>
                    <th>ID</th>
                    <th>Placa</th>
                    <th>Marca</th>
                    <th>Motor</th>
                    <th>Chasis</th>
                    <th>Combustible</th>
                    <th>Año</th>
                    <th>Color</th>
                    <th>Avalúo</th>
                    <th>Acciones</th>
                </tr>
            </thead>

            <tbody>
            <?php foreach ($vehiculos as $v): ?>
                <tr>
                    <td><?= $v["id"] ?></td>
                    <td><?= htmlspecialchars($v["placa"]) ?></td>
                    <td><?= htmlspecialchars($v["marca"]) ?></td>
                    <td><?= htmlspecialchars($v["motor"]) ?></td>
                    <td><?= htmlspecialchars($v["chasis"]) ?></td>
                    <td><?= htmlspecialchars($v["combustible"]) ?></td>
                    <td><?= $v["anio"] ?></td>
                    <td><?= htmlspecialchars($v["color"]) ?></td>
                    <td>$ <?= number_format($v["avaluo"], 2) ?></td>

                    <td>
                        <?php if ($rolReal === "AGENTE"): ?>
                            <a href="../matriculas/consultar_matricula.php?id=<?= $v["id"] ?>"
                               class="btn btn-xs btn-info">
                               Consultar
                            </a>

                            <a href="../matriculas/matricular.php?id=<?= $v["id"] ?>"
                               class="btn btn-xs btn-success">
                               Matricular
                            </a>
                        <?php else: ?>
                            <a href="vehiculo_form.php?id=<?= $v["id"] ?>"
                               class="btn btn-xs btn-primary">Editar</a>

                            <a href="vehiculo_delete.php?id=<?= $v["id"] ?>"
                               class="btn btn-xs btn-danger"
                               onclick="return confirm('¿Eliminar vehículo?');">
                               Eliminar
                            </a>
                        <?php endif; ?>
                    </td>
                </tr>
            <?php endforeach; ?>
            </tbody>

        </table>
    </div>

    <a href="../index.php" class="btn btn-default">
        Volver al Inicio
    </a>

</div>

</body>
</html>
