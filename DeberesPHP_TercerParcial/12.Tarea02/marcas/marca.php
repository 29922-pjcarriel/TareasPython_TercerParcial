<?php
// =====================================================
// marca.php
// CRUD DE MARCAS
// SOLO ADM (rol = CRUD)
// Base de datos: matriculacionfinal
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso (solo ADM)
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "CRUD") {
    die("Acceso denegado. Solo el rol ADM puede gestionar marcas.");
}

require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

$accion  = $_GET["accion"] ?? "";
$id      = $_GET["id"] ?? null;
$mensaje = "";

// -----------------------------------------------------
// INSERTAR / ACTUALIZAR
// -----------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $id         = $_POST["id"] ?? null;
    $descripcion = trim($_POST["descripcion"]);
    $pais        = trim($_POST["pais"]);
    $direccion   = trim($_POST["direccion"]);

    if ($id == "") {
        // INSERT
        $sql = "INSERT INTO marca (descripcion, pais, direccion)
                VALUES (?, ?, ?)";
        $stmt = $cnMatriculacion->prepare($sql);
        $stmt->execute([$descripcion, $pais, $direccion]);
        $mensaje = "Marca registrada correctamente.";
    } else {
        // UPDATE
        $sql = "UPDATE marca
                SET descripcion = ?, pais = ?, direccion = ?
                WHERE id = ?";
        $stmt = $cnMatriculacion->prepare($sql);
        $stmt->execute([$descripcion, $pais, $direccion, $id]);
        $mensaje = "Marca actualizada correctamente.";
    }
}

// -----------------------------------------------------
// ELIMINAR
// -----------------------------------------------------
if ($accion === "eliminar" && $id) {
    $sql = "DELETE FROM marca WHERE id = ?";
    $stmt = $cnMatriculacion->prepare($sql);
    $stmt->execute([$id]);
    $mensaje = "Marca eliminada correctamente.";
}

// -----------------------------------------------------
// OBTENER MARCA PARA EDITAR
// -----------------------------------------------------
$marcaEditar = null;
if ($accion === "editar" && $id) {
    $sql = "SELECT * FROM marca WHERE id = ?";
    $stmt = $cnMatriculacion->prepare($sql);
    $stmt->execute([$id]);
    $marcaEditar = $stmt->fetch();
}

// -----------------------------------------------------
// LISTADO DE MARCAS
// -----------------------------------------------------
$sql = "SELECT * FROM marca ORDER BY id";
$stmt = $cnMatriculacion->prepare($sql);
$stmt->execute();
$marcas = $stmt->fetchAll();
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>CRUD Marcas</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- Estilos -->
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

<div class="container" style="margin-top:30px; max-width:900px;">

    <h2>Gestión de Marcas</h2>
    <p>
        Usuario: <strong><?= htmlspecialchars($_SESSION["username"]) ?></strong>
        | Rol: <strong>ADM</strong>
    </p>
    <hr>

    <?php if ($mensaje !== "") : ?>
        <div class="alert alert-success">
            <?= htmlspecialchars($mensaje) ?>
        </div>
    <?php endif; ?>

    <!-- FORMULARIO -->
    <div class="panel panel-success">
        <div class="panel-heading">
            <strong><?= $marcaEditar ? "Editar Marca" : "Nueva Marca" ?></strong>
        </div>

        <div class="panel-body">
            <form method="post" action="marca.php">

                <input type="hidden" name="id"
                       value="<?= $marcaEditar["id"] ?? "" ?>">

                <div class="form-group">
                    <label>Descripción</label>
                    <input type="text" name="descripcion"
                           class="form-control"
                           value="<?= $marcaEditar["descripcion"] ?? "" ?>"
                           required>
                </div>

                <div class="form-group">
                    <label>País</label>
                    <input type="text" name="pais"
                           class="form-control"
                           value="<?= $marcaEditar["pais"] ?? "" ?>"
                           required>
                </div>

                <div class="form-group">
                    <label>Dirección</label>
                    <input type="text" name="direccion"
                           class="form-control"
                           value="<?= $marcaEditar["direccion"] ?? "" ?>">
                </div>

                <button type="submit" class="btn btn-success">
                    <?= $marcaEditar ? "Actualizar" : "Guardar" ?>
                </button>

                <?php if ($marcaEditar) : ?>
                    <a href="marca.php" class="btn btn-default">Cancelar</a>
                <?php endif; ?>
            </form>
        </div>
    </div>

    <hr>

    <!-- LISTADO -->
    <div class="table-responsive">
        <table class="table table-bordered table-striped">

            <thead class="bg-success">
                <tr>
                    <th>ID</th>
                    <th>Descripción</th>
                    <th>País</th>
                    <th>Dirección</th>
                    <th>Acciones</th>
                </tr>
            </thead>

            <tbody>
            <?php foreach ($marcas as $m) : ?>
                <tr>
                    <td><?= $m["id"] ?></td>
                    <td><?= htmlspecialchars($m["descripcion"]) ?></td>
                    <td><?= htmlspecialchars($m["pais"]) ?></td>
                    <td><?= htmlspecialchars($m["direccion"]) ?></td>
                    <td>
                        <a href="marca.php?accion=editar&id=<?= $m["id"] ?>"
                           class="btn btn-xs btn-primary">
                            Editar
                        </a>
                        <a href="marca.php?accion=eliminar&id=<?= $m["id"] ?>"
                           class="btn btn-xs btn-danger"
                           onclick="return confirm('¿Eliminar esta marca?');">
                            Eliminar
                        </a>
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
