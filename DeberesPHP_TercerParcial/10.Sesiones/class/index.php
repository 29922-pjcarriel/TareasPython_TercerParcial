<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sesiones en PHP</title>

  <!-- Bootstrap 5 -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body class="bg-light">

  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <a class="navbar-brand fw-semibold" href="../index.html">Página principal</a>
    </div>
  </nav>

  <div class="container py-4">

    <div class="card shadow-sm border-0">
      <div class="card-body p-4">

        <?php

        require_once("Notebook.php");

        $chronos = new Notebook(2,"Samsung",590000);
        $acer = new Notebook(1,"Acer",350000);
        $compaq = new Notebook(3,"Compaq",260000);
        $dell = new Notebook(4,"Dell",40000);

        $notebooks= array();
        $notebooks['Acer']=$acer;
        $notebooks['Samsung']=$chronos;
        $notebooks['Compaq']=$compaq;
        $notebooks['Dell']=$dell;

        echo "<h1 class='h4 mb-3'>Recorrer un vector con foreach</h1>";

        echo "<div class='table-responsive'>";
        echo "<table class='table table-bordered table-striped align-middle'>";
          echo "<thead class='table-dark'>";
            echo "<tr>";
              echo "<th>Codigo</th>";
              echo "<th>Marca</th>";
              echo "<th>Precio</th>";
            echo "</tr>";
          echo "</thead>";
          echo "<tbody>";

          foreach($notebooks as $obj){
            echo "<tr>";
              echo "<td>".$obj->getCodigo()."</td>";
              echo "<td class='fw-semibold'>".$obj->getMarca()."</td>";
              echo "<td>$ ".$obj->getPrecio()."</td>";
            echo "</tr>";
          }

          echo "</tbody>";
        echo "</table>";
        echo "</div>";

        echo "<hr class='my-4'>";

        // ESCOGER USUARIO PARA SESION (mismo flujo)
        echo "<h2 class='h5 mb-3'>Consultar notebook</h2>";
        echo '<form action="verNotebook.php" method="POST" class="row g-2 align-items-center">';
          echo '<div class="col-12 col-md-6">';
            echo '<select class="form-select" id="op" name="op">';

            foreach($notebooks as $obj){
              echo "<option value=".$obj->getMarca().">".$obj->getMarca()."</option>";
            }

            echo "</select>";
          echo "</div>";

          echo '<div class="col-12 col-md-auto">';
            echo "<button class='btn btn-primary' type='submit' value='consultar'>Consultar</button>";
          echo "</div>";
        echo "</form>";

        session_start();
        $_SESSION['LISTA']=$notebooks;

        ?>

      </div>
    </div>

  </div>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
