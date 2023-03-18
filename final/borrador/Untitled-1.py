import tkinter as tk
import pandas as pd

# Creamos un DataFrame de ejemplo
data = {'Nombre': ['Juan', 'María', 'Pedro'], 'Edad': [25, 30, 35], 'Ciudad': ['Madrid', 'Barcelona', 'Valencia']}
df = pd.DataFrame(data)

# Creamos la ventana principal
root = tk.Tk()
root.geometry('600x400')

# Creamos un canvas para colocar la tabla
canvas = tk.Canvas(root, bg='black')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Creamos un frame para contener la tabla
frame = tk.Frame(canvas, bg='red')
canvas.create_window((0,0), window=frame, anchor='nw')

# Creamos una etiqueta para cada celda en el DataFrame
for i, row in df.iterrows():
    for j, value in enumerate(row):
        label = tk.Label(frame, text=value)
        label.grid(row=i, column=j)
        label.bind('<Button-1>', lambda event, row=i, col=j: print(f'Fila {row}, Columna {col}'))
        label.bindtags((label, frame, canvas, 'all'))




root.mainloop()