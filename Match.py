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
    if "RUT" not in detalle_df.columns or "Tipo Gestion" not in detalle_df.columns:
        raise ValueError("El archivo de detalle debe contener las columnas 'RUT' y 'Tipo Gestion'")
    
    if "RUT" not in base_df.columns:
        raise ValueError("El archivo base debe contener la columna 'RUT'")


    detalle_df = detalle_df.with_columns(pl.col("RUT").cast(pl.Utf8)).with_columns(pl.col("RUT").str.split("-").list.get(0).alias("RUT_LIMPIO")
    ).select(["RUT_LIMPIO", "Tipo Gestion"])

    base_df = base_df.with_columns(pl.col("RUT").cast(pl.Utf8)).with_columns(pl.col("RUT").str.split("-").list.get(0).alias("RUT_LIMPIO"))

    resultado_df = base_df.join(detalle_df,on="RUT_LIMPIO",how="left").drop("RUT_LIMPIO")

    resultado_df.write_csv("CasosGestionesMAYO.csv", separator="|")
    print("Archivo generado: CasosGestionesMAYO.csv")
    return resultado_df



# Función principal
def main():
    archivo_principal = "ArchivoComparativo.csv"
    archivo_secundario = "Archivo Base.csv"    

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
