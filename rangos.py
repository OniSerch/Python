import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv("12052025_resultado_dim8.csv")

# Función para clasificar según "Dias de Mora"
def clasificar(mora):
    if 1 <= mora <= 14:
        return '01.[7-14]'
    elif 15 <= mora <= 30:
        return '02.[15-30]'
    elif 31 <= mora <= 60:
        return '03.[31-60]'
    elif 61 <= mora <= 90:
        return '04.[61-90]'
    elif 91 <= mora <= 180:
        return '05.[91-180]'
    else:
        return '06.[180+]'

# Asegurar que la columna sea numérica (por si viene como texto)
df['Dias de Mora'] = pd.to_numeric(df['Dias de Mora'], errors='coerce')

# Aplicar la función a una nueva columna
df['Rango Mora'] = df['Dias de Mora'].apply(clasificar)

# Guardar el resultado en un nuevo archivo
df.to_csv("12052025_resultado_dim8_con_rangos.csv", index=False)

print("Archivo guardado como '12052025_resultado_dim8_con_rangos.csv'")
