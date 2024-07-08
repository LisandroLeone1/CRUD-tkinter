from tkinter import *
from tkinter import messagebox
import sqlite3

def conexionBBDD():
    miConexion = sqlite3.connect("Usuarios")
    cursor= miConexion.cursor()

    try:
        cursor.execute('''
            CREATE TABLE DATOUSUARIOS(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE VARCHAR(50),
            CONTRASEÑA VARCHAR(50),
            APELLIDO VARCHAR(15),
            DIRECCION VARCHAR(50),
            COMENTARIOS VARCHAR(100))         
            ''')
        
        messagebox.showinfo("BBDD","BBDD creada correctamente")
    except:
        messagebox.showwarning("¡Atencion!","La BBDD ya existe")