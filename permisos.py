# permisos.py

PERMISOS = {
    "admin": {
        "inventario": ["ver", "agregar", "editar", "eliminar"],
        "reportes": ["ver", "exportar", "dashboard"],
        "ventas": ["ver", "crear"],
        "compras": ["ver", "crear"],
        "usuarios": ["ver", "crear", "editar", "eliminar"]
    },
    "vendedor": {
        "inventario": ["ver"],
        "reportes": ["ver", "dashboard"],
        "ventas": ["ver", "crear"],
        "compras": [],
        "usuarios": []
    },
    "auditor": {
        "inventario": ["ver"],
        "reportes": ["ver", "dashboard"],
        "ventas": ["ver"],
        "compras": ["ver"],
        "usuarios": []
    },
    "usuario": {
        "inventario": ["ver", "agregar"],
        "reportes": [],
        "ventas": [],
        "compras": [],
        "usuarios": []
    }
}


def tiene_permiso(rol, modulo, accion):
    return accion in PERMISOS.get(rol, {}).get(modulo, [])
