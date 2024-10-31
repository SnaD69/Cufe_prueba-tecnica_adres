import os
import re
import sqlite3
import fitz  # PyMuPDF para leer PDFs

# Expresión regular para el CUFE
CUFE_REGEX = r"\b([0-9a-fA-F]\n*){95,100}\b"

# Ruta al directorio que contiene los archivos PDF
pdf_directory = 'C:/Users/Usuario/Desktop/Programa python/pdf'

# Conectar a la base de datos SQLite o crearla si no existe
conn = sqlite3.connect("facturas.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS facturas (
        nombre_archivo TEXT PRIMARY KEY,
        numero_paginas INTEGER,
        cufe TEXT,
        peso INTEGER
    )
""")
conn.commit()

# Función para extraer información del PDF
def extract_pdf_info(file_path):
    # Nombre del archivo
    file_name = os.path.basename(file_path)
    # Peso del archivo en bytes
    file_size = os.path.getsize(file_path)

    # Abrir el archivo PDF
    with fitz.open(file_path) as pdf:
        # Número de páginas
        num_pages = pdf.page_count

        # Buscar el CUFE en cada página
        cufe = None
        for page_num in range(num_pages):
            page = pdf[page_num]
            text = page.get_text("text")
            match = re.search(CUFE_REGEX, text)
            if match:
                cufe = match.group(0).replace("\n", "")  # Quitar saltos de línea
                break  # Salir después de encontrar el primer CUFE válido

    return file_name, num_pages, cufe, file_size

# Contar cuántos archivos PDF hay en el directorio
pdf_files = [file for file in os.listdir(pdf_directory) if file.lower().endswith('.pdf')]
num_files = len(pdf_files)

print(f"Se encontraron {num_files} archivos PDF en la carpeta.\n")

# Procesar todos los archivos PDF en el directorio
for file_name in pdf_files:
    pdf_path = os.path.join(pdf_directory, file_name)
    file_name, num_pages, cufe, file_size = extract_pdf_info(pdf_path)

    # Verificar si los datos ya existen en la base de datos
    cursor.execute("SELECT * FROM facturas WHERE nombre_archivo = ?", (file_name,))
    existing_data = cursor.fetchone()

    if existing_data:
        # Pedir confirmación para sobrescribir
        confirm = input(f"Los datos para '{file_name}' ya existen. ¿Deseas sobrescribirlos? (s/n): ")
        if confirm.lower() != 's':
            print(f"No se modificará la entrada para {file_name}.\n")
            continue  # Saltar a la siguiente iteración

    # Verificar que el CUFE se haya encontrado y mostrar los datos extraídos
    if cufe is not None:
        print(f"Nombre del archivo: {file_name}")
        print(f"Número de páginas: {num_pages}")
        print(f"CUFE encontrado: {cufe}")
        print(f"Peso del archivo: {file_size} bytes\n")

        # Insertar o actualizar los datos en la base de datos
        cursor.execute("""
            INSERT OR REPLACE INTO facturas (nombre_archivo, numero_paginas, cufe, peso)
            VALUES (?, ?, ?, ?)
        """, (file_name, num_pages, cufe, file_size))
        conn.commit()
        print(f"Datos insertados/actualizados correctamente en la base de datos.")
    else:
        print(f"No se encontró un CUFE en el archivo: {file_name}")

# Cerrar la conexión a la base de datos
conn.close()

print("Proceso completado. Los datos han sido almacenados en la base de datos SQLite.")
