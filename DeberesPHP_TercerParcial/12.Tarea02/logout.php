<?php
// =====================================================
// logout.php
// CIERRE DE SESIÓN DEL SISTEMA
// =====================================================

session_start();

// Elimina todas las variables de sesión
session_unset();

// Destruye la sesión
session_destroy();

// Redirige al inicio (login)
header("Location: index.php");
exit;
