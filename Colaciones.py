import pandas as pd
from datetime import timedelta, datetime

# Leer el archivo de Excel
df = pd.read_excel('C:\\Users\\coffe\\OneDrive\\Escritorio\\Programa\\Horarios.xlsx')

# Crear columnas para el horario de inicio y término de colación
df['Horario de Inicio de Colacion'] = None
df['Horario de Termino de Colacion'] = None

# Ordenar el DataFrame por la hora de inicio del turno
df.sort_values('Hora de incio de turno', inplace=True)

# Crear una lista para llevar un registro de las personas en la cafetería
personas_en_cafeteria = []

# Crear un contador para llevar un registro del total de personas en la cafetería
total = 0

# Recorrer cada fila del DataFrame
for index, row in df.iterrows():
    # Convertir la hora de inicio del turno a un objeto datetime
    inicio_turno = datetime.combine(datetime.today(), row['Hora de incio de turno'])

    # Calcular el horario de inicio de colación
    inicio_colacion = inicio_turno + timedelta(hours=5)  # 5 horas después del inicio del turno

    # Asegurarse de que el horario de colación no sea menos de 4 horas antes del final del turno
    final_turno = inicio_turno + timedelta(hours=9)  # Suponiendo que todos los turnos duran 9 horas
    if inicio_colacion > final_turno - timedelta(hours=4):  # 4 horas antes del final del turno
        inicio_colacion = final_turno - timedelta(hours=4)

    # Calcular el horario de término de colación (40 minutos después del inicio)
    termino_colacion = inicio_colacion + timedelta(minutes=40)

    # Si el nombre de la persona contiene un asterisco, agregar 10 minutos adicionales al horario de término de la colación
    if '*' in row['Nombre']:
        termino_colacion += timedelta(minutes=10)

    # Convertir los horarios de inicio y término de colación a cadenas de texto
    inicio = inicio_colacion.time().strftime('%H:%M')
    termino = termino_colacion.time().strftime('%H:%M')

    # Verificar si el horario de colación cumple con las restricciones
    while total >= 9 or any(persona[2] == row['Area'] for persona in personas_en_cafeteria):
        # Si hay 9 o más personas en la cafetería, o si ya hay alguien de la misma área en la cafetería,
        # retrasar el horario de colación hasta que la primera persona salga de la cafetería
        if personas_en_cafeteria:
            primera_persona = min(personas_en_cafeteria, key=lambda x: x[1])
            inicio_colacion = datetime.combine(datetime.today(),
                                               datetime.strptime(primera_persona[1], '%H:%M').time()) + timedelta(
                minutes=10)
            termino_colacion = inicio_colacion + timedelta(minutes=40)
            inicio = inicio_colacion.time().strftime('%H:%M')
            termino = termino_colacion.time().strftime('%H:%M')
            # Actualizar el total de personas en la cafetería
            total -= 1
            personas_en_cafeteria.remove(primera_persona)
        else:
            break

    # Asignar los horarios de inicio y término de colación a la fila correspondiente
    df.at[index, 'Horario de Inicio de Colacion'] = inicio
    df.at[index, 'Horario de Termino de Colacion'] = termino
    # Añadir la persona a la lista de personas en la cafetería
    personas_en_cafeteria.append((inicio, termino, row['Area']))
    # Actualizar el total de personas en la cafetería
    total += 1

# Guardar el DataFrame modificado en un nuevo archivo de Excel
df.to_excel('C:\\Users\\coffe\\OneDrive\\Escritorio\\Programa\\Horarios_Modificados.xlsx', index=False)