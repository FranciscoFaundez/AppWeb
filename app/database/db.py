import pymysql
import json
from datetime import datetime


DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306
DB_CHARSET = "utf8"

# -- conn ---
def get_conn():
	conn = pymysql.connect(
		db=DB_NAME,
		user=DB_USERNAME,
		passwd=DB_PASSWORD,
		host=DB_HOST,
		port=DB_PORT,
		charset=DB_CHARSET
	)
	return conn

def create_artesano(region_artesano, comuna_artesano, tipo_artesania, desc_artesania, foto_artesania, nombre_artesano, email_artesano, celular_artesano):
	conn = get_conn()
	cursor = conn.cursor()

	#Obtengo la id de la comuna dada
	cursor.execute("SELECT id FROM comuna WHERE nombre = %s;", (comuna_artesano))
	comuna_id = cursor.fetchone()[0]

	cursor.execute("INSERT INTO artesano (comuna_id, descripcion_artesania, nombre, email, celular) VALUES (%s, %s, %s, %s, %s);", (comuna_id, desc_artesania, nombre_artesano, email_artesano, celular_artesano))

	#Obtengo la id del artesano recién creado
	cursor.execute("SELECT id FROM artesano WHERE nombre = %s;", (nombre_artesano))
	artesano_id = cursor.fetchone()[0]

	#Obtengo el id de cada tipo de artesanía los tipos del artesano que estoy creando
	for tipo in tipo_artesania:
		cursor.execute("SELECT id FROM tipo_artesania WHERE nombre = %s;", (tipo))
		tipo_id = cursor.fetchone()[0]
		cursor.execute("INSERT INTO artesano_tipo (artesano_id, tipo_artesania_id) VALUES (%s, %s);", (artesano_id, tipo_id))


	#Inserto la foto
	cursor.execute("INSERT INTO foto (ruta_archivo, nombre_archivo, artesano_id) VALUES (%s, %s, %s);", ("uploads/" + foto_artesania, foto_artesania, artesano_id))
	
	conn.commit()

def create_hincha(deporte, region_hincha, comuna_hincha, transporte, nombre_hincha, email_hincha, telefono_hincha, comentarios):
	conn = get_conn()
	cursor = conn.cursor()

	#Obtengo la id de la comuna dada
	cursor.execute("SELECT id FROM comuna WHERE nombre = %s;", (comuna_hincha))
	comuna_id = cursor.fetchone()[0]

	cursor.execute("INSERT INTO hincha (comuna_id, modo_transporte, nombre, email, celular, comentarios) VALUES (%s, %s, %s, %s, %s, %s);", (comuna_id, transporte, nombre_hincha, email_hincha, telefono_hincha, comentarios))

	#Obtengo la id del hincha recién creado
	cursor.execute("SELECT id FROM hincha WHERE nombre = %s;", (nombre_hincha))
	hincha_id = cursor.fetchone()[0]

	#Obtengo el id de los deportes
	for dep in deporte:
		cursor.execute("SELECT id FROM deporte WHERE nombre = %s;", (dep))
		dep_id = cursor.fetchone()[0]
		cursor.execute("INSERT INTO hincha_deporte (hincha_id, deporte_id) VALUES (%s, %s);", (hincha_id, dep_id))
	
	conn.commit()


def get_artesanos(page_size):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM artesano  ORDER BY id DESC LIMIT %s;", (page_size))
	artesanos = cursor.fetchall()
	return artesanos

def get_hinchas(page_size):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM hincha  ORDER BY id DESC LIMIT %s;", (page_size))
	hinchas = cursor.fetchall()
	return hinchas

def get_foto(artesano_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute("SELECT ruta_archivo FROM foto WHERE artesano_id = %s;", (artesano_id))
	foto = cursor.fetchone()
	return foto

def get_comuna(comuna_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute("SELECT nombre FROM comuna WHERE id = %s;", (comuna_id))
	comuna = cursor.fetchone()[0]
	return comuna

def get_tipos(artesano_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute("SELECT tipo_artesania.nombre FROM tipo_artesania, artesano_tipo WHERE artesano_tipo.artesano_id = %s AND artesano_tipo.tipo_artesania_id = tipo_artesania.id;", (artesano_id))
	tipos = cursor.fetchall()
	return tipos

def get_deportes(hincha_id):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute("SELECT deporte.nombre FROM deporte, hincha_deporte WHERE hincha_deporte.hincha_id = %s AND hincha_deporte.deporte_id = deporte.id;", (hincha_id))
	deportes = cursor.fetchall()
	return deportes

#Obtiene las personas de la base de datos,incluyendo hinchas y artesanos
def get_personas():
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM artesano;")
	artesanos = cursor.fetchall()
	cursor.execute("SELECT * FROM hincha;")
	hinchas = cursor.fetchall()	

	personas = []
	for artesano in artesanos:
		#obtener comuna de cada artesano
		cursor.execute("SELECT nombre FROM comuna WHERE id = %s;", (artesano[1]))
		comuna = cursor.fetchone()[0]
		personas.append({
			"tipo": "artesano",
			"id": artesano[0],
			"comuna": comuna,
			"nombre": artesano[3],
			"email": artesano[4],
		})
	for hincha in hinchas:
		#obtener comuna de cada hincha
		cursor.execute("SELECT nombre FROM comuna WHERE id = %s;", (hincha[1]))
		comuna = cursor.fetchone()[0]
		personas.append({
			"tipo": "hincha",
			"id": hincha[0],
			"comuna": comuna,
			"nombre": hincha[3],
			"email": hincha[4],
			"comentarios": hincha[6]
		})

	return personas

#Get comentarios in the database "comentario" by the id of the person
def get_comentarios(name_person):
	conn = get_conn()
	cursor = conn.cursor()

	#Obtener el id de la persona
	_, person_id = get_person_id(name_person)

	cursor.execute("SELECT * FROM comentario WHERE id_hincha = %s ORDER BY fecha;", (person_id))
	comentarios = cursor.fetchall()
	#Si comentarios es vacío, intentarlo con artesano
	if len(comentarios) == 0:
		cursor.execute("SELECT * FROM comentario WHERE id_artesano = %s ORDER BY fecha;", (person_id))
		comentarios = cursor.fetchall()
		
	return comentarios

def create_comentario(nombre, email, comentario, tipo, id_person):
	conn = get_conn()
	cursor = conn.cursor()
	if tipo == "artesano":
		cursor.execute("INSERT INTO comentario (nombre, email, fecha, comentario, id_artesano) VALUES (%s, %s, %s, %s, %s);", (nombre, email, datetime.now(), comentario, id_person))
	elif tipo == "hincha":
		cursor.execute("INSERT INTO comentario (nombre, email, fecha, comentario, id_hincha) VALUES (%s, %s, %s, %s, %s);", (nombre, email, datetime.now(), comentario, id_person))
	conn.commit()

#Retornar si es artesano o hincha y retornar el id
def get_person_id(name):
	conn = get_conn()
	cursor = conn.cursor()
	cursor.execute("SELECT id FROM artesano WHERE nombre = %s;", (name))
	artesano_id = cursor.fetchone()
	cursor.execute("SELECT id FROM hincha WHERE nombre = %s;", (name))
	hincha_id = cursor.fetchone()
	if artesano_id is not None:
		return "artesano", artesano_id[0]
	elif hincha_id is not None:
		return "hincha", hincha_id[0]
	else:
		return "", None