from flask import Flask,  render_template, redirect
from urllib import request

app = Flask(__name__)

# Lista de servidores backend y sus cargas máximas permitidas
backend_servers = [
    {'url': 'https://server05.alwaysdata.net', 'max_load': 80},
    {'url': 'https://server06.alwaysdata.net', 'max_load': 80},
    {'url': 'https://server07.alwaysdata.net', 'max_load': 80},
    {'url': 'https://server08.alwaysdata.net', 'max_load': 80}
    # Agrega más servidores según sea necesario
]

def get_load(url):
  # Obtener métricas de carga del sistema desde el servidor backend
  response = request.urlopen(f"{url}/load")
  load_data = response.read().decode('utf-8')
  return eval(load_data)

@app.route('/')
def load_balancer():
  for server in backend_servers:
    load_data = get_load(server['url'])
    if load_data['cpu_percent'] < server['max_load'] and load_data['memory_percent'] < server['max_load'] :
      return redirect(server['url'])

  # Si todos los servidores están ocupados, puedes redirigir a un servidor predeterminado o mostrar un mensaje de error.
  return "Todos los servidores están ocupados. Inténtalo de nuevo más tarde."


if __name__ == "__main__":
  app.run(debug=True)

