# coding=utf-8
from sheet import get_token_credentials, get_rows, connect_to_sheet_api, append_row_value, send_email, batch_update_row_value
from flask import Flask, render_template, jsonify, redirect, session
from base_de_datos import obtener_informacion_producto, nuevo_procesamiento_de_pedido, obtener_pedido_by_payment_link_id, update_row_by_webhook_respond
from wompi import generar_link_de_pago, verify_event, get_webhook_param, get_webhook_param_json
from tools import getenv_var, obtener_hora_colombia, convert_to_list, obtener_precio_dolar, calculate_seconds_remaining
from flask import request as rq
from datetime import timedelta
from copy import deepcopy
import platform
import psutil
import uuid
import json
import os
import time

ESTADO_PROYECTO = "TEST" # PROD

sist_op = platform.system()
print( "estas en un sistema " + str(sist_op) )
print( "path actual: ", os.getcwd() )
delta_time = -5 if sist_op == "Linux" else 0
env_file_path = ".env" # "myapp/bookstore/.env" if sist_op == "Linux" else ".env" # else "Windows"

# obtener variables de entorno
getenv_var(env_file_path=env_file_path)

print("hora Colombia" , obtener_hora_colombia(delta_time))

#SERVIDOR FLASK
app = Flask(__name__)

# Configuración para la sesión
print("clave_secreta_de_sesion: ", os.environ.get("clave_secreta_de_sesion") )
app.secret_key = os.environ.get("clave_secreta_de_sesion") 

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

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    request_data = rq.get_json()
    wompi_secret = os.environ.get("WOMPI_PRODUCTION_SECRET") if ESTADO_PROYECTO == "PROD" else os.environ.get("WOMPI_TEST_SECRET")
    # Verificar la autenticidad del evento
    if verify_event(wompi_secret, request_data):
        if "data" in request_data:
            if "transaction" in request_data["data"]:
                
                SCRIPT_ID = os.environ.get("SCRIPT_ID") 

                TOKEN_FILE = os.environ.get("SHEET_TOKEN_FILE")
                CLIENT_SECRET = os.environ.get("SHEET_CLIENT_SECRET") 
                SCOPES = convert_to_list( os.environ.get("SHEET_SCOPES") )
                #SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID") 
                SPREADSHEET_ID = os.environ.get("SPREADSHEET_2_ID") 
                #SHEET_NAME = os.environ.get("SHEET_NAME") 
                SHEET_NAME = os.environ.get("SHEET_2_NAME") 

                creds = get_token_credentials(TOKEN_FILE, CLIENT_SECRET, SCOPES)
                service = connect_to_sheet_api(creds)

                if(service):
                    print("conexion exitosa")
                    transaction_data = request_data["data"]["transaction"]
                    webhook_res = get_webhook_param( transaction_data )
                    row_json = get_webhook_param_json( transaction_data )
                    print("webhook_res: \n", webhook_res)
                    payment_link_id = row_json["payment_link_id"]

                    #new_row = [ proceso_compra_id,  "El niño aquel",  80000,    str(shipping_address),   "sayacorcal@gmail.com",  str(request_data["data"]) ]
                    time.sleep(4)
                    rows = get_rows(service, SPREADSHEET_ID, SHEET_NAME)
                    print("rows de g_sheet: \n", rows)
                    pos, row =  obtener_pedido_by_payment_link_id(rows, payment_link_id)
                    print("row of g_sheet: \n", pos, row)
                    
                    row = update_row_by_webhook_respond(row, webhook_res)
                    print("final row: \n", row)
                    productos_a_comprar = row[15]

                    rslt = batch_update_row_value( service, SPREADSHEET_ID, SHEET_NAME, row_to_update=pos+1, value=row ) 
                    #rslt = append_row_value(service, SPREADSHEET_ID, SHEET_NAME, webhook_res)
                    
                    print("result: ", rslt)
                    email = row_json["customer_email"]
                    proceso_compra_id = row_json["proceso_compra_id"]
                    asunto = f"Compra de Libro Cristiano - {proceso_compra_id}"
                    
                    pais = row_json["country"]
                    region = row_json["region"]
                    city = row_json["city"]
                    phone_number = row_json["phone_number"]
                    address_line_1 = row_json["address_line_1"]
                    address_line_2 = row_json["address_line_2"]
                    
                    if row_json["status"] ==  "APPROVED":
                        
                        descripcion = f"""
                            Dios te bendiga, Gracias por tu compra de libros cristianos.
                            Recibimos tu compra y estamos en proceso de envio a la siguiente direccion
                            pais:   {pais}
                            region: {region}
                            city:   {city}
                            phone_number:   {phone_number}
                            address_line_1: {address_line_1}
                            address_line_2: {address_line_2}
                            productos a comprar {productos_a_comprar}
                            """
                        send_email(creds,SCRIPT_ID,email,asunto,descripcion)
                    else:
                        descripcion = f"""
                            Dios te bendiga, El proceso de compra ha sido DECLINADA.
                            Intenta nuevamente o comunicate a: 
                            
                            https://m.me/said.cortescalderon 
                            
                            """
                        send_email(creds,SCRIPT_ID,email,asunto,descripcion)
                        print(rslt)
                else:
                    print("conexion fallida")
            else:
                print("no esta transaction en request data obtenida en el webhook")
        else:
            print("no esta data en request data obtenida en el webhook")
        return jsonify({"status": "Evento auténtico"}), 200
    else:
      print("El webhook recibido No es autentico ")
      # El evento no es auténtico, ignóralo
      return jsonify({"error": "Método no permitido"}), 405

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

@app.route('/product-review', methods=['GET','POST'])
def product():
    # Verifica si ya hay un identificador de sesión en las cookies
    if 'user_id' not in session:
        # Si no hay un identificador de sesión, genera uno y almacénalo en las cookies
        session['user_id'] = str(uuid.uuid4())
    
    if 'carrito' not in session:
        session['carrito'] = []

    no_productos = 0
    pais_producto = None

    for p in session["carrito"]:
        no_productos += int(p["cantidad"])
        if pais_producto == None:
            pais_producto = p["pais"]
            
    if rq.method == 'GET':
        if "libro" in rq.args:
            id = rq.args.get("libro")
            libro = obtener_informacion_producto(id)
            if libro != None:
                return render_template('product-review.html', libro=libro, noproductos = no_productos, pais=pais_producto)
            else:
                return redirect('/')

    elif rq.method == 'POST' :
        if "libro" in rq.form and "pais" in rq.form and "quantity" in rq.form:
            print("request.form: ", rq.form)
            id    = rq.form["libro"]
            pais     = rq.form["pais"]
            cantidad = int(rq.form["quantity"])

            # Obtener información del producto
            info_producto = obtener_informacion_producto(id)
                        
            # Inicializar el carrito si aún no existe en la sesión
            if 'carrito' not in session:
                session['carrito'] = []

            # Crear una copia de la lista del carrito en la sesión antes de realizar cambios
            carrito = deepcopy(session['carrito'])

            al_ready_exist = False
            index = -1
            for i in range(len(carrito)) :
                p = carrito[i]
                if p['id'] == id:
                    index = i
                    al_ready_exist = True
                    break

            if al_ready_exist:
                rv_p = carrito.pop(index)
                carrito.insert(index,{
                    'id': info_producto['id'],
                    'nombre': info_producto['nombre'],
                    'precio': [p["precio"] for p in info_producto['precio'] if p["pais"] == pais][0],
                    'imagenes': info_producto['imagenes'],
                    'pais'  : pais,
                    'cantidad': rv_p['cantidad'] + cantidad
                })

            else:
                # Agregar información del producto al carrito en la sesión
                carrito.append({
                    'id': info_producto['id'],
                    'nombre': info_producto['nombre'],
                    'precio': [p["precio"] for p in info_producto['precio'] if p["pais"] == pais][0],
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

    # print( session['user_id'], session['carrito'] if 'carrito' in session else "")
    # Inicializar el carrito si aún no existe en la sesión
    if 'carrito' not in session:
        session['carrito'] = []

    no_productos = 0
    pais_producto = None

    for p in session["carrito"]:
        no_productos += int(p["cantidad"])
        if pais_producto == None:
            pais_producto = p["pais"]

    if rq.method == 'GET':
        return render_template('cart.html', cart=session['carrito'], pais=pais_producto, no_productos=no_productos)
    else:
        # se obtiene los parametros enviados para el metodo de pago
        request_data = rq.get_json()
        print("request_data: ",request_data)
        # se verifica que se obtengan los parametros necesarios para procesar el link de pago
        if "productos" in request_data: # and "total" in request_data and "taxvalue" in request_data and "shipping" in request_data:
            productos   =  request_data["productos"]
            #taxvalue    =  float(request_data["taxvalue"])
            #shipping    =  int(request_data["shipping"])
            #total       =  float(request_data["total"])

            if pais_producto != "COLOMBIA":
                dolar = obtener_precio_dolar()

            # calculara el total a pagar
            h_total = 0 
            # calculara el total a pagar en dolar
            h_dolar_total = 0 

            # calcula el costo de envio
            h_shipping = 0 
            # calcula el numero total de libros
            total_amount = 0 
            # obtendra las lista de productos distintos con su subtotal
            productos_comprar = [] 
            for prod in productos:
                
                # se obtiene el producto de la base de datos con el id
                p = obtener_informacion_producto(prod["id"])
                # se verifica que el producto exista en la base de datos
                if p != None:
                    imageSrc = p["imagenes"][0]["image"]
                    amount = int(prod["amount"])
                    price = int([p2["precio"] for p2 in p['precio'] if p2["pais"] == pais_producto ][0])
                    name = p["nombre"]
                    dolar_price = -1

                    if pais_producto != "COLOMBIA":
                        #dolar = obtener_precio_dolar()
                        dolar_price = price
                        price = int(price * dolar)


                    # se va sumando la cantidad de libros a comprar
                    total_amount = total_amount + amount
                    # se va calculanto el subtotal de un tipo de libro
                    subtotal = amount * price
                    dolar_subtotal = amount * dolar_price
                    # se va sumando todos los subtotales para obtener el monto total a pagar
                    h_total = h_total + subtotal
                    h_dolar_total += dolar_subtotal

                    # se añade los datos calculados del producto a las lista de productos a comprar
                    productos_comprar.append({
                        "id": p["id"],
                        "name":name,
                        "image": imageSrc,
                        "price":price,
                        "amount":amount,
                        "subtotal": subtotal,
                        "price_dolar":dolar_price,
                        "dolar_subtotal":dolar_subtotal

                    })
                else:
                    return jsonify({"error": 2, "error-msg":"Producto Errorneo o inexistente"})
            
            if total_amount < 20:
                h_shipping = 10000 if total_amount < 10 else 20000 
                h_dolar_shipping = 0
                if total_amount < 10:
                    if pais_producto != "COLOMBIA":
                        h_dolar_shipping = 12
                        h_shipping = h_dolar_shipping * dolar
                else:
                    if pais_producto != "COLOMBIA":
                        h_dolar_shipping = 22
                        h_shipping = h_dolar_shipping * dolar

                nombre = "compra de libro cristiano" if total_amount <= 1 else "Compra de libros cristiano"
                id_Orden_de_Compra = str(uuid.uuid4())
                descripcion = "" 
                moneda = "COP" if pais_producto == "COLOMBIA" else "USD"

                for pr in productos_comprar:
                    name = pr["name"]
                    amount = pr["amount"]
                    subtotal = pr["subtotal"]
                    dolar_subtotal = pr["dolar_subtotal"]

                    descripcion = descripcion + f"""
                        Nombre: {name}
                        Cantidad: {amount}
                        subtotal: {subtotal} 
                    """
                    if pais_producto != "COLOMBIA":
                        descripcion += f"""
                            Dolar subtotal: {dolar_subtotal}

                        """
                    else:
                        descripcion += f"""
                        
                        """

                tax_value = h_total * 0.19
                h_total += h_shipping #+ tax_value
                h_dolar_total += h_dolar_shipping
                descripcion = descripcion + f"""
                    Costo de envio: {h_shipping}
                    total:  {h_total}
                """
                if pais_producto != "COLOMBIA":
                    descripcion += f"""
                        Costo de envio en Dolar: {h_dolar_shipping}
                        Dolar Total: {h_dolar_total}
                    """

                valor_a_pagar_centavos = int(h_total) * 100  # este pago debe ser en centavos de pesos, 100 pesos debe enviarse como 10000
                
                expiration_time = obtener_hora_colombia(delta_time+6) # el link de pago expira en 2 horas
                #Link_de_redireccion = "https://api.whatsapp.com/send?phone=15147125576&text=Hola%20DTB%20hice%20una%20compra%2C%20mi%20numero%20de%20pedido%20es%20("+id_Orden_de_Compra+")"
                Link_de_redireccion = f"https://ipuc-libros.my.canva.site/thanks-for-buy-elninoaquel"
                Link_de_img_logo = "https://saidc.pythonanywhere.com/static/images/hero_bg_1.jpg"
                
                private_key = os.environ.get("WOMPI_PRODUCTION_PRIVATE_KEY")if ESTADO_PROYECTO == "PROD" else os.environ.get("WOMPI_TEST_PRIVATE_KEY")
                wompi_url = os.environ.get("WOMPI_PRODUCTION_URL") if ESTADO_PROYECTO == "PROD" else os.environ.get("WOMPI_TEST_URL")
                response = generar_link_de_pago(wompi_url, private_key, nombre, descripcion, valor_a_pagar_centavos, expiration_time, Link_de_redireccion, Link_de_img_logo, id_Orden_de_Compra)
                
                if response is not None:
                    try:
                        response_data = json.loads(response)
                        if "data" in response_data:
                            data = response_data["data"]
                            #print("--> data: ", data)
                            payment_link_id = data["id"]
                            fecha_de_creacion = data["created_at"]
                            fecha_de_expiracion = data["expires_at"]
                            productos_a_comprar = json.dumps(productos_comprar)
                            #row = [str(payment_link_id), str(productos_a_comprar), str(fecha_de_creacion), str(fecha_de_expiracion),"INICIALIZO"]
                            row = nuevo_procesamiento_de_pedido(payment_link_id, productos_a_comprar, fecha_de_creacion, fecha_de_expiracion)

                            TOKEN_FILE = os.environ.get("SHEET_TOKEN_FILE")
                            CLIENT_SECRET = os.environ.get("SHEET_CLIENT_SECRET") 
                            SCOPES = convert_to_list( os.environ.get("SHEET_SCOPES") )
                            #SPREADSHEET_ID = os.environ.get("INIT_COMPRA_SPREADSHEET_ID") 
                            SPREADSHEET_ID = os.environ.get("SPREADSHEET_2_ID") 
                            #SHEET_NAME = os.environ.get("INIT_COMPRA_SHEET_NAME") 
                            SHEET_NAME = os.environ.get("SHEET_2_NAME") 
                            creds = get_token_credentials(TOKEN_FILE, CLIENT_SECRET, SCOPES)
                            service = connect_to_sheet_api(creds)
                            if(service):
                                rslt = append_row_value(service, SPREADSHEET_ID, SHEET_NAME, row)
                                print("intento de añadir fila de INIT_COMPRA: ", rslt , row)
                            else:
                                print("no se pudo añadir fila de INIT_COMPRA: ", row)

                            url = f"https://checkout.wompi.co/l/{payment_link_id}"
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
                return jsonify({"error": 3, "error-msg":"la cantidad maxima son 20 libros por compra"})
        else:
            return jsonify({"error": 1, "error-msg":"Parametros incorrectos o faltantes"})
        
@app.route('/purchase_confirmation')
def purchase_confirmation():
    print("argumentos: ", rq.args)
    if "libro" in rq.args:
        id_Orden_de_Compra = rq.args.get("id_Orden_de_Compra")   
        return render_template('purchase_confirmation.html', id_Orden_de_Compra=id_Orden_de_Compra)
    return render_template('purchase_confirmation.html', id_Orden_de_Compra=None)

@app.route('/load')
def get_load():
    # Obtener métricas de carga del sistema
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    return jsonify({
        'cpu_percent': cpu_percent,
        'memory_percent': memory_percent
    }), 200

@app.route('/count_down', methods=['POST'])
def count_down():
    TOKEN_FILE = os.environ.get("SHEET_TOKEN_FILE")
    CLIENT_SECRET = os.environ.get("SHEET_CLIENT_SECRET") 
    SCOPES = convert_to_list( os.environ.get("SHEET_SCOPES") )
    VALORES_SPREADSHEET_ID = os.environ.get("VALORES_SPREADSHEET_ID") 
    VALORES_SHEET_NAME = os.environ.get("VALORES_SHEET_NAME") 
    
    creds = get_token_credentials(TOKEN_FILE, CLIENT_SECRET, SCOPES)
    service = connect_to_sheet_api(creds)
    if(service):
       print("conexion exitosa")
       rows = get_rows(service ,VALORES_SPREADSHEET_ID , VALORES_SHEET_NAME)
       #print(rows)
       index = -1
       for i in range(len(rows)):
          row = rows[i]
          if(row[0]=="count_down"):
             index = i
             break
       if index > 0:
          days_of_count_down_text = rows[index][1]
          seconds_remaining =  calculate_seconds_remaining(days_of_count_down_text)
          print("Segundos restantes:", seconds_remaining, " minutos:", int(seconds_remaining/60), " horas", int((seconds_remaining/60)/60) , " dias: ", int(((seconds_remaining/60)/60))/24)
          return jsonify({
              'count_down': seconds_remaining
              }), 200
       else:
          print("no se encontro la variable count_down")
          return jsonify({
              'count_down': 267840
              }), 200
    else:
       print("conexion fallida")
       return jsonify({
           'count_down': 267840
           }), 200

if __name__ == "__main__":
  app.run(debug=True)


