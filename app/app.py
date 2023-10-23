from flask import Flask, render_template, redirect, url_for, flash, request, session
from database import db 
from utils.validations import validate_form
import hashlib
import filetype
from werkzeug.utils import secure_filename
import os
import uuid

app = Flask(__name__)


app.secret_key = 'mysecretkey'



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

            #2. Save img in static/img
            foto_artesania.save(os.path.join(app.config["UPLOAD_FOLDER"], img_filename))

            #3. Save form in db
            db.create_artesano(region_artesano, comuna_artesano, tipo_artesania, desc_artesania, foto_artesania, nombre_artesano, email_artesano, celular_artesano)
            print("Agregado a la db")
        return redirect(url_for('index'))

    with open('app/static/txt/regiones.txt', 'r', encoding='utf-8') as file:
        regiones = [line.strip() for line in file.readlines()]

    return render_template('agregar-artesano.html', regiones = regiones)


@app.route('/agregar-hincha', methods=['GET', 'POST'])
def agregar_hincha():
    if request.method == 'POST':
        deporte       = request.form['deporte']
        region_hincha = request.form['region_hincha']
        comuna_hincha = request.form['comuna_hincha']
        transporte    = request.form['transporte']
        nombre_hincha = request.form['nombre_hincha']
        email_hincha  = request.form['email_hincha']
        telefono_hincha = request.form['telefono_hincha']
        comentarios   = request.form['comentarios']
        #db.create_hincha(...)
        flash('Hincha agregado satisfactoriamente')
        return redirect(url_for('index'))
    
    with open('app/static/txt/deportes.txt', 'r', encoding='utf-8') as file:
        deportes = [line.strip() for line in file.readlines()]

    with open('app/static/txt/regiones.txt', 'r', encoding='utf-8') as file:
        regiones = [line.strip() for line in file.readlines()]

    return render_template('agregar-hincha.html', deportes = deportes, regiones = regiones)


@app.route('/ver-hinchas', methods=['GET', 'POST'])
def ver_hinchas():
    return "ver-hinchas"


@app.route('/ver-artesanos', methods=['GET', 'POST'])
def ver_artesanos():
    return "ver-artesanos"






if __name__ == '__main__':
    app.run(debug=True)