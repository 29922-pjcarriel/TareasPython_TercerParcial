# =====================================================
# app.py — CLON IDÉNTICO DEL PHP EN PYTHON
# HTML embebido, sin templates, sin archivos CSS
# SESIÓN GLOBAL (no Flask session — test_client la pierde)
# REDIRECT por JS (no Flask redirect — launcher pierde headers)
# =====================================================
import os, sys, re
import mysql.connector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_db_usuarios, get_db_matriculacion
from flask import Flask, request, make_response
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'tarea02_key'

# =====================================================
# SESIÓN PERSISTENTE EN ARCHIVO JSON
# (el launcher re-ejecuta exec_module cada request,
#  por lo que variables globales se pierden)
# =====================================================
import json

_SESION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_sesion.json')

def _cargar_sesion():
    try:
        with open(_SESION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def _guardar_sesion(data):
    with open(_SESION_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)

class SesionPersistente(dict):
    """Dict que se auto-guarda en disco al modificarse"""
    def __init__(self):
        super().__init__(_cargar_sesion())
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        _guardar_sesion(dict(self))
    def __delitem__(self, key):
        super().__delitem__(key)
        _guardar_sesion(dict(self))
    def clear(self):
        super().clear()
        _guardar_sesion({})
    def pop(self, key, *args):
        result = super().pop(key, *args)
        _guardar_sesion(dict(self))
        return result

SESION = SesionPersistente()

PREFIX = "/Tarea02/app.py"

def u(path=""):
    if path and not path.startswith("/"): path = "/" + path
    return PREFIX + path

def redir(path):
    full = u(path)
    return f'<html><head><meta http-equiv="refresh" content="0;url={full}"></head><body><script>window.location.href="{full}"</script></body></html>'

def es_placa(username):
    return bool(re.match(r'^[A-Z]{3}[0-9]{3,4}$', username or ''))

def get_rol_info():
    rol = SESION.get('rol')
    username = SESION.get('username')
    rn, rr = "INVITADO", None
    if rol == "CRUD": rn, rr = "ADMINISTRADOR", "ADM"
    elif rol == "C": rn, rr = "SUPERADMIN", "SUPERADM"
    elif rol == "R":
        if username and es_placa(username): rn, rr = "DUEÑO DEL VEHÍCULO", "DUEÑO"
        else: rn, rr = "AGENTE", "AGENTE"
    return rol, rn, rr, username

# =====================================================
# CSS EMBEBIDO
# =====================================================
CSS = '''
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:auto}
body{width:100%;margin:0;font-family:"Poppins",sans-serif;text-align:center;
background:linear-gradient(135deg,#e8f5e9 0%,#f0fff0 100%);color:#1b1b1b}
h2{text-align:center;margin-bottom:25px;color:#006633;font-size:32px;font-weight:700;letter-spacing:1px}
p{font-size:18px;margin:5px 0;color:#1b1b1b}
.box{border-radius:10px;box-shadow:0 6px 16px rgba(0,0,0,.15);padding:20px;margin-bottom:20px;border:3px solid transparent}
.white{background:#fff;border-color:#e8fff3}
.soft-green{background:#eafaf0;border-color:#006633;color:#004d26}
.dark-green{background:#00331a;border-color:#004d26}
.container-fluid>.row{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;margin-top:20px;margin-bottom:20px}
.navbar-inverse{background:linear-gradient(135deg,#1b5e20,#2e7d32);border:none}
.navbar-inverse .navbar-brand,.navbar-inverse .navbar-nav>li>a,.navbar-text{color:#fff!important;font-weight:500}
.navbar-inverse .navbar-nav>li>a:hover{background-color:rgba(255,255,255,.15);border-radius:4px}
.modal-content{border-radius:10px;box-shadow:0 15px 40px rgba(0,0,0,.3);border:none}
.modal-header{background:linear-gradient(135deg,#1b5e20,#43a047);color:#fff;border-top-left-radius:10px;border-top-right-radius:10px;text-align:center}
.modal-header h4{font-weight:700;letter-spacing:1px}
.modal-body{padding:25px}.modal-body label{font-weight:600;color:#2e7d32}
.modal-body .form-control{height:45px;border-radius:6px;font-size:15px}
.modal-footer{padding:15px 25px;border-top:none}
.modal-footer .btn{height:45px;font-size:16px;font-weight:600;border-radius:25px}
.btn-success{background:linear-gradient(135deg,#2e7d32,#66bb6a);border:none}
.btn-danger{background:linear-gradient(135deg,#c62828,#ef5350);border:none}
'''

def page(titulo, body, show_nav=True, extra_js=""):
    rol, rn, rr, usr = get_rol_info()
    nav = ""
    if show_nav:
        items = ""
        if rr == "AGENTE": items = f'<li><a href="{u("/vehiculos")}">Vehículos</a></li>'
        elif rr == "DUEÑO": items = f'<li><a href="{u("/mi_vehiculo")}">Mi Vehículo</a></li>'
        elif rr == "ADM": items = f'<li><a href="{u("/vehiculos")}">CRUD VEHÍCULOS</a></li><li><a href="{u("/marcas")}">CRUD MARCAS</a></li><li><a href="{u("/agencias")}">CRUD AGENCIAS</a></li>'
        elif rr == "SUPERADM": items = f'<li><a href="{u("/usuarios")}">CREAR USUARIOS</a></li>'
        if not rol:
            right = '<li><button class="btn btn-success navbar-btn" data-toggle="modal" data-target="#modalLogin">Iniciar Sesión</button></li>'
        else:
            right = f'<li class="navbar-text">{escape(usr or "")} | <strong>{escape(rn)}</strong></li><li><a href="{u("/?logout=1")}" class="btn btn-danger navbar-btn">Cerrar Sesión</a></li>'
        nav = f'''<nav class="navbar navbar-inverse"><div class="container-fluid">
<div class="navbar-header"><button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#mn"><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button><span class="navbar-brand">Grupo 5</span></div>
<div class="collapse navbar-collapse" id="mn"><ul class="nav navbar-nav">{items}</ul><ul class="nav navbar-nav navbar-right">{right}</ul></div></div></nav>'''
    
    header_img = f'''<div class="container-fluid"><div class="row"><header class="col-xs-12 text-center">
<img src="/Tarea02/static/img/logo_ESPE.png" class="img-responsive center-block" style="max-height:100px" alt="ESPE">
</header></div></div>'''

    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{escape(titulo)}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
<style>{CSS}</style></head><body>{header_img}{nav}{body}
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
{extra_js}</body></html>'''

# =====================================================
# INDEX + LOGIN + LOGOUT
# =====================================================
@app.route('/', methods=['GET','POST'])
def index():
    error = ""
    if request.method == 'POST' and request.form.get('accion') == 'login':
        user = request.form.get('username','').strip()
        pw = request.form.get('password','').strip()
        if not user or not pw:
            error = "Debe ingresar usuario y contraseña."
        else:
            cn = get_db_usuarios()
            if cn:
                cur = cn.cursor(dictionary=True)
                cur.execute("SELECT u.username, r.rol FROM usuarios u JOIN roles r ON u.roles_id=r.id WHERE u.username=%s AND u.password=%s LIMIT 1",(user,pw))
                row = cur.fetchone(); cur.close(); cn.close()
                if row:
                    SESION['username'] = row['username']; SESION['rol'] = row['rol']
                    return redir("/")
                else: error = "Usuario o contraseña incorrectos."
            else: error = "Error de conexión a la base de datos."

    if request.args.get('logout') == '1':
        SESION.clear(); return redir("/")

    rol, rn, rr, usr = get_rol_info()
    err_h = f'<div class="alert alert-danger text-center">{escape(error)}</div>' if error else ""
    left = f'<p><strong>Usuario:</strong> {escape(usr)}</p><p><strong>Rol:</strong> {escape(rn)}</p>' if rol else '<p class="text-center">Inicie sesión para acceder al sistema.</p>'

    body = f'''
<div class="container-fluid"><div class="row">
<aside class="col-sm-3"><div class="box white"><h4 class="text-center">Estado del Sistema</h4><hr>{left}</div></aside>
<main class="col-sm-6"><div class="box soft-green text-center"><h2>Aplicación de Tecnologías WEB</h2><hr>
<p><strong>Estudiantes:</strong></p><p>Pamela Carriel</p><p>Karla Molina</p><p>Josue Tapia</p>
<hr><p><strong>NRC:</strong> 29922</p><p><strong>Grupo:</strong> 05</p><p><strong>Fecha:</strong> 30 de octubre del 2025</p></div></main>
<section class="col-sm-3"><div class="box dark-green"><iframe width="100%" height="220" src="https://www.youtube.com/embed/_mLQ4BaMPoY?autoplay=1&mute=1" frameborder="0" allowfullscreen></iframe></div></section>
</div></div>
<div class="modal fade" id="modalLogin"><div class="modal-dialog modal-sm"><div class="modal-content">
<div class="modal-header"><h4 class="modal-title text-center">&#128274; Inicio de Sesión</h4></div>
<form method="post" action=""><input type="hidden" name="accion" value="login"><div class="modal-body">{err_h}
<div class="form-group"><label>Usuario</label><input name="username" class="form-control" required></div>
<div class="form-group"><label>Password</label><input name="password" type="password" class="form-control" value="123" required>
<small class="text-muted">Contraseña por defecto: <b>123</b></small></div></div>
<div class="modal-footer"><button class="btn btn-success btn-block">Ingresar</button></div></form>
</div></div></div>'''

    js = "<script>$('#modalLogin').modal('show');</script>" if error else ""
    return page("Aplicación Web", body, extra_js=js)

# =====================================================
# VEHÍCULOS LISTADO
# =====================================================
@app.route('/vehiculos')
def vehiculos():
    if 'rol' not in SESION: return redir("/")
    rol_bd = SESION['rol']; usr = SESION.get('username','')
    cn = get_db_matriculacion()
    if not cn: return "Error BD", 500
    cur = cn.cursor(dictionary=True)
    if rol_bd == "CRUD": rr = "ADM"
    elif rol_bd == "R":
        if es_placa(usr): cur.close(); cn.close(); return redir("/mi_vehiculo")
        rr = "AGENTE"
    else: cur.close(); cn.close(); return redir("/")
    cur.execute("SELECT v.id,v.placa,m.descripcion AS marca,v.motor,v.chasis,v.combustible,v.anio,c.descripcion AS color,v.avaluo FROM vehiculo v JOIN marca m ON v.marca=m.id JOIN color c ON v.color=c.id ORDER BY v.id")
    vs = cur.fetchall(); cur.close(); cn.close()
    btn = f'<a href="{u("/vehiculo_form")}" class="btn btn-success"><span class="glyphicon glyphicon-plus"></span> Nuevo Vehículo</a><br><br>' if rr=="ADM" else ""
    rows = ""
    for v in vs:
        av = f"$ {float(v['avaluo']):,.2f}"
        if rr == "AGENTE":
            act = f'<a href="{u(f"/consultar_matricula?id={v["id"]}")}" class="btn btn-xs btn-info">Consultar</a> <a href="{u(f"/matricular?id={v["id"]}")}" class="btn btn-xs btn-success">Matricular</a>'
        else:
            act = f'<a href="{u(f"/vehiculo_form?id={v["id"]}")}" class="btn btn-xs btn-primary">Editar</a> <a href="{u(f"/vehiculo_delete?id={v["id"]}")}" class="btn btn-xs btn-danger" onclick="return confirm(\'¿Eliminar?\')">Eliminar</a>'
        rows += f'<tr><td>{v["id"]}</td><td>{escape(v["placa"])}</td><td>{escape(v["marca"])}</td><td>{escape(v["motor"])}</td><td>{escape(v["chasis"])}</td><td>{escape(v["combustible"])}</td><td>{v["anio"]}</td><td>{escape(v["color"])}</td><td>{av}</td><td>{act}</td></tr>'
    rd = "ADMINISTRADOR" if rr=="ADM" else "AGENTE"
    body = f'''<div class="container-fluid" style="margin-top:20px"><h2>Listado de Vehículos</h2>
<p>Usuario: <strong>{escape(usr)}</strong> | Rol: <strong>{rd}</strong></p><hr>{btn}
<div class="table-responsive"><table class="table table-bordered table-striped table-hover">
<thead class="bg-success"><tr><th>ID</th><th>Placa</th><th>Marca</th><th>Motor</th><th>Chasis</th><th>Combustible</th><th>Año</th><th>Color</th><th>Avalúo</th><th>Acciones</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<a href="{u("/")}" class="btn btn-default">Volver al Inicio</a></div>'''
    return page("Vehículos", body, show_nav=False)

# =====================================================
# VEHÍCULO FORM (crear/editar)
# =====================================================
@app.route('/vehiculo_form', methods=['GET','POST'])
def vehiculo_form():
    if SESION.get('rol') != 'CRUD': return redir("/")
    cn = get_db_matriculacion()
    if not cn: return "Error BD", 500
    cur = cn.cursor(dictionary=True)
    cur.execute("SELECT id,descripcion FROM marca ORDER BY descripcion"); marcas = cur.fetchall()
    cur.execute("SELECT id,descripcion FROM color ORDER BY descripcion"); colores = cur.fetchall()
    id_v = request.args.get('id'); id_v = int(id_v) if id_v and id_v.isdigit() else None
    veh = None; error = ""
    if id_v:
        cur.execute("SELECT * FROM vehiculo WHERE id=%s",(id_v,)); veh = cur.fetchone()
        if not veh: cur.close(); cn.close(); return "No encontrado",404
    if request.method == 'POST':
        pl = request.form.get('placa','').strip().upper()
        mk = request.form.get('marca','').strip(); mo = request.form.get('motor','').strip()
        ch = request.form.get('chasis','').strip(); co = request.form.get('combustible','').strip()
        an = request.form.get('anio','').strip(); cl = request.form.get('color','').strip()
        av = request.form.get('avaluo','').strip()
        if not all([pl,mk,mo,ch,co,an,cl,av]): error = "Complete todos los campos."
        else:
            if id_v:
                cur.execute("UPDATE vehiculo SET placa=%s,marca=%s,motor=%s,chasis=%s,combustible=%s,anio=%s,color=%s,avaluo=%s WHERE id=%s",(pl,mk,mo,ch,co,an,cl,av,id_v))
                cn.commit(); cur.close(); cn.close(); return redir("/vehiculos")
            else:
                cur.execute("SELECT COUNT(*) as c FROM vehiculo WHERE placa=%s",(pl,))
                if cur.fetchone()['c'] > 0: error = "La placa ya existe."
                else:
                    cur.execute("INSERT INTO vehiculo (placa,marca,motor,chasis,combustible,anio,color,avaluo,foto) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,'')",(pl,mk,mo,ch,co,an,cl,av))
                    cn.commit()
                    cu = get_db_usuarios()
                    if cu:
                        c2 = cu.cursor(dictionary=True); c2.execute("SELECT COUNT(*) as c FROM usuarios WHERE username=%s",(pl,))
                        if c2.fetchone()['c'] == 0: c2.execute("INSERT INTO usuarios(username,password,roles_id) VALUES(%s,'123',2)",(pl,)); cu.commit()
                        c2.close(); cu.close()
                    cur.close(); cn.close(); return redir("/vehiculos")
    f = {}
    for c in ['placa','motor','chasis','combustible','anio','avaluo','marca','color']:
        f[c] = request.form.get(c,'') if request.method=='POST' else (str(veh[c]) if veh and veh.get(c) is not None else '')
    cur.close(); cn.close()
    eh = f'<div class="alert alert-danger">{escape(error)}</div>' if error else ""
    mo2 = '<option value="">-- Seleccione --</option>'
    for m in marcas:
        s = 'selected' if str(f['marca'])==str(m['id']) else ''
        mo2 += f'<option value="{m["id"]}" {s}>{escape(m["descripcion"])}</option>'
    combs = ["Gasolina","Diésel","Eléctrico","Híbrido"]
    co2 = ""
    for c in combs:
        s = 'selected' if f['combustible']==c else ''
        co2 += f'<option value="{c}" {s}>{c}</option>'
    cl2 = '<option value="">-- Seleccione --</option>'
    for c in colores:
        s = 'selected' if str(f['color'])==str(c['id']) else ''
        cl2 += f'<option value="{c["id"]}" {s}>{escape(c["descripcion"])}</option>'
    tf = "Editar Vehículo" if id_v else "Registrar Nuevo Vehículo"
    bt = "Actualizar" if id_v else "Guardar"
    body = f'''<div class="container" style="margin-top:30px;max-width:800px"><h3 class="text-center">{tf}</h3><hr>{eh}
<form method="post" action="">
<div class="form-group"><label>Placa</label><input type="text" name="placa" class="form-control" value="{escape(f['placa'])}" required></div>
<div class="form-group"><label>Marca</label><select name="marca" class="form-control" required>{mo2}</select></div>
<div class="form-group"><label>Motor</label><input type="text" name="motor" class="form-control" value="{escape(f['motor'])}" required></div>
<div class="form-group"><label>Chasis</label><input type="text" name="chasis" class="form-control" value="{escape(f['chasis'])}" required></div>
<div class="form-group"><label>Combustible</label><select name="combustible" class="form-control" required>{co2}</select></div>
<div class="form-group"><label>Año</label><input type="number" name="anio" class="form-control" value="{escape(f['anio'])}" required></div>
<div class="form-group"><label>Color</label><select name="color" class="form-control" required>{cl2}</select></div>
<div class="form-group"><label>Avalúo</label><input type="number" step="0.01" name="avaluo" class="form-control" value="{escape(f['avaluo'])}" required></div>
<button class="btn btn-success">{bt}</button> <a href="{u("/vehiculos")}" class="btn btn-default">Cancelar</a></form></div>'''
    return page(tf, body, show_nav=False)

# =====================================================
# VEHÍCULO DELETE
# =====================================================
@app.route('/vehiculo_delete')
def vehiculo_delete():
    if SESION.get('rol') != 'CRUD': return "Acceso denegado",403
    iv = request.args.get('id')
    if not iv or not iv.isdigit(): return "ID inválido",400
    cn = get_db_matriculacion()
    if cn:
        cur = cn.cursor(); cur.execute("DELETE FROM vehiculo WHERE id=%s",(int(iv),)); cn.commit(); cur.close(); cn.close()
    return redir("/vehiculos")

# =====================================================
# MI VEHÍCULO (DUEÑO)
# =====================================================
@app.route('/mi_vehiculo')
def mi_vehiculo():
    if SESION.get('rol') != 'R': return redir("/")
    placa = SESION.get('username','').strip()
    cn = get_db_matriculacion()
    if not cn: return "Error BD",500
    cur = cn.cursor(dictionary=True)
    cur.execute("SELECT v.id,v.placa,m.descripcion AS marca,v.motor,v.chasis,v.combustible,v.anio,c.descripcion AS color,v.avaluo FROM vehiculo v JOIN marca m ON v.marca=m.id JOIN color c ON v.color=c.id WHERE v.placa=%s",(placa,))
    v = cur.fetchone()
    if not v: cur.close(); cn.close(); return "No existe vehículo para este usuario."
    cur.execute("SELECT DISTINCT anio FROM matricula WHERE vehiculo=%s ORDER BY anio",(v['id'],))
    anios = [r['anio'] for r in cur.fetchall()]; cur.close(); cn.close()
    al = '<div class="alert alert-warning">No registra matrículas.</div>' if not anios else "<ul>"+"".join(f"<li>{a}</li>" for a in anios)+"</ul>"
    av = f"$ {float(v['avaluo']):,.2f}"
    body = f'''<div class="container" style="margin-top:30px;max-width:900px"><h2 class="text-center">Mi Vehículo</h2>
<p class="text-center">Usuario: <strong>{escape(placa)}</strong> | Rol: <strong>DUEÑO DEL VEHÍCULO</strong></p><hr>
<div class="panel panel-success"><div class="panel-heading"><h4 class="panel-title">Información del Vehículo</h4></div><div class="panel-body">
<table class="table table-bordered"><tr><th>Placa</th><td>{escape(v['placa'])}</td></tr><tr><th>Marca</th><td>{escape(v['marca'])}</td></tr>
<tr><th>Motor</th><td>{escape(v['motor'])}</td></tr><tr><th>Chasis</th><td>{escape(v['chasis'])}</td></tr>
<tr><th>Combustible</th><td>{escape(v['combustible'])}</td></tr><tr><th>Año</th><td>{v['anio']}</td></tr>
<tr><th>Color</th><td>{escape(v['color'])}</td></tr><tr><th>Avalúo</th><td>{av}</td></tr></table></div></div>
<div class="panel panel-info"><div class="panel-heading"><h4 class="panel-title">Años Matriculados</h4></div><div class="panel-body">{al}</div></div>
<div class="text-center"><a href="{u("/")}" class="btn btn-default">Volver al Inicio</a></div></div>'''
    return page("Mi Vehículo", body, show_nav=False)

# =====================================================
# MARCAS CRUD
# =====================================================
@app.route('/marcas', methods=['GET','POST'])
def marcas():
    if SESION.get('rol') != 'CRUD': return "Acceso denegado",403
    cn = get_db_matriculacion()
    if not cn: return "Error BD",500
    cur = cn.cursor(dictionary=True); msg = ""; me = None
    if request.method == 'POST':
        id_m = request.form.get('id','').strip(); d = request.form.get('descripcion','').strip()
        p = request.form.get('pais','').strip(); di = request.form.get('direccion','').strip()
        try:
            if not id_m:
                cur.execute("INSERT INTO marca(descripcion,pais,direccion) VALUES(%s,%s,%s)",(d,p,di)); cn.commit(); msg="Marca registrada."
            else:
                cur.execute("UPDATE marca SET descripcion=%s,pais=%s,direccion=%s WHERE id=%s",(d,p,di,id_m)); cn.commit(); msg="Marca actualizada."
        except mysql.connector.Error as e: msg=f"Error: {e}"
    ac = request.args.get('accion'); ia = request.args.get('id')
    if ac=='eliminar' and ia:
        try: cur.execute("DELETE FROM marca WHERE id=%s",(ia,)); cn.commit(); msg="Marca eliminada."
        except mysql.connector.Error as e: msg=f"Error: {e}"
    elif ac=='editar' and ia:
        cur.execute("SELECT * FROM marca WHERE id=%s",(ia,)); me=cur.fetchone()
    cur.execute("SELECT * FROM marca ORDER BY id"); ml=cur.fetchall(); cur.close(); cn.close()
    mh = f'<div class="alert alert-success">{escape(msg)}</div>' if msg else ""
    tf="Editar Marca" if me else "Nueva Marca"; bt="Actualizar" if me else "Guardar"
    cn2 = f'<a href="{u("/marcas")}" class="btn btn-default">Cancelar</a>' if me else ""
    vd=escape(me['descripcion']) if me else ""; vp=escape(me['pais']) if me else ""; vdi=escape(me['direccion']) if me else ""; vid=me['id'] if me else ""
    rows=""
    for m in ml:
        rows+=f'<tr><td>{m["id"]}</td><td>{escape(m["descripcion"])}</td><td>{escape(m["pais"])}</td><td>{escape(m["direccion"])}</td><td><a href="{u(f"/marcas?accion=editar&id={m["id"]}")}" class="btn btn-xs btn-primary">Editar</a> <a href="{u(f"/marcas?accion=eliminar&id={m["id"]}")}" class="btn btn-xs btn-danger" onclick="return confirm(\'¿Eliminar?\')">Eliminar</a></td></tr>'
    body=f'''<div class="container" style="margin-top:30px;max-width:900px"><h2>Gestión de Marcas</h2>
<p>Usuario: <strong>{escape(SESION.get("username",""))}</strong> | Rol: <strong>ADM</strong></p><hr>{mh}
<div class="panel panel-success"><div class="panel-heading"><strong>{tf}</strong></div><div class="panel-body">
<form method="post" action=""><input type="hidden" name="id" value="{vid}">
<div class="form-group"><label>Descripción</label><input type="text" name="descripcion" class="form-control" value="{vd}" required></div>
<div class="form-group"><label>País</label><input type="text" name="pais" class="form-control" value="{vp}" required></div>
<div class="form-group"><label>Dirección</label><input type="text" name="direccion" class="form-control" value="{vdi}"></div>
<button type="submit" class="btn btn-success">{bt}</button> {cn2}</form></div></div><hr>
<div class="table-responsive"><table class="table table-bordered table-striped">
<thead class="bg-success"><tr><th>ID</th><th>Descripción</th><th>País</th><th>Dirección</th><th>Acciones</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<a href="{u("/")}" class="btn btn-default">Volver al Inicio</a></div>'''
    return page("CRUD Marcas", body, show_nav=False)

# =====================================================
# AGENCIAS CRUD
# =====================================================
@app.route('/agencias', methods=['GET','POST'])
def agencias():
    if SESION.get('rol') != 'CRUD': return "Acceso denegado",403
    cn = get_db_matriculacion()
    if not cn: return "Error BD",500
    cur = cn.cursor(dictionary=True); msg=""; ae=None
    if request.method == 'POST':
        ia=request.form.get('id','').strip(); d=request.form.get('descripcion','').strip()
        di=request.form.get('direccion','').strip(); t=request.form.get('telefono','').strip()
        hi=request.form.get('horainicio','').strip(); hf=request.form.get('horafin','').strip()
        try:
            if not ia:
                cur.execute("INSERT INTO agencia(descripcion,direccion,telefono,horainicio,horafin,foto) VALUES(%s,%s,%s,%s,%s,'')",(d,di,t,hi,hf)); cn.commit(); msg="Agencia registrada."
            else:
                cur.execute("UPDATE agencia SET descripcion=%s,direccion=%s,telefono=%s,horainicio=%s,horafin=%s WHERE id=%s",(d,di,t,hi,hf,ia)); cn.commit(); msg="Agencia actualizada."
        except mysql.connector.Error as e: msg=f"Error: {e}"
    ac=request.args.get('accion'); ida=request.args.get('id')
    if ac=='eliminar' and ida:
        try: cur.execute("DELETE FROM agencia WHERE id=%s",(ida,)); cn.commit(); msg="Agencia eliminada."
        except mysql.connector.Error as e: msg=f"Error: {e}"
    elif ac=='editar' and ida:
        cur.execute("SELECT * FROM agencia WHERE id=%s",(ida,)); ae=cur.fetchone()
    cur.execute("SELECT * FROM agencia ORDER BY id"); al=cur.fetchall(); cur.close(); cn.close()
    mh=f'<div class="alert alert-success">{escape(msg)}</div>' if msg else ""
    tf="Editar Agencia" if ae else "Nueva Agencia"; bt="Actualizar" if ae else "Guardar"
    cn2=f'<a href="{u("/agencias")}" class="btn btn-default">Cancelar</a>' if ae else ""
    a = ae or {}
    vid=a.get('id',''); vd=escape(str(a.get('descripcion',''))); vdi=escape(str(a.get('direccion','')))
    vt=escape(str(a.get('telefono',''))); vhi=str(a.get('horainicio','')); vhf=str(a.get('horafin',''))
    rows=""
    for ag in al:
        rows+=f'<tr><td>{ag["id"]}</td><td>{escape(ag["descripcion"])}</td><td>{escape(ag["direccion"])}</td><td>{escape(ag["telefono"])}</td><td>{ag["horainicio"]} - {ag["horafin"]}</td><td><a href="{u(f"/agencias?accion=editar&id={ag["id"]}")}" class="btn btn-xs btn-primary">Editar</a> <a href="{u(f"/agencias?accion=eliminar&id={ag["id"]}")}" class="btn btn-xs btn-danger" onclick="return confirm(\'¿Eliminar?\')">Eliminar</a></td></tr>'
    body=f'''<div class="container" style="margin-top:30px;max-width:950px"><h2>Gestión de Agencias</h2>
<p>Usuario: <strong>{escape(SESION.get("username",""))}</strong> | Rol: <strong>ADM</strong></p><hr>{mh}
<div class="panel panel-success"><div class="panel-heading"><strong>{tf}</strong></div><div class="panel-body">
<form method="post" action=""><input type="hidden" name="id" value="{vid}">
<div class="form-group"><label>Descripción</label><input type="text" name="descripcion" class="form-control" value="{vd}" required></div>
<div class="form-group"><label>Dirección</label><input type="text" name="direccion" class="form-control" value="{vdi}" required></div>
<div class="form-group"><label>Teléfono</label><input type="text" name="telefono" class="form-control" value="{vt}" required></div>
<div class="row"><div class="col-sm-6"><div class="form-group"><label>Hora Inicio</label><input type="time" name="horainicio" class="form-control" value="{vhi}" required></div></div>
<div class="col-sm-6"><div class="form-group"><label>Hora Fin</label><input type="time" name="horafin" class="form-control" value="{vhf}" required></div></div></div>
<button type="submit" class="btn btn-success">{bt}</button> {cn2}</form></div></div><hr>
<div class="table-responsive"><table class="table table-bordered table-striped">
<thead class="bg-success"><tr><th>ID</th><th>Descripción</th><th>Dirección</th><th>Teléfono</th><th>Horario</th><th>Acciones</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<a href="{u("/")}" class="btn btn-default">Volver al Inicio</a></div>'''
    return page("CRUD Agencias", body, show_nav=False)

# =====================================================
# USUARIOS CREAR (SUPERADMIN)
# =====================================================
@app.route('/usuarios', methods=['GET','POST'])
def usuarios():
    if SESION.get('rol') != 'C': return redir("/")
    cn = get_db_usuarios()
    if not cn: return "Error BD",500
    cur = cn.cursor(dictionary=True); msg=""; error=""
    if request.method == 'POST':
        un=request.form.get('username','').strip(); ri=request.form.get('rol_id','').strip()
        if not un or not ri: error="Todos los campos son obligatorios."
        elif ri not in ['2','5']: error="Rol no permitido."
        else:
            cur.execute("SELECT COUNT(*) as c FROM usuarios WHERE username=%s",(un,))
            if cur.fetchone()['c']>0: error="El username ya existe."
            else:
                try: cur.execute("INSERT INTO usuarios(username,password,roles_id) VALUES(%s,'123',%s)",(un,ri)); cn.commit(); msg="Usuario creado correctamente."
                except mysql.connector.Error as e: error=f"Error: {e}"
    cur.close(); cn.close()
    eh=f'<div class="alert alert-danger text-center">{escape(error)}</div>' if error else ""
    mh=f'<div class="alert alert-success text-center">{escape(msg)}</div>' if msg else ""
    body=f'''<div class="container" style="margin-top:30px;max-width:600px">
<div class="panel panel-success"><div class="panel-heading text-center"><h3 class="panel-title">Crear Usuario (SUPERADMIN)</h3></div>
<div class="panel-body">{eh}{mh}
<form method="post" action="">
<div class="form-group"><label>Username</label><input type="text" name="username" class="form-control" placeholder="Ej: PCH3465" required></div>
<div class="form-group"><label>Rol</label><select name="rol_id" class="form-control" required><option value="">-- Seleccione --</option><option value="2">AGENTE</option><option value="5">ADMINISTRADOR</option></select></div>
<div class="form-group"><label>Password</label><input type="text" class="form-control" value="123" disabled><small class="text-muted">Contraseña por defecto: <b>123</b></small></div>
<button type="submit" class="btn btn-success btn-block"><span class="glyphicon glyphicon-plus"></span> Crear Usuario</button>
<a href="{u("/")}" class="btn btn-default btn-block" style="margin-top:10px">Volver al Inicio</a></form></div></div></div>'''
    return page("Crear Usuario", body, show_nav=False)

# =====================================================
# CONSULTAR MATRÍCULA (AGENTE)
# =====================================================
@app.route('/consultar_matricula')
def consultar_matricula():
    if SESION.get('rol') != 'R': return redir("/")
    iv=request.args.get('id')
    if not iv or not iv.isdigit(): return redir("/vehiculos")
    SESION['vehiculo_id']=int(iv)
    return redir("/ver_matriculas")

# =====================================================
# VER MATRÍCULAS
# =====================================================
@app.route('/ver_matriculas')
def ver_matriculas():
    if SESION.get('rol') != 'R': return "Acceso denegado",403
    vid=SESION.get('vehiculo_id')
    if not vid: return "Seleccione un vehículo."
    cn=get_db_matriculacion()
    if not cn: return "Error BD",500
    cur=cn.cursor(dictionary=True)
    cur.execute("SELECT v.placa,m.descripcion AS marca,v.motor,v.chasis,v.combustible,v.anio,c.descripcion AS color,v.avaluo FROM vehiculo v JOIN marca m ON v.marca=m.id JOIN color c ON v.color=c.id WHERE v.id=%s",(vid,))
    v=cur.fetchone()
    if not v: cur.close(); cn.close(); return "Vehículo no encontrado."
    cur.execute("SELECT mt.anio,mt.fecha,a.descripcion AS agencia FROM matricula mt JOIN agencia a ON mt.agencia=a.id WHERE mt.vehiculo=%s ORDER BY mt.anio",(vid,))
    mats=cur.fetchall(); cur.close(); cn.close()
    av=f"$ {float(v['avaluo']):,.2f}"
    if not mats: mth='<div class="alert alert-warning">No registra matrículas.</div>'
    else:
        fr="".join(f"<tr><td>{m['anio']}</td><td>{m['fecha']}</td><td>{escape(m['agencia'])}</td></tr>" for m in mats)
        mth=f'<table class="table table-striped table-bordered"><thead class="bg-success"><tr><th>Año</th><th>Fecha</th><th>Agencia</th></tr></thead><tbody>{fr}</tbody></table>'
    body=f'''<div class="container" style="margin-top:30px;max-width:1000px">
<div class="panel panel-success"><div class="panel-heading"><h3 class="panel-title">Consulta de Matrículas</h3></div><div class="panel-body">
<h4>Información del Vehículo</h4>
<table class="table table-bordered"><tr><th>Placa</th><td>{escape(v['placa'])}</td></tr><tr><th>Marca</th><td>{escape(v['marca'])}</td></tr>
<tr><th>Motor</th><td>{escape(v['motor'])}</td></tr><tr><th>Chasis</th><td>{escape(v['chasis'])}</td></tr>
<tr><th>Combustible</th><td>{escape(v['combustible'])}</td></tr><tr><th>Año</th><td>{v['anio']}</td></tr>
<tr><th>Color</th><td>{escape(v['color'])}</td></tr><tr><th>Avalúo</th><td>{av}</td></tr></table><hr>
<h4>Historial de Matrículas</h4>{mth}<hr>
<a href="{u("/vehiculos")}" class="btn btn-default">Volver a Vehículos</a> <a href="{u("/")}" class="btn btn-primary">Inicio</a></div></div></div>'''
    return page("Consulta Matrículas", body, show_nav=False)

# =====================================================
# MATRICULAR (AGENTE)
# =====================================================
@app.route('/matricular', methods=['GET','POST'])
def matricular():
    if SESION.get('rol') != 'R': return redir("/")
    iv=request.args.get('id')
    if not iv or not iv.isdigit(): return redir("/vehiculos")
    iv=int(iv); SESION['vehiculo_id']=iv
    cn=get_db_matriculacion()
    if not cn: return "Error BD",500
    cur=cn.cursor(dictionary=True); msg=""; error=""
    cur.execute("SELECT v.placa,m.descripcion AS marca,v.anio FROM vehiculo v JOIN marca m ON v.marca=m.id WHERE v.id=%s",(iv,))
    v=cur.fetchone()
    if not v: cur.close(); cn.close(); return "Vehículo no encontrado."
    cur.execute("SELECT id,descripcion FROM agencia ORDER BY descripcion"); ags=cur.fetchall()
    if request.method == 'POST':
        an=request.form.get('anio','').strip(); fe=request.form.get('fecha','').strip(); ag=request.form.get('agencia','').strip()
        if not an or not fe or not ag: error="Todos los campos son obligatorios."
        else:
            cur.execute("SELECT COUNT(*) as c FROM matricula WHERE vehiculo=%s AND anio=%s",(iv,an))
            if cur.fetchone()['c']>0: error="Ya matriculado en ese año."
            else: cur.execute("INSERT INTO matricula(anio,fecha,agencia,vehiculo) VALUES(%s,%s,%s,%s)",(an,fe,ag,iv)); cn.commit(); msg="Matrícula registrada."
    cur.close(); cn.close()
    eh=f'<div class="alert alert-danger">{escape(error)}</div>' if error else ""
    mh=f'<div class="alert alert-success">{escape(msg)}</div>' if msg else ""
    ao='<option value="">-- Seleccione --</option>'
    for a in ags: ao+=f'<option value="{a["id"]}">{escape(a["descripcion"])}</option>'
    body=f'''<div class="container" style="margin-top:30px;max-width:700px">
<div class="panel panel-success"><div class="panel-heading"><h3 class="panel-title">Matricular Vehículo</h3></div><div class="panel-body">
{eh}{mh}<h4>Vehículo</h4>
<table class="table table-bordered"><tr><th>Placa</th><td>{escape(v['placa'])}</td></tr><tr><th>Marca</th><td>{escape(v['marca'])}</td></tr><tr><th>Año</th><td>{v['anio']}</td></tr></table><hr>
<form method="post" action="">
<div class="form-group"><label>Año de Matrícula</label><input type="number" name="anio" class="form-control" placeholder="Ej: 2025" required></div>
<div class="form-group"><label>Fecha</label><input type="date" name="fecha" class="form-control" required></div>
<div class="form-group"><label>Agencia</label><select name="agencia" class="form-control" required>{ao}</select></div>
<button class="btn btn-success"><span class="glyphicon glyphicon-check"></span> Registrar Matrícula</button>
<a href="{u("/vehiculos")}" class="btn btn-default">Cancelar</a></form></div></div></div>'''
    return page("Matricular", body, show_nav=False)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
