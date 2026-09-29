import pandas as pd


def transform_data(df):
    """Limpia y transforma el dataset."""

    # Eliminar registros duplicados
    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)

    print(f"🗑️ Duplicados eliminados: {duplicates_removed}")

    # Optimización básica de memoria
    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].astype("category")

    print("🧹 Transformación completada")

    return df