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