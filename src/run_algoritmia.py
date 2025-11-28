import sys
import os
from antlr4 import *

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SRC_DIR, "temp")
MEDIA_DIR = os.path.join(SRC_DIR, "media")

# --- IMPORTACIONES DEL LENGUAJE ---
sys.path.append(SRC_DIR)

try:
    from algoritmia.AlgoritmiaLexer import AlgoritmiaLexer
    from algoritmia.AlgoritmiaParser import AlgoritmiaParser
    from algoritmia.Executor import AlgoritmiaExecutor
except ImportError as e:
    print(" Error de importación. Asegúrate de haber generado los archivos de ANTLR.")
    print(f"Detalle: {e}")
    sys.exit(1)


def listar_archivos():
    print("\n Archivos .alg disponibles en temp/:")
    if not os.path.exists(TEMP_DIR):
        print(f"   (No existe el directorio {TEMP_DIR})")
        return

    archivos = [f for f in os.listdir(TEMP_DIR) if f.endswith(".alg")]
    if not archivos:
        print("   (La carpeta está vacía)")
    else:
        for f in archivos:
            print(f" - {f}")


def procesar_archivo(nombre_archivo, entry_point="Main"):
    ruta_completa = os.path.join(TEMP_DIR, nombre_archivo)

    if not os.path.isfile(ruta_completa):
        print(f" El archivo no existe: {ruta_completa}")
        return

    print("\n" + "=" * 40)
    print(f"  Ejecutando Algoritmia...")
    print(f"  Archivo: {nombre_archivo}")
    print(f"  Inicio : {entry_point}")
    print("=" * 40 + "\n")

    try:
        input_stream = FileStream(ruta_completa, encoding='utf-8') # Lectura del archivo

        # Análisis Léxico y Sintáctico
        lexer = AlgoritmiaLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = AlgoritmiaParser(stream)

        tree = parser.programa()

        # DETECCIÓN DE ERRORES SINTÁCTICOS
        n_errors = parser.getNumberOfSyntaxErrors()
        if n_errors > 0:
            print(f"\n [!] Se encontraron {n_errors} errores de sintaxis.")
            print("     La ejecución se ha cancelado para evitar fallos.")
            return

        # Conf Ejecutor
        visitor = AlgoritmiaExecutor()

        # Conf Visitor
        nombre_base = os.path.splitext(nombre_archivo)[0]
        visitor.output_filename = nombre_base  # Para que el archivo de salida se llame igual

        if entry_point and entry_point.strip():
            visitor.entry_point = entry_point.strip()

        # El Executor se genera los archivos al final
        visitor.visit(tree)


        print(f"\n [Proceso Finalizado]")
        print(f" Archivos generados en: {MEDIA_DIR}")

    except Exception as e:
        print(f"\n Error durante la ejecución: {e}")
        # import traceback; traceback.print_exc()


if __name__ == "__main__":
    try:
        listar_archivos()
        print("\n--- Configuración de Ejecución ---")
        archivo = input("1. Nombre del archivo (ej: piano.alg): ").strip()

        if archivo:
            proc = input("2. Procedimiento inicial (Enter para 'Main'): ").strip()
            if not proc: proc = "Main"

            procesar_archivo(archivo, proc)
        else:
            print(" Debes escribir un nombre de archivo.")

    except KeyboardInterrupt:
        print("\n Ejecución cancelada.")