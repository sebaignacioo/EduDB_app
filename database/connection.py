from mysql.connector import connect, connection

from database.models import Alumno, Apoderado, Asignatura, Asistencia, Clase, Curso, Email, Persona, Profesor, Telefono


class EduDBConnection:
    _credentials = {
        'host': 'localhost',
        'user': 'root',
        'password': 'ZFgpZmdfpvxXP2Rr',
        'database': 'EduDB'
    }

    _con: connection

    def __init__(self):
        self._con = connect(
            host=self._credentials.get('host'),
            user=self._credentials.get('user'),
            password=self._credentials.get('password'),
            database=self._credentials.get('database')
        )

    def ex_insert(self, sql: str, val: tuple):
        cursor = self._con.cursor()
        cursor.execute(sql, val)
        self._con.commit()
        id_gen = cursor.lastrowid
        cursor.close()
        return id_gen

    def insert_persona(self, persona: Persona):
        if persona.segundo_nombre is None and persona.apellido_materno is None:
            sql = f'INSERT INTO Persona (rut, primerNombre, apellidoPat) VALUES (%s, %s, %s)'
            values = (persona.rut, persona.primer_nombre[:20], persona.apellido_paterno[:20])
        elif persona.segundo_nombre is None and persona.apellido_materno is not None:
            sql = f'INSERT INTO Persona (rut, primerNombre, apellidoPat, apellidoMat) VALUES (%s, %s, %s, %s)'
            values = (persona.rut, persona.primer_nombre[:20], persona.apellido_paterno[:20], persona.apellido_materno[:20])
        elif persona.apellido_materno is None:
            sql = f'INSERT INTO Persona (rut, primerNombre, segundoNombre, apellidoPat) VALUES (%s, %s, %s, %s)'
            values = (persona.rut, persona.primer_nombre[:20], persona.segundo_nombre[:20], persona.apellido_paterno[:20])
        else:
            sql = f'INSERT INTO Persona (rut, primerNombre, segundoNombre, apellidoPat, apellidoMat) VALUES (%s, %s, ' \
                  f'%s, %s, %s)'
            values = (persona.rut, persona.primer_nombre[:20], persona.segundo_nombre[:20], persona.apellido_paterno[:20],
                      persona.apellido_materno[:20])

        self.ex_insert(sql, values)

        self.insert_emails(persona.emails, persona.rut)
        self.insert_telefonos(persona.telefonos, persona.rut)

    def insert_profesor(self, profesor: Profesor, cod_asig: int):
        self.insert_persona(profesor)
        sql = f'INSERT INTO Profesor (rut, codAsig) VALUES (%s, %s)'
        values = (profesor.rut, cod_asig)
        self.ex_insert(sql, values)

    def insert_alumno(self, alumno: Alumno, nivel: int, paralelo: chr):
        self.insert_persona(alumno)
        self.insert_apoderado(alumno.apoderado)
        sql = f'INSERT INTO Alumno (rut, rutApoderado, nivel, paralelo) VALUES (%s, %s, %s, %s)'
        values = (f'{alumno.rut}', f'{alumno.apoderado.rut}', f'{nivel}', paralelo)
        self.ex_insert(sql, values)

    def insert_apoderado(self, apoderado: Apoderado):
        self.insert_persona(apoderado)
        sql = f'INSERT INTO Apoderado (rut) VALUES (%s)'
        values = (f'{apoderado.rut}', )
        self.ex_insert(sql, values)

    def insert_asignatura(self, asignatura: Asignatura):
        sql = f'INSERT INTO Asignatura (nombre) VALUES (%s)'
        values = (f'{asignatura.nombre[:25]}',)
        asignatura.codAsig = self.ex_insert(sql, values)

    def insert_asistencia(self, asistencia: Asistencia):
        print(asistencia.valor_asist)
        sql = f'INSERT INTO Asistencia (codClase, rutAlumno, valorAsist, justificado, hizoRetiro)' \
              f'VALUES (%s, %s, %s, %s, %s)'
        values = (f'{asistencia.cod_clase}', f'{asistencia.rut_alumno}', asistencia.valor_asist,
                  int(asistencia.justificado), int(asistencia.hizo_retiro))
        self.ex_insert(sql, values)

    def insert_clase(self, clase: Clase, rut_profesor: str):
        sql = f'INSERT INTO Clase (fechaClase, codAsig, nivel, paralelo, rutProfesor) VALUES (%s, %s, %s, %s, %s)'
        values = (clase.fecha, f'{clase.cod_asig}', clase.nivel, clase.paralelo, f'{rut_profesor}')
        clase.cod_clase = self.ex_insert(sql, values)

    def insert_curso(self, curso: Curso):
        sql = f'INSERT INTO Curso (nivel, paralelo) VALUES (%s, %s)'
        values = (curso.nivel, curso.paralelo)
        self.ex_insert(sql, values)

    def insert_emails(self, emails: Email, rut_persona: str):
        for email in emails.emails:
            sql = f'INSERT INTO Email (email, rutPersona) VALUES (%s, %s)'
            values = (email[:60], rut_persona)
            self.ex_insert(sql, values)

    def insert_telefonos(self, telefonos: Telefono, rut_persona: str):
        for tel in telefonos.telefonos:
            sql = f'INSERT INTO Telefono (numTel, rutPersona) VALUES (%s, %s)'
            values = (tel, rut_persona)
            self.ex_insert(sql, values)
