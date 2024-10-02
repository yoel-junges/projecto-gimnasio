
reservas_archivo = 'reservas.txt'
usuarios_archivo = 'usuarios.txt'
turnos_archivo = 'turnos.txt'
usuarios = []  # Lista global para almacenar los usuarios
turnos = []  # Lista para guardar los turnos
reservas = []

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



class Turno:
    # Atributo de clase para mantener el último ID generado
    ultimo_id = 0

    def __init__(self, id, nombre, instructor, horario, capacidad):
        self.id = id
        self.nombre = nombre
        self.instructor = instructor
        self.horario = horario
        self.capacidad = capacidad
        self.estado = False
        

    @staticmethod
    def alta(nombre, instructor, horario, capacidad):
        Turno.ultimo_id += 1
        nuevo_turno = Turno(Turno.ultimo_id, nombre, instructor, horario, capacidad)
        turnos.append(nuevo_turno)
        return nuevo_turno

    @staticmethod
    def baja(turno_id):
        turno_id = str(turno_id)  # Convertir el turno_id a string para compararlo
        with open('turnos.txt', 'r') as file:
            lineas = file.readlines()

        with open('turnos.txt', 'w') as file:
            for linea in lineas:
                datos_turno = linea.strip().split(',')  # Asumiendo que los turnos están separados por comas
                if datos_turno[0] != turno_id:  # Comparar con el ID del turno
                    file.write(linea)

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
        try:
            # Abrimos el archivo para escritura en modo 'w' para guardar datos de los turnos
            with open(turnos_archivo, 'w') as archivo: 
                # Guardamos el último ID
                archivo.write(f"ultimo_id:{Turno.ultimo_id}\n")
                # Guardamos los datos de cada turno
                for t in turnos:
                    archivo.write(f"{t.id},{t.nombre},{t.instructor},{t.horario},{t.capacidad}\n")
        except Exception as e:
            print("Error al guardar datos:", e)  # Imprimir el error si ocurre

                

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


class Reservas:
    def __init__(self,usuario_dni, turno_id):
        self.turno_id = turno_id
        self.usuario_dni = usuario_dni

    @staticmethod
    def cargar_reservas():
        """Cargar todas las reservas desde el archivo."""
        reservas = []
        try:
            with open('reservas.txt', 'r') as f:
                for linea in f:
                    usuario_dni, turno_id = linea.strip().split(',')
                    reservas.append(Reservas(usuario_dni , int(turno_id))) 
        except FileNotFoundError:
            pass  
        return reservas

    @staticmethod
    def guardar_reserva(reserva):
        """Guardar una nueva reserva en el archivo."""
        with open(reservas_archivo , 'a') as f:
            f.write(f"{reserva.usuario_dni},{reserva.turno_id}\n")

    @staticmethod
    def verificar_reserva(usuario_dni, turno_id):
        """Verificar si el usuario ya ha reservado ese turno."""
        reservas = Reservas.cargar_reservas()  
        for reserva in reservas:
            if reserva.usuario_dni == usuario_dni and reserva.turno_id == turno_id:
                return True
        return False

    @staticmethod
    def obtener_turnos_reservados(usuario_dni):
        """Obtener los IDs de los turnos reservados por un usuario."""
        reservas = Reservas.cargar_reservas()  
        return [int(reserva.turno_id) for reserva in reservas if reserva.usuario_dni == usuario_dni]


Turno.cargar_datos()
Persona.cargar_datos()
Reservas.cargar_reservas()

