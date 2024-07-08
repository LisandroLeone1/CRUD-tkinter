from tkinter import *
from tkinter import messagebox
import sqlite3
from base_datos import conexionBBDD


#-------------funciones-----------------
def salirAplicacion():
    valor = messagebox.askquestion("Salir","Deseas salir de la aplicacion?")
    if valor == "yes":
        root.destroy()

def limpiarCampos():
    miNombre.set("")
    miId.set("")
    miPass.set("")
    miApellido.set("")
    miDireccion.set("")
    textoComentario.delete(1.0,END) # le decimos que debe borrar desde el primer caracter hasta el final


def crear():
    nombre = miNombre.get()
    contrasena = miPass.get()
    apellido = miApellido.get()
    direccion = miDireccion.get()
    comentario = textoComentario.get(1.0, "end").strip()  
    
    if nombre == "" or contrasena == "" or apellido == "" or direccion == "" or comentario == "":
        messagebox.showerror("Error", "Debes ingresar todos los datos")
    else:
        miConexion = sqlite3.connect("Usuarios")
        cursor = miConexion.cursor()
        datos = (nombre, contrasena, apellido, direccion, comentario)
        
        cursor.execute("INSERT INTO DATOUSUARIOS VALUES(NULL,?,?,?,?,?)", datos)
        
        miConexion.commit()
        messagebox.showinfo("BBDD", "Registro insertado correctamente")
        miConexion.close()

def leer():
    id = miId.get()
    if id == "":
        messagebox.showerror("Error", "Debes ingresar un ID")
    else:
        miConexion = sqlite3.connect("Usuarios")
        cursor = miConexion.cursor()
        cursor.execute("SELECT * FROM DATOUSUARIOS WHERE ID=" + miId.get())
        elUsuario= cursor.fetchall()

        if not elUsuario:
            messagebox.showerror("Error", "ID inexistente")
            miConexion.close()
            return
    
        else:
            for usuario in elUsuario:
                miId.set(usuario[0])
                miNombre.set(usuario[1])
                miPass.set(usuario[2])
                miApellido.set(usuario[3])
                miDireccion.set(usuario[4])
                textoComentario.insert(1.0, usuario[5])

    miConexion.commit()

def actualizar():
    id = miId.get()
    if id == "":
        messagebox.showerror("Error", "Debes ingresar un ID de un usuario existente")
        return
    
    miConexion = sqlite3.connect("Usuarios")
    cursor = miConexion.cursor()
    
    cursor.execute("SELECT * FROM DATOUSUARIOS WHERE ID=" + miId.get())
    elUsuario = cursor.fetchall()
    
    if not elUsuario:
        messagebox.showerror("Error", "ID inexistente")
        miConexion.close()
        return
    
    usuario = elUsuario[0]
    nombre_actual = usuario[1]
    contraseña_actual = usuario[2]
    apellido_actual = usuario[3]
    direccion_actual = usuario[4]
    comentario_actual = usuario[5]
    
    
    nombre = miNombre.get()
    contrasena = miPass.get()
    apellido = miApellido.get()
    direccion = miDireccion.get()
    comentario = textoComentario.get(1.0, "end").strip()
    
    if (nombre != nombre_actual or contrasena != contraseña_actual or 
        apellido != apellido_actual or direccion != direccion_actual or comentario != comentario_actual):
        
        datos = (nombre, contrasena, apellido, direccion, comentario)
        
        cursor.execute("UPDATE DATOUSUARIOS SET NOMBRE=?, CONTRASEÑA=?, APELLIDO=?, DIRECCION=?, COMENTARIOS=?" +
                       " WHERE ID=" + miId.get(), (datos))
        
        miConexion.commit()
        messagebox.showinfo("BBDD", "Registro actualizado correctamente")
    
    else:
        messagebox.showerror("Error", "Los datos a actualizar son iguales a los ya existentes")
    
    miConexion.close()
 
def eliminar():
    miConexion= sqlite3.connect("Usuarios")
    cursor= miConexion.cursor()
    cursor.execute("DELETE FROM DATOUSUARIOS WHERE ID=" + miId.get())
    miConexion.commit()
    messagebox.showinfo("BBDD", "Registro eliminado correctamente")
    miConexion.close()
    limpiarCampos()


root= Tk()

barraMenu= Menu(root)
root.config(menu=barraMenu,width=300,height=300)

bbddMenu= Menu(barraMenu,tearoff=0)
bbddMenu.add_command(label="Conectar",command=conexionBBDD)
bbddMenu.add_command(label="Salir",command=salirAplicacion)

borrarMenu= Menu(barraMenu,tearoff=0)
borrarMenu.add_command(label="Limpiar Campos",command=limpiarCampos)

crudMenu= Menu(barraMenu,tearoff=0)
crudMenu.add_command(label="Crear", command= crear)
crudMenu.add_command(label="Leer", command=leer)
crudMenu.add_command(label="Actualizar", command=actualizar)
crudMenu.add_command(label="Borrar", command=eliminar)

ayudaMenu= Menu(barraMenu,tearoff=0)
ayudaMenu.add_command(label="Acerca de...")
ayudaMenu.add_command(label="Ayuda")

barraMenu.add_cascade(label="BBDD",menu=bbddMenu)
barraMenu.add_cascade(label="Limpiar",menu=borrarMenu)
barraMenu.add_cascade(label="Crud",menu=crudMenu)
barraMenu.add_cascade(label="Ayuda",menu=ayudaMenu)

#--------------campos---------------------

miFrame= Frame(root)
miFrame.pack()


miId = StringVar()
miNombre = StringVar()
miPass = StringVar()
miApellido = StringVar()
miDireccion = StringVar()


cuadroID= Entry(miFrame, textvariable= miId)
cuadroID.grid(row=0,column=1,padx=10,pady=10)

cuadroNombre= Entry(miFrame, textvariable= miNombre)
cuadroNombre.grid(row=1,column=1,padx=10,pady=10)

cuadroPass= Entry(miFrame, textvariable= miPass)
cuadroPass.grid(row=2,column=1,padx=10,pady=10)
cuadroPass.config(show="*")

cuadroApellido= Entry(miFrame, textvariable= miApellido)
cuadroApellido.grid(row=3,column=1,padx=10,pady=10)

cuadroDireccion= Entry(miFrame, textvariable= miDireccion)
cuadroDireccion.grid(row=4,column=1,padx=10,pady=10)

textoComentario= Text(miFrame,width=16,height=5)
textoComentario.grid(row=5,column=1,padx=10,pady=10)
scrollVert = Scrollbar(miFrame, command=textoComentario.yview)
scrollVert.grid(row=5,column=2,sticky="nsew")

textoComentario.config(yscrollcommand=scrollVert.set)

#--------------label----------------------

idLabel= Label(miFrame, text="Id:")
idLabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)

nombreLabel= Label(miFrame, text="Nombre:")
nombreLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

passLabel= Label(miFrame, text="Contraseña:")
passLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)

apellidoLabel= Label(miFrame, text="Apellido:")
apellidoLabel.grid(row=3, column=0, sticky="e", padx=10, pady=10)

direccionLabel= Label(miFrame, text="Direccion:")
direccionLabel.grid(row=4, column=0, sticky="e", padx=10, pady=10)

comentariosLabel= Label(miFrame, text="Comentarios:")
comentariosLabel.grid(row=5, column=0, sticky="e", padx=10, pady=10)

#--------------------botones------------------

miFrame2= Frame(root)
miFrame2.pack()

botonCrear= Button(miFrame2, text="Crear", command= crear)
botonCrear.grid(row=1,column=0,sticky="e", padx=10, pady=10)

botonLeer= Button(miFrame2, text="Leer", command=leer)
botonLeer.grid(row=1,column=1,sticky="e", padx=10, pady=10)

botonActualizar= Button(miFrame2, text="Actualizar", command=actualizar)
botonActualizar.grid(row=1,column=2,sticky="e", padx=10, pady=10)

botonBorrar= Button(miFrame2, text="Borrar", command=eliminar)
botonBorrar.grid(row=1,column=3,sticky="e", padx=10, pady=10)



root.mainloop()