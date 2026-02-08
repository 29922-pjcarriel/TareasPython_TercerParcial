<html>
  <head>
    <meta charset="utf-8">
    <title>Sesiones en PHP</title>

    <!-- BOOTSTRAP CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>

  <body class="bg-light">

    <div class="container py-5">

      <div class="card shadow mx-auto" style="max-width: 700px;">
        <div class="card-body text-center">

          <a href="../index.html" class="btn btn-outline-secondary mb-4">
            Página principal
          </a>

          <h2 class="fw-bold mb-4">HOME PAGE</h2>

<?php
require_once("Notebook.php");

			$chronos = new Notebook(2,"Samsung",5900);
			$acer = new Notebook(1,"Acer",3500.50);
			$compaq = new Notebook(3,"Compaq",2600.33);
			$lenovo = new Notebook(4,"Lenovo",1555.00);

			$notebooks= array();
			$notebooks['Acer']=$acer;
			$notebooks['Samsung']=$chronos;
			$notebooks['Compaq']=$compaq;
			$notebooks['Lenovo']=$lenovo;
			
	echo"<br><br>";
	
	echo '<form action="verNotebook.php" method="POST" class="d-flex flex-column align-items-center gap-3">';
		echo '<select id="op" name="op" class="form-select" style="max-width: 350px;">';
				
			foreach($notebooks as $n){
					echo "<option value=".$n->getMarca().">".$n->getMarca()."</option>";
			}
		echo "</select>";
		echo "<button type='submit' value='consultar' class='btn btn-primary'>Session</button>";
		

		session_start();
		$_SESSION['listaNote']=$notebooks;

		echo "</br></br>";
		echo "<a href='FormularioLogin.php' class='btn btn-link'>Login</a>";
	
	echo "</form>";

?>

        </div>
      </div>

    </div>

    <!-- BOOTSTRAP JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
