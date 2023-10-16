from flask import Flask, render_template, request, redirect, url_for, flash
from database import db 

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
        db.create_artesano(region_artesano, comuna_artesano, tipo_artesania, desc_artesania, foto_artesania, nombre_artesano, email_artesano, celular_artesano)
        flash('Artesano agregado satisfactoriamente')
        return redirect(url_for('index'))

    #Si es es un GET
    #muestro las opciones de regiones y según lo elegido, muestro las comunas
    #leer el archivo de regiones y mostrarlas en el select
    with open('app/static/txt/regiones.txt', 'r', encoding='utf-8') as file:
        regiones = [line.strip() for line in file.readlines()]

    return render_template('agregar-artesano.html', regiones = regiones)


@app.route('/agregar-hincha', methods=['GET', 'POST'])
def agregar_hincha():
    return "agregar-hincha"

@app.route('/ver-hinchas', methods=['GET', 'POST'])
def ver_hinchas():
    return "ver-hinchas"


@app.route('/ver-artesanos', methods=['GET', 'POST'])
def ver_artesanos():
    return "ver-artesanos"






if __name__ == '__main__':
    app.run(debug=True)