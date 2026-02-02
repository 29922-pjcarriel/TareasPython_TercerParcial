<?php
// =====================================================
// conexion_matriculacion.php
// CONEXIÓN A LA BASE DE DATOS matriculacionfinal
// =====================================================

// Datos de conexión
$host = "localhost";
$db   = "matriculacionfinal";
$user = "root";
$pass = "123";          // XAMPP / WAMP normalmente vacío
$charset = "utf8";

// DSN
$dsn = "mysql:host=$host;dbname=$db;charset=$charset";

try {
    // Crear conexión PDO
    $cnMatriculacion = new PDO($dsn, $user, $pass);

    // Modo de errores
    $cnMatriculacion->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Fetch asociativo por defecto
    $cnMatriculacion->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

} catch (PDOException $e) {
    // Error crítico de conexión
    die("Error de conexión a matriculacionfinal: " . $e->getMessage());
}
