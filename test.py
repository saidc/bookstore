from base_de_datos import obtener_informacion_producto, nuevo_procesamiento_de_pedido, obtener_pedido_by_payment_link_id, update_row_by_webhook_respond
from sheet import get_token_credentials, get_rows, connect_to_sheet_api, append_row_value, send_email, batch_update_row_value
import  time
import os 
from tools import getenv_var, convert_to_list, obtener_hora_colombiana, sumar_horas
from datetime import datetime, timedelta
import pytz
from pytz import timezone 

env_file_path = ".env"
# obtener variables de entorno
getenv_var(env_file_path=env_file_path)

TOKEN_FILE = os.environ.get("SHEET_TOKEN_FILE")
CLIENT_SECRET = os.environ.get("SHEET_CLIENT_SECRET") 
SCOPES = convert_to_list( os.environ.get("SHEET_SCOPES") )
SPREADSHEET_ID = os.environ.get("SPREADSHEET_2_ID") 
SHEET_NAME = os.environ.get("SHEET_2_NAME") 
creds = get_token_credentials(TOKEN_FILE, CLIENT_SECRET, SCOPES)
service = connect_to_sheet_api(creds)


fecha_creacion_str = "2024-04-21T00:06:20.258Z"
fecha_creacion =  datetime.strptime(fecha_creacion_str, "%Y-%m-%dT%H:%M:%S.%fZ")
zona_horaria_colombiana = pytz.timezone('America/Bogota')
fecha_creacion = fecha_creacion.replace(tzinfo=zona_horaria_colombiana)

hora_actual_colombiana = obtener_hora_colombiana()
hora_actual_colombiana_mas_5 = hora_actual_colombiana + timedelta(hours=5)
hace_2_horas = hora_actual_colombiana_mas_5 - timedelta(hours=2)

print(zona_horaria_colombiana)
print("fecha de crearcion de pedido: ",fecha_creacion.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
# Obtener la fecha y hora actual colombia
print("fecha actual colombia: ",hora_actual_colombiana.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
print("fecha actual colombia + 5: ",hora_actual_colombiana_mas_5.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

print("\nfecha actual colombia + 5 - 2: ",hace_2_horas.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))


if( fecha_creacion >= hace_2_horas ):
    print("la fecha es mayor de hace dos horas")
else:
    print("la fecha es menor de hace dos horas")



payment_link_id = "test_q9C8aV"
#fecha_de_creacion = fecha_actual.strftime("%Y-%m-%dT%H:%M:%S.%fZ") #"2024-02-28T15:59:35.744Z" 
#print("Fecha Actual: ", fecha_de_creacion)
#print("Fecha Actual colombia: ", hora_actual_colombiana.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
#nueva_hora = sumar_horas(hora_actual_colombiana, 5)
#print("Fecha Actual colombia + 5 horas: ", nueva_hora.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

# Calcular la hora en 2 horas como fecha de expiracion 
#fecha_de_expiracion = (fecha_actual + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S.%fZ") #"2024-02-28T17:59:35.450Z"
status = "ESPERANDO"
tipo_de_venta = "VENTAS WEB"
productos_a_comprar = '[{"id": "elni\u00f1oaquel", "name": "El ni\u00f1o aquel", "image": "https://live.staticflickr.com/65535/53550559789_776de25b1c_o.png", "price": 30000, "amount": 1, "subtotal": 30000, "price_dolar": -1, "dolar_subtotal": -1}]' 



# Ejemplo de uso
#fila = 3
#ancho = 10
#rango = calcular_rango(fila, ancho)
#print("El rango es:", rango)

#test_products = [
#    #0   1   2                     3                       4   5                         6            7                   8   9   10  11  12  13  14  15                       16 17 18 19 20 21 22 23 24 25 26 27         
#    ["", "", str(payment_link_id), str(fecha_de_creacion), "", str(fecha_de_expiracion), str(status), str(tipo_de_venta), "", "", "", "", "", "", "", str(productos_a_comprar),"","","","","","","","","","","","" ]
#]
#for i in test_products:
#    payment_link_id = i[2]
#    fecha_de_creacion= i[3] 
#    fecha_de_expiracion= i[5]
#    productos_a_comprar = i[13]    
#    row = nuevo_procesamiento_de_pedido(payment_link_id, productos_a_comprar, fecha_de_creacion, fecha_de_expiracion)
#    rslt = append_row_value(service, SPREADSHEET_ID, SHEET_NAME, row)
#time.sleep(5)
#add_row = ['', '', 'test_wodeTj', '2024-04-19T22:10:51.495Z', '', '2024-04-20T01:10:51.195Z', 'ESPERANDO', 'VENTAS WEB', '', '', '', '', '', '', '', '[{"id": "elni\\u00f1oaquel", "name": "El ni\\u00f1o aquel", "image": "https://live.staticflickr.com/65535/53550559789_776de25b1c_o.png", "price": 40000, "amount": 1, "subtotal": 40000, "price_dolar": -1, "dolar_subtotal": -1}]', '', '', '', '', '', '', '', '', '', '', '', '']
#updaterowbaywebhookrespond = ['139086-1713564676-32081', '2024-04-19T22:11:16.648Z', '2024-04-19T22:11:17.627Z', '5000000', 'saidjoc@gmail.com', 'COP', 'PSE', 'APPROVED', 'carrera 11#20-57', 'Casa', 'CO', 'Cesar', 'Valledupar', 'SAID JOSÉ CORTÉS CALDERÓN', '+573106016968', '200001', 'https://ipuc-libros.my.canva.site/thanks-for-buy-elninoaquel', 'test_wodeTj']

#webhook_res = ['139086-1713564676-32081', '2024-04-19T22:11:16.648Z', '2024-04-19T22:11:17.627Z', '5000000', 'saidjoc@gmail.com', 'COP', 'PSE', 'APPROVED', 'carrera 11#20-57', 'Casa', 'CO', 'Cesar', 'Valledupar', 'SAID JOSÉ CORTÉS CALDERÓN', '+573106016968', '200001', 'https://ipuc-libros.my.canva.site/thanks-for-buy-elninoaquel', 'test_p81hD8']
#rows = get_rows(service, SPREADSHEET_ID, SHEET_NAME)
#pos, row =  obtener_pedido_by_payment_link_id(rows, payment_link_id)
#row = update_row_by_webhook_respond(row, webhook_res)
#print("final row ", row)
#rslt = batch_update_row_value(service, SPREADSHEET_ID, SHEET_NAME, row_to_update=pos, value=row)

#rows = get_rows(service, SPREADSHEET_ID, SHEET_NAME)
##print(rows)
#pos, row = obtener_pedido_by_payment_link_id(rows, payment_link_id)
##     posicion,contenido
#print(pos, row)

#0  proceso_compra_id       #1  PROCESO_COMPRA_ID
#1  created_at              #3  CREATED_AT 
#2  finalized_at            #4  FINALIZED_AT
#3  amount_in_cents         #8  TOTAL PAGADO 
#4  customer_email          #16 CUSTOMER_EMAIL 
#5  currency                #10 CURRENCY 
#6  payment_method_type     #13 MEDIO DE PAGO
#7  status                  #6  STATUS 
#8  address_line_1          #19 DIRECCION 1
#9  address_line_2          #20 DIRECCION 2
#10 country                 #21 PAIS
#11 region                  #22 REGION
#12 city                    #23 CIUDAD
#13 name                    #17 NAME
#14 phone_number            #18 CELULAR
#15 postal_code             #24 CODIGO POSTAL
#16 redirect_url            
#17 payment_link_id         #2  PAYMENT_LINK_ID

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