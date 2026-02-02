<?php
// =====================================================
// agencia.php
// CRUD DE AGENCIAS (Centro de Matriculación)
// SOLO ADM (rol = CRUD)
// Base de datos: matriculacionfinal
// Tabla: agencia
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso (solo ADM)
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "CRUD") {
    die("Acceso denegado. Solo el rol ADM puede gestionar agencias.");
}

require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

$accion  = $_GET["accion"] ?? "";
$id      = $_GET["id"] ?? null;
$mensaje = "";

// -----------------------------------------------------
// INSERTAR / ACTUALIZAR
// -----------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $id          = $_POST["id"] ?? null;
    $descripcion = trim($_POST["descripcion"]);
    $direccion   = trim($_POST["direccion"]);
    $telefono    = trim($_POST["telefono"]);
    $horainicio  = $_POST["horainicio"];
    $horafin     = $_POST["horafin"];

    if ($id == "") {
        // INSERT
        $sql = "
            INSERT INTO agencia
            (descripcion, direccion, telefono, horainicio, horafin, foto)
            VALUES (?, ?, ?, ?, ?, '')
        ";
        $stmt = $cnMatriculacion->prepare($sql);
        $stmt->execute([
            $descripcion,
            $direccion,
            $telefono,
            $horainicio,
            $horafin
        ]);

        $mensaje = "Agencia registrada correctamente.";
    } else {
        // UPDATE
        $sql = "
            UPDATE agencia
            SET descripcion = ?, direccion = ?, telefono = ?,
                horainicio = ?, horafin = ?
            WHERE id = ?
        ";
        $stmt = $cnMatriculacion->prepare($sql);
        $stmt->execute([
            $descripcion,
            $direccion,
            $telefono,
            $horainicio,
            $horafin,
            $id
        ]);

        $mensaje = "Agencia actualizada correctamente.";
    }
}

// -----------------------------------------------------
// ELIMINAR
// -----------------------------------------------------
if ($accion === "eliminar" && $id) {
    $sql = "DELETE FROM agencia WHERE id = ?";
    $stmt = $cnMatriculacion->prepare($sql);
    $stmt->execute([$id]);
    $mensaje = "Agencia eliminada correctamente.";
}

// -----------------------------------------------------
// OBTENER AGENCIA PARA EDITAR
// -----------------------------------------------------
$agenciaEditar = null;
if ($accion === "editar" && $id) {
    $sql = "SELECT * FROM agencia WHERE id = ?";
    $stmt = $cnMatriculacion->prepare($sql);
    $stmt->execute([$id]);
    $agenciaEditar = $stmt->fetch();
}

// -----------------------------------------------------
// LISTADO DE AGENCIAS
// -----------------------------------------------------
$sql = "SELECT * FROM agencia ORDER BY id";
$stmt = $cnMatriculacion->prepare($sql);
$stmt->execute();
$agencias = $stmt->fetchAll();
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>CRUD Agencias</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- Estilos -->
    <link rel="stylesheet" href="../Recursos/css/estilos.css">
</head>

<body>

<div class="container" style="margin-top:30px; max-width:950px;">

    <h2>Gestión de Centros de Matriculación (Agencias)</h2>
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
            <strong><?= $agenciaEditar ? "Editar Agencia" : "Nueva Agencia" ?></strong>
        </div>

        <div class="panel-body">
            <form method="post" action="agencia.php">

                <input type="hidden" name="id"
                       value="<?= $agenciaEditar["id"] ?? "" ?>">

                <div class="form-group">
                    <label>Descripción</label>
                    <input type="text" name="descripcion"
                           class="form-control"
                           value="<?= $agenciaEditar["descripcion"] ?? "" ?>"
                           required>
                </div>

                <div class="form-group">
                    <label>Dirección</label>
                    <input type="text" name="direccion"
                           class="form-control"
                           value="<?= $agenciaEditar["direccion"] ?? "" ?>"
                           required>
                </div>

                <div class="form-group">
                    <label>Teléfono</label>
                    <input type="text" name="telefono"
                           class="form-control"
                           value="<?= $agenciaEditar["telefono"] ?? "" ?>"
                           required>
                </div>

                <div class="row">
                    <div class="col-sm-6">
                        <div class="form-group">
                            <label>Hora Inicio</label>
                            <input type="time" name="horainicio"
                                   class="form-control"
                                   value="<?= $agenciaEditar["horainicio"] ?? "" ?>"
                                   required>
                        </div>
                    </div>

                    <div class="col-sm-6">
                        <div class="form-group">
                            <label>Hora Fin</label>
                            <input type="time" name="horafin"
                                   class="form-control"
                                   value="<?= $agenciaEditar["horafin"] ?? "" ?>"
                                   required>
                        </div>
                    </div>
                </div>

                <button type="submit" class="btn btn-success">
                    <?= $agenciaEditar ? "Actualizar" : "Guardar" ?>
                </button>

                <?php if ($agenciaEditar) : ?>
                    <a href="agencia.php" class="btn btn-default">Cancelar</a>
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
                    <th>Dirección</th>
                    <th>Teléfono</th>
                    <th>Horario</th>
                    <th>Acciones</th>
                </tr>
            </thead>

            <tbody>
            <?php foreach ($agencias as $a) : ?>
                <tr>
                    <td><?= $a["id"] ?></td>
                    <td><?= htmlspecialchars($a["descripcion"]) ?></td>
                    <td><?= htmlspecialchars($a["direccion"]) ?></td>
                    <td><?= htmlspecialchars($a["telefono"]) ?></td>
                    <td>
                        <?= $a["horainicio"] ?> - <?= $a["horafin"] ?>
                    </td>
                    <td>
                        <a href="agencia.php?accion=editar&id=<?= $a["id"] ?>"
                           class="btn btn-xs btn-primary">
                            Editar
                        </a>
                        <a href="agencia.php?accion=eliminar&id=<?= $a["id"] ?>"
                           class="btn btn-xs btn-danger"
                           onclick="return confirm('¿Eliminar esta agencia?');">
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
