import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from clases import Turno, usuarios, turnos

def pantalla_principal(usuario):
    # Crear la ventana principal
    ventana_principal = tk.Toplevel()
    ventana_principal.title('Pantalla Principal')

    # Frame para los botones de administrador
    frame_admin = tk.Frame(ventana_principal)
    frame_admin.pack(pady=10)

    # Inicializar la lista de turnos en el Treeview
    columns = ("ID", "Nombre", "Instructor", "Horario", "Capacidad")
    tree = ttk.Treeview(ventana_principal, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True)

    def actualizar_lista_turnos():
        # Limpiar la lista actual
        for item in tree.get_children():
            tree.delete(item)

        # Insertar los turnos actuales
        for t in turnos:
            tree.insert("", tk.END, values=(str(t.id), t.nombre, t.instructor, str(t.horario), str(t.capacidad)))

    if usuario.funcion == 'administrador':
        # Función para mostrar la pantalla de alta de turno
        def pantalla_alta_turno():
            limpiar_campos_alta()
            pantalla_alta_turno_window.deiconify()  # Mostrar ventana de alta de turno

        # Función para limpiar los campos de entrada en la ventana de alta
        def limpiar_campos_alta():
            entry_nombre.delete(0, tk.END)
            entry_instructor.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
            entry_capacidad.delete(0, tk.END)
            entry_nombre.focus_set()

        # Función para realizar el alta de un turno
        def alta_turno():
            nombre = entry_nombre.get()
            instructor = entry_instructor.get()
            horario = entry_horario.get()
            capacidad = entry_capacidad.get()

            # Validación de campos vacíos
            if not nombre or not instructor or not horario or not capacidad:
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            # Alta de turno
            Turno.alta(nombre, instructor, horario, int(capacidad))
            actualizar_lista_turnos()  # Actualizar la lista de turnos
            messagebox.showinfo("Turnos", "Turno dado de alta")
            pantalla_alta_turno_window.withdraw()  # Ocultar ventana de alta

        # Función para eliminar un turno
        def baja_turno():
            # Pedir el nombre del turno a eliminar
            nombre_turno = simpledialog.askstring("Eliminar Turno", "Ingrese el nombre del turno a eliminar:")

            if nombre_turno:
                # Buscar el turno con el nombre ingresado
                turno_eliminado = False
                for t in turnos:
                    if t.nombre == nombre_turno:
                        turnos.remove(t)  # Eliminar el turno de la lista
                        turno_eliminado = True
                        break

                if turno_eliminado:
                    Turno.baja(nombre_turno)  # Eliminar del archivo
                    actualizar_lista_turnos()  # Actualizar la interfaz
                    messagebox.showinfo("Éxito", "Turno eliminado correctamente.")
                else:
                    messagebox.showerror("Error", "El turno no fue encontrado.")
            else:
                messagebox.showwarning("Advertencia", "Debe ingresar un nombre de turno.")

        # Función para modificar un turno
        def modificacion_turno():
            nombre = entry_nombre.get()
            instructor = entry_instructor.get()
            horario = entry_horario.get()
            capacidad = entry_capacidad.get()

            # Modificar turno con los nuevos datos
            Turno.modificacion(nombre, nuevo_instructor=instructor, nuevo_horario=horario, nueva_capacidad=int(capacidad) if capacidad else None)
            actualizar_lista_turnos()
            limpiar_campos_turno()

        # Función para limpiar los campos de entrada después de modificar/eliminar un turno
        def limpiar_campos_turno():
            entry_nombre.delete(0, tk.END)
            entry_instructor.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
            entry_capacidad.delete(0, tk.END)

        # Ventana de alta de turno (inicialmente oculta)
        pantalla_alta_turno_window = tk.Toplevel(ventana_principal)
        pantalla_alta_turno_window.title('Turnos')
        pantalla_alta_turno_window.geometry('225x450')
        pantalla_alta_turno_window.withdraw()

        # Botón de alta en la ventana de alta
        boton_alta_turno = tk.Button(pantalla_alta_turno_window, text="Dar de alta", command=alta_turno)
        boton_alta_turno.pack()

        # Botones para alta de turnos
        boton_alta = tk.Button(frame_admin, text="Cargar turno", command=pantalla_alta_turno)
        boton_alta.pack(side=tk.LEFT, padx=5)

        # Botones para baja y modificación de turnos
        boton_baja = tk.Button(frame_admin, text="Eliminar", command=baja_turno)
        boton_baja.pack(side=tk.LEFT, padx=5)

        boton_modificacion = tk.Button(frame_admin, text="Editar", command=modificacion_turno)
        boton_modificacion.pack(side=tk.LEFT, padx=5)

        # Campos de entrada para los detalles del turno
        frame_detalles = tk.Frame(pantalla_alta_turno_window)
        frame_detalles.pack(pady=10)

        tk.Label(frame_detalles, text="Nombre").grid(row=0, column=0)
        entry_nombre = tk.Entry(frame_detalles)
        entry_nombre.grid(row=0, column=1)

        tk.Label(frame_detalles, text="Instructor").grid(row=1, column=0)
        entry_instructor = tk.Entry(frame_detalles)
        entry_instructor.grid(row=1, column=1)

        tk.Label(frame_detalles, text="Horario").grid(row=2, column=0)
        entry_horario = tk.Entry(frame_detalles)
        entry_horario.grid(row=2, column=1)

        tk.Label(frame_detalles, text="Capacidad").grid(row=3, column=0)
        entry_capacidad = tk.Entry(frame_detalles)
        entry_capacidad.grid(row=3, column=1)

    elif usuario.funcion == 'socio':
        tk.Label(ventana_principal, text="Bienvenido socio").pack()
        # Aquí puedes agregar los elementos de la interfaz para los socios

    # Inicializar la lista de turnos en el Treeview
    Turno.cargar_datos()
    actualizar_lista_turnos()
