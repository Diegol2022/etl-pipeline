import re

import pandas as pd


# Si una columna de texto tiene más de este porcentaje de nulos, no se imputa
# con la moda (sería inventar demasiados datos) sino con un valor explícito.
UMBRAL_NULOS_TEXTO = 0.5
VALOR_DESCONOCIDO = "desconocido"


def to_snake_case(nombre):
    """Convierte un nombre de columna a snake_case (ej: 'PassengerId' -> 'passenger_id')."""
    nombre = str(nombre).strip()
    nombre = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", nombre)   # camelCase -> camel_Case
    nombre = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", nombre)  # HTMLParser -> HTML_Parser
    nombre = re.sub(r"[^0-9a-zA-Z]+", "_", nombre)             # espacios y símbolos -> _
    return nombre.strip("_").lower()


def normalize_column_names(df):
    """Normaliza los nombres de todas las columnas a snake_case."""
    nuevos_nombres = {col: to_snake_case(col) for col in df.columns}
    df = df.rename(columns=nuevos_nombres)

    print("🔤 Columnas normalizadas: " + ", ".join(df.columns))

    return df


def handle_missing_values(df):
    """Trata los valores ausentes según el tipo de cada columna.

    - Numéricas: se imputan con la mediana (robusta frente a outliers).
    - Texto con pocos nulos: se imputan con la moda (valor más frecuente).
    - Texto con muchos nulos (> UMBRAL_NULOS_TEXTO): se rellenan con
      'desconocido' para no inventar información.
    """
    nulos = df.isna().sum()
    columnas_con_nulos = nulos[nulos > 0]

    if columnas_con_nulos.empty:
        print("✅ No se encontraron valores ausentes")
        return df

    print("🔍 Valores ausentes encontrados:")
    for columna, cantidad in columnas_con_nulos.items():
        proporcion = cantidad / len(df)

        if pd.api.types.is_numeric_dtype(df[columna]):
            valor = df[columna].median()
            estrategia = f"mediana ({valor})"
        elif proporcion > UMBRAL_NULOS_TEXTO:
            valor = VALOR_DESCONOCIDO
            estrategia = f"'{VALOR_DESCONOCIDO}'"
        else:
            valor = df[columna].mode().iloc[0]
            estrategia = f"moda ('{valor}')"

        df[columna] = df[columna].fillna(valor)
        print(f"   - {columna}: {cantidad} nulos ({proporcion:.1%}) → rellenados con {estrategia}")

    return df


def transform_data(df):
    """Limpia y transforma el dataset."""

    # Normalizar nombres de columnas
    df = normalize_column_names(df)

    # Eliminar registros duplicados
    before = len(df)
    df = df.drop_duplicates().copy()
    duplicates_removed = before - len(df)

    print(f"🗑️ Duplicados eliminados: {duplicates_removed}")

    # Tratamiento de valores ausentes
    df = handle_missing_values(df)

    # Optimización básica de memoria
    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].astype("category")

    print("🧹 Transformación completada")

    return df
