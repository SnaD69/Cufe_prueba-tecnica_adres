Extractor de CUFE en Archivos

Este proyecto consiste en un script en Python que extrae información específica del CUFE (Código Único de Facturación Electrónica) de archivos utilizando una expresión regular definida. La información extraída se almacena en una base de datos SQLite, lo que permite una gestión eficiente de los datos.

Funcionalidades

Extracción de CUFE: Utiliza la expresión regular (\b([0-9a-fA-F]\n*){95,100}\b) para identificar y extraer el CUFE de los archivos.

Almacenamiento en SQLite: La información extraída se guarda en una base de datos SQLite con los siguientes campos:
-Nombre del archivo: El nombre del archivo de donde se extrajo el CUFE.
-Número de páginas: La cantidad de páginas del archivo.
-CUFE: El código único extraído.
-Peso del archivo: El tamaño del archivo en bytes.

Requisitos:
 -Python 3.x
 -Bibliotecas necesarias: sqlite3, re, os# Programa-Python
