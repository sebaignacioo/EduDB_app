from tabulate import tabulate

from database.connection import EduDBConnection
from database.models import Alumno
from fakedata import fakedata

generar_datos = False
datos_locales = False
conexion = EduDBConnection(local=datos_locales)

print('Aplicación de ejemplo')
print('EduDB\n')
if generar_datos:
    print('Generando datos de prueba...')
    fakedata.generate_curso()
    print('Datos generados y almacenados en la base de datos\n')


# Obtener alumnos de un curso determinado
print('Ejemplo: Obtener los alumnos de un curso determinado')
print('Curso seleccionado: 2 \'B\'')
print("""\nInstrucción SQL:
SELECT Alumno.rut, Alumno.nivel, Alumno.paralelo,
       Persona.primerNombre, Persona.segundoNombre,
       Persona.apellidoPat, Persona.apellidoMat,
       Alumno.rutApoderado
FROM (Alumno JOIN Persona ON Alumno.rut = Persona.rut)
WHERE Alumno.nivel = 2 AND Alumno.paralelo = 'B'\n""")
headers_alumnos = ['RUT Alumno', 'Nivel', 'Par.', 'Primer nombre',
                   'Segundo nombre', 'Ap. Pat.', 'Ap. Mat.', 'RUT Apoderado']
alumnos = conexion.obtener_alumnos_curso(2, 'B')
print(tabulate(alumnos, headers=headers_alumnos))
print()

# Obtener todos los apoderados del colegio
print('Ejemplo: Obtener los apoderados del colegio')
print("""\nInstrucción SQL:
SELECT Apoderado.rut, Persona.primerNombre, Persona.segundoNombre,
       Persona.apellidoPat, Persona.apellidoMat
FROM (Apoderado JOIN Persona ON Apoderado.rut = Persona.rut)\n""")

headers_apoderados = ['RUT Apoderado', 'Primer nombre',
                   'Segundo nombre', 'Ap. Pat.', 'Ap. Mat.']
apoderados = conexion.obtener_apoderados_colegio()
print(tabulate(apoderados, headers=headers_apoderados))
print()

# Obtener la asistencia de un alumno específico
if datos_locales:
    rut = '18863163-8'
else:
    rut = '11220162-6'
print('Ejemplo: Obtener los datos de asistencia de un alumno')
print(f"""\nInstrucción SQL:
SELECT Alumno.rut, Alumno.rutApoderado, Alumno.nivel, Alumno.paralelo, 
       Persona.primerNombre, Persona.segundoNombre,
       Persona.apellidoPat, Persona.apellidoMat,
       AVG(Asistencia.valorAsist)
FROM (
       (Alumno JOIN Persona ON Alumno.rut = Persona.rut)
       JOIN Asistencia ON Alumno.rut = Asistencia.rutAlumno
)
WHERE Alumno.rut = '{rut}'\n""")

al: Alumno = conexion.obtener_alumno(rut)
print(f"""Alumno:
    -> RUT: {al[0]}
    -> Nombre completo: {al[4]} {al[5] if al[5] is not None else ''}  {al[6]} {al[7] if al[7] is not None else ''}
    -> Curso: {al[2]} '{al[3]}'
    -> RUT Apoderado: {al[1]}
    -> Promedio asistencia: {(float(al[8]) * 100.0):.2f}%""")
print()

# Obtener los alumnos que tienen inasistencias injustificadas
print('Ejemplo: Obtener los alumnos que tienen inasistencias injustificadas, y que son del nivel 3')
print("""\nInstrucción SQL:
SELECT
    Clase.fechaClase, Alumno.rut, Alumno.paralelo, Persona.primerNombre,
    Persona.segundoNombre, Persona.apellidoPat, Persona.apellidoMat
FROM (
    (Alumno JOIN Persona on Alumno.rut = Persona.rut)
     JOIN Asistencia on Alumno.rut = Asistencia.rutAlumno), Clase
WHERE Clase.codClase = Asistencia.codClase
AND Asistencia.valorAsist = 0
AND Asistencia.justificado = false
AND Alumno.nivel = 3
ORDER BY Clase.fechaClase ASC;\n""")

headers_al_inj = ['Fecha', 'RUT Alumno', 'Paralelo',
                  'Primer nombre', 'Segundo nombre',
                  'Ap. Pat.', 'Ap. Mat.']
al_inj = conexion.obtener_alumnos_injustificados(3)
print(tabulate(al_inj, headers=headers_al_inj))
print()
