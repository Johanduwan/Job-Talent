import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests

# Crear base de datos y usuario de ejemplo si no existe
def crear_base_datos():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT,
            password TEXT
        )
    """)
    # Agregar un usuario de prueba si no existe
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", ("admin", "1234"))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ("admin", "1234"))
    conn.commit()
    conn.close()

# Validar usuario contra la base de datos
def validar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (usuario, contrasena))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        mostrar_api()
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Mostrar personajes desde la API de Rick and Morty
def mostrar_api():
    ventana_login.destroy()
    ventana_api = tk.Tk()
    ventana_api.title("Rick and Morty API")

    label = tk.Label(ventana_api, text="Personajes de Rick and Morty", font=("Arial", 14, "bold"))
    label.pack(pady=10)

    try:
        response = requests.get("https://rickandmortyapi.com/api/character")
        data = response.json()
        for personaje in data["results"][:10]:  # Mostrar los primeros 10
            tk.Label(ventana_api, text=personaje["name"]).pack()
    except:
        tk.Label(ventana_api, text="Error al conectar con la API.").pack()

    ventana_api.mainloop()

# Crear interfaz de login
crear_base_datos()
ventana_login = tk.Tk()
ventana_login.title("Login")

tk.Label(ventana_login, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
entry_usuario = tk.Entry(ventana_login)
entry_usuario.grid(row=0, column=1)

tk.Label(ventana_login, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
entry_contrasena = tk.Entry(ventana_login, show="*")
entry_contrasena.grid(row=1, column=1)

tk.Button(ventana_login, text="Login", command=validar_login).grid(row=2, column=0, columnspan=2, pady=10)

ventana_login.mainloop()
