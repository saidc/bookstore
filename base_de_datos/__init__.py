
from datetime import datetime, timedelta
from tools import asignar_valor, obtener_hora_colombiana,sumar_horas
import pytz

db_orders = {
 "SELECCION MANUAL":0,
 "PROCESO_COMPRA_ID":1,
 "PAYMENT_LINK_ID":2,
 "CREATED_AT":3,
 "FINALIZED_AT":4,
 "EXPIRED_AT":5,
 "STATUS":6,
 "TIPO DE VENTA":7,
 "TOTAL PAGADO":8,
 "PRECIO ESTABLECIDO DE ENVIO":9,
 "CURRENCY":10,
 "COSTO ADICIONAL":11,
 "DESCRIPCION DE COSTO ADICIONAL":12,
 "MEDIO DE PAGO":13,
 "COMPROBANTE DE PAGO":14,
 "DESCRIPCION DE PEDIDO":15,
 "CUSTOMER_EMAIL":16,
 "NAME":17,
 "CELULAR":18,
 "DIRECCION 1":19,
 "DIRECCION 2":20,
 "PAIS":21,
 "REGION":22,
 "CIUDAD":23,
 "CODIGO POSTAL":24,
 "NUMERO DE GUIA ENVIO":25,
 "EMPRESA DE ENVIO":26,
 "COSTO FINAL DE ENVIO":27
}

def obtener_informacion_producto(id):
    # Aquí deberías implementar la lógica para obtener la información del producto
    # Puedes obtener el ID, nombre y precio del producto desde una base de datos o cualquier otra fuente de datos.
    # Por ahora, simplemente retornaré una lista con diccionarios de ejemplo

    #BASE DE DATOS
    libros = [
        {
            'id':"elniñoaquel",
            'nombre':"El niño aquel",
            'precio': [
                {"pais":"COLOMBIA",       "precio":40000, "precio-anterior":45000, "moneda":"COP"},
                {"pais":"CANADA",         "precio":35,    "precio-anterior":45,    "moneda":"USD"},
                {"pais":"ESTADOS UNIDOS", "precio":35,    "precio-anterior":45,    "moneda":"USD"}
                ],
            'descripcion-corta': 'Descubre la fascinante odisea de ARMANDO JOSÉ CALDERÓN, un hombre cuya vida trasciende los límites de lo ordinario en "el niño aquel". Desde sus modestos comienzos en Maicao, LA GUAJIRA-COLOMBIA hasta su destacada labor ministerial en Bucaramanga, esta cautivadora autobiografía te sumergirá en un viaje emocional donde la fe y la determinación desafían todo pronóstico.',
            'descripcion': """
                Descubre la fascinante odisea de ARMANDO JOSÉ CALDERÓN, un hombre cuya vida trasciende los límites de lo ordinario en "el niño aquel". Desde sus modestos comienzos en Maicao, LA GUAJIRA-COLOMBIA hasta su destacada labor ministerial en Bucaramanga, esta cautivadora autobiografía te sumergirá en un viaje emocional donde la fe y la determinación desafían todo pronóstico.

                'EL NIÑO AQUEL' no es solo una autobiografía, sino un tributo a la fuerza espiritual que impulsó a Armando a dedicar su vida a la fe y al servicio a Dios y a su prójimo. Su historia inspiradora se convierte en un faro de esperanza, recordándonos que, con fe y perseverancia, podemos superar cualquier adversidad y dejar una huella perdurable en la comunidad.
            """,
            'imagenes': [
                {"image":"https://live.staticflickr.com/65535/53550559789_776de25b1c_o.png","miniatura":"https://live.staticflickr.com/65535/53544406384_fe6307a3f7_o.png"}, # foto_01.jpg
                {"image":"https://live.staticflickr.com/65535/53542553219_4414c9666a_o.png","miniatura":"https://live.staticflickr.com/65535/53544261148_f7999c1aa1_o.png"}, # foto_02.png
                {"image":"https://live.staticflickr.com/65535/53550679674_768fe6f88d_o.png","miniatura":"https://live.staticflickr.com/65535/53544513400_892722f6e3_o.png"}, # foto_03.png 
            ],
            'video': {
                "hasVideo": True,
                "href": "https://www.flickr.com/photos/200131147@N06/53543632894/in/dateposted-public/",
                "title": "Video del libro el niño aquel",
                "img-src": "https://live.staticflickr.com/31337/53543632894_4eb1eb834f_o.jpg",
                "miniatura":"https://live.staticflickr.com/65535/53543210447_33d62c1610_o.png", #elniдoaquel_miniatura_play
                "width": 540,
                "height": 540,  
            }	
        },
        {
            'id':"palabrasmemorables",
            'nombre':"Palabras Memorables",
            'precio': [
                {"pais":"COLOMBIA",       "precio":70000, "precio-anterior":80000, "moneda":"COP"},
                {"pais":"CANADA",         "precio":45,    "precio-anterior":55,    "moneda":"USD"},
                {"pais":"ESTADOS UNIDOS", "precio":45,    "precio-anterior":55,    "moneda":"USD"}
                ],
            'descripcion-corta': "Palabras memorables es la compilación de más de 150 enseñanzas que contienen una cantidad de temas doctrinales y de formación ministerial de nuestro visionero, Eliceo Duarte. Transcritas por el pastor Armando José Calderón, trabajo que hizo por muchas horas y años para lograr lo que hoy es palabras memorables.",
            'descripcion': """
                Palabras memorables es la compilación de más de 150 enseñanzas que contienen una cantidad de temas doctrinales y de formación ministerial de nuestro visionero, Eliceo Duarte. Transcritas por el pastor Armando José Calderón, trabajo que hizo por muchas horas y años para lograr lo que hoy es palabras memorables. 
                
                Leer palabras memorables es de mucha utilidad para el crecimiento cristiano, la instrucción, la edificación para aquellos que se dedican por entero a la enseñanza de las sagradas escrituras y también para los que quieran prepararse para servir al Señor en un futuro. El Evangelio es lo único que Jesús mandó predicar, creer y obedecer para ser salvos. Jesucristo no mandó predicar otra cosa.""",
            'imagenes': [
                {"image":"https://live.staticflickr.com/65535/53542410328_7392d8a4d0_o.jpg","miniatura":"https://live.staticflickr.com/65535/53544405924_41f8258860_o.jpg"}, # foto_01.jpg
                {"image":"https://live.staticflickr.com/65535/53542228811_0d3a009021_o.png","miniatura":"https://live.staticflickr.com/65535/53544512980_bdcf470254_o.png"}, # foto_02.png
                {"image":"https://live.staticflickr.com/65535/53542553074_f8c119ff75_o.png","miniatura":"https://live.staticflickr.com/65535/53544512990_7e8f7b2a12_o.png"}, # foto_03.png
            ],
            'video': {
                "hasVideo": True,
                "href": "https://www.flickr.com/photos/200131147@N06/53543633009/in/dateposted-public/",
                "title": "Video del libro palabras memorables",
                "img-src": "https://live.staticflickr.com/31337/53543633009_6b147d4317_o.jpg",
                "miniatura":"https://live.staticflickr.com/65535/53544083106_49c4dcb8ac_o.png", # palabrasmemorables_miniatura_play
                "width": 540,
                "height": 540,  
            }
            
        },
        {
            'id':"pequeñosinstrumentos",
            'nombre':"Pequeños Instrumentos",
            'precio': [
                {"pais":"COLOMBIA",       "precio":35000, "precio-anterior":45000,   "moneda":"COP"},
                {"pais":"CANADA",         "precio":35,    "precio-anterior":45,      "moneda":"USD"},
                {"pais":"ESTADOS UNIDOS", "precio":35,    "precio-anterior":45,      "moneda":"USD"}
                ],
            'descripcion-corta': "Se trata del relato de la vida de una misionera, de tiempo completo, que por más de cincuenta años se ha dedicado a predicar el evangelio y a enseñar a vivir en Cristo.  Si, es la vida de la hermana Isabel Torres, que ahora, retirada del trajín de la obra, decidió contarnos como fue ese trabajo en diversos países.",
            'descripcion': """
                Se trata del relato de la vida de una misionera, de tiempo completo, que por más de cincuenta años se ha dedicado a predicar el evangelio y a enseñar a vivir en Cristo.  Si, es la vida de la hermana Isabel Torres, que ahora, retirada del trajín de la obra, decidió contarnos como fue ese trabajo en diversos países.
                
                Comienza relatando su niñez y conversión, y nos lleva de la mano para explicarnos como fueron los comienzos de su trabajo en la cálida ciudad de Barranquilla, en la costa caribe de Colombia.
                
                De allí nos lleva por Suramérica, y nos cuenta de su labor en España, Canadá, Francia e inclusive su visita a Suiza.
            """,
            'imagenes': [
                {"image":"https://live.staticflickr.com/65535/53542657250_700ab17f7b_o.jpg","miniatura":"https://live.staticflickr.com/65535/53542657250_700ab17f7b_o.jpg"}, # foto_01.jpg
                {"image":"https://live.staticflickr.com/65535/53542410233_64fd16a91c_o.png","miniatura":"https://live.staticflickr.com/65535/53542410233_64fd16a91c_o.png"}, # foto_02.png
                {"image":"https://live.staticflickr.com/65535/53542657215_07452bf09e_o.png","miniatura":"https://live.staticflickr.com/65535/53542657215_07452bf09e_o.png"}, # foto_03.png                
            ],
            'video': {
                "hasVideo": True,
                "href": "https://www.flickr.com/photos/200131147@N06/53543764645/in/dateposted-public/",
                "title": "Video del libro pequeños instrumentos",
                "img-src": "https://live.staticflickr.com/31337/53543764645_6955ccc268_o.jpg",
                "miniatura":"https://live.staticflickr.com/65535/53543289562_72d5c3a301_o.png", #pequeдosinstrumentos_miniatura_play
                "width": 540,
                "height": 540,  
            }			
        }
    ]

    for book in libros:
        if book["id"] == id:
            return book
    else:
        return None

def nuevo_procesamiento_de_pedido(payment_link_id, productos_a_comprar, fecha_de_creacion, fecha_de_expiracion):
    global db_orders
    lista = []
    lista = asignar_valor(lista, 27, "")

    lista[db_orders["SELECCION MANUAL"]]                = "" 
    lista[db_orders["PROCESO_COMPRA_ID"]]               = "" 
    lista[db_orders["PAYMENT_LINK_ID"]]                 = str(payment_link_id) 
    lista[db_orders["CREATED_AT"]]                      = str(fecha_de_creacion) 
    lista[db_orders["FINALIZED_AT"]]                    = "" 
    lista[db_orders["EXPIRED_AT"]]                      = str(fecha_de_expiracion) 
    lista[db_orders["STATUS"]]                          = "ESPERANDO" 
    lista[db_orders["TIPO DE VENTA"]]                   = "VENTAS WEB" 
    lista[db_orders["TOTAL PAGADO"]]                    = "" 
    lista[db_orders["PRECIO ESTABLECIDO DE ENVIO"]]     = "" 
    lista[db_orders["CURRENCY"]]                        = "" 
    lista[db_orders["COSTO ADICIONAL"]]                 = "" 
    lista[db_orders["DESCRIPCION DE COSTO ADICIONAL"]]  = "" 
    lista[db_orders["MEDIO DE PAGO"]]                   = "" 
    lista[db_orders["COMPROBANTE DE PAGO"]]             = "" 
    lista[db_orders["DESCRIPCION DE PEDIDO"]]           = str(productos_a_comprar) 
    lista[db_orders["CUSTOMER_EMAIL"]]                  = "" 
    lista[db_orders["NAME"]]                            = "" 
    lista[db_orders["CELULAR"]]                         = "" 
    lista[db_orders["DIRECCION 1"]]                     = "" 
    lista[db_orders["DIRECCION 2"]]                     = "" 
    lista[db_orders["PAIS"]]                            = "" 
    lista[db_orders["REGION"]]                          = "" 
    lista[db_orders["CIUDAD"]]                          = "" 
    lista[db_orders["CODIGO POSTAL"]]                   = "" 
    lista[db_orders["NUMERO DE GUIA ENVIO"]]            = "" 
    lista[db_orders["EMPRESA DE ENVIO"]]                = "" 
    lista[db_orders["COSTO FINAL DE ENVIO"]]            = "" 
    
    return lista
     

def obtener_pedido_by_payment_link_id(rows, payment_link_id):
    global db_orders
    
    # Obtener la hora actual Colombia
    hora_actual_colombiana = obtener_hora_colombiana()
    # se le suman 5 Horas a la hora colombiana 
    hora_actual = hora_actual_colombiana + timedelta(hours=5)
    # se resta 2 horas para obtener 2 horas antes de la zona horaria del servidor de wompi
    hora_hace_dos_horas = hora_actual - timedelta(hours=2)
    # # defino la zona horaria de colombia
    zona_horaria_colombiana = pytz.timezone('America/Bogota')

    #print("hora actual: ", hora_actual.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    
    # Lista para almacenar elementos que cumplen con las condiciones
    elementos_cumplen_condicion = []
    
    # Iterar sobre la lista de listas, quitando el encabezado
    for i in range(1, len(rows)):
        row = rows[i]
        # se obtiene la columna de fecha de creacion de la orden 
        CREATED_AT = row[db_orders["CREATED_AT"]]

        fecha_creacion = datetime.strptime(CREATED_AT, "%Y-%m-%dT%H:%M:%S.%fZ")
        #fecha_creacion = fecha_creacion.astimezone(zona_horaria_colombiana)
        fecha_creacion = fecha_creacion.replace(tzinfo=zona_horaria_colombiana)

        # Verificar si la fecha de creación está dentro del rango de 2 horas
        if fecha_creacion >= hora_hace_dos_horas:
            elementos_cumplen_condicion.append([i,row])
    
    #print("elementos_cumplen_condicion: ", elementos_cumplen_condicion)

    # Buscar el elemento con el id_link especificado
    for elemento in elementos_cumplen_condicion:
        # se obtine la columba de id de link de pago
        PAYMENT_LINK_ID = elemento[1][db_orders["PAYMENT_LINK_ID"]]
        if PAYMENT_LINK_ID == payment_link_id:
            return elemento[0], elemento[1]

    # Si no se encuentra ningún elemento con el id_link especificado
    return -1, None

def update_row_by_webhook_respond(row, webhook_res):
    row = asignar_valor(row, 27, "")
    row[db_orders["PROCESO_COMPRA_ID"]] = str(webhook_res[0])  #0  proceso_compra_id  
    row[db_orders["PAYMENT_LINK_ID"]]   = str(webhook_res[17]) #17 payment_link_id
    row[db_orders["CREATED_AT"]]        = str(webhook_res[1])  #1  created_at  
    row[db_orders["FINALIZED_AT"]]      = str(webhook_res[2])  #2  finalized_at
    row[db_orders["STATUS"]]            = str(webhook_res[7])  #7  status    
    row[db_orders["TOTAL PAGADO"]]      = str(webhook_res[3])  #3  amount_in_cents
    row[db_orders["CURRENCY"]]          = str(webhook_res[5])  #5  currency    
    row[db_orders["MEDIO DE PAGO"]]     = str(webhook_res[6])  #6  payment_method_type         
    row[db_orders["CUSTOMER_EMAIL"]]    = str(webhook_res[4])  #4  customer_email           
    row[db_orders["NAME"]]              = str(webhook_res[13]) #13 name
    row[db_orders["CELULAR"]]           = str(webhook_res[14]) #14 phone_number   
    row[db_orders["DIRECCION 1"]]       = str(webhook_res[8])  #8  address_line_1       
    row[db_orders["DIRECCION 2"]]       = str(webhook_res[9])  #9  address_line_2       
    row[db_orders["PAIS"]]              = str(webhook_res[10]) #10 country
    row[db_orders["REGION"]]            = str(webhook_res[11]) #11 region  
    row[db_orders["CIUDAD"]]            = str(webhook_res[12]) #12 city  
    row[db_orders["CODIGO POSTAL"]]     = str(webhook_res[15]) #15 postal_code         
    return row
