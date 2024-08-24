
usuarios_archivo = 'usuarios.txt'
turnos_archivo = 'turnos.txt'
usuarios = []  # Lista global para almacenar los usuarios
turnos = []  # Lista para guardar los turnos

class Persona:
    def __init__(self, nombre, apellido, edad, dni, telefono, usuario, contraseña, funcion):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.dni = dni
        self.telefono = telefono
        self.usuario = usuario
        self.contraseña = contraseña
        self.funcion = funcion

    @staticmethod
    def agregar_usuario(usuario):
        usuarios.append(usuario)

    @staticmethod
    def guardar_datos():
        with open(usuarios_archivo, 'w') as archivo:
            for usuario in usuarios:
                archivo.write(f"{usuario.nombre},{usuario.apellido},{usuario.edad},{usuario.dni},{usuario.telefono},{usuario.usuario},{usuario.contraseña},{usuario.funcion}\n")

    @staticmethod
    def cargar_datos():
        global usuarios
        try:
            with open(usuarios_archivo, 'r') as file:
                usuarios = []
                for linea in file:
                    nombre, apellido, edad, dni, telefono, usuario, contraseña, funcion = linea.strip().split(',')
                    usuarios.append(Persona(nombre, apellido, int(edad), dni, telefono, usuario, contraseña, funcion))
        except (FileNotFoundError, ValueError):
            usuarios = []

# Inicializar cargando los datos
Persona.cargar_datos()

class Turno:
    # Atributo de clase para mantener el último ID generado
    ultimo_id = 0

    def __init__(self, id, nombre, instructor, horario, capacidad):
        self.id = id
        self.nombre = nombre
        self.instructor = instructor
        self.horario = horario
        self.capacidad = capacidad

    @staticmethod
    def alta(nombre, instructor, horario, capacidad):
        Turno.ultimo_id += 1
        nuevo_turno = Turno(Turno.ultimo_id, nombre, instructor, horario, capacidad)
        turnos.append(nuevo_turno)
        return nuevo_turno

    @staticmethod
    def baja(nombre):
        global turnos
        turnos = [t for t in turnos if t.nombre != nombre]
        Turno.guardar_datos()

    @staticmethod
    def modificacion(nombre, nuevo_instructor=None, nuevo_horario=None, nueva_capacidad=None):
        for t in turnos:
            if t.nombre == nombre:
                if nuevo_instructor:
                    t.instructor = nuevo_instructor
                if nuevo_horario:
                    t.horario = nuevo_horario
                if nueva_capacidad is not None:
                    t.capacidad = nueva_capacidad
        Turno.guardar_datos()

    @staticmethod
    def guardar_datos():
        with open(turnos_archivo, 'w') as archivo:
            archivo.write(f"ultimo_id:{Turno.ultimo_id}\n")
            for t in turnos:
                archivo.write(f"{t.id},{t.nombre},{t.instructor},{t.horario},{t.capacidad}\n")

    @staticmethod
    def cargar_datos():
        global turnos
        turnos = []
        try:
            with open(turnos_archivo, 'r') as archivo:
                primera_linea = archivo.readline().strip()
                if primera_linea.startswith("ultimo_id:"):
                    Turno.ultimo_id = int(primera_linea.split(':')[1])
                else:
                    Turno.ultimo_id = 0

                for linea in archivo:
                    id, nombre, instructor, horario, capacidad = linea.strip().split(',')
                    turnos.append(Turno(int(id), nombre, instructor, horario, int(capacidad)))
        except FileNotFoundError:
            Turno.ultimo_id = 0
            print("No se encontró el archivo. Lista de turnos vacía.")
        except ValueError:
            print("Error en el formato del archivo de turnos.")

# Inicializar cargando los datos
Turno.cargar_datos()



