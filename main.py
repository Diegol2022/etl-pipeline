from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data


# Rutas
RUTA_CSV_ORIGEN = "data/raw/dataset.csv"
RUTA_PARQUET_DESTINO = "data/processed/dataset_procesado.parquet"


def main():

    print("🚀 Iniciando pipeline ETL...\n")

    # 1. Extracción
    print("📥 Etapa 1: Extracción")
    df = extract_data(RUTA_CSV_ORIGEN)

    # 2. Transformación
    print("\n🧹 Etapa 2: Transformación")
    df_transformado = transform_data(df)

    # 3. Carga
    print("\n💾 Etapa 3: Carga")
    load_data(df_transformado, RUTA_PARQUET_DESTINO)

    print("\n🎉 Pipeline ejecutado con éxito.")


if __name__ == "__main__":
    main()