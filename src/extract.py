import pandas as pd

def extract_data(file_path):
    """Carga un archivo CSV en un DataFrame."""
    df = pd.read_csv(file_path)

    print(f"✅ Dataset cargado: {len(df)} filas, {len(df.columns)} columnas")

    return df