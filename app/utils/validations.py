import re

def validate_region(region):
    if (not region):
        print("Región vacía")
        return False
    print("región: " + region)
    return True

def validate_comuna(comuna):
    if (not comuna):
        print("Comuna vacía")
        return False
    print("comuna: " + comuna)
    return True

def validate_tipo_artesania(tipo_artesania):
    if (not tipo_artesania):
        return False
    return True


def validate_form(region):
    return validate_region(region)

