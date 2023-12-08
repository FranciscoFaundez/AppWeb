import re
import filetype

def validate_region(region):
    if (not region):
        print("Región vacía")
        return False
    return True

def validate_comuna(comuna):
    if (not comuna):
        print("Comuna vacía")
        return False
    return True

def validate_tipo_artesania(tipo_artesania):
    if (len(tipo_artesania)==0):
        print("No se seleccionó ningún tipo de artesanía")
        return False
    #Queremos que los elementos seleccionados no sean más de 3
    if (len(tipo_artesania) > 3):
        print("Se seleccionaron más de 3 tipos de artesanía")
        return False
    return True

def validate_desc_artesania(desc_artesania):
    return True

def validate_foto(foto):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png"}

    #Check if a file was submited
    if (foto is None):
        print("No se subió ninguna foto")
        return False
    if (foto.filename == ""):
        print("No se subió ninguna foto")
        return False
    #Check file extension
    ftype_guess = filetype.guess(foto)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        print("Extensión inválida")
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        print("Mimetype inválido")
        return False
    return True

def validate_nombre(nombre):
    if (not nombre):
        print("Nombre vacío")
        return False
    if (3 <= len(nombre) <= 80):
        return True
    print("Nombre inválido")
    return False

def validate_email(email):
    if (not email):
        print("Email vacío")
        return False
    email_regex = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    if (re.match(email_regex, email)):
        return True
    print("Email inválido")
    return False

def validate_telefono(telefono):
    if (not telefono):
        return True
    telefono_regex = r"^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$"
    if (re.match(telefono_regex, telefono)):
        return True
    print("Teléfono inválido")
    return False

def validate_deporte(deporte):
    if (len(deporte)==0):
        print("Deporte vacío")
        return False
    #Queremos que los elementos seleccionados no sean más de 3
    if (len(deporte) > 3):
        print("Muchos deportes seleccionados")
        return False
    return True

def validate_transporte(transporte):
    if (not transporte):
        print("Transporte inválido")
        return False
    return True


def validate_form(region, comuna, tipo_artesania, desc_artesania, foto, nombre, email, telefono):
    if (validate_region(region) and validate_comuna(comuna) and validate_tipo_artesania(tipo_artesania) and validate_desc_artesania(desc_artesania) and validate_foto(foto) and validate_nombre(nombre) and validate_email(email) and validate_telefono(telefono)):
        print("Formulario válido")
        return True
    else:
        print("Formulario inválido")
        return False

def validate_form_hincha(deporte, region, comuna, transporte, nombre, email, telefono, comentarios):
    if (validate_deporte(deporte) and validate_region(region) and validate_comuna(comuna) and validate_transporte(transporte) and validate_nombre(nombre) and validate_email(email) and validate_telefono(telefono)):
        print("Formulario válido")
        return True
    else:
        print("Formulario inválido")
        return False