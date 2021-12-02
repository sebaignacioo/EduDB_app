from faker import Faker
from random import randrange

from mysql.connector import Date

fake: Faker = Faker('es')


def create_rut():
    rut_num = randrange(10000000, 25000000)
    dv = randrange(0, 10)
    if dv == 10:
        dv_c = 'K'
    else:
        dv_c = str(dv)
    return f'{rut_num}-{dv_c}'


class Email:
    emails: list[str]

    def __init__(self):
        self.emails = []
        cant_email = randrange(1, 3)
        for i in range(cant_email):
            self.emails.append(fake.email())


class Telefono:
    telefonos: list[int]

    def __init__(self):
        self.telefonos = []
        cant_tel = randrange(1, 3)
        for i in range(cant_tel):
            self.telefonos.append(randrange(950000000, 999999999))


class Persona:
    rut: str
    primer_nombre: str
    segundo_nombre: str = None
    apellido_paterno: str
    apellido_materno: str = None
    telefonos: Telefono
    emails: Email

    def __init__(self, apellido=''):
        male = fake.boolean(50)
        self.emails = Email()
        self.telefonos = Telefono()
        tiene_segundo_nombre = fake.boolean(90)
        tiene_apellido_materno = fake.boolean(95)
        self.rut = create_rut()
        if male:
            self.primer_nombre = fake.first_name_male()
            if tiene_segundo_nombre:
                self.segundo_nombre = fake.first_name_male()
        else:
            self.primer_nombre = fake.first_name_female()
            if tiene_segundo_nombre:
                self.segundo_nombre = fake.first_name_female()
        if apellido == '':
            self.apellido_paterno = fake.last_name()
        else:
            self.apellido_paterno = apellido
        if tiene_apellido_materno:
            self.apellido_materno = fake.last_name()


class Apoderado(Persona):
    def __init__(self):
        Persona.__init__(self)


class Alumno(Persona):
    apoderado: Apoderado

    def __init__(self):
        self.apoderado = Apoderado()
        Persona.__init__(self, self.apoderado.apellido_paterno)


class Profesor(Persona):
    def __init__(self):
        Persona.__init__(self)


class Curso:
    nivel: int
    paralelo: chr

    alumnos: list[Alumno] = []

    def __init__(self, nivel: int, paralelo: chr):
        self.nivel = nivel
        self.paralelo = paralelo


class Asignatura:
    nombre: str
    codAsig: int

    def __init__(self):
        self.nombre = fake.job()


class Clase:
    cod_clase: int
    fecha: Date
    cod_asig: int
    nivel: int
    paralelo: chr

    def __init__(self,
                 anno: int,
                 mes: int,
                 dia: int,
                 cod_asig: int,
                 nivel: int,
                 paralelo: chr):
        self.fecha = Date(anno, mes, dia)
        self.cod_asig = cod_asig
        self.nivel = nivel
        self.paralelo = paralelo


class Asistencia:
    cod_clase: int
    rut_alumno: str
    valor_asist: float
    justificado: bool
    hizo_retiro: bool

    def __init__(self,
                 cod_clase: int,
                 rut_alumno: str):
        self.cod_clase = cod_clase
        self.rut_alumno = rut_alumno
        asiste = fake.boolean(75)
        if asiste:
            self.justificado = False
            self.hizo_retiro = fake.boolean(10)
            if self.hizo_retiro:
                self.valor_asist = randrange(0, 100, 1) / 100.0
            else:
                self.valor_asist = 1.0
        else:
            self.justificado = fake.boolean(50)
            self.hizo_retiro = False
            self.valor_asist = 0.0
