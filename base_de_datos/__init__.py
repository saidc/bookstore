
from datetime import datetime, timedelta
from tools import asignar_valor

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
    #       0   1   2                     3                       4   5                         6            7             8   9   10  11  12  13  14  15                       16 17 18 19 20 21 22 23 24 25 26 27      
    return ["", "", str(payment_link_id), str(fecha_de_creacion), "", str(fecha_de_expiracion), "ESPERANDO", "VENTAS WEB", "", "", "", "", "", "", "", str(productos_a_comprar),"","","","","","","","","","","","" ]
     
    #0  SELECCION MANUAL
    #1  PROCESO_COMPRA_ID
    #2  PAYMENT_LINK_ID
    #3  CREATED_AT
    #4  FINALIZED_AT
    #5  EXPIRED_AT
    #6  STATUS
    #7  TIPO DE VENTA
    #8  TOTAL PAGADO
    #9  PRECIO ESTABLECIDO DE ENVIO
    #10 CURRENCY

    #11 COSTO ADICIONAL
    #12 DESCRIPCION DE COSTO ADICIONAL

    #13 MEDIO DE PAGO
    #14 COMPROBANTE DE PAGO
    #15 DESCRIPCION DE PEDIDO
    #16 CUSTOMER_EMAIL

    #17 NAME
    #18 CELULAR
    #19 DIRECCION 1
    #20 DIRECCION 2
    #21 PAIS

    #22 REGION
    #23 CIUDAD
    #24 CODIGO POSTAL
    #25 NUMERO DE GUIA ENVIO
    #26 EMPRESA DE ENVIO
    #27 COSTO FINAL DE ENVIO

def obtener_pedido_by_payment_link_id(rows, payment_link_id):
     # Obtener la hora actual
    hora_actual = datetime.now()

    # Calcular la hora hace 2 horas
    hora_hace_dos_horas = hora_actual - timedelta(hours=2)

    # Lista para almacenar elementos que cumplen con las condiciones
    elementos_cumplen_condicion = []

     # Iterar sobre la lista de listas, quitando el encabezado
    for i in range(1, len(rows)):
        elemento = rows[i]
        fecha_creacion = datetime.strptime(elemento[3], "%Y-%m-%dT%H:%M:%S.%fZ")
        # Verificar si la fecha de creación está dentro del rango de 2 horas
        if fecha_creacion >= hora_hace_dos_horas and fecha_creacion <= hora_actual:
            elementos_cumplen_condicion.append([i,elemento])
    
    #print("elementos_cumplen_condicion: ", elementos_cumplen_condicion)

    # Buscar el elemento con el id_link especificado
    for elemento in elementos_cumplen_condicion:
        if elemento[1][2] == payment_link_id:
            return elemento[0], elemento[1]

    # Si no se encuentra ningún elemento con el id_link especificado
    return -1, None

def update_row_by_webhook_respond(row, webhook_res):
    row = asignar_valor(row, 28, "")
    row[1] = webhook_res[0]    #1
    row[2] = webhook_res[17]   #2
    row[3] = webhook_res[1]    #3
    row[4] = webhook_res[2]    #4
    row[6] = webhook_res[7]    #6
    row[8] = webhook_res[3]    #8
    row[10] = webhook_res[5]   #10
    row[13] = webhook_res[6]   #13
    row[16] = webhook_res[4]   #16
    row[17] = webhook_res[13]  #17
    row[18] = webhook_res[14]  #18
    row[19] = webhook_res[8]   #19
    row[20] = webhook_res[9]   #20
    row[21] = webhook_res[10]  #21
    row[22] = webhook_res[11]  #22
    row[23] = webhook_res[12]  #23
    row[24] = webhook_res[15]  #24
    return row

    #   ROW                                     WEBHOOK_RES
    #0  SELECCION MANUAL                    
    #1  PROCESO_COMPRA_ID                   #0  proceso_compra_id  
    #2  PAYMENT_LINK_ID                     #17 payment_link_id
    #3  CREATED_AT                          #1  created_at  
    #4  FINALIZED_AT                        #2  finalized_at
    #5  EXPIRED_AT                              
    #6  STATUS                              #7  status    
    #7  TIPO DE VENTA                                
    #8  TOTAL PAGADO                        #3  amount_in_cents
    #9  PRECIO ESTABLECIDO DE ENVIO                
    #10 CURRENCY                            #5  currency    

    #11 COSTO ADICIONAL                                
    #12 DESCRIPCION DE COSTO ADICIONAL                

    #13 MEDIO DE PAGO                       #6  payment_method_type         
    #14 COMPROBANTE DE PAGO                 
    #15 DESCRIPCION DE PEDIDO                
    #16 CUSTOMER_EMAIL                      #4  customer_email           

    #17 NAME                                #13 name
    #18 CELULAR                             #14 phone_number   
    #19 DIRECCION 1                         #8  address_line_1       
    #20 DIRECCION 2                         #9  address_line_2       
    #21 PAIS                                #10 country

    #22 REGION                              #11 region  
    #23 CIUDAD                              #12 city  
    #24 CODIGO POSTAL                       #15 postal_code         
    #25 NUMERO DE GUIA ENVIO                
    #26 EMPRESA DE ENVIO                
    #27 COSTO FINAL DE ENVIO                