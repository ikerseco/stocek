import os

from pathlib import Path

"""""
arr = []
def listar_todos_los_directorios_pathlib(raiz="/"):
    ruta = Path(raiz)
    print(f"Explorando desde la raíz: {ruta.resolve()}")
    for directorio in ruta.rglob("*"):  # Recursivamente busca todos los elementos
        if directorio.is_dir():
            print(f"Directorio: {directorio}")
        else:
            arr.append(directorio)

# Cambia '/' por 'C:\\' en Windows si quieres explorar desde la raíz del sistema.
listar_todos_los_directorios_pathlib("/")





"""""
import os


def listar_archivos_excluyendo_system32(raiz="C:\\"):
    arr = []
    print(f"Explorando desde la raíz: {raiz}")
    for directorio_actual, subdirectorios, archivos in os.walk(raiz):
        # Excluir el directorio System32
        subdirectorios[:] = [d for d in subdirectorios if d.lower() != "windows"]
        for archivo in archivos:
            print(os.path.join(directorio_actual, archivo))
            arr.append(os.path.join(directorio_actual, archivo))
    print(arr[4])

# Cambia 'C:\\' por la raíz de tu sistema.
listar_archivos_excluyendo_system32("C:\\")