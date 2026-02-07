<?php
// =====================================================
// vehiculo_delete.php
// ELIMINAR VEHÍCULO
// SOLO ADM (rol = CRUD)
// =====================================================

session_start();

// -----------------------------------------------------
// Validar acceso
// -----------------------------------------------------
if (!isset($_SESSION["rol"]) || $_SESSION["rol"] !== "CRUD") {
    die("Acceso denegado.");
}

// -----------------------------------------------------
// Validar ID
// -----------------------------------------------------
if (!isset($_GET["id"]) || !is_numeric($_GET["id"])) {
    die("ID de vehículo no válido.");
}

$id = (int) $_GET["id"];

require_once(__DIR__ . "/../conexion/conexion_matriculacion.php");

// -----------------------------------------------------
// ELIMINAR VEHÍCULO
// -----------------------------------------------------
$sql = "DELETE FROM vehiculo WHERE id = ?";
$stmt = $cnMatriculacion->prepare($sql);
$stmt->execute([$id]);

// -----------------------------------------------------
// Volver al listado
// -----------------------------------------------------
header("Location: vehiculos.php");
exit;
