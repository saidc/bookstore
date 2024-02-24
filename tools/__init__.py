from datetime import datetime, timedelta
import ast
import os

def getenv_var(env_file_path):
    # Obtener las variables de entorno 
    if os.path.exists(env_file_path):
        with open(env_file_path, "r") as file:
            # Lee cada línea del archivo y configura las variables de entorno
            for line in file:
                # Ignora líneas que comienzan con "#" (comentarios) o están en blanco
                if not line.startswith("#") and "=" in line:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
                    #print("key:",key, " - value:",value)
    else:
        print("el path: ", env_file_path,  " no existe")

def obtener_hora_colombia(delta):
    # Obtener la hora actual en UTC
    hora_actual_utc = datetime.now() # datetime.utcnow() 
    diferencia_horas = timedelta(hours=delta)
    hora_colombia = hora_actual_utc + diferencia_horas
    return hora_colombia.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def convert_to_list(value):
    try:
        # Intenta evaluar el valor como una expresión de Python
        evaluated_value = ast.literal_eval(value)
        # Verifica si el resultado es una lista
        if isinstance(evaluated_value, list):
            return evaluated_value
    except (SyntaxError, ValueError):
        pass  # Ignora errores de evaluación

    # Si no se pudo evaluar como lista, devuelve el valor original
    return value