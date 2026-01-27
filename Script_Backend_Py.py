# Script_Backend_Py.py

import os
import importlib.util
import sys
from flask import Flask, render_template, send_from_directory, request
from flask import send_from_directory

# =========================
# CONFIGURACIÓN BASE
# =========================
directorio_base = os.path.dirname(os.path.abspath(__file__))

# NOTA: Basado en tu estructura, 'templates' está en la raíz de TAREASPY/
ruta_templates = os.path.join(directorio_base, 'templates') 

app = Flask(__name__, template_folder=ruta_templates)

# =========================
# 🔊 RUTA GLOBAL PARA SONIDOS
# =========================
@app.route('/sounds/<path:filename>')
def servir_sonidos(filename):
    """
    Busca el archivo de sonido dentro de cualquier proyecto
    que tenga una carpeta 'sounds'
    """
    # Recorre las subcarpetas dentro de templates/
    for carpeta in os.listdir(ruta_templates):
        ruta_proyecto = os.path.join(ruta_templates, carpeta)
        ruta_sounds = os.path.join(ruta_proyecto, 'sounds')

        if os.path.isdir(ruta_sounds):
            archivo = os.path.join(ruta_sounds, filename)
            if os.path.exists(archivo):
                return send_from_directory(ruta_sounds, filename)

    return "Archivo de sonido no encontrado", 404

# =========================
# EJECUTAR APP HIJA
# =========================
def ejecutar_flask_hijo(ruta_archivo, metodo='GET', datos=None):
    import os
    import sys
    import importlib.util
    from flask import request

    ruta_proyecto_hijo = os.path.dirname(ruta_archivo)          # .../templates/vehiculo_PARTE1
    nombre_archivo_py = os.path.basename(ruta_archivo)          # app.py
    nombre_carpeta_hijo = os.path.basename(ruta_proyecto_hijo)  # vehiculo_PARTE1

    prefijo_externo = f"/{nombre_carpeta_hijo}/{nombre_archivo_py}"

    try:
        # 1) Cargar módulo (app.py del hijo)
        nombre_modulo = f"{nombre_carpeta_hijo}_{nombre_archivo_py}".replace(".py", "")
        spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
        modulo = importlib.util.module_from_spec(spec)

        # 2) Para que funcionen imports del hijo (vehiculo.py, etc.)
        if ruta_proyecto_hijo not in sys.path:
            sys.path.insert(0, ruta_proyecto_hijo)

        spec.loader.exec_module(modulo)

        if not hasattr(modulo, "app"):
            return b"<h1>Error</h1><p>El script no contiene una variable 'app' de Flask.</p>", 500

        app_hija = modulo.app

        # 3) Subruta interna (lo que viene después de /carpeta/app.py)
        path_externo = request.path  # ej: /vehiculo_PARTE1/app.py  ó /vehiculo_PARTE1/app.py/otra
        if path_externo.startswith(prefijo_externo):
            subruta = path_externo[len(prefijo_externo):]
        else:
            subruta = ""

        if not subruta:
            subruta = "/"
        if not subruta.startswith("/"):
            subruta = "/" + subruta

        # 4) ✅ QUERYSTRING CORRECTO (DICT, NO BYTES)
        qs_dict = request.args.to_dict(flat=True)  # {"d":"C/1", ...}

        # 5) Ejecutar en el test_client del hijo
        with app_hija.test_client() as cliente:
            if metodo.upper() == "POST":
                data = {}
                if datos:
                    data.update(datos)

                # reenviar archivos
                for key, f in request.files.items():
                    if f and f.filename:
                        try:
                            f.stream.seek(0)
                        except Exception:
                            pass
                        data[key] = (f.stream, f.filename)

                respuesta = cliente.post(
                    subruta,
                    query_string=qs_dict,             # ✅ dict
                    data=data,
                    content_type="multipart/form-data"
                )
            else:
                respuesta = cliente.get(
                    subruta,
                    query_string=qs_dict              # ✅ dict
                )

            return respuesta.data, respuesta.status_code

    except Exception as e:
        return f"<h1>Error al ejecutar el script</h1><pre>{e}</pre>".encode("utf-8"), 500

    finally:
        if ruta_proyecto_hijo in sys.path:
            sys.path.remove(ruta_proyecto_hijo)

    """
    Ejecuta una app Flask "hija" (ej. templates/POST/app.py) dentro del lanzador,
    reenviando:
      - subruta (path interno)
      - querystring (?d=C/1)
      - POST form data
      - archivos (multipart)
    """
    ruta_proyecto_hijo = os.path.dirname(ruta_archivo)          # .../templates/POST
    nombre_archivo_py = os.path.basename(ruta_archivo)          # app.py
    nombre_carpeta_hijo = os.path.basename(ruta_proyecto_hijo)  # POST

    # Prefijo externo que usa el lanzador: /<carpeta>/<archivo_py>
    prefijo_externo = f"/{nombre_carpeta_hijo}/{nombre_archivo_py}"

    app_hija.config["BASE_PATH"] = prefijo_externo  # 👈 AÑADIR ESTO


    try:
        # 1) Cargar módulo python (app.py del proyecto hijo)
        nombre_modulo = f"{nombre_carpeta_hijo}_{nombre_archivo_py}".replace(".py", "")
        spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
        modulo = importlib.util.module_from_spec(spec)

        # 2) Agregar path del proyecto hijo para que import vehiculo, etc funcione
        if ruta_proyecto_hijo not in sys.path:
            sys.path.insert(0, ruta_proyecto_hijo)

        spec.loader.exec_module(modulo)

        if not hasattr(modulo, "app"):
            return b"<h1>Error</h1><p>El script no contiene una variable 'app' de Flask.</p>", 500

        app_hija = modulo.app

        # 3) Calcular subruta interna real (lo que va después del prefijo externo)
        # Ejemplo:
        # request.path = /POST/app.py/something
        # subruta = /something
        path_externo = request.path

        if path_externo.startswith(prefijo_externo):
            subruta = path_externo[len(prefijo_externo):]
        else:
            # fallback: si por alguna razón no coincide, manda a /
            subruta = ""

        if not subruta:
            subruta = "/"
        if not subruta.startswith("/"):
            subruta = "/" + subruta

        # 4) Querystring (IMPORTANTÍSIMO para ?d=C/1)
        qs = request.query_string  # bytes

        # 5) Ejecutar request dentro del test_client del hijo
        with app_hija.test_client() as cliente:
            if metodo.upper() == "POST":
                data = {}

                # form fields
                if datos:
                    data.update(datos)

                # archivos (multipart)
                for key, f in request.files.items():
                    if f and f.filename:
                        try:
                            f.stream.seek(0)
                        except Exception:
                            pass
                        data[key] = (f.stream, f.filename)

                respuesta = cliente.post(
                    subruta,
                    query_string=qs,
                    data=data,
                    content_type="multipart/form-data"
                )
            else:
                respuesta = cliente.get(
                    subruta,
                    query_string=qs
                )

            return respuesta.data, respuesta.status_code

    except Exception as e:
        return f"<h1>Error al ejecutar el script</h1><pre>{e}</pre>".encode("utf-8"), 500

    finally:
        # 6) Limpiar sys.path siempre
        if ruta_proyecto_hijo in sys.path:
            sys.path.remove(ruta_proyecto_hijo)

    try:
        nombre_modulo = os.path.basename(ruta_archivo).replace('.py', '')
        
        # 1. Cargar el módulo (app.py del proyecto hijo)
        spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo)
        modulo = importlib.util.module_from_spec(spec)

        # 2. Añadir la ruta del proyecto hijo al path para resolver las IMPORTACIONES ABSOLUTAS
        sys.path.append(os.path.dirname(ruta_archivo))
        spec.loader.exec_module(modulo)

        if hasattr(modulo, 'app'):
            app_hija = modulo.app

            # 🔑 OBTENER RUTA INTERNA (por ejemplo /argentina/)
            ruta_a_eliminar = f'/{os.path.basename(os.path.dirname(ruta_archivo))}/{os.path.basename(ruta_archivo)}'
            subruta = request.path.replace(ruta_a_eliminar, '')

            if not subruta:
                subruta = '/'
            
            if not subruta.startswith('/'):
                subruta = '/' + subruta
            
            with app_hija.test_client() as cliente:
                if metodo == 'POST':
                    data = {}
                    if datos:
                        data.update(datos)

                    # ✅ reenviar archivos al hijo (multipart/form-data)
                    for key, f in request.files.items():
                        if f and f.filename:
                            try:
                                f.stream.seek(0)
                            except Exception:
                                pass
                            data[key] = (f.stream, f.filename)

                    respuesta = cliente.post(subruta, data=data, content_type='multipart/form-data')
                else:
                    respuesta = cliente.get(subruta)

                # Devolvemos la data de la respuesta y el código de estado
                return respuesta.data, respuesta.status_code

        return b"<h1>Error</h1><p>El script no contiene una variable 'app' de Flask.</p>", 500

    except Exception as e:
        # Importamos traceback solo para logging, no lo mostramos al usuario final
        # import traceback; traceback.print_exc() 
        return f"<h1>Error al ejecutar el script</h1><pre>{e}</pre>".encode('utf-8'), 500

    finally:
        # 4. Limpiar el sys.path
        if os.path.dirname(ruta_archivo) in sys.path:
            sys.path.remove(os.path.dirname(ruta_archivo))


# =========================
# MENÚ PRINCIPAL DEL LANZADOR
# =========================
@app.route('/')
def menu_principal():
    estructura_proyectos = {}

    if os.path.exists(ruta_templates):
        # Itera sobre los proyectos (subcarpetas dentro de templates/)
        for nombre in os.listdir(ruta_templates):
            ruta_completa = os.path.join(ruta_templates, nombre)
            if os.path.isdir(ruta_completa):
                archivos = [
                    a for a in os.listdir(ruta_completa)
                    if a.lower().endswith(('.html', '.py'))
                ]
                if archivos:
                    estructura_proyectos[nombre] = archivos

        # Archivos sueltos en templates/ (si los hay)
        sueltos = [
            a for a in os.listdir(ruta_templates)
            if os.path.isfile(os.path.join(ruta_templates, a))
            and a.lower().endswith(('.html', '.py'))
            and a != 'menu.html'
        ]

        if sueltos:
            estructura_proyectos['General (Sin Carpeta)'] = sueltos

    # Este menu.html es el que está en la raíz de TAREASPY/
    return render_template('menu.html', proyectos=estructura_proyectos)

# =========================
# SERVIR PROYECTOS (CRÍTICAMENTE CORREGIDO)
# =========================
@app.route('/<carpeta>/<path:archivo>', methods=['GET', 'POST'])
def servir_proyecto(carpeta, archivo):

    if carpeta == 'General (Sin Carpeta)':
        path_destino = ruta_templates
    else:
        # path_destino = TAREASPY/templates/AbstractasPOO
        path_destino = os.path.join(ruta_templates, carpeta)

    # El archivo real es el primer componente (ej. AbstractasPOO.py)
    archivo_base = archivo.split('/')[0] 

    # ruta_archivo_real = TAREASPY/templates/AbstractasPOO/AbstractasPOO.py
    ruta_archivo_real = os.path.join(path_destino, archivo_base)

    if not os.path.exists(ruta_archivo_real):
        return "Archivo no encontrado", 404

    if archivo_base.lower().endswith('.py'):
        metodo = request.method
        # Pasamos el diccionario de request.form para ejecutar_flask_hijo
        datos = dict(request.form) if metodo == 'POST' else None 
        
        # 1. Obtener la ruta URL completa que usó el navegador
        # (ej. /AbstractasPOO/AbstractasPOO.py o /AbstractasPOO/AbstractasPOO.py/subruta)
        full_external_path = request.path 

        # 2. Ejecutar el archivo Python (AbstractasPOO.py)
        response_data, status_code = ejecutar_flask_hijo(ruta_archivo_real, metodo=metodo, datos=datos)

        # 3. INTERCEPTAR Y CORREGIR EL HTML (SOLUCIÓN AL ERROR 405)
        if status_code == 200 and isinstance(response_data, bytes):
            try:
                html_content = response_data.decode('utf-8')
            except UnicodeDecodeError:
                # Si falla al decodificar, devolvemos los datos originales
                return response_data, status_code

            # Buscar 'action=""' (que pusiste en form_figuras.html) y reemplazarlo
            # por la URL externa completa.
            if 'action=""' in html_content:
                # Reemplazamos el action vacío por la ruta completa.
                response_data = html_content.replace('action=""', f'action="{full_external_path}"').encode('utf-8')
            
        return response_data, status_code

    elif archivo_base.lower().endswith('.html'):
        # Si es un HTML, asume que no tiene subrutas de Blueprint
        if carpeta == 'General (Sin Carpeta)':
            return render_template(archivo_base)
        
        # Renderiza el HTML dentro de la carpeta 
        return render_template(f'{carpeta}/{archivo_base}')

    else:
        # Sirve archivos estáticos que están dentro de la carpeta (si los hubiera)
        return send_from_directory(path_destino, archivo_base)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # carpeta donde está Script_Backend_Py.py

@app.route('/<carpeta>/static/images/<path:filename>')
def servir_static_hijo(carpeta, filename):

    # 1) Ruta tipo: TAREASPYTHON/POST/static/images
    ruta1 = os.path.join(BASE_DIR, carpeta, 'static', 'images')

    # 2) Ruta tipo: TAREASPYTHON/templates/POST/static/images
    ruta2 = os.path.join(ruta_templates, carpeta, 'static', 'images')

    if os.path.isdir(ruta1):
        archivo1 = os.path.join(ruta1, filename)
        if os.path.exists(archivo1):
            return send_from_directory(ruta1, filename)

    if os.path.isdir(ruta2):
        archivo2 = os.path.join(ruta2, filename)
        if os.path.exists(archivo2):
            return send_from_directory(ruta2, filename)

    return "Archivo estático no encontrado en el proyecto", 404


# =========================
# MAIN
# =========================
if __name__ == '__main__':
    # Usamos el puerto 5000 por si acaso
    app.run(debug=True, port=5000)