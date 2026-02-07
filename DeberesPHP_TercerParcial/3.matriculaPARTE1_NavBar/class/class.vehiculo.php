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
        
		$combustibles = ["Gasolina Extra",
						 "Diesel",
						 "Eléctrico",
						 "EcoPais"
						 ];
		$html = '
		<form name="vehiculo" method="POST" action="index.php" enctype="multipart/form-data">
			<table border="1" align="center">
				<tr>
					<th colspan="2">DATOS VEHÍCULO</th>
				</tr>
				<tr>
					<td>Placa:</td>
					<td><input type="text" size="6" name="placa"></td>
				</tr>
				<tr>
					<td>Marca:</td>
					<td>' . $this->_get_combo_db("marca","id","descripcion","marcaCMB") . '</td>
				</tr> 
				<tr>
					<td>Motor:</td>
					<td><input type="text" size="15" name="motor"></td>
				</tr>	
				<tr>
					<td>Chasis:</td>
					<td><input type="text" size="15" name="chasis"></td>
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
					<td><input type="file" name="foto"></td>
				</tr>
				<tr>
					<td>Avalúo:</td>
					<td><input type="text" size="8" name="avaluo"></td>
				</tr>
				<tr>
					<th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
				</tr>												
			</table>';
		return $html;
	}
    
	
//*****************************  CERRAR LA CONEXION A LA BASE DE DATOS ***************************************************************************	   
 
 
 
//*************************************************************************************************        






	/*
     $this->_get_combo_db("marca","id","descripcion","marcaCMB") 
	 $tabla es la tabla de la base de datos
	 $valor es el nombre del campo que utilizaremos como valor del option
	 $etiqueta es nombre del campo que utilizaremos como etiqueta del option
	 $nombre es el nombre del campo tipo combo box (select)
	 */ 
    
	private function _get_combo_db($tabla,$valor,$etiqueta,$nombre){
		$html = '<select name="' . $nombre . '">';
		$sql = "SELECT $valor,$etiqueta FROM $tabla;";
		$res = $this->con->query($sql);
		while($row = $res->fetch_assoc()){
			//ImpResultQuery($row);
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
	
    // $this->_get_radio($combustibles, "combustibleRBT")
	private function _get_radio($arreglo,$nombre){
		$html = '
		<table border=0 align="left">';
		foreach($arreglo as $i=>$etiqueta){
            $html .= '
			<tr>
				<td>' . $etiqueta . '</td>';
            $html .= ($i==2) ?  '<td><input type="radio" value="' . $etiqueta . '" name="' . $nombre . '" checked/></td>' : '<td><input type="radio" value="' . $etiqueta . '" name="' . $nombre . '"/></td>';
			$html .= '</tr>';
		}
		$html .= '
		</table>';
		return $html;
	}
	
	//***********************************************************************************************	
	public function get_list(){
		$html = '
		<table border="1" align="center">
			<tr>
				<th colspan="8">Lista de Vehículos</th>
			</tr>
			<tr>
				<th>Placa</th>
				<th>Marca</th>
				<th>Color</th>
				<th>Año</th>
				<th>Avalúo</th>
				<th colspan="3">Acciones</th>
			</tr>';
		$sql = "SELECT v.id, v.placa, m.descripcion as marca, c.descripcion as color, v.anio, v.avaluo  FROM vehiculo v, color c, marca m WHERE v.marca=m.id AND v.color=c.id;";	
		$res = $this->con->query($sql);
		while($row = $res->fetch_assoc()){
			
			//ImpResultQuery($row);
			
			$html .= '
				<tr>
					<td>' . $row['placa'] . '</td>
					<td>' . $row['marca'] . '</td>
					<td>' . $row['color'] . '</td>
					<td>' . $row['anio'] . '</td>
					<td>' . $row['avaluo'] . '</td>
					<td>BORRAR</td>
					<td>ACTUALIZAR</td>
					<td>DETALLE</td>
				</tr>';
		
		
		}
		$html .= '  
				</table>';
		
		return $html;
		
	}
	

//******************************************************************************************
	private function _message_error($tipo){
        $html = '
		<table border="0" align="center">
			<tr>
				<th>Error al ' . $tipo . '. Favor contactar a ..............</th>
			</tr>
			<tr>
				<th><a href="index.php">Regresar</a></th>
			</tr>
		</table>';
		return $html;
	}
	
	
	
//*******************************************************************************************************************


}



function ImpResultQuery($data){
	
			echo "<pre>";
				print_r($data);
			echo "</pre>"; 

 }
 
 

?>

