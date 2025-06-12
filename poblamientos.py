import pandas as pd
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import re
import polars as pl


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|,]', '_', name)




# Aliases por compañía
def get_alias(company):
    company = company.strip()
    # Eliminar abreviación de país al inicio, si la hay
    if "/" in company:
        partes = company.split("/", 1)
        company = partes[1].strip()

    company_lower = company.lower()

    if "santander" in company_lower:
        return "san"
    elif "caja los andes" in company_lower:
        return "cla"
    elif "la polar" in company_lower:
        return "lp"
    elif "colektia-falabella perú" in company_lower:
        return "cfp"
    elif "falabella peru" in company_lower:
        return "fp"
    elif "techreo" in company_lower:
        return "tco"
    elif "openbank" in company_lower:
        return "ODS"
    else:
        # Si no hay alias conocido, limpiar espacios
        return company.replace(" ", "").lower()

# Procesamiento principal
def procesar_csv(filepath, tipo, salida):
    # Leer CSV como LazyFrame
    lazy_df = pl.read_csv(filepath).lazy()

    # Renombrar columnas quitando espacios
    schema = lazy_df.collect_schema()
    lazy_df = lazy_df.rename({col: col.strip() for col in schema})

    # Filtro base: Status == Done
    lazy_df = lazy_df.filter(pl.col("Status") == "Done")

    # Filtrar por tipo de request
    if tipo == "Poblamiento":
        lazy_df = lazy_df.filter(pl.col("Request_type") == "Poblamiento")
        sufijo = "_t_"
    elif tipo == "Reactivación":
        lazy_df = lazy_df.filter(pl.col("Request_type") == "Reactivación")
        sufijo = "_t_"
    else:
        messagebox.showerror("Error", "Tipo inválido.")
        return

    # Convertir LazyFrame a DataFrame real
    df = lazy_df.collect()

    # Filtrar por tipo de contacto (en minúsculas)
    df_email = df.filter(pl.col("Type").str.to_lowercase() == "email")
    df_phone = df.filter(pl.col("Type").str.to_lowercase() == "phone")

    # Obtener fecha actual
    fecha = datetime.today().strftime("%d%m")

    def exportar(df_contacto, tipo_contacto):
        # Obtener compañías únicas como lista de strings
        companias = df_contacto.get_column("Company").unique().to_list()

        for company in companias:
            alias = get_alias(company)
            if alias:
                df_final = df_contacto.filter(pl.col("Company") == company)
                extension = "_e_" if tipo_contacto == "email" else sufijo
                columna_contacto = "Email" if tipo_contacto == "email" else "telefono"
                filename = sanitize_filename(f"{alias}{extension}{fecha}.xlsx")
                ruta_final = os.path.join(salida, filename)

                # Convertir a pandas para exportar a Excel
                df_export = df_final.select(["Account", "Contact"]).to_pandas()
                df_export.columns = ["Cuenta", columna_contacto]
                df_export.to_excel(ruta_final, index=False)

    exportar(df_email, "email")
    exportar(df_phone, "phone")





# --- INTERFAZ ---
def seleccionar_archivo():
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if path:
        entry_csv.delete(0, tk.END)
        entry_csv.insert(0, path)

def seleccionar_carpeta():
    path = filedialog.askdirectory()
    if path:
        entry_salida.delete(0, tk.END)
        entry_salida.insert(0, path)

def on_check_poblamiento():
    check_reactivacion_var.set(0)

def on_check_reactivacion():
    check_poblamiento_var.set(0)

def ejecutar():
    ruta_csv = entry_csv.get()
    ruta_salida = entry_salida.get()

    tipo = None
    if check_poblamiento_var.get():
        tipo = "Poblamiento"
    elif check_reactivacion_var.get():
        tipo = "Reactivación"

    if not ruta_csv or not ruta_salida or not tipo:
        messagebox.showerror("Error", "Completa todos los campos y selecciona una opción.")
        return

    try:
        procesar_csv(ruta_csv, tipo, ruta_salida)
        messagebox.showinfo("Éxito", "Proceso finalizado con éxito.")
    except Exception as e:
        messagebox.showerror("Error en la ejecución", str(e))

# --- Interfaz con tkinter ---
root = tk.Tk()
root.title("Poblamientos y Reactivaciones")

tk.Label(root, text="Archivo CSV:").grid(row=0, column=0, sticky="w")
entry_csv = tk.Entry(root, width=60)
entry_csv.grid(row=0, column=1)
tk.Button(root, text="Seleccionar archivo", command=seleccionar_archivo).grid(row=0, column=2)

tk.Label(root, text="Carpeta de salida:").grid(row=1, column=0, sticky="w")
entry_salida = tk.Entry(root, width=60)
entry_salida.grid(row=1, column=1)
tk.Button(root, text="Seleccionar carpeta", command=seleccionar_carpeta).grid(row=1, column=2)

check_poblamiento_var = tk.IntVar()
check_reactivacion_var = tk.IntVar()

tk.Label(root, text="Selecciona tipo de acción:").grid(row=2, column=0, sticky="w")
tk.Checkbutton(root, text="Poblamiento", variable=check_poblamiento_var, command=on_check_poblamiento).grid(row=2, column=1, sticky="w")
tk.Checkbutton(root, text="Reactivación", variable=check_reactivacion_var, command=on_check_reactivacion).grid(row=3, column=1, sticky="w")

tk.Button(root, text="Ejecutar", command=ejecutar, bg="green", fg="white", padx=10).grid(row=4, column=1, pady=15)

root.mainloop()
