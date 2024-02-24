
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

