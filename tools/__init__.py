from datetime import datetime, timedelta
import urllib.request
import base64
import json
import ast
import os

def asignar_valor(lista, posicion, valor):
    # Verificar si la posición está dentro del rango de la lista
    if posicion < 0:
        #print("La posición no puede ser negativa.")
        return lista
    elif posicion >= len(lista):
        # Si la posición está fuera del rango de la lista, agregar elementos vacíos hasta alcanzarla
        lista.extend([""] * (posicion - len(lista) + 1))
    # Asignar el valor a la posición especificada
    lista[posicion] = valor
    #print("Lista actualizada:", lista)
    return lista

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

def obtener_precio_dolar():
    try:
        # URL base de la API
        base_url = "https://www.datos.gov.co/api/id/32sa-8pi3.json"
        
        # Calcular la fecha de hoy
        fecha_actual = datetime.now()
        
        # Construir la consulta
        consulta = "?$query=select%20*%2C%20%3Aid%20order%20by%20%60vigenciadesde%60%20desc%20limit%20100"
        url = f"{base_url}{consulta}"

        # Headers
        headers = {
            "accept": "application/json",
            "x-app-token": "U29jcmF0YS0td2VraWNrYXNz0",
            "x-csrf-token": "r1uXrJjAY/pQF4HkN6eSIp5c9P3hnbUvAGPH/TzPlw2ybnPCKtLmaOetCVkA3sS5CSmUZn+rpV34I0K3OMi0cQ==",
            "x-socrata-federation": "Honey Badger"
        }

        # Crear un objeto de solicitud y agregar los encabezados necesarios
        solicitud = urllib.request.Request(url, headers=headers)

        # Realizar la solicitud GET
        respuesta = urllib.request.urlopen(solicitud)
        
        # Leer la respuesta y cargar los datos JSON
        datos = json.loads(respuesta.read().decode())

        # Ordenar los datos por la fecha de vigencia desde de forma descendente
        datos_ordenados = sorted(datos, key=lambda x: x['vigenciadesde'], reverse=True)

        # Tomar el primer valor de la lista (el más cercano a la fecha actual)
        valor_mas_cercano = int(float(datos_ordenados[0]['valor']))

        return valor_mas_cercano

    except Exception as e:
        print("Error al obtener el precio del dólar:", e)
        return 4000

# Función para obtener la fecha y hora actual
def get_current_datetime():
    now = datetime.now()
    return now

# Función para calcular segundos restantes hasta days_of_count_down
def calculate_seconds_remaining(days_of_count_down_text):
    days_of_count_down = datetime.strptime(days_of_count_down_text, "%Y-%m-%d %H:%M:%S")
    # Convertir la cadena de texto a un objeto datetime
    current_datetime = get_current_datetime()
    time_difference = days_of_count_down - current_datetime
    seconds_remaining = int(time_difference.total_seconds())
    return seconds_remaining
