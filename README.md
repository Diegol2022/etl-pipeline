# Pipeline ETL de datos

Este proyecto implementa un pipeline ETL sencillo en Python para procesar el dataset de datos. En este caso de ejemplo son los pasajeros del Titanic. Lee los datos desde un archivo CSV, elimina registros duplicados y guarda el resultado en formato Parquet.

## Flujo del programa

El punto de entrada es `main.py`. Al ejecutarlo, procesa las etapas en este orden:

1. **Extracción:** lee `data/raw/dataset.csv` con pandas y muestra la cantidad de filas y columnas cargadas.
2. **Transformación:** elimina filas completamente duplicadas y convierte las columnas de tipo texto (`object`) a tipo `category` para reducir el uso de memoria.
3. **Carga:** escribe el DataFrame transformado en `data/processed/dataset_procesado.parquet`, sin guardar el índice.

La transformación no completa valores ausentes ni modifica los valores de las columnas; solo elimina duplicados y cambia el tipo de las columnas de texto.

## Requisitos

- Python instalado.
- Dependencias declaradas en `requirements.txt`: `pandas` y `pyarrow`.

Instala las dependencias desde la carpeta raíz del proyecto:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Desde la carpeta raíz del proyecto, ejecuta:

```bash
python main.py
```

El programa muestra mensajes de progreso y confirma la ruta del archivo generado. Las rutas de entrada y salida están definidas al principio de `main.py` y son relativas a la carpeta desde la que se ejecuta el comando. La carpeta `data/processed` debe existir antes de iniciar el pipeline.

## Estructura

```text
main.py                 # Coordina las etapas del pipeline
src/extract.py          # Lectura del CSV
src/transform.py        # Eliminación de duplicados y conversión de tipos
src/load.py             # Escritura del archivo Parquet
data/raw/dataset.csv    # Dataset de entrada
data/processed/         # Ubicación del resultado
requirements.txt        # Dependencias
```

El archivo de salida se puede leer posteriormente con pandas, por ejemplo:

```python
import pandas as pd

df = pd.read_parquet("data/processed/dataset_procesado.parquet")
```
