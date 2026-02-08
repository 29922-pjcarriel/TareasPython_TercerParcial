<?php
	session_start();
	
			echo "<br>VARIABLE SESSION: <br>";
			echo "<pre>";
				print_r($_SESSION);
			echo "</pre>";
    
			echo "<br>VARIABLE POST: <br>";
			echo "<pre>";
				print_r($_POST);
			echo "</pre>";
				
	
	$usuario = $_POST['usuario'];
	$clave = $_POST['clave'];   	
    	

	//Conectar a la base de datos
	$conexion = mysqli_connect("localhost", "root", "123", "sesionesbd");
	$consulta = "SELECT * FROM usuarios WHERE usuario = '$usuario' and clave = '$clave'";
	$resultado = mysqli_query($conexion, $consulta);

	$filas = mysqli_num_rows($resultado); //0 si no coincide, 1 o + si concidio
	
	if($filas>0){
		//echo "<br>AUTENTICACION EXISTOSA<br>";
		header("location:verNotebook.php?op=".$usuario);
	}
	else{		
		//echo "<br>Error en la autentificación";
		header("location:ErrorAutentificacion.php");
	}

	mysqli_free_result($resultado);
	mysqli_close($conexion);
?>