<?php
require_once("constantes.php");
include_once("class/class.producto.php");
include_once("class/class.cliente.php");
include_once("class/class.pedido.php");

// ✅ Zona horaria Ecuador
date_default_timezone_set('America/Guayaquil');

/* ============================
   CONEXIÓN
   ============================ */
function conectar(){
  $c = new mysqli(SERVER, USER, PASS, BD);
  if($c->connect_errno){
    die("Error de conexión: ".$c->connect_error);
  }
  $c->set_charset("utf8");
  return $c;
}

$cn = conectar();
$p  = new producto($cn);
$c  = new cliente($cn);
$o  = new pedido($cn);

$contenido = "";

/* ======================================================
   ROUTER: d= base64("op/id") o base64("op/id/id2")
   ====================================================== */
if(isset($_GET["d"])){

  $dato = base64_decode($_GET["d"]);
  $tmp  = explode("/", $dato);

  $op  = $tmp[0];
  $id  = isset($tmp[1]) ? (int)$tmp[1] : 0;
  $id2 = isset($tmp[2]) ? (int)$tmp[2] : 0;

  // =========================
  // PRODUCTOS
  // =========================
  if($op=="plist"){
    $contenido = $p->get_list();
  }elseif($op=="pnew"){
    $contenido = $p->get_form();
  }elseif($op=="pact"){
    $contenido = $p->get_form($id);
  }elseif($op=="pdet"){
    $contenido = $p->get_detail_producto($id);
  }elseif($op=="pdel"){
    ob_start(); $p->delete_producto($id); $contenido = ob_get_clean();

  // =========================
  // CLIENTES
  // =========================
  }elseif($op=="clist"){
    $contenido = $c->get_list();
  }elseif($op=="cnew"){
    $contenido = $c->get_form();
  }elseif($op=="cact"){
    $contenido = $c->get_form($id);
  }elseif($op=="cdet"){
    $contenido = $c->get_detail_cliente($id);
  }elseif($op=="cdel"){
    ob_start(); $c->delete_cliente($id); $contenido = ob_get_clean();

  // =========================
  // ✅ PEDIDOS (FLUJO: lista -> nuevo -> cliente -> productos)
  // =========================
  }elseif($op=="olist"){
    $contenido = $o->get_list_pedidos();

  }elseif($op=="onew"){
    $contenido = $o->get_form_pedido($c); // nuevo

  }elseif($op=="oact"){
    $contenido = $o->get_form_pedido($c, $id); // actualizar cliente (si quieres)

  }elseif($op=="odel"){
    ob_start(); $o->delete_pedido($id); $contenido = ob_get_clean();

  }elseif($op=="odet"){
    $contenido = $o->get_detail_pedido($id);

  }elseif($op=="oitems"){
    $contenido = $o->get_items_form($id); // elegir productos

  }elseif($op=="oadd"){
    $o->pedido_add_item($id, $id2); // redirige

  }elseif($op=="orm"){
    $o->pedido_rm_item($id, $id2); // redirige

  }elseif($op=="oclear"){
    $o->pedido_clear_items($id); // redirige

  }elseif($op=="opay"){
    ob_start(); $o->pagar_pedido($id); $contenido = ob_get_clean();

  }else{
    $contenido = "<div class='alert alert-danger'>Operación no válida</div>";
  }

}else{

  // =========================
  // POST
  // =========================
  if($_SERVER["REQUEST_METHOD"]==="POST"){

    // PRODUCTOS
    if(isset($_POST["Guardar"]) && $_POST["op"]=="pnew"){
      ob_start(); $p->save_producto(); $contenido = ob_get_clean();
    }elseif(isset($_POST["Guardar"]) && $_POST["op"]=="pupdate"){
      ob_start(); $p->update_producto(); $contenido = ob_get_clean();

    // CLIENTES
    }elseif(isset($_POST["Guardar"]) && $_POST["op"]=="cnew"){
      ob_start(); $c->save_cliente(); $contenido = ob_get_clean();
    }elseif(isset($_POST["Guardar"]) && $_POST["op"]=="cupdate"){
      ob_start(); $c->update_cliente(); $contenido = ob_get_clean();

    // ✅ PEDIDOS
    }elseif(isset($_POST["Guardar"]) && $_POST["op"]=="osave"){
      // crea pedido con hora REAL del servidor y redirige a productos
      $o->save_pedido_redirect_to_items(); // redirige y exit

    }elseif(isset($_POST["Guardar"]) && $_POST["op"]=="oupdate"){
      ob_start(); $o->update_pedido(); $contenido = ob_get_clean();

    }elseif(isset($_POST["Actualizar"]) && $_POST["op"]=="oitems_update"){
      $o->pedido_update_qty(); // redirige y exit

    }else{
      $contenido = $o->get_list_pedidos();
    }

  }else{
    // ✅ GET sin d=: arrancar en pedidos
    $contenido = $o->get_list_pedidos();
  }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Carrito CRUD</title>

  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"/>
</head>

<body class="bg-light">

<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container">
    <a class="navbar-brand fw-bold" href="index.php">Carrito CRUD</a>

    <div class="d-flex gap-2">
      <a class="btn btn-outline-light btn-sm" href="index.php?d=<?=base64_encode("olist/0")?>">Pedidos</a>
      <a class="btn btn-outline-light btn-sm" href="index.php?d=<?=base64_encode("plist/0")?>">Productos</a>
      <a class="btn btn-outline-light btn-sm" href="index.php?d=<?=base64_encode("clist/0")?>">Clientes</a>
    </div>
  </div>
</nav>

<div class="container my-4">
  <?=$contenido?>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
