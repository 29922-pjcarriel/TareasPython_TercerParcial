<?php
// =====================================================
// index.php
// LOGIN CON MODAL + HOME DINÁMICO SEGÚN ROL (SESIONES)
// =====================================================

session_start();

// -----------------------------------------------------
// CONEXIÓN A usuariosdb
// -----------------------------------------------------
require_once(__DIR__ . "/conexion/conexion_usuarios.php");

// -----------------------------------------------------
// Variables de sesión
// -----------------------------------------------------
$rol = $_SESSION["rol"] ?? null;        // R | CRUD | C
$username_sesion = $_SESSION["username"] ?? null;
$error = "";

// -----------------------------------------------------
// FUNCIÓN: detectar si username es PLACA
// (3 letras + 3 o 4 números)
// -----------------------------------------------------
function esPlaca($username) {
    return preg_match('/^[A-Z]{3}[0-9]{3,4}$/', $username);
}

// -----------------------------------------------------
// LOGIN (DESDE MODAL)
// -----------------------------------------------------
if ($_SERVER["REQUEST_METHOD"] === "POST"
    && isset($_POST["accion"])
    && $_POST["accion"] === "login"
) {

    $user = trim($_POST["username"] ?? "");
    $pass = trim($_POST["password"] ?? "");

    if ($user === "" || $pass === "") {
        $error = "Debe ingresar usuario y contraseña.";
    } else {

        $sql = "
            SELECT u.username, r.rol
            FROM usuarios u
            JOIN roles r ON u.roles_id = r.id
            WHERE u.username = ? AND u.password = ?
            LIMIT 1
        ";

        $stmt = $cnUsuarios->prepare($sql);
        $stmt->execute([$user, $pass]);
        $row = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($row) {
            $_SESSION["username"] = $row["username"];
            $_SESSION["rol"] = $row["rol"];
            header("Location: index.php");
            exit;
        } else {
            $error = "Usuario o contraseña incorrectos.";
        }
    }
}

// -----------------------------------------------------
// LOGOUT
// -----------------------------------------------------
if (isset($_GET["logout"]) && $_GET["logout"] == "1") {
    session_unset();
    session_destroy();
    header("Location: index.php");
    exit;
}

// -----------------------------------------------------
// DEFINIR ROL REAL (SIN BD EXTRA)
// -----------------------------------------------------
$rolNombre = "INVITADO";
$rolReal   = null;

if ($rol === "CRUD") {
    $rolNombre = "ADMINISTRADOR";
    $rolReal   = "ADM";

} elseif ($rol === "C") {
    $rolNombre = "SUPERADMIN";
    $rolReal   = "SUPERADM";

} elseif ($rol === "R") {

    // 👇 CLAVE: si el username es una placa → ES DUEÑO
    if ($username_sesion && esPlaca($username_sesion)) {
        $rolNombre = "DUEÑO DEL VEHÍCULO";
        $rolReal   = "DUEÑO";
    } else {
        $rolNombre = "AGENTE";
        $rolReal   = "AGENTE";
    }
}
?>
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Aplicación Web</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- Estilos -->
    <link rel="stylesheet" href="Recursos/css/estilos.css">
    <link rel="stylesheet" href="Recursos/icons/style.css">
</head>

<body>

<!-- ================= HEADER ================= -->
<div class="container-fluid">
    <div class="row">
        <header class="col-xs-12 text-center">
            <img src="Recursos/img/logo_ESPE.png"
                 class="img-responsive center-block"
                 style="max-height:100px"
                 alt="ESPE">
        </header>
    </div>
</div>

<!-- ================= NAVBAR ================= -->
<nav class="navbar navbar-inverse">
    <div class="container-fluid">

        <div class="navbar-header">
            <button type="button" class="navbar-toggle"
                    data-toggle="collapse" data-target="#main-nav">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <span class="navbar-brand">Grupo 5</span>
        </div>

        <div class="collapse navbar-collapse" id="main-nav">
            <ul class="nav navbar-nav">

                <?php if ($rolReal === "AGENTE"): ?>
                    <li><a href="vehiculos/vehiculos.php">Vehículos</a></li>

                <?php elseif ($rolReal === "DUEÑO"): ?>
                    <!-- 🔐 DUEÑO VA SOLO A SU ARCHIVO -->
                    <li><a href="vehiculos/mi_vehiculo.php">Mi Vehículo</a></li>

                <?php elseif ($rolReal === "ADM"): ?>
                    <li><a href="vehiculos/vehiculos.php">CRUD VEHÍCULOS</a></li>
                    <li><a href="marcas/marca.php">CRUD MARCAS</a></li>
                    <li><a href="agencias/agencia.php">CRUD AGENCIAS</a></li>

                <?php elseif ($rolReal === "SUPERADM"): ?>
                    <li><a href="usuarios/crear_usuario.php">CREAR USUARIOS</a></li>
                <?php endif; ?>

            </ul>

            <ul class="nav navbar-nav navbar-right">
                <?php if (!$rol): ?>
                    <li>
                        <button class="btn btn-success navbar-btn"
                                data-toggle="modal"
                                data-target="#modalLogin">
                            Iniciar Sesión
                        </button>
                    </li>
                <?php else: ?>
                    <li class="navbar-text">
                        <?= htmlspecialchars($username_sesion) ?> |
                        <strong><?= $rolNombre ?></strong>
                    </li>
                    <li>
                        <a href="index.php?logout=1"
                           class="btn btn-danger navbar-btn">
                            Cerrar Sesión
                        </a>
                    </li>
                <?php endif; ?>
            </ul>

        </div>
    </div>
</nav>

<!-- ================= CONTENIDO ================= -->
<div class="container-fluid">
    <div class="row">

        <!-- LEFT -->
        <aside class="col-sm-3">
            <div class="box white">
                <h4 class="text-center">Estado del Sistema</h4>
                <hr>
                <?php if ($rol): ?>
                    <p><strong>Usuario:</strong> <?= htmlspecialchars($username_sesion) ?></p>
                    <p><strong>Rol:</strong> <?= $rolNombre ?></p>
                <?php else: ?>
                    <p class="text-center">Inicie sesión para acceder al sistema.</p>
                <?php endif; ?>
            </div>
        </aside>

        <!-- CENTER -->
        <main class="col-sm-6">
            <div class="box soft-green text-center">
                <h2>Aplicación de Tecnologías WEB</h2>
                <hr>

                <p><strong>Estudiantes:</strong></p>
                <p>Pamela Carriel</p>
                <p>Karla Molina</p>
                <p>Josue Tapia</p>

                <hr>
                <p><strong>NRC:</strong> 29922</p>
                <p><strong>Grupo:</strong> 05</p>
                <p><strong>Fecha:</strong> 30 de octubre del 2025</p>
            </div>
        </main>

        <!-- RIGHT -->
        <section class="col-sm-3">
            <div class="box dark-green">
                <iframe width="100%" height="220"
                        src="https://www.youtube.com/embed/_mLQ4BaMPoY?autoplay=1&mute=1"
                        frameborder="0"
                        allowfullscreen>
                </iframe>
            </div>
        </section>

    </div>
</div>

<!-- ================= MODAL LOGIN ================= -->
<div class="modal fade" id="modalLogin">
    <div class="modal-dialog modal-sm">
        <div class="modal-content">

            <div class="modal-header">
                <h4 class="modal-title text-center">🔐 Inicio de Sesión</h4>
            </div>

            <form method="post">
                <input type="hidden" name="accion" value="login">

                <div class="modal-body">

                    <?php if ($error): ?>
                        <div class="alert alert-danger text-center">
                            <?= htmlspecialchars($error) ?>
                        </div>
                    <?php endif; ?>

                    <div class="form-group">
                        <label>Usuario</label>
                        <input name="username" class="form-control" required>
                    </div>

                    <div class="form-group">
                        <label>Password</label>
                        <input name="password"
                               type="password"
                               class="form-control"
                               value="123"
                               required>
                        <small class="text-muted">
                            Contraseña por defecto: <b>123</b>
                        </small>
                    </div>

                </div>

                <div class="modal-footer">
                    <button class="btn btn-success btn-block">
                        Ingresar
                    </button>
                </div>
            </form>

        </div>
    </div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

<?php if ($error): ?>
<script>
    $('#modalLogin').modal('show');
</script>
<?php endif; ?>

</body>
</html>
