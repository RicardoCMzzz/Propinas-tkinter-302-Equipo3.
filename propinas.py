import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# CONFIGURACIÓN DE LA BASE DE DATOS
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "PROPINAS",
    "port": 3306
}


# FUNCIÓN PARA CALCULAR LA PROPINA
def calcular():

    total_texto = entry_total.get().strip()
    porc_texto = entry_porc.get().strip()

    if total_texto == "" or porc_texto == "":
        messagebox.showwarning(
            "Falta un dato",
            "Por favor llena los dos campos."
        )
        return

    try:
        total = float(total_texto)
        porcentaje = float(porc_texto)

    except ValueError:
        messagebox.showerror(
            "Dato inválido",
            "Solo puedes escribir números. Revisa los campos."
        )
        return

    if total < 0 or porcentaje < 0:
        messagebox.showwarning(
            "Dato inválido",
            "No puedes poner números negativos."
        )
        return

    # OPERACIONES
    propina = total * (porcentaje / 100)
    total_pagar = total + propina

    # MOSTRAR RESULTADOS
    label_propina.config(
        text=f"Propina: ${propina:.2f}"
    )

    label_total_pagar.config(
        text=f"Total a pagar: ${total_pagar:.2f}"
    )

    # GUARDAR EN MYSQL
    try:
        conn = mysql.connector.connect(**DB_CONFIG)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO cuentas
            (total_cuenta, porcentaje, propina, total_pagar)
            VALUES (%s, %s, %s, %s)
            """,
            (total, porcentaje, propina, total_pagar)
        )

        conn.commit()

        label_guardado.config(
            text="Guardado en PROPINAS ✓",
            fg="green"
        )

        cursor.close()
        conn.close()

    except Error as e:
        messagebox.showerror(
            "Error XAMPP",
            f"Prende MySQL en XAMPP y vuelve a intentar:\n{e}"
        )


# FUNCIÓN PARA LIMPIAR
def limpiar():

    entry_total.delete(0, tk.END)
    entry_porc.delete(0, tk.END)

    label_propina.config(
        text="Propina: $0.00"
    )

    label_total_pagar.config(
        text="Total a pagar: $0.00"
    )

    label_guardado.config(text="")


# VENTANA PRINCIPAL
ventana = tk.Tk()

ventana.title("PROPINAS")
ventana.geometry("350x320")
ventana.resizable(False, False)


# TÍTULO
tk.Label(
    ventana,
    text="PROPINAS",
    font=("Arial", 16, "bold italic")
).pack(pady=10)


# CAMPO DEL TOTAL
tk.Label(
    ventana,
    text="Total de la cuenta:"
).pack()

entry_total = tk.Entry(
    ventana,
    width=30,
    justify="center"
)

entry_total.pack(pady=5)


# CAMPO DEL PORCENTAJE
tk.Label(
    ventana,
    text="Porcentaje de propina (%):"
).pack()

entry_porc = tk.Entry(
    ventana,
    width=30,
    justify="center"
)

entry_porc.pack(pady=5)


# BOTÓN CALCULAR
tk.Button(
    ventana,
    text="Calcular",
    command=calcular,
    bg="#33CCCC",
    fg="white",
    width=20,
    bd=10,
    font=("Arial", 11, "bold italic")
).pack(pady=10)


# RESULTADO DE LA PROPINA
label_propina = tk.Label(
    ventana,
    text="Propina: $0.00",
    font=("Arial", 12)
)

label_propina.pack()


# RESULTADO TOTAL
label_total_pagar = tk.Label(
    ventana,
    text="Total a pagar: $0.00",
    font=("Arial", 12, "bold italic")
)

label_total_pagar.pack()


# MENSAJE DE GUARDADO
label_guardado = tk.Label(
    ventana,
    text="",
    font=("Arial", 9)
)

label_guardado.pack(pady=5)


# BOTÓN LIMPIAR
tk.Button(
    ventana,
    text="Limpiar",
    command=limpiar,
    width=15
).pack()


# EJECUTAR PROGRAMA
ventana.mainloop()
