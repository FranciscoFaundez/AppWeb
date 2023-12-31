from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from database import db 
from utils.validations import validate_form, validate_form_hincha
import hashlib
import filetype
from werkzeug.utils import secure_filename
import os
import uuid


UPLOAD_FOLDER = 'app/static/uploads'

app = Flask(__name__)

app.secret_key = 'mysecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar-artesano', methods=['GET', 'POST'])
def agregar_artesano(): 
    if request.method == 'POST':
        region_artesano = request.form['region_artesano']
        comuna_artesano = request.form['comuna_artesano']
        tipo_artesania = request.form.getlist('tipo_artesania')
        desc_artesania = request.form['desc_artesania']
        foto_artesania = request.files['foto_artesania']
        nombre_artesano = request.form['nombre_artesano']
        email_artesano = request.form['email_artesano']
        celular_artesano = request.form['celular_artesano']

        if validate_form(region_artesano, comuna_artesano, tipo_artesania, desc_artesania, foto_artesania, nombre_artesano, email_artesano, celular_artesano):

            #1. Generate random name for img
            _filename = hashlib.sha256(secure_filename(foto_artesania.filename).encode("utf-8")).hexdigest()
            _extension = filetype.guess(foto_artesania).extension
            img_filename = f"{_filename}_{str(uuid.uuid4())}.{_extension}"

            #2. Save img in static/uploads
            foto_artesania.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))

            #3. Save form in db
            db.create_artesano(region_artesano, comuna_artesano, tipo_artesania, desc_artesania, img_filename, nombre_artesano, email_artesano, celular_artesano)
            print("Agregado a la db")
        
            return redirect(url_for('index'))

    with open('app/static/txt/regiones.txt', 'r', encoding='utf-8') as file:
        regiones = [line.strip() for line in file.readlines()]

    return render_template('agregar-artesano.html', regiones = regiones)


@app.route('/agregar-hincha', methods=['GET', 'POST'])
def agregar_hincha():
    if request.method == 'POST':
        deporte       = request.form.getlist('deporte')
        region_hincha = request.form['region_hincha']
        comuna_hincha = request.form['comuna_hincha']
        transporte    = request.form['transporte']
        nombre_hincha = request.form['nombre_hincha']
        email_hincha  = request.form['email_hincha']
        telefono_hincha = request.form['telefono_hincha']
        comentarioss   = request.form['comentario']
        if validate_form_hincha(deporte, region_hincha, comuna_hincha, transporte, nombre_hincha, email_hincha, telefono_hincha, comentarioss):
            db.create_hincha(deporte, region_hincha, comuna_hincha, transporte, nombre_hincha, email_hincha, telefono_hincha, comentarioss)
            print("Agregado a la db")

            return redirect(url_for('index'))
    
    with open('app/static/txt/deportes.txt', 'r', encoding='utf-8') as file:
        deportes = [line.strip() for line in file.readlines()]

    with open('app/static/txt/regiones.txt', 'r', encoding='utf-8') as file:
        regiones = [line.strip() for line in file.readlines()]

    return render_template('agregar-hincha.html', deportes = deportes, regiones = regiones)


@app.route('/ver-hinchas', methods=['GET', 'POST'])
def ver_hinchas():
    page_size = 5
    data = []
    for hincha in db.get_hinchas(page_size):
        id_hincha, comuna_id, transporte, nombre, email, telefono, comentarios = hincha

        #Recuperar nombre de la comuna
        comuna = db.get_comuna(comuna_id)

        #Obtener deportes
        deportes = db.get_deportes(id_hincha)
        print(deportes)

        #Pasar a string los deportes
        deportes = ", ".join([deporte[0] for deporte in deportes])

        data.append({
            "id_hincha": id_hincha,
            "deportes": deportes,
            "comuna": comuna,
            "transporte": transporte,
            "nombre": nombre,
            "email": email,
            "telefono": str(telefono),
            "comentarios": comentarios
        })
    return render_template('ver-hinchas.html', data = data)

@app.route('/ver-artesanos', methods=['GET'])
def ver_artesanos():
    page_size = 5
    data = []
    for artesano in db.get_artesanos(page_size):
        id_artesano, comuna_id, descripcion, nombre, email, celular = artesano
        ruta_foto = db.get_foto(id_artesano)[0]
        print(ruta_foto)
        #Recuperar nombre de la comuna
        comuna = db.get_comuna(comuna_id)

        #Recuperar tipos de artesanía
        tipos = db.get_tipos(id_artesano)
        tipo_str = ""
        for tipo in tipos:
            tipo_str += tipo[0] + ", "

        data.append({
            "id_artesano": id_artesano,
            "comuna": comuna,
            "descripcion": descripcion,
            "nombre": nombre,
            "email": email,
            "celular": str(celular),
            "ruta_foto": str(ruta_foto),
            "tipo_artesania": tipo_str[:-2] #Elimino la última coma y espacio (,
        })

    return render_template('ver-artesanos.html', data = data)


@app.route('/buscar-persona', methods=['GET'])
def buscar_persona():
    #Hacer que los elementos de search-list en buscar-persona.html sean links a /comentarios/<nombre>
    return render_template('buscar-persona.html')


@app.route('/comentarios/<name_person>', methods=['GET'])
def comentarios(name_person):
    data= []
    test = db.get_comentarios(name_person)
    comentariossss = db.get_comentarios(name_person)

    for i_comentario in comentariossss:
        data.append({
            "id_comentario": i_comentario[0],
            "nombre": i_comentario[1],
            "email": i_comentario[2],
            "fecha": i_comentario[3],
            "comentario": i_comentario[4]
        })

    return render_template('comentarios.html', data = data, name_person = name_person)

@app.route('/agregar-comentario/<name>', methods=['GET', 'POST'])
def agregar_comentario(name):
    if request.method == 'POST':
        nombre = request.form['nombre_comentario']
        email = request.form['email_comentario']
        comentario = request.form['texto_comentario']
        #Ver si el nombre es de artesano o de hincha y entregar el id
        tipo, id_person = db.get_person_id(name)
        db.create_comentario(nombre, email, comentario, tipo, id_person)
        print("Agregado a la db")
        return redirect(url_for('comentarios', name_person = name))

    return render_template('agregar-comentario.html', name = name)

@app.route('/get-people/<title__substring>', methods=['GET'])
def get_people(title__substring):
    people = db.get_personas()
    #filtramos la lista de personas por el substring
    matches = [person for person in people if title__substring.lower() in person["nombre"].lower()]
    return jsonify({"status": "ok", "data": matches})

if __name__ == '__main__':
    app.run(debug=True)