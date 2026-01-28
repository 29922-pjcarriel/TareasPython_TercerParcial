<?php
class vehiculo{
	private $id;
	private $placa;
	private $marca;
	private $motor;
	private $chasis;
	private $combustible;
	private $anio;
	private $color;
	private $foto;
	private $avaluo;
	private $con;
	
	function __construct($cn){
		$this->con = $cn;
	}
		
	public function get_form($id=NULL){
        
		$combustibles = [
			"Gasolina Extra",
			"Diesel",
			"Eléctrico",
			"EcoPais"
		];

		$html = '
		<div class="container mt-4">
		<form name="vehiculo" method="POST" action="index.php" enctype="multipart/form-data">
			<table class="table table-bordered align-middle">
				<tr class="table-dark text-center">
					<th colspan="2">DATOS VEHÍCULO</th>
				</tr>
				<tr>
					<td>Placa:</td>
					<td>
						<input type="text" size="6" name="placa" class="form-control w-50">
					</td>
				</tr>
				<tr>
					<td>Marca:</td>
					<td>' . $this->_get_combo_db("marca","id","descripcion","marcaCMB") . '</td>
				</tr> 
				<tr>
					<td>Motor:</td>
					<td>
						<input type="text" size="15" name="motor" class="form-control">
					</td>
				</tr>	
				<tr>
					<td>Chasis:</td>
					<td>
						<input type="text" size="15" name="chasis" class="form-control">
					</td>
				</tr>
				<tr>
					<td>Combustible:</td>
					<td>' . $this->_get_radio($combustibles, "combustibleRBT") . '</td>
				</tr>
				<tr>
					<td>Año:</td>
					<td>' . $this->_get_combo_anio("anio",2000) . '</td>
				</tr>
				<tr>
					<td>Color:</td>
					<td>' . $this->_get_combo_db("color","id","descripcion","colorCMB") . '</td>
				</tr>
				<tr>
					<td>Foto:</td>
					<td>
						<input type="file" name="foto" class="form-control">
					</td>
				</tr>
				<tr>
					<td>Avalúo:</td>
					<td>
						<input type="text" size="8" name="avaluo" class="form-control w-50">
					</td>
				</tr>
				<tr class="text-center">
					<th colspan="2">
						<input type="submit" name="Guardar" value="GUARDAR" class="btn btn-success px-5">
					</th>
				</tr>												
			</table>
		</form>
		</div>';

		return $html;
	}
    
	//================================================================================================
	// $this->_get_combo_db("marca","id","descripcion","marcaCMB") 
	//================================================================================================
	private function _get_combo_db($tabla,$valor,$etiqueta,$nombre){
		$html = '<select name="' . $nombre . '" class="form-select">';
		$sql = "SELECT $valor,$etiqueta FROM $tabla;";
		$res = $this->con->query($sql);
		while($row = $res->fetch_assoc()){
			$html .= '<option value="' . $row[$valor] . '">' . $row[$etiqueta] . '</option>';
		}
		$html .= '</select>';
		return $html;
	}

	private function _get_combo_anio($nombre,$anio_inicial){
		$html = '<select name="' . $nombre . '" class="form-select w-50">';
		$anio_actual = date('Y');
		for($i=$anio_inicial;$i<=$anio_actual;$i++){
			$html .= '<option value="' . $i . '">' . $i . '</option>';
		}
		$html .= '</select>';
		return $html;
	}
	
	//================================================================================================
	// $this->_get_radio($combustibles, "combustibleRBT")
	//================================================================================================
	private function _get_radio($arreglo,$nombre){
		$html = '<div class="d-flex flex-column">';
		foreach($arreglo as $i=>$etiqueta){
			$checked = ($i==2) ? 'checked' : '';
			$html .= '
			<div class="form-check">
				<input class="form-check-input" type="radio" value="' . $etiqueta . '" name="' . $nombre . '" '.$checked.'>
				<label class="form-check-label">' . $etiqueta . '</label>
			</div>';
		}
		$html .= '</div>';
		return $html;
	}
	
	//================================================================================================
	public function get_list(){
		$html = '
		<div class="container mt-4">
		<table class="table table-bordered table-hover text-center align-middle">
			<tr class="table-dark">
				<th colspan="8">Lista de Vehículos</th>
			</tr>
			<tr class="table-secondary">
				<th>Placa</th>
				<th>Marca</th>
				<th>Color</th>
				<th>Año</th>
				<th>Avalúo</th>
				<th colspan="3">Acciones</th>
			</tr>';

		$sql = "SELECT 
					v.id, 
					v.placa, 
					m.descripcion as marca, 
					c.descripcion as color, 
					v.anio, 
					v.avaluo  
				FROM vehiculo v, color c, marca m 
				WHERE v.marca=m.id AND v.color=c.id;";
		$res = $this->con->query($sql);

		while($row = $res->fetch_assoc()){
			$html .= '
			<tr>
				<td>' . $row['placa'] . '</td>
				<td>' . $row['marca'] . '</td>
				<td>' . $row['color'] . '</td>
				<td>' . $row['anio'] . '</td>
				<td>' . $row['avaluo'] . '</td>
				<td class="text-danger">BORRAR</td>
				<td class="text-warning">ACTUALIZAR</td>
				<td class="text-info">DETALLE</td>
			</tr>';
		}

		$html .= '</table></div>';
		return $html;
	}
	
	//================================================================================================
	private function _message_error($tipo){
        $html = '
		<div class="container mt-5">
			<div class="alert alert-danger text-center">
				Error al ' . $tipo . '. Favor contactar a soporte.
				<br><br>
				<a href="index.php" class="btn btn-primary">Regresar</a>
			</div>
		</div>';
		return $html;
	}
}

// DEBUG (NO eliminar, solo usar cuando haga falta)
function ImpResultQuery($data){
	echo "<pre>";
	print_r($data);
	echo "</pre>"; 
}
?>
