from flask import Flask, render_template, request, jsonify, redirect, session
from datetime import timedelta
from copy import deepcopy
import requests
import uuid 
import os

# Ruta al archivo .env
env_file_path = ".env"

# Verifica si el archivo .env existe antes de intentar cargar las variables
if os.path.exists(env_file_path):
    with open(env_file_path, "r") as file:
        # Lee cada línea del archivo y configura las variables de entorno
        for line in file:
            # Ignora líneas que comienzan con "#" (comentarios) o están en blanco
            if not line.startswith("#") and "=" in line:
                key, value = line.strip().split("=", 1)
                os.environ[key] = value
                print("key:",key, " - value:",value)

# Carga las variables de entorno desde el archivo .env

# Accede a las variables de entorno
clave_secreta_de_sesion = os.environ.get("clave_secreta_de_sesion")
print("clave_secreta_de_sesion: ",clave_secreta_de_sesion)
# ----------> WOMPI <--------------

# Configura las llaves y la URL base según el ambiente (Sandbox o Producción)
public_key  = os.environ.get("WOMPI_TEST_PUBLIC_KEY")
private_key = os.environ.get("WOMPI_TEST_PRIVATE_KEY")
# Secreto proporcionado por Wompi
wompi_secret = os.environ.get("WOMPI_TEST_SECRET")
wompi_url = os.environ.get("WOMPI_TEST_URL")

#FUNCIONES
def generar_link_de_pago( private_key, nombre, descripcion, valor_cliente_a_pagar, expiration_time, Link_de_redireccion, Link_de_img_logo, id_Orden_de_Compra):
  # "https://production.wompi.co/v1" # version de produccion
  # "https://sandbox.wompi.co/v1" # Usar la URL de Sandbox para version de prueba
  base_url    = "https://production.wompi.co/v1"  # Usar la URL de Sandbox

  # Crear el encabezado de autenticación
  headers = {
      "Authorization": f"Bearer {private_key}"
  }

  # Crear el cuerpo de la petición con los detalles del link de pago
  payment_link_data = {
    "name": nombre,
    "description": descripcion,
    "single_use": True, # True si quiero que despues del primer pago ya no servira el link de pago, False si se puede hacer multiples pagos con el link
    "collect_shipping": False, # Si deseas que el cliente inserte su información de envío current el checkout, o no
    "collect_customer_legal_id": False,
    "currency": "COP",
    "amount_in_cents": valor_cliente_a_pagar, # Si el pago current por un monto específico, si no lo incluyes el pagador podrá elegir el valor a pagar.
                                              # los pagos son en centavos , el monto en pesos de debe multiplicar por 100
    "expires_at": expiration_time,  # Fecha de expiración
    "redirect_url": Link_de_redireccion, # URL donde será redirigido el cliente una vez termine el proceso de pago
    "image_url": Link_de_img_logo,
    "sku": id_Orden_de_Compra, # Identificador interno del producto current tu comercio. Máximo 36 caracteres
  }

  # Realizar la petición POST para crear el link de pago
  response = requests.post(f"{base_url}/payment_links", json=payment_link_data, headers=headers)

  return response

def obtener_informacion_producto(id):
    # Aquí deberías implementar la lógica para obtener la información del producto
    # Puedes obtener el ID, nombre y precio del producto desde una base de datos o cualquier otra fuente de datos.
    # Por ahora, simplemente retornaré una lista con diccionarios de ejemplo
    
    #BASE DE DATOS
    libros = [
        {
            'id':"elniñoaquel",
            'nombre':"El niño aquel",
            'precio': 70000,
            'precio-anterior':90000,
            'descripcion-corta': 'Descubre la fascinante odisea de ARMANDO JOSÉ CALDERÓN, un hombre cuya vida trasciende los límites de lo ordinario en "el niño aquel". Desde sus modestos comienzos en Maicao, LA GUAJIRA-COLOMBIA hasta su destacada labor ministerial en Bucaramanga, esta cautivadora autobiografía te sumergirá en un viaje emocional donde la fe y la determinación desafían todo pronóstico.',
            'descripcion': "...",
            'imagenes': [
                "static/images/elniдoaquel/foto_01.png",
                "static/images/elniдoaquel/foto_02.png",
                "static/images/elniдoaquel/foto_03.png",
            ]
        },
        {
            'id':"palabrasmemorables",
            'nombre':"Palabras Memorables",
            'precio': 70000,
            'precio-anterior':90000,
            'descripcion-corta': "Palabras memorables es la compilación de más de 150 enseñanzas que contienen una cantidad de temas doctrinales y de formación ministerial de nuestro visionero, Eliceo Duarte. Transcritas por el pastor Armando José Calderón, trabajo que hizo por muchas horas y años para lograr lo que hoy es palabras memorables.",
            'descripcion': "...",
            'imagenes': [
                "static/images/palabrasmemorables/foto_01.jpg",
                "static/images/palabrasmemorables/foto_02.png",
                "static/images/palabrasmemorables/foto_03.png",
            ]
        },
        {
            'id':"pequeñosinstrumentos",
            'nombre':"Pequeños Instrumentos",
            'precio': 70000,
            'precio-anterior':90000,
            'descripcion-corta': "Se trata del relato de la vida de una misionera, de tiempo completo, que por más de cincuenta años se ha dedicado a predicar el evangelio y a enseñar a vivir en Cristo.  Si, es la vida de la hermana Isabel Torres, que ahora, retirada del trajín de la obra, decidió contarnos como fue ese trabajo en diversos países.",
            'descripcion': "...",
            'imagenes': [
                "static/images/pequeдosinstrumentos/foto_01.jpg",
                "static/images/pequeдosinstrumentos/foto_02.png",
                "static/images/pequeдosinstrumentos/foto_03.png",
            ]
        }
    ]

    for book in libros:
        if book["id"] == id:
            return book
    else:
        return None

#SERVIDOR FLASK

app = Flask(__name__)

# Configuración para la sesión
app.secret_key = clave_secreta_de_sesion
app.permanent_session_lifetime = timedelta(hours=1) # la sesion se vence en 1 horas

@app.route('/', methods=['GET','POST'])
def index():
    # Verifica si ya hay un identificador de sesión en las cookies
    if 'user_id' not in session:
        # Si no hay un identificador de sesión, genera uno y almacénalo en las cookies
        session['user_id'] = str(uuid.uuid4())

    print( session['user_id'], session['carrito'] if 'carrito' in session else "")

    if request.method == 'GET':
        return render_template('index.html')
    
    return redirect('/')

@app.route('/product-review', methods=['GET','POST'])
def product():
    # Verifica si ya hay un identificador de sesión en las cookies
    if 'user_id' not in session:
        # Si no hay un identificador de sesión, genera uno y almacénalo en las cookies
        session['user_id'] = str(uuid.uuid4())

    print( session['user_id'], session['carrito'] if 'carrito' in session else "")

    if request.method == 'GET':
        if "libro" in request.args:
            libro = request.args.get("libro")
            libro = obtener_informacion_producto(libro)
            if libro != None:
                return render_template('product-review.html', libro=libro)
            else:
                return redirect('/')

    elif request.method == 'POST' :
        if "libro" in request.form and "pais" in request.form and "quantity" in request.form:
            print("request.form: ", request.form)
            libro    = request.form["libro"]
            pais     = request.form["pais"]
            cantidad = int(request.form["quantity"])

            # Obtener información del producto
            info_producto = obtener_informacion_producto(libro)
            
            # Inicializar el carrito si aún no existe en la sesión
            if 'carrito' not in session:
                session['carrito'] = []
            
            # Crear una copia de la lista del carrito en la sesión antes de realizar cambios
            carrito = deepcopy(session['carrito'])

            al_ready_exist = False
            index = -1
            for i in range(len(carrito)) :
                p = carrito[i]
                if p['id'] == libro:
                    index = i
                    al_ready_exist = True
                    break

            if al_ready_exist:
                rv_p = carrito.pop(index)
                carrito.insert(index,{
                    'id': info_producto['id'],
                    'nombre': info_producto['nombre'],
                    'precio': info_producto['precio'],
                    'imagenes': info_producto['imagenes'],
                    'pais'  : pais,
                    'cantidad': rv_p['cantidad'] + cantidad
                })
                
            else:
                # Agregar información del producto al carrito en la sesión
                carrito.append({
                    'id': info_producto['id'],
                    'nombre': info_producto['nombre'],
                    'precio': info_producto['precio'],
                    'imagenes': info_producto['imagenes'],
                    'pais'  : pais,
                    'cantidad': cantidad
                })
            
            session['carrito'] = carrito 

            return redirect('/cart')

    return redirect('/')

@app.route('/cart', methods=['GET','POST'])
def cart():
    # Verifica si ya hay un identificador de sesión en las cookies
    if 'user_id' not in session:
        # Si no hay un identificador de sesión, genera uno y almacénalo en las cookies
        session['user_id'] = str(uuid.uuid4())
    
    print( session['user_id'], session['carrito'] if 'carrito' in session else "")

    if request.method == 'GET':
        # Inicializar el carrito si aún no existe en la sesión
        if 'carrito' not in session:
            session['carrito'] = []

        return render_template('cart.html', cart=session['carrito'])
    else:
        request_data = request.get_json()
        print("request_data: ",request_data)
        return jsonify({"error": 0, "url": "aqui url"})
    
    
#if __name__ == "__main__":
#  app.run(debug=True)