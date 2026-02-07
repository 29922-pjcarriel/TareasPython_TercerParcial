<?php
// OPCION 1
session_destroy();

//OPCION 2
//session_start();
//unset($_SESSION['LISTA']);


header("location: index.php");
?>
