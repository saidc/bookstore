from flask import Flask, render_template,request, redirect

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

#FUNCIONES
def obtener_informacion_producto(id):
    # Aquí deberías implementar la lógica para obtener la información del producto
    # Puedes obtener el ID, nombre y precio del producto desde una base de datos o cualquier otra fuente de datos.
    # Por ahora, simplemente retornaré una lista con diccionarios de ejemplo.
    for book in libros:
        if book["id"] == id:
            return book
    else:
        return None

#SERVIDOR FLASK

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/product-review', methods=['GET','POST'])
def product():
    if request.method == 'GET':
        if "libro" in request.args:
            libro = request.args.get("libro")
            libro = obtener_informacion_producto(libro)
            if libro != None:
                print(request.form, libro)
                return render_template('product-review.html', libro=libro)
            else:
                return redirect('/')

    elif request.method == 'POST' :
        if "libro" in request.form:
            libro = request.form["libro"]
            libro = obtener_informacion_producto(libro)
            print("libro", libro)

    return redirect('/')


