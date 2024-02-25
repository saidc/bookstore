
from urllib import request as urllib_rq
from urllib.error import HTTPError
import hashlib
import json

def generar_link_de_pago(base_url, private_key, nombre, descripcion, valor_cliente_a_pagar, expiration_time, Link_de_redireccion, Link_de_img_logo, id_Orden_de_Compra):
  # "https://production.wompi.co/v1" # version de produccion
  # "https://sandbox.wompi.co/v1" # Usar la URL de Sandbox para version de prueba
  
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
  
def verify_event(wompi_secret, request_data):
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

def get_webhook_param( transaction_data ):
  shipping_address = extract_shipping_address(transaction_data["shipping_address"] if "shipping_address" in transaction_data["shipping_address"] else None)
  
  proceso_compra_id     = transaction_data["id"]                  if "id" in shipping_address else None
  created_at            = transaction_data["created_at"]          if "created_at" in shipping_address else None
  finalized_at          = transaction_data["finalized_at"]        if "finalized_at" in shipping_address else None
  amount_in_cents       = transaction_data["amount_in_cents"]     if "amount_in_cents" in shipping_address else None
  customer_email        = transaction_data["customer_email"]      if "customer_email" in shipping_address else None
  currency              = transaction_data["currency"]            if "currency" in shipping_address else None
  payment_method_type   = transaction_data["payment_method_type"] if "payment_method_type" in shipping_address else None
  status                = transaction_data["status"]              if "status" in shipping_address else None
  address_line_1        = shipping_address["address_line_1"]      if "address_line_1" in shipping_address else None
  address_line_2        = shipping_address["address_line_2"]      if "address_line_2" in shipping_address else None
  country               = shipping_address["country"]             if "country" in shipping_address else None
  region                = shipping_address["region"]              if "region" in shipping_address else None
  city                  = shipping_address["city"]                if "city" in shipping_address else None
  name                  = shipping_address["name"]                if "name" in shipping_address else None
  phone_number          = shipping_address["phone_number"]        if "phone_number" in shipping_address else None
  postal_code           = shipping_address["postal_code"]         if "postal_code" in shipping_address else None
  redirect_url          = transaction_data["redirect_url"]        if "redirect_url" in shipping_address else None
  payment_link_id       = transaction_data["payment_link_id"]     if "payment_link_id" in shipping_address else None
  
  return {
    str( proceso_compra_id ) , # "proceso_compra_id"
    str( created_at ) , # "created_at"
    str( finalized_at ) , # "finalized_at"
    str( amount_in_cents ) , # "amount_in_cents"
    str( customer_email ) , # "customer_email"
    str( currency ) , # "currency"
    str( payment_method_type ) , # "payment_method_type"
    str( status ) , # "status"
    str( address_line_1 ) , # "address_line_1"
    str( address_line_2 ) , # "address_line_2"
    str( country ) , # "country"
    str( region ) , # "region"
    str( city ) , # "city"
    str( name ) , # "name"
    str( phone_number ) , # "phone_number"
    str( postal_code ) , # "postal_code"
    str( redirect_url ) , # "redirect_url"
    str( payment_link_id ) , # "payment_link_id"
  }

def extract_shipping_address(shipping_address):
  if shipping_address != None:
    address_line_1 = shipping_address["address_line_1"] if "address_line_1" in shipping_address else None
    address_line_2 = shipping_address["address_line_2"] if "address_line_2" in shipping_address else None
    country = shipping_address["country"] if "country" in shipping_address else None
    region = shipping_address["region"] if "region" in shipping_address else None
    city = shipping_address["city"] if "city" in shipping_address else None
    name = shipping_address["name"] if "name" in shipping_address else None
    phone_number = shipping_address["phone_number"] if "phone_number" in shipping_address else None
    postal_code = shipping_address["postal_code"] if "postal_code" in shipping_address else None

    return {
      "address_line_1": address_line_1 ,
      "address_line_2": address_line_2 ,
      "country": country ,
      "region": region ,
      "city": city ,
      "name": name ,
      "phone_number": phone_number ,
      "postal_code": postal_code ,
    }
  return {}

  
