import tkinter as tk
from tkinter import messagebox, ttk
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
            for item in tree.get_children():
                tree.delete(item)
         
            for t in turnos:
                tree.insert("", tk.END, values=(str(t.id), t.nombre, t.instructor, str(t.horario), str(t.capacidad), str(t.fecha)))

        def agregar_turno_a_treeview(turno):
            tree.insert("", tk.END, values=(str(turno.id), turno.nombre, turno.instructor, str(turno.horario), str(turno.capacidad), str(turno.fecha)))
            tree.update_idletasks()

        def pantalla_alta_turno():
            limpiar_campos_alta()
            pantalla_alta_turno_window.deiconify()  # Mostrar ventana de alta de turno

        def limpiar_campos_alta():
            entry_nombre.delete(0, tk.END)
            entry_instructor.delete(0, tk.END)
            entry_horario.delete(0, tk.END)
            entry_capacidad.delete(0, tk.END)
            entry_fecha.delete(0, tk.END)
            entry_nombre.focus_set()

        def alta_turno():
            nombre = entry_nombre.get()
            instructor = entry_instructor.get()
            horario = entry_horario.get()
            fecha = entry_fecha.get()
            
            try:
                capacidad = int(entry_capacidad.get())
                if capacidad < 0:
                    raise ValueError("La capacidad no puede ser negativa.")  # Lanzar un error si es negativa
            except ValueError as ve:
                messagebox.showerror("Error", f"Por favor ingrese una capacidad válida. {ve}")
                return
            capacidad = capacidad
            if not nombre or not instructor or not horario or not capacidad:
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            nuevo_turno = Turno.alta(nombre, instructor, horario, capacidad, fecha)
            agregar_turno_a_treeview(nuevo_turno)
            nuevo_turno.guardar_datos()
            messagebox.showinfo("Turnos", "Turno dado de alta")
            pantalla_alta_turno_window.withdraw()  

        def baja_turno():
            turno_seleccionado = tree.selection()
            if turno_seleccionado:
                turno_id = tree.item(turno_seleccionado)['values'][0] 
                turno_a_eliminar = obtener_turno_por_id(int(turno_id))
        
                if turno_a_eliminar:
                    turnos.remove(turno_a_eliminar)  
                    Turno.baja(turno_a_eliminar.id)  
                    actualizar_lista_turnos()  
                    messagebox.showinfo("Éxito", "Turno eliminado correctamente.")
                else:
                    messagebox.showerror("Error", "No se encontró el turno.")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un turno de la lista.")

        def obtener_turno_por_id(turno_id):
            for t in turnos:
                if t.id == turno_id:
                    return t
            return None

        def guardar_cambios(turno, entry_nombre, entry_instructor, entry_horario, entry_capacidad, entry_fecha):
            # Obtener los nuevos valores de los campos
            turno.nombre = entry_nombre.get()
            turno.instructor = entry_instructor.get()
            turno.horario = entry_horario.get()
            turno.fecha = entry_fecha.get()
            
            try:
                capacidad = int(entry_capacidad.get())
                if capacidad < 0:
                    raise ValueError("La capacidad no puede ser negativa.") 
            except ValueError as ve:
                messagebox.showerror("Error", f"Por favor ingrese una capacidad válida. {ve}")
                return

            # Asignar la capacidad si es válida
            turno.capacidad = capacidad

            if not turno.nombre or not turno.instructor or not turno.horario or not turno.capacidad or not turno.fecha:
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            Turno.guardar_datos()
            actualizar_lista_turnos()
            messagebox.showinfo("Turnos", "Turno actualizado correctamente")
            pantalla_edicion_turno_window.withdraw()  # Ocultar ventana de edición
 
            
        def mostrar_ventana_edicion():
            """Muestra la ventana para editar un turno."""
            global pantalla_edicion_turno_window
            pantalla_edicion_turno_window = tk.Toplevel(pantalla_admin)
            pantalla_edicion_turno_window.title("Editar Turno")
    
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Seleccione un turno para editar")
                return

            item_id = tree.item(selected_item[0], 'values')[0]  # Obtener el ID del turno
            turno = obtener_turno_por_id(int(item_id))  # Obtener el objeto Turno
    
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

            tk.Label(pantalla_edicion_turno_window, text="Fecha").grid(row=4, column=0)
            entry_fecha = tk.Entry(pantalla_edicion_turno_window )
            entry_fecha.grid(row=4, column=1)
            entry_fecha.insert(0,turno.fecha )
            
            tk.Button(pantalla_edicion_turno_window, text="Guardar", command=lambda: guardar_cambios(turno, entry_nombre, entry_instructor, entry_horario, entry_capacidad, entry_fecha)).grid(row=5, column=0, columnspan=2)
            
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
        
        # Etiqueta y entrada para la fecha
        tk.Label(frame_detalles, text="Fecha (DD/MM/AAAA): ").grid(row=4, column=0, sticky="w")
    
        # Crear la entrada de fecha con el texto marcador de posición
        entry_fecha = tk.Entry(frame_detalles, fg='grey')
        entry_fecha.grid(row=4, column=1)
    
        # Insertar el marcador de posición "DD/MM/AAAA" cuando se abre la ventana
        entry_fecha.insert(0, "DD/MM/AAAA")
    
        # Función que se ejecuta cuando el campo obtiene el foco
        def on_focus_in(event):
            if entry_fecha.get() == "DD/MM/AAAA":
                entry_fecha.delete(0, tk.END)  # Eliminar el marcador de posición
                entry_fecha.config(fg='black')  # Cambiar el color a negro
    
        # Función que se ejecuta cuando el campo pierde el foco
        def on_focus_out(event):
            if entry_fecha.get() == "":  
                entry_fecha.insert(0, "DD/MM/AAAA")  
                entry_fecha.config(fg='grey') 
    
        # Asociar los eventos a las funciones correspondientes
        entry_fecha.bind("<FocusIn>", on_focus_in)
        entry_fecha.bind("<FocusOut>", on_focus_out)
    
        #frame para contener los botones en la parte derecha
        frame_botones = tk.Frame(pantalla_admin)
        frame_botones.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        boton_alta = tk.Button(frame_botones, text="Cargar turno", command=pantalla_alta_turno)
        boton_alta.pack(pady=5, fill=tk.X)  

        boton_baja = tk.Button(frame_botones, text="Eliminar", command=baja_turno)
        boton_baja.pack(pady=5, fill=tk.X)  

        boton_modificacion = tk.Button(frame_botones, text="Editar", command = mostrar_ventana_edicion)
        boton_modificacion.pack(pady=5, fill=tk.X) 
        
        columns = ("ID", "Nombre", "Instructor", "Horario", "Capacidad", "Fecha")
        tree = ttk.Treeview(pantalla_admin, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
       
        actualizar_lista_turnos()

    elif usuario.funcion == 'socio':
        
        def cancelar_reserva():
            turno_seleccionado = tree_reservas.selection() 
            if turno_seleccionado:
                item = tree_reservas.item(turno_seleccionado)
                turno_id = int(item['values'][4]) # Obtener el ID del turno
                usuario_dni = usuario_logueado.dni
                
                Reservas.eliminar_reserva(usuario_dni, turno_id)
                actualizar_capacidad_turno_cancelado(turno_id)
                mis_reservas() 
                actualizar_lista_turnos_socio()

                messagebox.showinfo("Éxito", "Reserva cancelada con éxito.")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un turno en mis reservas.")

        # Función para reservar un turno
        def reservar_turno():
            turno_seleccionado = tree.selection()
            if turno_seleccionado:
                # Obtener el índice del turno seleccionado
                item = tree.item(turno_seleccionado)
                turno_id = int(item['values'][4])
                usuario_dni = usuario_logueado.dni
                # Buscar el turno por ID
                turno_objeto = next((t for t in turnos if t.id == turno_id), None)
               
                if turno_objeto and turno_objeto.capacidad > 0:
                    actualizar_capacidad_turno(turno_id)
                    nueva_reserva = Reservas(usuario_dni, turno_id)
                    Reservas.guardar_reserva(nueva_reserva)
        
                    actualizar_lista_turnos_socio()
                    mis_reservas()
                    messagebox.showinfo("Reserva", f"Has reservado el turno {turno_objeto.nombre}.")
                else:
                    messagebox.showwarning("Sin cupo", "Este turno ya está lleno o no tiene capacidad disponible.")
            else:
                messagebox.showwarning("Advertencia", "Debe seleccionar un turno.")
            
        def actualizar_capacidad_turno(turno_id):
            turno_encontrado = False  # Para verificar si el turno fue encontrado
            for turno in turnos:
                if turno.id == turno_id:
                    turno.capacidad -= 1
                    turno_encontrado = True  # Marcamos que encontramos y modificamos el turno
  
                    if turno.capacidad < 0:
                        turno.capacidad = 0
                    break  
            if turno_encontrado:
                Turno.guardar_datos() 
                       
        def actualizar_capacidad_turno_cancelado(turno_id):
            for turno in turnos:
                if turno.id == turno_id:
                    turno.capacidad += 1
                    # Guardar los datos actualizados en el archivo
                    Turno.guardar_datos()  
                    break 
        
        # Función para actualizar la lista de turnos
        def actualizar_lista_turnos_socio():
            # Limpiar la lista actual
            for item in tree.get_children():
                tree.delete(item)

            # Cargar los turnos reservados por el usuario
            turnos_reservados = Reservas.obtener_turnos_reservados(usuario_logueado.dni)

            # Mostrar solo los turnos que no han sido reservados por este usuario y que tengan capacidad
            for turno in turnos:
                if turno.capacidad >= 1 and turno.id not in turnos_reservados:
                    tree.insert("", tk.END, values=(turno.nombre, turno.instructor, turno.horario, turno.fecha, turno.id))

        def mis_reservas(): 
            # Limpiar la lista actual
            for item in tree_reservas.get_children():
                tree_reservas.delete(item)

            # Cargar los turnos reservados por el usuario
            turnos_reservados = Reservas.obtener_turnos_reservados(usuario_logueado.dni)

            
            for turno in turnos:
                if  turno.id in turnos_reservados:
                    tree_reservas.insert("", tk.END, values=(turno.nombre,turno.instructor, turno.horario, turno.fecha,turno.id))

        # Frame para la pantalla de socio
        pantalla_socio = tk.Frame(ventana_principal)
        pantalla_socio.pack(pady=10)

        # Frame para los botones
        frame_botones = tk.Frame(pantalla_socio)
        frame_botones.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Botón para reservar
        btn_reservar = tk.Button(frame_botones, text="Reservar", command=reservar_turno)
        btn_reservar.pack(pady=5, fill=tk.X)

        # Botón para ver detalles
        bton_cancelarR = tk.Button(frame_botones, text="Cancelar reserva", command=cancelar_reserva)
        bton_cancelarR.pack(pady=10, fill=tk.X)

        # Frame para el título y la lista de turnos disponibles
        frame_turnos = tk.Frame(pantalla_socio)
        frame_turnos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Etiqueta de título "Turnos disponibles"
        lbl_turnos = tk.Label(frame_turnos, text="Turnos disponibles", font=("Arial", 14))
        lbl_turnos.pack(pady=5)
        
        # Crear el Treeview con solo la columna "Nombre" para turnos disponibles
        tree = ttk.Treeview(frame_turnos, columns=('Nombre', 'Instructor','Horario','Fecha'), show='headings')
        tree.heading('Nombre', text='Actividad')
        tree.heading('Instructor', text= 'Profesor')
        tree.heading("Horario", text = 'Horario')
        tree.heading("Fecha", text = "Fecha")
        tree.column('Nombre', width=150, anchor=tk.W)
        tree.column('Instructor', width= 150, anchor=tk.W)
        tree.column("Horario", width = 100, anchor=tk.W)
        tree.column('Fecha', width=100,anchor= tk.W )
        tree.pack(fill=tk.BOTH, expand=True)

        # Frame para el título y la nueva lista
        frame_reservas = tk.Frame(pantalla_socio)
        frame_reservas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Etiqueta de título "Mis reservas"
        lbl_reservas = tk.Label(frame_reservas, text="Mis reservas", font=("Arial", 14))
        lbl_reservas.pack(pady=5)

        # Crear un segundo Treeview para "Mis reservas"
        tree_reservas = ttk.Treeview(frame_reservas, columns=('Nombre','Instructor','Horario', 'Fecha'), show='headings')
        tree_reservas.heading('Nombre', text='Actividad')
        tree_reservas.heading('Instructor', text='Profesor')
        tree_reservas.heading('Horario', text= ' Horario')
        tree_reservas.heading("Fecha", text = 'Fecha')
        tree_reservas.column('Nombre', width=150, anchor=tk.W)
        tree_reservas.column('Instructor', width= 150, anchor= tk.W)
        tree_reservas.column('Horario', width= 100, anchor=tk.W)
        tree_reservas.column('Fecha', width=100, anchor= tk.W)
        tree_reservas.pack(fill=tk.BOTH, expand=True)

        actualizar_lista_turnos_socio()
        mis_reservas()

