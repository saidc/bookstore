from flask import Flask, render_template, jsonify, redirect, session
from flask import request as rq
from datetime import datetime, timedelta
from datetime import timedelta
from urllib import request as urllib_rq
from urllib.error import HTTPError
from copy import deepcopy
import platform
import hashlib
import tools
import uuid
import json
import os

sist_op = platform.system()
print( "estas en un sistema " + str(sist_op))

print("path actual: ", os.getcwd())
delta_time = -5 if sist_op == "Linux" else 0
env_file_path = ".env"#"myapp/bookstore/.env" if sist_op == "Linux" else ".env" # else "Windows"

# obtener variables de entorno
tools.getenv_var(env_file_path=env_file_path)

# Accede a las variables de entorno
clave_secreta_de_sesion = os.environ.get("clave_secreta_de_sesion")

# ----------> WOMPI <--------------
# Configura las llaves y la URL base según el ambiente (Sandbox o Producción)
public_key  = os.environ.get("WOMPI_TEST_PUBLIC_KEY")
private_key = os.environ.get("WOMPI_TEST_PRIVATE_KEY")
# Secreto proporcionado por Wompi
wompi_secret = os.environ.get("WOMPI_TEST_SECRET")
wompi_url = os.environ.get("WOMPI_TEST_URL")

print( "public_key: ", public_key )
print( "private_key: ", private_key )
print( "wompi_secret: ", wompi_secret )
print( "wompi_url: ", wompi_url )

#FUNCIONES
def generar_link_de_pago( private_key, nombre, descripcion, valor_cliente_a_pagar, expiration_time, Link_de_redireccion, Link_de_img_logo, id_Orden_de_Compra):
  global wompi_url
  # "https://production.wompi.co/v1" # version de produccion
  # "https://sandbox.wompi.co/v1" # Usar la URL de Sandbox para version de prueba
  base_url = wompi_url  # Usar la URL de Sandbox
  
  # Crear el encabezado de autenticación
  headers = {
    "Authorization": f"Bearer {private_key}"
  }

  # Crear el cuerpo de la petición con los detalles del link de pago
  payment_link_data = {
    "name": nombre,
    "description": descripcion,
    "single_use": True, # True si quiero que despues del primer pago ya no servira el link de pago, False si se puede hacer multiples pagos con el link
    "collect_shipping": True, # Si deseas que el cliente inserte su información de envío current el checkout, o no
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
  try:
    req = urllib_rq.Request(f"{base_url}/payment_links", data=json.dumps(payment_link_data).encode(), headers=headers, method='POST')
    with urllib_rq.urlopen(req) as response:
      return response.read().decode()
  except HTTPError as e:
    print("Error HTTP:", e.code)
    print("Respuesta:", e.read().decode())
    return None
  
def verify_event(request_data):
  global wompi_secret
  if "signature" not in request_data:
    return False

  event_signature = request_data["signature"]["checksum"]
  properties = request_data["signature"]["properties"]
  data_values = []

  for prop in properties:
    prop_split = prop.split('.')
    prop_split_rslt = request_data["data"][prop_split[0]][prop_split[1]]
    data_values.append(str(prop_split_rslt))

  timestamp = str(request_data["timestamp"])
  data_string = "".join(data_values)
  data_string += timestamp
  data_string += wompi_secret

  # Calcular el checksum SHA256 utilizando hashlib
  m = hashlib.sha256()
  m.update(data_string.encode('utf-8'))
  calculated_checksum = m.hexdigest()#.upper()
  #print("calculated_checksum: ", calculated_checksum)
  #print("event_signature: ", event_signature)
  # Comparar el checksum calculado con el proporcionado en el evento
  return calculated_checksum == event_signature

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
                "https://live.staticflickr.com/65535/53541352177_10a216e3c0_o.png",
                "https://live.staticflickr.com/65535/53542553219_4414c9666a_o.png",
                "https://live.staticflickr.com/65535/53541352132_1f384312ab_o.png",
            ],
            'video': {
                "hasVideo": True,
                "href": "https://www.flickr.com/photos/200131147@N06/53543632894/in/dateposted-public/",
                "title": "Video del libro el niño aquel",
                "img-src": "https://live.staticflickr.com/31337/53543632894_4eb1eb834f_o.jpg",
                "width": 404,
                "height": 720,  
            }	
        },
        {
            'id':"palabrasmemorables",
            'nombre':"Palabras Memorables",
            'precio': 70000,
            'precio-anterior':90000,
            'descripcion-corta': "Palabras memorables es la compilación de más de 150 enseñanzas que contienen una cantidad de temas doctrinales y de formación ministerial de nuestro visionero, Eliceo Duarte. Transcritas por el pastor Armando José Calderón, trabajo que hizo por muchas horas y años para lograr lo que hoy es palabras memorables.",
            'descripcion': "...",
            'imagenes': [
                "https://live.staticflickr.com/65535/53542410328_7392d8a4d0_o.jpg",
                "https://live.staticflickr.com/65535/53542228811_0d3a009021_o.png",
                "https://live.staticflickr.com/65535/53542553074_f8c119ff75_o.png",                
            ],
            'video': {
                "hasVideo": True,
                "href": "https://www.flickr.com/photos/200131147@N06/53543633009/in/dateposted-public/",
                "title": "Video del libro palabras memorables",
                "img-src": "https://live.staticflickr.com/31337/53543633009_6b147d4317_o.jpg",
                "width": 270,
                "height": 360,  
            }
            
        },
        {
            'id':"pequeñosinstrumentos",
            'nombre':"Pequeños Instrumentos",
            'precio': 70000,
            'precio-anterior':90000,
            'descripcion-corta': "Se trata del relato de la vida de una misionera, de tiempo completo, que por más de cincuenta años se ha dedicado a predicar el evangelio y a enseñar a vivir en Cristo.  Si, es la vida de la hermana Isabel Torres, que ahora, retirada del trajín de la obra, decidió contarnos como fue ese trabajo en diversos países.",
            'descripcion': "...",
            'imagenes': [
                "https://live.staticflickr.com/65535/53542657250_700ab17f7b_o.jpg",
                "https://live.staticflickr.com/65535/53542410233_64fd16a91c_o.png",
                "https://live.staticflickr.com/65535/53542657215_07452bf09e_o.png",                
            ],
            'video': {
                "hasVideo": True,
                "href": "https://www.flickr.com/photos/200131147@N06/53543764645/in/dateposted-public/",
                "title": "Video del libro pequeños instrumentos",
                "img-src": "https://live.staticflickr.com/31337/53543764645_6955ccc268_o.jpg",
                "width": 1920,
                "height": 1080,  
            }			
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

    if 'carrito' not in session:
                session['carrito'] = []

    no_productos = 0
    for p in session["carrito"]:
        no_productos += int(p["cantidad"])

    #print("user_id: ", session['user_id'], session['carrito'] if 'carrito' in session else "")

    if rq.method == 'GET':
        return render_template('index.html',noproductos = no_productos)

    return redirect('/')

@app.route('/product-review', methods=['GET','POST'])
def product():
    # Verifica si ya hay un identificador de sesión en las cookies
    if 'user_id' not in session:
        # Si no hay un identificador de sesión, genera uno y almacénalo en las cookies
        session['user_id'] = str(uuid.uuid4())
    
    if 'carrito' not in session:
                session['carrito'] = []

    no_productos = 0

    for p in session["carrito"]:
        no_productos += int(p["cantidad"])

    if rq.method == 'GET':
        if "libro" in rq.args:
            libro = rq.args.get("libro")
            libro = obtener_informacion_producto(libro)
            if libro != None:
                return render_template('product-review.html', libro=libro, noproductos = no_productos)
            else:
                return redirect('/')

    elif rq.method == 'POST' :
        if "libro" in rq.form and "pais" in rq.form and "quantity" in rq.form:
            print("request.form: ", rq.form)
            libro    = rq.form["libro"]
            pais     = rq.form["pais"]
            cantidad = int(rq.form["quantity"])

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

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    request_data = rq.get_json()
    print("webhook request_data: ", request_data)

    # Verificar la autenticidad del evento
    if verify_event(request_data):
        print("El webhook recibido es autentico ")
        if "data" in request_data:
            if "transaction" in request_data["data"]:
                keys = ["id","created_at","status","amount_in_cents","payment_link_id","payment_method","customer_email","shipping_address"]
                # se verifica si request["data"]["transaction"] contiene la lista de keys 
                keys_in_request = [k in request_data["data"]["transaction"] for k in keys]
                if not False in keys_in_request:
                    print( "el request contiene los siguientes keys: ", keys )
                    payment_link_id = request_data["data"]["transaction"]["payment_link_id"]
                    proceso_compra_id = request_data["data"]["transaction"]["id"]
                    estado_compra = request_data["data"]["transaction"]["status"]
                    shipping_address = request_data["data"]["transaction"]["shipping_address"]
                    
                    #user_id, creditos_comprados = dbm.actualizar_proceso_compra(payment_link_id, proceso_compra_id, estado_compra)
                    print("variables de respuesta de pago: \n", )
                    print("     payment_link_id: ", payment_link_id)
                    print("     proceso_compra_id: ", proceso_compra_id)
                    print("     estado_compra: ", estado_compra) 
                    print("     shipping_address: ", shipping_address) 
                else:
                    print(f"la pregunta not false in {keys_in_request} \n segun la lista es {keys}") 
            else:
                print("no esta transaction en request data obtenida en el webhook")
        else:
            print("no esta data en request data obtenida en el webhook")
        return jsonify({"status": "Evento auténtico"})
    else:
      print("El webhook recibido No es autentico ")
      # El evento no es auténtico, ignóralo
      return jsonify({"status": "Evento no auténtico"}), 400

@app.route('/goHome', methods=['GET','POST'])
def goHome():

    if 'user_id' not in session:
        # Si no hay un identificador de sesión, genera uno y almacénalo en las cookies
        session['user_id'] = str(uuid.uuid4())

    request_data = rq.get_json()
    #print("request_data: ",request_data)
    print("presionaste /goHome")
    # se verifica que se obtengan los parametros necesarios para procesar el link de pago
    if "productos" in request_data :
        productos   =  request_data["productos"]
        if len(productos) > 0:
            print(" hay productos en el carrito")
            # Inicializar el carrito si aún no existe en la sesión
            if 'carrito' not in session:
                session['carrito'] = []

            # Crear una copia de la lista del carrito en la sesión antes de realizar cambios
            carrito = deepcopy(session['carrito'])
            print("carrito antes de actualizacion: ", carrito )
            #existentes = []
            porborrar = []
            porActualizar = []

            # se verifica los productos que existen
            for i, p in enumerate(carrito):
                sw = False
                for p_t in productos:
                    if p_t["id"] == p["id"]:
                        #existentes.append(p_t)
                        sw = True
                        if p_t["amount"] != p["cantidad"]:
                            porActualizar.append({"id":p["id"], "cantidad":p_t["amount"]})
                            print("por actualizar: ",{"id":p["id"], "cantidad":p_t["amount"]}, " canitada anterior: ", p["cantidad"])
                        break
                if sw == False:
                    porborrar.append(p["id"])
                    print("por borrar ", p["id"])

            # se borra los productos borrados en el carrito del navegador
            while len(porborrar) > 0:
                pb = porborrar.pop(0)
                for i in range(len(carrito)):
                    if carrito[i]["id"] == pb:
                        carrito.pop(i)
                        break

            # actualizar cantidad 
            while len(porActualizar) > 0:
                pa = porActualizar.pop(0)
                for i in range(len(carrito)):
                    if( carrito[i]["id"] == pa["id"]):
                        carrito[i]["cantidad"] = pa["cantidad"]
                        break
            
            print("carrito despues de actualizacion: ", carrito )

            session['carrito'] = carrito
        else:
            session['carrito'] = []

        return jsonify({"error": 2, "msg":"se actualizo "})
    else:
        return jsonify({"error": 1, "error-msg":"error al actualizar cookie"})

@app.route('/cart', methods=['GET','POST'])
def cart():
    global private_key
    # Verifica si ya hay un identificador de sesión en las cookies
    if 'user_id' not in session:
        # Si no hay un identificador de sesión, genera uno y almacénalo en las cookies
        session['user_id'] = str(uuid.uuid4())

    #print( session['user_id'], session['carrito'] if 'carrito' in session else "")

    if rq.method == 'GET':
        # Inicializar el carrito si aún no existe en la sesión
        if 'carrito' not in session:
            session['carrito'] = []

        return render_template('cart.html', cart=session['carrito'])
    else:
        # se obtiene los parametros enviados para el metodo de pago
        request_data = rq.get_json()
        print("request_data: ",request_data)
        # se verifica que se obtengan los parametros necesarios para procesar el link de pago
        if "total" in request_data and "productos" in request_data and "taxvalue" in request_data and "shipping" in request_data:
            productos   =  request_data["productos"]
            taxvalue    =  float(request_data["taxvalue"])
            shipping    =  int(request_data["shipping"])
            total       =  float(request_data["total"])

            #print(type(productos),type(taxvalue),type(shipping),type(total))
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
                
                expiration_time = obtener_hora_colombia(delta_time+6) # el link de pago expira en 2 horas
                Link_de_redireccion = "https://api.whatsapp.com/send?phone=15147125576&text=Hola%20DTB%20hice%20una%20compra%2C%20mi%20numero%20de%20pedido%20es%20("+id_Orden_de_Compra+")"
                Link_de_img_logo = "https://saidc.pythonanywhere.com/static/images/hero_bg_1.jpg"

                print( "variables que generan link de pago: \n", private_key, nombre, descripcion, valor_a_pagar_centavos, expiration_time, Link_de_redireccion, Link_de_img_logo, id_Orden_de_Compra)
                #url = "aqui tu url"
                response = generar_link_de_pago( private_key, nombre, descripcion, valor_a_pagar_centavos, expiration_time, Link_de_redireccion, Link_de_img_logo, id_Orden_de_Compra)
                print("responses.status_code: ", response)
    
                if response is not None:
                    try:
                        response_data = json.loads(response)
                        if "data" in response_data:
                            data = response_data["data"]
                            payment_link_id = data["id"]
                            fecha_de_creacion = data["created_at"]
                            fecha_de_expiracion = data["expires_at"]
                            print("Link de pago --> fecha_de_creacion: ",fecha_de_creacion, " fecha_de_expiracion: ",fecha_de_expiracion)
                            
                            url = f"https://checkout.wompi.co/l/{payment_link_id}"
                            print( {"error": 0, "url": url})
                            session['carrito'] = []
                            return jsonify({"error": 0, "url": url})
                        else:
                            print( {"error": 4, "error-msg":"Error al obtener el link de pago, intentar mas tarde"})
                            return( {"error": 4, "error-msg":"Error al obtener el link de pago, intentar mas tarde"})
                    except json.JSONDecodeError as e:
                        print("Error al decodificar la respuesta JSON:", e)
                        return("Error al decodificar la respuesta JSON:", e)
                else:
                    return jsonify({"error": 4, "error-msg":"Error al obtener el link de pago, intentar mas tarde"})
            else:
                return jsonify({"error": 3, "error-msg":"la cantidad maxima son 100 libros por compra"})
        else:
            return jsonify({"error": 1, "error-msg":"Parametros incorrectos o faltantes"})
        
if __name__ == "__main__":
  app.run(debug=True)
