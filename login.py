import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from clases import Persona, usuarios
from pantalla_principal import pantalla_principal
from datetime import datetime

codigo_admi= "12A34"
# Función para manejar el login
def login():
    usuario_nombre = entry_usuario.get()
    contraseña = entry_clave.get()

    for usuario in usuarios:
        if usuario.usuario == usuario_nombre and usuario.contraseña == contraseña:
            pantalla_principal(usuario)
            pantalla_login.withdraw()  # Ocultar ventana de pantalla
            return
    messagebox.showerror("Error", "Usuario o contraseña incorrectos")

# Función para registrar el usuario
def registrar_usuario():
    # Obtener todos los valores de los campos
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    edad = entry_edad.get()
    dni = entry_dni.get()
    telefono = entry_telefono.get()
    usuario_nombre = entry_usuario_reg.get()
    contraseña = entry_clave_reg.get()
    funcion = funcion_var.get()  # Obtener la función seleccionada
    # Validación del código si se selecciona "administrador"
    if funcion == "administrador":
        codigo_ingresado = entry_codigo.get()
        if codigo_ingresado != codigo_admi:
            messagebox.showerror("Error", "Código de administrador incorrecto.")
            return

    # Verificar que todos los campos obligatorios estén llenos
    if not nombre or not apellido or not edad or not dni or not telefono or not usuario_nombre or not contraseña or funcion == 'opciones':
        messagebox.showerror("Error", "Por favor complete todos los campos")
        return

    # Crear un nuevo objeto Persona y agregarlo a la base de datos
    nuevo_usuario = Persona(nombre, apellido, int(edad), dni, telefono, usuario_nombre, contraseña, funcion)
    Persona.agregar_usuario(nuevo_usuario)
    Persona.guardar_datos()

    # Mostrar mensaje de registro exitoso y cerrar ventana de registro
    messagebox.showinfo("Registro", "Registro exitoso")
    ventana_registro.withdraw()

# Función para abrir la ventana de registro y limpiar los campos
def abrir_ventana_registro():
    limpiar_campos_registro()
    ventana_registro.deiconify()

def limpiar_campos_registro():
    # Limpiar todos los campos de entrada
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    entry_dni.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_usuario_reg.delete(0, tk.END)
    entry_clave_reg.delete(0, tk.END)
    entry_codigo.delete(0, tk.END)

    # Establecer el foco en el primer campo de entrada
    entry_nombre.focus_set()


# Función para actualizar la hora y fecha en la etiqueta
def actualizar_fecha_hora():
    # Obtener la fecha y hora actual de la computadora
    fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Actualizar el texto de la etiqueta
    etiqueta_fecha_hora.config(text=fecha_hora_actual)
    
    # Llamar a la función cada 1000 ms (1 segundo) para actualizar la hora
    pantalla_login.after(1000, actualizar_fecha_hora)

    
# Ventana login de la aplicación
pantalla_login = tk.Tk()
pantalla_login.title('Ingreso')
pantalla_login.geometry('325x495')
# Cargar la imagen de fondo
fondo_imagen = Image.open('img-login.jpg')  
fondo_imagen = fondo_imagen.resize((325, 495),  Image.Resampling.LANCZOS)  
fondo = ImageTk.PhotoImage(fondo_imagen)

# Crear un label para mostrar la imagen de fondo
label_fondo = tk.Label(pantalla_login, image=fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Colocar la imagen en toda la ventana  

  

# Etiquetas y campos de entrada para login
label_usuario = tk.Label(pantalla_login, text="Usuario:", bg='#d9d9d9')
label_usuario.pack(pady=(50,5))
entry_usuario = tk.Entry(pantalla_login)
entry_usuario.pack(pady=5)

label_clave = tk.Label(pantalla_login, text="Clave:", bg='#d9d9d9')
label_clave.pack(pady=(15,5))
entry_clave = tk.Entry(pantalla_login, show="*")
entry_clave.pack(pady=5)

# Botón de login
boton_login = tk.Button(pantalla_login, text="Ingresar", command=login)
boton_login.pack(pady=20)

# Botón para abrir ventana de registro
boton_registro = tk.Button(pantalla_login, text="Registrarse", command=abrir_ventana_registro)
boton_registro.pack(pady=(60,20))

# Ventana de registro (inicialmente oculta)
ventana_registro = tk.Toplevel(pantalla_login)
ventana_registro.title('Registro')
ventana_registro.geometry('225x450')
ventana_registro.withdraw()

# Etiquetas y campos de entrada para registro
label_nombre = tk.Label(ventana_registro, text="Nombre")
label_nombre.pack()
entry_nombre = tk.Entry(ventana_registro)
entry_nombre.pack()

label_apellido = tk.Label(ventana_registro, text="Apellido")
label_apellido.pack()
entry_apellido = tk.Entry(ventana_registro)
entry_apellido.pack()

label_edad = tk.Label(ventana_registro, text="Edad")
label_edad.pack()
entry_edad = tk.Entry(ventana_registro)
entry_edad.pack()

label_dni = tk.Label(ventana_registro, text="DNI")
label_dni.pack()
entry_dni = tk.Entry(ventana_registro)
entry_dni.pack()

label_telefono = tk.Label(ventana_registro, text="Teléfono")
label_telefono.pack()
entry_telefono = tk.Entry(ventana_registro)
entry_telefono.pack()

label_usuario_reg = tk.Label(ventana_registro, text="Usuario")
label_usuario_reg.pack()
entry_usuario_reg = tk.Entry(ventana_registro)
entry_usuario_reg.pack()

label_clave_reg = tk.Label(ventana_registro, text="Clave")
label_clave_reg.pack()
entry_clave_reg = tk.Entry(ventana_registro, show="*")
entry_clave_reg.pack()

# Etiqueta y menú desplegable para elegir la función
label_funcion = tk.Label(ventana_registro, text="Elige función:")
label_funcion.pack()

opciones_funcion = ["administrador", "socio"]
funcion_var = tk.StringVar(ventana_registro)
funcion_var.set(opciones_funcion[0])
menu_funcion = tk.OptionMenu(ventana_registro, funcion_var, *opciones_funcion)
menu_funcion.pack()
# Etiqueta y campo para el código del administrador
tk.Label(ventana_registro, text="Código (solo para administrador):").pack()
entry_codigo = tk.Entry(ventana_registro, show="*")
entry_codigo.pack()


# Botón de registro
boton_registrar = tk.Button(ventana_registro, text="Registrar", command=registrar_usuario)
boton_registrar.pack()

# Crear una etiqueta para mostrar la fecha y hora
etiqueta_fecha_hora = tk.Label(pantalla_login, font=('Arial', 14), bg="lightblue", fg="black")

# Posicionar la etiqueta en la parte inferior derecha de la ventana
etiqueta_fecha_hora.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)  # -10 px de margen

# Llamar a la función por primera vez para iniciar la actualización
actualizar_fecha_hora()
# Iniciar la aplicación Tkinter
pantalla_login.mainloop()
