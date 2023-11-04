from selenium import webdriver

def get_source_code_using_selenium(url):
    """
    Obtiene el código fuente HTML de una página web después de que se haya ejecutado el JavaScript.
        Parámetros:
            url: La dirección URL de la página web a la que se quiere acceder.
        Devuelve:
            html: El código fuente HTML de la página web después de la ejecución de JavaScript.
    """
    
    # Inicializamos el navegador Firefox en modo "headless" (sin interfaz gráfica de usuario)
    opciones = webdriver.FirefoxOptions()
    opciones.headless = True
    
    # Creamos una nueva instancia del navegador Firefox con las opciones definidas anteriormente
    navegador = webdriver.Firefox(options=opciones)
    
    # Navegamos a la dirección URL especificada
    navegador.get(url)
    
    # Obtenemos el código fuente HTML de la página, incluyendo cualquier cambio realizado por JavaScript
    html = navegador.page_source
    
    # Escribimos el código fuente HTML en un archivo de texto
    with open('./src/otras_funcionalidades/4sourceCodeAMAZON.txt', "w", encoding='utf-8') as archivo:
        archivo.write(html)
        
    # Cerramos la instancia del navegador para liberar recursos
    navegador.quit()
    
    # Devolvemos el código fuente HTML como una cadena de texto
    return html

# Ejecución
# La URL corresponde a una búsqueda de "auriculares inalámbricos" en la web de AMAZON
url = "https://www.amazon.es/s?k=auriculares+inalambricos&crid=2Z95CFUYNBBHX&sprefix=auriculares+inalam%2Caps%2C94&ref=nb_sb_ss_ts-doa-p_2_18"
htmlSource = get_source_code_using_selenium(url)
