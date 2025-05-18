import duckdb
import polars as pl



def cargar_y_limpia_rut(con, archivo, tabla):
    """
    Lee archivo CSV en DuckDB, agrega columna RUT_LIMPIO y lo guarda como tabla temporal.
    """
    con.execute(f"""
        CREATE OR REPLACE TABLE {tabla} AS
        SELECT
            *,
            regexp_replace(CAST(RUT AS VARCHAR), '-.*$', '') AS RUT_LIMPIO
        FROM read_csv_auto('{archivo}', delim='|', header=True)
    """)
    print(f"Cargado y limpiado: {archivo} → tabla '{tabla}'")


def main():
    archivo_detalle = "Archivo Comparativo.csv"
    archivo_base = "Archivo que se hace cruce.csv"
    archivo_salida = "Resultado.csv"

    con = duckdb.connect()

    # Carga y limpieza de RUT
    cargar_y_limpia_rut(con, archivo_detalle, "detalle")
    cargar_y_limpia_rut(con, archivo_base, "base")

    # Ejecuta el JOIN y guarda en un archivo Parquet temporal (más rápido para Polars)
    archivo_temp_parquet = "resultado_temp.parquet"
    con.execute(f"""
        COPY (
            SELECT 
                base.*,
                detalle."Tipo Gestion"
            FROM base
            LEFT JOIN detalle
            ON base.RUT_LIMPIO = detalle.RUT_LIMPIO
        ) TO '{archivo_temp_parquet}' (FORMAT PARQUET)
    """)

    print("🔄 JOIN completado, cargando resultado con Polars...")

    # Leer resultado en Polars y guardar como CSV con |
    df_resultado = pl.read_parquet(archivo_temp_parquet)
    df_resultado.write_csv(archivo_salida, separator="|")

    print(f"Archivo final guardado: {archivo_salida}")
    print("Vista previa:")
    print(df_resultado.head(10))


if __name__ == "__main__":
    main()
