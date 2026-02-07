<?php
class matricula{
	private $id;
	private $fecha;
	private $vehiculo;
	private $agencia;
	private $anio;
	private $con;
	
	function __construct($cn){
		$this->con = $cn;
	}
		
	public function get_form($id=NULL){

		$html = '
		<form name="matricula" method="POST" action="matricula.php">
			<table border="1" align="center">
				<tr>
					<th colspan="2">DATOS MATRÍCULA</th>
				</tr>

				<tr>
					<td>Fecha:</td>
					<td><input type="date" name="fecha"></td>
				</tr>

				<tr>
					<td>Vehículo:</td>
					<td>' . $this->_get_combo_db("vehiculo","id","placa","vehiculoCMB") . '</td>
				</tr>

				<tr>
					<td>Agencia:</td>
					<td>' . $this->_get_combo_db("agencia","id","descripcion","agenciaCMB") . '</td>
				</tr>

				<tr>
					<td>Año:</td>
					<td>' . $this->_get_combo_anio("anio",2000) . '</td>
				</tr>

				<tr>
					<th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
				</tr>												
			</table>';
		return $html;
	}

	/*
	 $this->_get_combo_db("tabla","campo_valor","campo_etiqueta","nombreSelect") 
	*/
	private function _get_combo_db($tabla,$valor,$etiqueta,$nombre){
		$html = '<select name="' . $nombre . '">';
		$sql = "SELECT $valor,$etiqueta FROM $tabla;";
		$res = $this->con->query($sql);

		while($res && $row = $res->fetch_assoc()){
			$html .= '<option value="' . $row[$valor] . '">' . $row[$etiqueta] . '</option>' . "\n";
		}

		$html .= '</select>';
		return $html;
	}

	private function _get_combo_anio($nombre,$anio_inicial){
		$html = '<select name="' . $nombre . '">';
		$anio_actual = date('Y');
		for($i=$anio_inicial;$i<=$anio_actual;$i++){
			$html .= '<option value="' . $i . '">' . $i . '</option>' . "\n";
		}
		$html .= '</select>';
		return $html;
	}
	
	public function get_list(){
		$html = '
		<table border="1" align="center">
			<tr>
				<th colspan="6">Lista de Matrículas</th>
			</tr>
			<tr>
				<th>Fecha</th>
				<th>Vehículo</th>
				<th>Agencia</th>
				<th>Año</th>
				<th colspan="3">Acciones</th>
			</tr>';

		$sql = "SELECT m.id, m.fecha, v.placa as vehiculo, a.descripcion as agencia, m.anio
				FROM matricula m, vehiculo v, agencia a
				WHERE m.vehiculo = v.id AND m.agencia = a.id;";
		
		$res = $this->con->query($sql);

		while($res && $row = $res->fetch_assoc()){
			$html .= '
				<tr>
					<td>' . $row['fecha'] . '</td>
					<td>' . $row['vehiculo'] . '</td>
					<td>' . $row['agencia'] . '</td>
					<td>' . $row['anio'] . '</td>
					<td>BORRAR</td>
					<td>ACTUALIZAR</td>
					<td>DETALLE</td>
				</tr>';
		}

		$html .= '</table>';
		return $html;
	}


	private function _message_error($tipo){
        $html = '
		<table border="0" align="center">
			<tr>
				<th>Error al ' . $tipo . '. Favor contactar a ..............</th>
			</tr>
			<tr>
				<th><a href="matricula.php">Regresar</a></th>
			</tr>
		</table>';
		return $html;
	}
}

function ImpResultQuery($data){
	echo "<pre>";
		print_r($data);
	echo "</pre>"; 
}
?>
