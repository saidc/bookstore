

def obtener_informacion_producto(id):
    # Aquí deberías implementar la lógica para obtener la información del producto
    # Puedes obtener el ID, nombre y precio del producto desde una base de datos o cualquier otra fuente de datos.
    # Por ahora, simplemente retornaré una lista con diccionarios de ejemplo

    #BASE DE DATOS
    libros = [
        {
            'id':"elniñoaquel",
            'nombre':"El niño aquel",
            'precio': 30000,
            'precio-anterior':40000,
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
            'precio': 60000,
            'precio-anterior':70000,
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
            'precio': 30000,
            'precio-anterior':40000,
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
