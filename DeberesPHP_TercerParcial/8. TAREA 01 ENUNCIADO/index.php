<?php
  include_once("constantes.php");

  $mod = (isset($_GET['mod'])) ? $_GET['mod'] : 'inicio';
  if($mod == "marcas") $mod = "marca";
?>
<!DOCTYPE html>
<html>
  <head>
    <title>EXAMEN</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>

    <!-- Bootstrap 5 (CDN) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

    <style>
      .box-border { border: 4px solid #6c757d; border-radius: 12px; }
      .header-area { background: #18e7ea; }
      .nav-area { background: #fff200; }
      .footer-area { background: #fff200; }
      .h-hero { min-height: 310px; }

      .video-box { padding: 0; overflow: hidden; }
      .video-box .ratio { height: 100%; }
      .video-box iframe { width: 100%; height: 100%; border: 0; }
    </style>
  </head>

  <body class="<?php echo ($mod=='inicio') ? '' : 'modo-crud'; ?>" style="background:#f8f9fa;">


<?php
  include_once("constantes.php");
  require_once("class/class.vehiculo.php");
  require_once("class/class.matricula.php");
  require_once("class/class.marca.php");

  $cn = conectar();

  $mod = (isset($_GET['mod'])) ? $_GET['mod'] : 'inicio';
  if($mod == "marcas") $mod = "marca";

  $obj = null;

  if($mod == "vehiculo"){
      $obj = new vehiculo($cn);

  }elseif($mod == "matricula"){
      $obj = new matricula($cn);

  }elseif($mod == "marca"){
      $obj = new marca($cn);

  }else{
      $mod = "inicio";
  }
?>

    <!-- =========================
         HEADER (celeste con logo)
         ========================= -->
    <header class="container-fluid py-4 header-area box-border">
      <div class="d-flex justify-content-center align-items-center">
        <img src="Recursos/img/logo_ESPE.png" alt="ESPE" class="img-fluid" style="max-height:95px;">
      </div>
    </header>

    <!-- =========================
         NAVBAR (amarilla)
         ========================= -->
    <nav class="container-fluid nav-area box-border mt-2">
      <div class="container py-2">
        <ul class="nav justify-content-center gap-4">
          <li class="nav-item">
            <a class="nav-link text-dark fw-semibold <?php echo ($mod=='inicio') ? 'fw-bold text-decoration-underline' : ''; ?>"
               href="index.php?mod=inicio">INICIO</a>
          </li>

          <li class="nav-item">
            <a class="nav-link text-dark fw-semibold <?php echo ($mod=='vehiculo') ? 'fw-bold text-decoration-underline' : ''; ?>"
               href="index.php?mod=vehiculo">VEHICULO</a>
          </li>

          <li class="nav-item">
            <a class="nav-link text-dark fw-semibold <?php echo ($mod=='matricula') ? 'fw-bold text-decoration-underline' : ''; ?>"
               href="index.php?mod=matricula">MATRICULA</a>
          </li>

          <li class="nav-item">
            <a class="nav-link text-dark fw-semibold <?php echo ($mod=='marca') ? 'fw-bold text-decoration-underline' : ''; ?>"
               href="index.php?mod=marca">MARCA</a>
          </li>
        </ul>
      </div>
    </nav>


<?php if($mod == "inicio"){ ?>

    <!-- =========================
         CUERPO INICIO (3 columnas)
         ========================= -->
    <main class="container-fluid mt-3">
      <div class="container">
        <div class="row g-3 align-items-stretch">

          <!--Left (Bienvenida) -->
          <div class="col-12 col-lg-3">
            <div class="box-border bg-white h-hero d-flex flex-column justify-content-center p-3 text-center">
              <h5 class="fw-bold mb-2">¡Bienvenidos al CRUD!</h5>
              <p class="mb-2">
                Desde el menú superior podrás gestionar:
              </p>
              <div class="d-grid gap-2">
                <span class="badge text-bg-primary py-2">Vehículo</span>
                <span class="badge text-bg-warning py-2 text-dark">Matrícula</span>
                <span class="badge text-bg-dark py-2">Marca</span>
              </div>
              <hr class="my-3">
              <small class="text-muted">
                Usa <b>NUEVO</b> para registrar y <b>Detalle</b> para ver información completa.
              </small>
            </div>
          </div>

          <!-- Centro (verde) -->
          <div class="col-12 col-lg-5">
            <div class="box-border h-hero d-flex flex-column justify-content-center text-center"
                 style="background:#2f8f2f;">
              <h2 class="text-white fw-bold mb-3">Aplicación de aplicaciones WEB</h2>
              <p class="text-dark fs-5 mb-1">Integrantes: Pamela Carriel, Karla Molina, Josue Tapia</p>
              <p class="text-dark fs-5 mb-1">NRC: 29922</p>
              <p class="text-dark fs-5 mb-0">Fecha: 2026</p>
            </div>
          </div>

          <!-- Derecha (video FULL alto del cuadro) -->
          <div class="col-12 col-lg-4">
            <div class="box-border bg-dark h-hero video-box">
              <div class="ratio ratio-16x9">
                <iframe
                  src="https://www.youtube.com/embed/B03ff1xSMoQ"
                  title="YouTube video"
                  allowfullscreen></iframe>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

<?php } else { ?>

    <!-- =========================
         CUERPO CRUD (solo content)
         ========================= -->
    <main class="container-fluid mt-3">
      <div class="container">
        <div class="box-border bg-white p-3">

          <?php
            // ==========================
            // POST: GUARDAR / UPDATE
            // ==========================
            if(isset($_POST['op'])){

              $opPost = $_POST['op'];

              if($mod=="vehiculo"){
                if($opPost=="new") echo $obj->save_vehiculo();
                elseif($opPost=="update") echo $obj->update_vehiculo();

              }elseif($mod=="matricula"){
                if($opPost=="new") echo $obj->save_matricula();
                elseif($opPost=="update") echo $obj->update_matricula();

              }elseif($mod=="marca"){
                if($opPost=="new") echo $obj->save_marca();
                elseif($opPost=="update") echo $obj->update_marca();
              }

            }else{

              // ==========================
              // GET: new / act / det / del
              // ==========================
              if(isset($_GET['d'])){

                $dato = base64_decode($_GET['d']);
                $tmp = explode("/", $dato);

                $op = $tmp[0];
                $id = $tmp[1];

                // -------- VEHICULO --------
                if($mod=="vehiculo"){
                  if($op=="new") echo $obj->get_form(NULL);
                  elseif($op=="act") echo $obj->get_form($id);
                  elseif($op=="det") echo $obj->get_detail_vehiculo($id);
                  elseif($op=="del") echo $obj->delete_vehiculo($id);
                  else echo $obj->get_list();

                // -------- MATRICULA --------
                }elseif($mod=="matricula"){
                  if($op=="new") echo $obj->get_form(NULL);
                  elseif($op=="act") echo $obj->get_form($id);
                  elseif($op=="det") echo $obj->get_detail_matricula($id);
                  elseif($op=="del") echo $obj->delete_matricula($id);
                  else echo $obj->get_list();

                // -------- MARCA --------
                }elseif($mod=="marca"){
                  if($op=="new") echo $obj->get_form(NULL);
                  elseif($op=="act") echo $obj->get_form($id);
                  elseif($op=="det") echo $obj->get_detail_marca($id);
                  elseif($op=="del") echo $obj->delete_marca($id);
                  else echo $obj->get_list();
                }

              }else{
                // LISTA POR DEFECTO
                echo $obj->get_list();
              }
            }
          ?>

        </div>
      </div>
    </main>

<?php } ?>


    <!-- =========================
         FOOTER (amarillo)
         ========================= -->
    <footer class="container-fluid footer-area box-border mt-3">
      <div class="container py-3 text-center">
        <p class="mb-0 fw-semibold">Contacto</p>
      </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>

  </body>
</html>

<?php
//*******************************************************
function conectar(){
  $c = new mysqli(SERVER,USER,PASS,BD);

  if($c->connect_errno) {
    die("Error de conexión: " . $c->connect_errno . " - " . $c->connect_error);
  }

  $c->set_charset("utf8");
  return $c;
}
//**********************************************************
?>
