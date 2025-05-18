import polars as pl
import os

# Función para leer y mostrar las primeras filas de un archivo
def ver_csv(archivo):
    """Leer el archivo con el que vamos a validar el QA sea detalle clientes o gestiones."""
    print(f"Cargando archivo: {archivo}")   
    df = pl.read_csv(archivo, separator="|", has_header=True)
    print("Columnas detectadas:", df.columns)
    print(df.head(5))
    return df

# Función para guardar el DataFrame con delimitador personalizado
def guardar_csv_columnado(df: pl.DataFrame, nombre_salida: str, delimitador: str = "|"):
    df.write_csv(nombre_salida, separator=delimitador)
    print(f"Archivo guardado como '{nombre_salida}' con delimitador '{delimitador}'")

# Función para hacer join e insertar dim_8 en archivo 05052025
def unir_dim8_por_info1(archivo_detalle, archivo_base):
    """
    Hace un left join entre archivo_base y archivo_detalle usando info_1,
    y agrega la columna dim_8 del archivo detalle al archivo base.
    """
    detalle_df = pl.read_csv(archivo_detalle, separator="|", has_header=True)
    base_df = pl.read_csv(archivo_base, separator="|", has_header=True)

    # Verificamos columnas requeridas
    if "info_1" not in detalle_df.columns or "Dias de Mora" not in detalle_df.columns:
        raise ValueError("El archivo de detalle debe contener las columnas 'info_1' y 'Dias de Mora'")
    
    if "info_1" not in base_df.columns:
        raise ValueError("El archivo base debe contener la columna 'info_1'")

    # Join: base_df LEFT JOIN detalle_df para conservar todos los registros del archivo base
    resultado = base_df.join(detalle_df.select(["info_1", "Dias de Mora"]), on="info_1", how="left")

    # Guardar resultado
    resultado.write_csv("12052025_resultado_dim8.csv", separator="|")
    print("Archivo '12052025_resultado_dim8.csv' guardado con columna 'dim_8' agregada.")
    return resultado

# Función principal
def main():
    archivo_principal = "Detalle_de_Clientes_14-mayo-2025_8a6eca0d-3b90-45cb-a433-0fa30fa3075b.csv"
    archivo_secundario = "colektia_20250513.csv"

    # Leer y guardar archivo columnado
    df1 = ver_csv(archivo_principal)
    archivo_columnado = "Detalle_de_Clientes_columnado.csv"
    guardar_csv_columnado(df1, archivo_columnado)

    # Hacer el join y generar resultado
    resultado = unir_dim8_por_info1(archivo_columnado, archivo_secundario)
    print("\nVista previa del archivo final con dim_8:")
    print(resultado.head(10))

# Ejecutar si es el archivo principal
if __name__ == "__main__":
    main()
