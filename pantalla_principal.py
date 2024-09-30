import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from clases import Turno, turnos, Reservas


def pantalla_principal(usuario):
    global tree  # Asegúrate de que tree sea accesible

    # Crear la ventana principal
    ventana_principal = tk.Toplevel()
    ventana_principal.title('Pantalla Principal')
    
   
    usuario_logueado= usuario
        
    if usuario.funcion == 'administrador':

        # Frame para los botones de administrador
        pantalla_admin = tk.Frame(ventana_principal)
        pantalla_admin.pack(pady=10)


        def actualizar_lista_turnos():
            """Función para actualizar la lista de turnos en el Treeview."""
            # Limpiar la lista actual
            for item in tree.get_children():
                tree.delete(item)

            # Insertar los turnos actuales
            for t in turnos:
                tree.insert("", tk.END, values=(str(t.id), t.nombre, t.instructor, str(t.horario), str(t.capacidad)))

        def agregar_turno_a_treeview(turno):
            tree.insert("", tk.END, values=(str(turno.id), turno.nombre, turno.instructor, str(turno.horario), str(turno.capacidad)))
            tree.update_idletasks()

    
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
            nuevo_turno = Turno.alta(nombre, instructor, horario, capacidad)
            agregar_turno_a_treeview(nuevo_turno)
            nuevo_turno.guardar_datos()
            messagebox.showinfo("Turnos", "Turno dado de alta")
            pantalla_alta_turno_window.withdraw()  # Ocultar ventana de alta

        def baja_turno():
            turno_seleccionado = tree.selection()
            if turno_seleccionado:
                turno_id = tree.item(turno_seleccionado)['values'][0]  # Obtener el ID del turno seleccionado
                turno_a_eliminar = obtener_turno_por_id(int(turno_id))
        
                if turno_a_eliminar:
                    turnos.remove(turno_a_eliminar)  # Eliminar el turno de la lista
                    Turno.baja(turno_a_eliminar.id)  # Eliminar del archivo usando el ID
                    actualizar_lista_turnos()  # Actualizar la interfaz
                    messagebox.showinfo("Éxito", "Turno eliminado correctamente.")
                else:
                    messagebox.showerror("Error", "No se encontró el turno.")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un turno de la lista.")


        # Función para abrir la ventana de edición de un turno
        def modificar_turno():

            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Seleccione un turno para editar")
                return

            item_id = tree.item(selected_item[0], 'values')[0]  # Obtener el ID del turno
            turno = obtener_turno_por_id(int(item_id))  # Obtener el objeto Turno

            if turno:
                mostrar_ventana_edicion(turno)

        def obtener_turno_por_id(turno_id):
            """Buscar un turno en la lista por su ID."""
            for t in turnos:
                if t.id == turno_id:
                    return t
            return None

        def guardar_cambios(turno, entry_nombre, entry_instructor, entry_horario, entry_capacidad):
            """Guardar los cambios realizados en un turno."""
            nombre = entry_nombre.get()
            instructor = entry_instructor.get()
            horario = entry_horario.get()
            capacidad = entry_capacidad.get()

            # Validación de campos vacíos
            if not nombre or not instructor or not horario or not capacidad:
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            # Actualizar los datos del turno
            turno.nombre = nombre
            turno.instructor = instructor
            turno.horario = horario
            turno.capacidad = capacidad

            # Actualizar en el Treeview
            actualizar_lista_turnos()

            messagebox.showinfo("Turnos", "Turno actualizado correctamente")
            pantalla_edicion_turno_window.withdraw()  # Ocultar ventana de edición

        def mostrar_ventana_edicion(turno):
            """Muestra la ventana para editar un turno."""
            global pantalla_edicion_turno_window
            pantalla_edicion_turno_window = tk.Toplevel(pantalla_admin)
            pantalla_edicion_turno_window.title("Editar Turno")

            # Crear campos y etiquetas
            tk.Label(pantalla_edicion_turno_window, text="Nombre").grid(row=0, column=0)
            entry_nombre = tk.Entry(pantalla_edicion_turno_window)
            entry_nombre.insert(0, turno.nombre)
            entry_nombre.grid(row=0, column=1)

            tk.Label(pantalla_edicion_turno_window, text="Instructor").grid(row=1, column=0)
            entry_instructor = tk.Entry(pantalla_edicion_turno_window)
            entry_instructor.insert(0, turno.instructor)
            entry_instructor.grid(row=1, column=1)

            tk.Label(pantalla_edicion_turno_window, text="Horario").grid(row=2, column=0)
            entry_horario = tk.Entry(pantalla_edicion_turno_window)
            entry_horario.insert(0, turno.horario)
            entry_horario.grid(row=2, column=1)

            tk.Label(pantalla_edicion_turno_window, text="Capacidad").grid(row=3, column=0)
            entry_capacidad = tk.Entry(pantalla_edicion_turno_window)
            entry_capacidad.insert(0, turno.capacidad)
            entry_capacidad.grid(row=3, column=1)

            tk.Button(pantalla_edicion_turno_window, text="Guardar", command=lambda: guardar_cambios(turno, entry_nombre, entry_instructor, entry_horario, entry_capacidad)).grid(row=4, column=0, columnspan=2)

        # Ventana de alta de turno (inicialmente oculta)
        pantalla_alta_turno_window = tk.Toplevel(pantalla_admin)
        pantalla_alta_turno_window.title('Alta de Turno')
        pantalla_alta_turno_window.geometry('225x450')
        pantalla_alta_turno_window.withdraw()

        # Botón de alta en la ventana de alta
        boton_alta_turno = tk.Button(pantalla_alta_turno_window, text="Dar de alta", command=alta_turno)
        boton_alta_turno.pack()

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
        
        # Crear un frame para contener los botones en la parte derecha
        frame_botones = tk.Frame(pantalla_admin)
        frame_botones.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Botones para alta, baja y modificación de turnos
        boton_alta = tk.Button(frame_botones, text="Cargar turno", command=pantalla_alta_turno)
        boton_alta.pack(pady=5, fill=tk.X)  

        boton_baja = tk.Button(frame_botones, text="Eliminar", command=baja_turno)
        boton_baja.pack(pady=5, fill=tk.X)  

        boton_modificacion = tk.Button(frame_botones, text="Editar", command=modificar_turno)
        boton_modificacion.pack(pady=5, fill=tk.X) 
        
        # Inicializar la lista de turnos en el Treeview
        columns = ("ID", "Nombre", "Instructor", "Horario", "Capacidad")
        tree = ttk.Treeview(pantalla_admin, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
       
        # Inicializar la lista de turnos
        Turno.cargar_datos()
        actualizar_lista_turnos()

    elif usuario.funcion == 'socio':
        
        def mostrar_detalles():
            turno_seleccionado = tree.selection()
            if turno_seleccionado:
                # Obtener el índice del turno seleccionado
                item = tree.item(turno_seleccionado)
                turno_nombre = item['values'][1]  # Obtener el nombre del turno

                # Buscar el turno en la lista de turnos
                turno = next((t for t in turnos if t.nombre == turno_nombre), None)

                if turno:
                    # Mostrar detalles del turno encontrado
                    messagebox.showinfo("Detalles del Turno", f"Nombre: {turno.nombre}\nInstructor: {turno.instructor}\nHorario: {turno.horario}\nCapacidad disponible: {turno.capacidad}")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un turno.")

        # Función para reservar un turno
        def reservar_turno():
            turno_seleccionado = tree.selection()

            if turno_seleccionado:
                # Obtener el índice del turno seleccionado
                item = tree.item(turno_seleccionado)
                turno_id = item['values'][0]
                usuario_dni = usuario_logueado.dni
                # Buscar el turno por ID
                turno = next((t for t in turnos if t.id == turno_id), None)

                if turno and turno.capacidad > 0:
                    # Verificar si el usuario ya reservó este turno
                    if not Reservas.verificar_reserva(usuario_dni, turno_id):
                        # Crear una nueva reserva
                        nueva_reserva = Reservas(usuario_dni, turno_id)
                        Reservas.guardar_reserva(nueva_reserva)

                        # Mensaje de confirmación
                        messagebox.showinfo("Reserva", f"Has reservado el turno {turno.nombre}.")

                        # Actualizar la capacidad del turno
                        actualizar_capacidad_turno(turno_id)

                        # Actualizar la lista de turnos
                        actualizar_lista_turnos_socio()
                    else:
                        messagebox.showwarning("Advertencia", "Ya has reservado este turno.")
                else:
                    messagebox.showwarning("Sin cupo", "Este turno ya está lleno o no tiene capacidad disponible.")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un turno.")

        # Función para actualizar la lista de turnos
        def actualizar_lista_turnos_socio():
            # Limpiar la lista actual
            for item in tree.get_children():
                tree.delete(item)

            # Cargar los turnos reservados por el usuario
            turnos_reservados = Reservas.obtener_turnos_reservados(usuario_logueado.dni)

            # Mostrar solo los turnos que no han sido reservados por este usuario y que tengan capacidad
            for turno in turnos:
                if turno.capacidad > 0 and turno.id not in turnos_reservados:
                    tree.insert("", tk.END, values=(turno.id, turno.nombre))

        # Función para actualizar la capacidad del turno
        def actualizar_capacidad_turno(turno_id):
            for turno in turnos:
                if turno.id == turno_id:
                    turno.capacidad -= 1  # Reducir la capacidad en 1

                    if turno.capacidad < 0:
                        turno.capacidad = 0  # Asegurarse de que la capacidad no sea menor a 0

                    # Guardar los datos actualizados
                    Turno.guardar_datos()
                    break


        # Frame para la pantalla de socio
        pantalla_socio = tk.Frame(ventana_principal)
        pantalla_socio.pack(pady=10)

        # Frame para los botones
        frame_botones = tk.Frame(pantalla_socio)
        frame_botones.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Botón para ver detalles
        btn_detalles = tk.Button(frame_botones, text="Detalles", command=mostrar_detalles)
        btn_detalles.pack(pady=5, fill=tk.X)
        
        # Botón para reservar
        btn_reservar = tk.Button(frame_botones, text="Reservar", command= lambda: reservar_turno())
        btn_reservar.pack(pady=10, fill=tk.X)

        # Crear el Treeview con solo la columna "Nombre"
        tree = ttk.Treeview(pantalla_socio, columns=('ID', 'Nombre'), show='headings')
        tree.heading('Nombre', text='Nombre del Turno')
        tree.heading('ID', text= 'ID') 
        tree.column('ID', width=50, anchor=tk.CENTER) 
        tree.column('Nombre', width=200, anchor=tk.W) 
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
       
    
        # Cargar y mostrar los turnos
        Turno.cargar_datos()
        actualizar_lista_turnos_socio()


