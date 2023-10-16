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

	#Chequeo que los valores estén bien
	print(comuna_id)

	cursor.execute("INSERT INTO artesano (comuna_id, descripcion_artesania, nombre, email, celular) VALUES (%s, %s, %s, %s, %s);", (comuna_id, desc_artesania, nombre_artesano, email_artesano, celular_artesano))

	#Obtengo la id del artesano recién creado
	cursor.execute("SELECT id FROM artesano WHERE nombre = %s;", (nombre_artesano))
	artesano_id = cursor.fetchone()[0]

	#Obtengo el id de cada tipo de artesanía
	for tipo in tipo_artesania:
		cursor.execute("SELECT id FROM tipo_artesania WHERE nombre = %s;", (tipo))
		tipo_id = cursor.fetchone()[0]
		cursor.execute("INSERT INTO artesano_tipo (artesano_id, tipo_artesania_id) VALUES (%s, %s);", (artesano_id, tipo_id))


	#Falta insertar la foto
	
	conn.commit()
