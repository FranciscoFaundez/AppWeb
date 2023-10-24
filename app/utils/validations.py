import re
import filetype

def validate_region(region):
    if (not region):
        return False
    return True

def validate_comuna(comuna):
    if (not comuna):
        return False
    return True

def validate_tipo_artesania(tipo_artesania):
    if (len(tipo_artesania)==0):
        return False
    #Queremos que los elementos seleccionados no sean más de 3
    if (len(tipo_artesania) > 3):
        return False
    return True

def validate_desc_artesania(desc_artesania):
    return True

def validate_foto(foto):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png"}

    #Check if a file was submited
    if (foto is None):
        return False
    if (foto.filename == ""):
        return False
    #Check file extension
    ftype_guess = filetype.guess(foto)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validate_nombre(nombre):
    if (not nombre):
        return False
    if (3 <= len(nombre) <= 80):
        return True
    return False

def validate_email(email):
    if (not email):
        return False
    email_regex = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    if (re.match(email_regex, email)):
        return True
    return False

def validate_telefono(telefono):
    if (not telefono):
        print("Teléfono vacío")
        return True
    telefono_regex = r"^(\+?56)?(\s?)(0?9)(\s?)[98765432]\d{7}$"
    if (re.match(telefono_regex, telefono)):
        print("Teléfono válido")
        return True
    print("Teléfono inválido")
    return False

def validate_form(region, comuna, tipo_artesania, desc_artesania, foto, nombre, email, telefono):
    if (validate_region(region) and validate_comuna(comuna) and validate_tipo_artesania(tipo_artesania) and validate_desc_artesania(desc_artesania) and validate_foto(foto) and validate_nombre(nombre) and validate_email(email) and validate_telefono(telefono)):
        print("Formulario válido")
        return True
    else:
        print("Formulario inválido")
        return False

