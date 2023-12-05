import pymysql
import json


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