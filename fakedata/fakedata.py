from database.connection import EduDBConnection
from database.models import Persona, Apoderado, Alumno, Profesor, Curso, Clase, Asignatura, Asistencia


def generate_curso():
    edudb_conn = EduDBConnection()

    asignaturas: list[list] = [[], []]

    for i in range(1, 4):
        asig = Asignatura()
        edudb_conn.insert_asignatura(asig)

        pr = Profesor()
        edudb_conn.insert_profesor(pr, asig.codAsig)
        asignaturas[0].append(asig)
        asignaturas[1].append(pr)

    for nivel in range(1, 5):
        for paralelo in range(65, 67):
            curso = Curso(nivel, chr(paralelo))
            edudb_conn.insert_curso(curso)
            for alumno in range(5):
                al = Alumno()
                edudb_conn.insert_alumno(al, nivel, chr(paralelo))
                curso.alumnos.append(al)
            for i in range(len(asignaturas[0])):
                for clase in range(1, 3):
                    cl = Clase(2021, 10, clase, asignaturas[0][i].codAsig, nivel, chr(paralelo))
                    edudb_conn.insert_clase(cl, asignaturas[1][i].rut)
                    for alumno in curso.alumnos:
                        asis = Asistencia(cl.cod_clase, alumno.rut)
                        edudb_conn.insert_asistencia(asis)
