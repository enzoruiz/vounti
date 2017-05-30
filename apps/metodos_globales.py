from apps.inicio.models import Ubigeo


def get_departamentos(codigo):
    ubigeo = Ubigeo.objects.all()
    departamentos = {}
    for elemento in ubigeo:
        if (elemento.codigo[:2] == codigo
                and elemento.codigo[:4] != elemento.codigo[:2]+'00'):
            departamentos[elemento.codigo[:4]] = elemento.nombre

    return departamentos


def get_provincias(codigo):
    ubigeo = Ubigeo.objects.all()
    provincias = {}
    for elemento in ubigeo:
        if (elemento.codigo[:4] == codigo
                and elemento.codigo[:6] != elemento.codigo[:4]+'00'):
            provincias[elemento.codigo[:6]] = elemento.nombre

    return provincias


def get_distritos(codigo):
    ubigeo = Ubigeo.objects.all()
    distritos = {}
    for elemento in ubigeo:
        if (elemento.codigo[:6] == codigo
                and elemento.codigo[:8] != elemento.codigo[:6]+'00'):
            distritos[elemento.codigo[:8]] = elemento.nombre

    return distritos
