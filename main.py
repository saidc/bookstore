from flask import Flask, render_template, request, jsonify, redirect, session
from datetime import datetime, timedelta
from datetime import timedelta
from copy import deepcopy
import platform
import requests
import uuid
import os

sist_op = platform.system()

print("path actual: ", os.getcwd())
delta_time = -5 if sist_op == "Linux" else 0
env_file_path = "myapp/bookstore/.env" if sist_op == "Linux" else ".env" # else "Windows"
print( "estas en un sistema " + str(sist_op))

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
else:
    print("el path: ", env_file_path,  " no existe")

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

def obtener_hora_colombia(delta):
    # Obtener la hora actual en UTC
    hora_actual_utc = datetime.now() # datetime.utcnow() 
    diferencia_horas = timedelta(hours=delta)
    hora_colombia = hora_actual_utc + diferencia_horas
    return hora_colombia.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

print("hora Colombia" , obtener_hora_colombia(delta_time))

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

    #print( session['user_id'], session['carrito'] if 'carrito' in session else "")

    if request.method == 'GET':
        # Inicializar el carrito si aún no existe en la sesión
        if 'carrito' not in session:
            session['carrito'] = []
        return render_template('cart.html', cart=session['carrito'])
    
    else:
        # se obtiene los parametros enviados para el metodo de pago
        request_data = request.get_json()
        print("request_data: ",request_data)
        # se verifica que se obtengan los parametros necesarios para procesar el link de pago
        if "total" in request_data and "productos" in request_data and "taxvalue" in request_data and "shipping" in request_data:
            productos   =  request_data["productos"]
            taxvalue    =  float(request_data["taxvalue"])
            shipping    =  int(request_data["shipping"])
            total       =  float(request_data["total"])

            print(type(productos),type(taxvalue),type(shipping),type(total))
            # calculara el total a pagar
            h_total = 0
            # calcula el costo de envio
            h_shipping = 0
            # calcula el numero total de libros
            total_amount = 0
            # obtendra las lista de productos distintos con su subtotal
            productos_comprar = []
            for prod in productos:
                # id del producto
                id = prod["id"]
                # se obtiene el producto de la base de datos con el id
                p = obtener_informacion_producto(id)
                # se verifica que el producto exista en la base de datos
                if p != None:
                    imageSrc = prod["imageSrc"]
                    amount = int(prod["amount"])
                    price = int(prod["price"])
                    name = prod["name"]

                    # se va sumando la cantidad de libros a comprar
                    total_amount = total_amount + amount
                    # se va calculanto el subtotal de un tipo de libro
                    subtotal = amount * price
                    # se va sumando todos los subtotales para obtener el monto total a pagar
                    h_total = h_total + subtotal
                    # se añade los datos calculados del producto a las lista de productos a comprar
                    productos_comprar.append({
                        "id": id,
                        "name":name,
                        "image": imageSrc,
                        "amount":amount,
                        "price":price,
                        "subtotal": subtotal
                    })
                    
                else:
                    return jsonify({"error": 2, "error-msg":"Un producto a comprar no existe"})
            
            if total_amount < 100:
                #print(h_total, total)
                #print(productos_comprar, taxvalue/h_total )
                
                h_shipping = 10000 if total_amount < 10 else 20000 if total_amount < 25 else 35000 if total_amount < 50 else 50000 if total_amount < 75 else 65000
                nombre = "compra de libro cristiano" if total_amount == 1 else "Compra de libros cristiano"
                id_Orden_de_Compra = str(uuid.uuid4())
                descripcion = "" 
                for pr in productos_comprar:
                    name = pr["name"]
                    amount = pr["amount"]
                    subtotal = pr["subtotal"]
                    descripcion = descripcion + f"""
                        Nombre: {name}
                        Cantidad: {amount}
                        subtotal: {subtotal}

                    """
                h_total += h_shipping
                descripcion = descripcion + f"""
                    Costo de envio: {h_shipping}
                    total:  {h_total}
                """
                valor_a_pagar_centavos = h_total * 100  # este pago debe ser en centavos de pesos, 100 pesos debe enviarse como 10000
                
                expiration_time = obtener_hora_colombia(delta_time+2) # el link de pago expira en 2 horas
                Link_de_redireccion = "https://api.whatsapp.com/send?phone=15147125576&text=Hola%20DTB%20hice%20una%20compra%2C%20mi%20numero%20de%20pedido%20es%20("+id_Orden_de_Compra+")"
                Link_de_img_logo = "https://saidc.pythonanywhere.com/static/images/hero_bg_1.jpg"

                print( private_key, nombre, descripcion, valor_a_pagar_centavos, expiration_time, Link_de_redireccion, Link_de_img_logo, id_Orden_de_Compra)
                #url = "aqui tu url"
                response = generar_link_de_pago( private_key, nombre, descripcion, valor_a_pagar_centavos, expiration_time, Link_de_redireccion, Link_de_img_logo, id_Orden_de_Compra)
                if response.status_code == 201:
                    data = response.json()["data"]
                    payment_link_id = data["id"] # payment_link_id
                    fecha_de_creacion = data["created_at"]
                    fecha_de_expiracion = data["expires_at"]
                    print("link de pago response: ", response.json())
                    url = f"https://checkout.wompi.co/l/{payment_link_id}" 
                    return jsonify({"error": 0, "url": url})
                else:
                    return jsonify({"error": 4, "error-msg":"Error al obtener el link de pago, intentar mas tarde"})
            else:
                return jsonify({"error": 3, "error-msg":"la cantidad maxima son 100 libros por compra"})
        else:
            return jsonify({"error": 1, "error-msg":"Parametros incorrectos o faltantes"})
        



#if __name__ == "__main__":
#  app.run(debug=True)