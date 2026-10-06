# Pipeline ETL de datos

Este proyecto implementa un pipeline ETL sencillo en Python para procesar un dataset. En este caso de ejemplo son los pasajeros del Titanic. Lee los datos desde un archivo CSV, normaliza los nombres de las columnas, elimina registros duplicados, trata los valores ausentes y guarda el resultado en formato Parquet.

## Flujo del programa

El punto de entrada es `main.py`. Al ejecutarlo, procesa las etapas en este orden:

1. **Extracción:** lee `data/raw/dataset.csv` con pandas y muestra la cantidad de filas y columnas cargadas.
2. **Transformación** (`src/transform.py`):
   1. **Normalización de columnas:** convierte todos los nombres a `snake_case` en minúsculas (por ejemplo, `PassengerId` → `passenger_id`, `SibSp` → `sib_sp`).
   2. **Eliminación de duplicados:** descarta las filas completamente repetidas.
   3. **Tratamiento de valores ausentes:** completa los nulos según el tipo de cada columna (ver detalle más abajo).
   4. **Optimización de memoria:** convierte las columnas de texto (`object`) a tipo `category`.
3. **Carga:** escribe el DataFrame transformado en `data/processed/dataset_procesado.parquet`, sin guardar el índice.

### Tratamiento de valores ausentes

| Tipo de columna | Estrategia | Motivo |
|---|---|---|
| Numérica | Mediana | Es robusta frente a valores extremos, a diferencia de la media. |
| Texto con hasta 50% de nulos | Moda (valor más frecuente) | Con pocos faltantes, es la estimación más probable. |
| Texto con más de 50% de nulos | Valor `"desconocido"` | Imputar la moda inventaría demasiada información; se deja explícito que el dato falta. |

En el dataset del Titanic esto resulta en:

| Columna | Nulos | Tratamiento |
|---|---|---|
| `age` | 177 (19,9%) | Mediana (28.0) |
| `cabin` | 687 (77,1%) | `"desconocido"` |
| `embarked` | 2 (0,2%) | Moda (`"S"`) |

El umbral del 50% se puede ajustar con la constante `UMBRAL_NULOS_TEXTO` al principio de `src/transform.py`. Durante la ejecución, el pipeline informa por consola cada columna con nulos, su proporción y la estrategia aplicada.

## ¿Por qué Parquet?

El resultado se guarda en Parquet en lugar de CSV por las siguientes razones técnicas:

- **Almacenamiento columnar:** los datos se guardan por columna y no por fila. Las consultas analíticas suelen leer solo algunas columnas, y con Parquet se puede cargar únicamente lo necesario (`pd.read_parquet(ruta, columns=["age", "fare"])`) sin recorrer el archivo completo.
- **Compresión eficiente:** al agrupar valores del mismo tipo, la compresión (Snappy por defecto en `pyarrow`) y las codificaciones como *dictionary encoding* o *run-length encoding* son mucho más efectivas. En este proyecto, el archivo Parquet ocupa unos 40 KB frente a los 59 KB del CSV original (alrededor de un 30% menos). En datasets grandes la diferencia suele ser bastante mayor.
- **Esquema y tipos de datos preservados:** el archivo guarda el tipo de cada columna (enteros, decimales, categorías, fechas). Un CSV es texto plano, así que al releerlo pandas tiene que volver a inferir los tipos, lo que puede dar errores (por ejemplo, códigos con ceros a la izquierda que se leen como números). Con Parquet, las columnas `category` creadas en la transformación se recuperan tal cual.
- **Lectura más rápida:** al no tener que interpretar texto ni inferir tipos, la carga es considerablemente más rápida que la de un CSV equivalente.
- **Metadatos y estadísticas:** cada bloque del archivo guarda estadísticas como mínimos y máximos por columna, lo que permite a los motores de consulta saltear bloques que no cumplen un filtro (*predicate pushdown*).
- **Estándar del ecosistema de datos:** es compatible de forma nativa con Spark, Polars, DuckDB, BigQuery, Amazon Athena, Snowflake y la mayoría de los data lakes, lo que facilita reutilizar la salida del pipeline en otras herramientas.

La contrapartida es que Parquet es un formato binario: no se puede abrir ni editar con un editor de texto o Excel como un CSV. Para un pipeline cuyo destino es el análisis de datos, esto no suele ser un inconveniente.

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
src/transform.py        # Normalización de columnas, duplicados, valores ausentes y tipos
src/load.py             # Escritura del archivo Parquet
data/raw/dataset.csv    # Dataset de entrada
data/processed/         # Ubicación del resultado
requirements.txt        # Dependencias
.gitignore              # Archivos excluidos del control de versiones
```

El archivo de salida se puede leer posteriormente con pandas. Hay que tener en cuenta que las columnas quedan en `snake_case`:

```python
import pandas as pd

df = pd.read_parquet("data/processed/dataset_procesado.parquet")

# Leer solo algunas columnas
df_parcial = pd.read_parquet(
    "data/processed/dataset_procesado.parquet",
    columns=["passenger_id", "age", "fare"],
)
```
