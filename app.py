from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import os

# Importaciones específicas del proyecto
from lib.pymapdl.soporte import *
from lib.pymapdl.viga_doble_voladizo import *
from lib.pymapdl.cortador_de_torno import *

app = Flask(__name__)

# Configuración del directorio de imágenes
IMAGE_DIR = os.path.join(os.getcwd(), 'static', 'images')
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/escuadra', methods=['GET', 'POST'])
def escuadra():
    if request.method == 'POST':
        # Extraer los valores enviados desde el formulario
        box1 = request.form.get('box1', '').split(',')
        box2 = request.form.get('box2', '').split(',')
        radio_perno = float(request.form.get('pinhole_radius', 0))
        tamaño_elemento = float(request.form.get('element_size', 0))
        carga_presion = request.form.get('pressure_load', '').split(',')
        
        # Convertir los valores de string a los tipos correctos
        box1 = [float(value) for value in box1]
        box2 = [float(value) for value in box2]
        carga_presion = [float(value) for value in carga_presion]

        # Llamar a la función analizar_soporte
        ruta_imagen_deformacion = analizar_soporte(
            box1, box2, radio_perno, tamaño_elemento, carga_presion
        )

        # Rutas de las imágenes para usar en HTML
        url_imagen_deformacion = os.path.join('images', os.path.basename(ruta_imagen_deformacion))
        return render_template('escuadra.html', solve_status="Solved",
                               deformation_image_url=url_imagen_deformacion)
    return render_template('escuadra.html')

@app.route('/dobleviga', methods=['GET', 'POST'])
def doble_viga():
    if request.method == 'POST':
        # Extraer los valores enviados desde el formulario
        longitud = float(request.form.get('length', 0))
        precorte = float(request.form.get('pre_crack', 0))
        ancho = float(request.form.get('width', 0))
        altura = float(request.form.get('height', 0))
        d = float(request.form.get('d', 0))
        
        # Llamar a la función analizar_viga_doble_voladizo
        ruta_imagen_fuerza_desplazamiento = analizar_viga_doble_voladizo(longitud, precorte, ancho, altura, d)
        
        # Rutas de las imágenes para usar en HTML
        url_imagen_fuerza_desplazamiento = os.path.join('images', os.path.basename(ruta_imagen_fuerza_desplazamiento))
        
        return render_template('dobleviga.html', solve_status="Solved",
                               ForcevsDisplacement_image_url=url_imagen_fuerza_desplazamiento)
    return render_template('dobleviga.html')

@app.route('/cortador_de_torno', methods=['GET', 'POST'])
def cortador_de_torno():
    if request.method == 'POST':
        # Extraer los valores enviados desde el formulario
        EXX = float(request.form.get('EXX', 1.0e7))
        NU = float(request.form.get('NU', 0.27))
        Fuerza = float(request.form.get('Fuerza', 10000))

        # Llamar a la función analizar_cortador_de_torno
        resultados = analizar_cortador_de_torno(EXX, NU, Fuerza)
        
        # Rutas de las imágenes para usar en HTML
        load_image_url, stress_image_url, xy_stress_image_url = resultados
        
        return render_template('cortador.html', solve_status="Solved",
                               load_image_url=load_image_url,
                               stress_image_url=stress_image_url,
                               xy_stress_image_url=xy_stress_image_url)
    return render_template('cortador.html')

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
