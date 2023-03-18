import tkinter as tk
from tkinter import ttk
import pandas as pd

# Creamos un DataFrame de ejemplo
data = {'Nombre': ['Juan', 'Ana', 'Carlos', 'María'],
        'Edad': [25, 30, 40, 35],
        'País': ['México', 'España', 'Argentina', 'Colombia']}
df = pd.DataFrame(data)

# Función para manejar el evento de clic en la tabla
def on_click(event):
    row = (table.identify_row(event.y))  # Obtenemos la fila donde se hizo clic
    col = (table.identify_column(event.x))  # Obtenemos la columna donde se hizo clic
    print("Se hizo clic en la celda ({}, {})".format(row, col))

# Creamos la aplicación de tkinter
root = tk.Tk()
root.title('Tabla de datos')

# Creamos el widget Table
table = ttk.Treeview(root)
table['columns'] = list(df.columns)
table['show'] = 'headings'

# Agregamos las columnas a la tabla
for column in table['columns']:
    table.heading(column, text=column)

# Agregamos las filas a la tabla
for index, row in df.iterrows():
    table.insert('', 'end', values=list(row))

# Asociamos la función on_click al evento Button-1 (clic izquierdo) en la tabla
table.bind("<Button-1>", on_click)

# Empaquetamos la tabla en la ventana
table.pack()

# Ejecutamos la aplicación de tkinter
root.mainloop()
