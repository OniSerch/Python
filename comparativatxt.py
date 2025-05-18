import tkinter as tk
from tkinter import filedialog, messagebox

# Función para cargar archivo y devolver líneas únicas
def cargar_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if not ruta:
        return None, None
    with open(ruta, 'r', encoding='utf-8') as f:
        lineas = f.read().splitlines()
    return set(lineas), ruta

# Función para comparar archivos
def comparar():
    resultado_text.delete('1.0', tk.END)

    contenido1, ruta1 = cargar_archivo()
    if contenido1 is None:
        return
    contenido2, ruta2 = cargar_archivo()
    if contenido2 is None:
        return

    # Solo mostrar lo que falta en archivo 2 para que sea como archivo 1
    faltantes_en_2 = sorted(contenido1 - contenido2)

    resultado_text.insert(tk.END, f"Líneas que están en {ruta1} pero NO en {ruta2}:\n\n")
    resultado_text.insert(tk.END, '\n'.join(faltantes_en_2))

    # Guardar en archivo
    with open('faltantes_en_archivo2.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(faltantes_en_2))

    messagebox.showinfo("Resultado", "Comparación completada.\nSe guardó el archivo: faltantes_en_archivo2.txt")

# Interfaz
root = tk.Tk()
root.title("Verificar Faltantes en TXT")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_comparar = tk.Button(frame, text="Seleccionar Archivos TXT y Verificar Faltantes", command=comparar)
btn_comparar.pack()

resultado_text = tk.Text(root, wrap=tk.WORD, height=20)
resultado_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
