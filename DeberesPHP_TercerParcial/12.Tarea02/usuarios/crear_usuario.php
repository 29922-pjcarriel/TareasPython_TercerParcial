<?php
// =====================================================
// crear_usuario.php
// SOLO SUPERADM (rol = C)
// Crea usuarios AGENTE (rol = R)
// Username = placa del vehículo
// Password fijo = 123
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso (solo SUPERADM)
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "C") {
    die("Acceso denegado. Solo SUPERADM puede crear usuarios.");
}

require_once(__DIR__ . "/../conexion/conexion_usuarios.php");

$mensaje = "";
$error   = "";

// -----------------------------------------------------
// PROCESAR FORMULARIO
// -----------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $username = trim($_POST["username"] ?? "");

    if ($username === "") {
        $error = "Debe ingresar el username (placa del vehículo).";
    } else {

        // -------------------------------------------------
        // Verificar que el username NO se repita
        // -------------------------------------------------
        $sql = "SELECT COUNT(*) FROM usuarios WHERE username = ?";
        $stmt = $cnUsuarios->prepare($sql);
        $stmt->execute([$username]);

        if ($stmt->fetchColumn() > 0) {
            $error = "El username ya existe. No se permiten duplicados.";
        } else {

            // -------------------------------------------------
            // Insertar usuario AGENTE
            // Rol AGENTE = Read = id 2 (según tu script SQL)
            // -------------------------------------------------
            $sql = "
                INSERT INTO usuarios (username, password, roles_id)
                VALUES (?, '123', 2)
            ";
            $stmt = $cnUsuarios->prepare($sql);
            $stmt->execute([$username]);

            $mensaje = "Usuario AGENTE creado correctamente.";
        }
    }
}
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Crear Usuario - SUPERADM</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- Tus estilos -->
    <link rel="stylesheet" href="../Recursos/css/estilos.css" type="text/css">
</head>

<body>

<div class="container" style="margin-top:30px; max-width:600px;">
    <div class="panel panel-success">
        <div class="panel-heading">
            <h3 class="panel-title">
                Crear Usuario AGENTE
            </h3>
        </div>

        <div class="panel-body">

            <?php if ($error !== "") : ?>
                <div class="alert alert-danger">
                    <?= htmlspecialchars($error) ?>
                </div>
            <?php endif; ?>

            <?php if ($mensaje !== "") : ?>
                <div class="alert alert-success">
                    <?= htmlspecialchars($mensaje) ?>
                </div>
            <?php endif; ?>

            <form method="post" action="crear_usuario.php">

                <div class="form-group">
                    <label>Username (Placa del vehículo)</label>
                    <input
                        type="text"
                        name="username"
                        class="form-control"
                        placeholder="Ej: PCH3465"
                        required
                    >
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <input
                        type="text"
                        class="form-control"
                        value="123"
                        disabled
                    >
                    <small class="text-muted">
                        El password por defecto es 123 para todos los usuarios.
                    </small>
                </div>

                <button type="submit" class="btn btn-success btn-block">
                    <span class="glyphicon glyphicon-plus"></span>
                    Crear Usuario
                </button>

                <a href="../index.php" class="btn btn-default btn-block" style="margin-top:10px;">
                    Volver al Inicio
                </a>

            </form>

        </div>
    </div>
</div>

</body>
</html>
