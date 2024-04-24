## Configuración y Ejecución

Para ejecutar este proyecto en tu entorno local, sigue estos pasos:

1. Clona este repositorio en tu máquina:

    ```bash
    git clone https://github.com/tu_usuario/libreria-cristiana.git
    ```

2. Navega hasta el directorio del proyecto:

    ```bash
    cd libreria-cristiana
    ```

3. Crea y activa un entorno virtual para el proyecto:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4. Instala las dependencias del proyecto utilizando pip y el archivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

5. Agrega los archivos de configuración necesarios:
    - `.env`: Contiene las variables de entorno y la configuración necesaria para acceder a servicios externos como Google Sheets.
    - `credentials.json`: Las credenciales necesarias para acceder a la API de Google Cloud.
    - `token.json`: El token de autenticación generado para acceder a los servicios de Google Cloud.

6. Ejecuta el servidor Flask:

    ```bash
    flask run
    ```

¡Y listo! Ahora puedes acceder a la Librería Cristiana Online en tu navegador local en la dirección [http://localhost:5000](http://localhost:5000).

---

Para obtener más información sobre cómo contribuir al proyecto o resolver problemas, consulta nuestra [guía de contribución](link_a_tu_guia_de_contribucion.md).

![Imagen de más información](https://live.staticflickr.com/65535/53542553219_4414c9666a_o.png)
