import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time, csv, os
from lxml import etree
from dtos import ClasePeliculaDTO





###########################################################################################################################
##################################### FUNCIÓN CON EL FLUJO GENERAL DEL PROGRAMA ###########################################
###########################################################################################################################

def execute_program():
    """
    Función de entrada al programa, donde se encuentra el flujo general del programa y las llamadas a las funcionalidades.
    
    Args:
        None.
    Return:
        None.
    """
    
    # Capturo instante temporal inicial (t0)
    t0 = time.perf_counter_ns()

    # Se inicializa objeto DTO de "ClasePeliculaDTO"
    url = "https://www.filmaffinity.com/es/topgen.php?genres=&chv=0&orderby=avg&movietype=movie%7C&country=&fromyear=2013&toyear=2023&ratingcount=3&runtimemin=0&runtimemax=4"
    obj_detalles_peliculas = ClasePeliculaDTO("",[],[],[],[],[],[],[],[],[],[],[],[])

    # Abrimos navegador Firefox en modo headless
    print("Abriendo el navegador Firefox en modo 'headless'...")
    options = Options()
    # Modificamos el user-agent para evitar detección
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)

    # Comprobamos que el user-agent se ha cambiado correctamente
    user_agent = browser.execute_script("return navigator.userAgent;")
    print("El 'User-Agent' es:", user_agent)

    # Accedemos a la página de FilmAffinity con un resumen de las mejores películas de los años 2013–2023
    print("Accediendo a la página de FilmAffinity...")
    browser.get(url)
    time.sleep(5)

    # Busca el botón «ACEPTO» y lo clica automáticamente
    print("Clicando en el botón 'ACEPTO'...")
    button = browser.find_element(By.CLASS_NAME, "css-v43ltw")
    button.click()
    time.sleep(3)

    # Realizar 33 veces scroll hasta conseguir 1020 películas generadas dinámicamente.
    # Luego guardar HTML de todo la página con las 1020 películas.
    html = return_html_after_scraping_movie_info_from_summary_page(browser, 33)
    obj_detalles_peliculas.set_html(html)

    # Tomo instante de tiempo (t1) después del raspado de la página de resumen (con las 1020 películas)
    t1 = time.perf_counter_ns()
    tiempo_raspando_inicial = (t1 - t0) / 10**9

    # Recopilamos los datos de interés del HTML de la página de resumen (con las 1020 películas).
    # Datos recogidos se almacenan en objeto DTO "ClasePeliculaDTO"
    obj_detalles_peliculas = scrape_data_from_summary_page(obj_detalles_peliculas)

    # Ahora recopilamos datos específicos de cada película.
    t2 = time.perf_counter_ns()

    # Dos parámetros de entra: 
    #                   1) el DTO con los enlaces de las 1020 películas
    #                   2) el nº de películas máximas que se quieren escribir en el dataset
    obj_detalles_peliculas = scrape_movie_details(obj_detalles_peliculas, 1000)
    t3 = time.perf_counter_ns()
    tiempo_raspando_datos_especificos_de_cada_pelicula = (t3 - t2) / 10**9
    

    # Creación del DATASET
    write_data_in_csv(obj_detalles_peliculas)

    # Se toma instante de tiempo t3 y se calcula el tiempo que cuesta escribir el dataset el fichero TXT
    t4 = time.perf_counter_ns()
    tiempo_escribiendo_csv = (t4 - t3) / 10**9
    print("-----------------------------------------------")
    print("Informe de tiempos:")
    print("Tiempo raspando datos de la página de resumen: {} segundos".format(tiempo_raspando_inicial))
    print("Tiempo raspando datos específicos de cada película: {} segundos".format(tiempo_raspando_datos_especificos_de_cada_pelicula))
    print("Tiempo escribiendo todos los datos raspados en fichero CSV: {} segundos".format(tiempo_escribiendo_csv))

####################################################### FIN PROGRAMA ####################################################












###########################################################################################################################
########################## FUNCIONES Y LIBRERÍAS PROPIAS PARA FUNCIONALIDAD ESPECÍFICA ####################################
###########################################################################################################################

#################### SE CONSIGUE HTML DE LA PÁGINA DE RESUMEN TRAS GENERAR LOS 1020 LINK DE PELÍCULAS #################

def return_html_after_scraping_movie_info_from_summary_page(browser, num_clics):
    """
    Función que obtiene el código fuente HTML tras la ejecución de JavaScript de la página de resumen.
    
    Args:
        browser:    Con los datos de la conexión HTTP establecida y la web cargada.
        num_clics:  El número de veces para hacer clic en la flecha para cargar más películas.
                    Por defecto, se diseña para que haga clic 33 veces y así cargar 1020 películas.
    Return:
        html: El código fuente HTML como una cadena de texto.
    """
    
    # Bucle para hacer 33 veces scroll hacia abajo y click en la flecha que con javascript sigue mostrando más películas
    for i in range(num_clics):
        print("Realizando scroll hacia abajo y clicando en la flecha para mostrar más películas {}/{}...".format(i+1, num_clics))

        # Esperamos para evitar sobrecargar el servidor
        time.sleep(3)

        # Hacemos clic en la flecha para cargar más películas
        button = browser.find_element(By.ID, "load-more-bt")
        browser.execute_script("arguments[0].scrollIntoView(true);", button)
        browser.execute_script("arguments[0].click();", button)
    
    # Esperamos para que las últimas 30 películas carguen
    time.sleep(3)
    
    # Obtenemos todo el código fuente (HTML) de la Summary Page (con las 1020 películas ya generadas)
    print("Generando HTML del código fuente de la página de resumen y almacenándolo en una variable...")
    html = browser.page_source

    # Cerramos el navegador para liberar recursos
    browser.quit()
    return html

















############## SE RASPAN EN EL DTO LOS DATOS GENERALES DE CADA PELÍCULA ###########################

def scrape_data_from_summary_page(obj_pelicula):
    """
    A partir del HTML, extraído de la página de resumen, se localizan los datos de interés.
    
    Args:
        Objeto tipo "ClasePeliculaDTO": Objeto entrada como DTO para rellenar las propiedades de los datos recopilados.
    Return:
        Objeto tipo "ClasePeliculaDTO": Devolución del objeto entrante con los valores nuevos guardados.
    """
    
    print("Raspando datos de la página de resumen...")
   
    # Creamos listas para guardar los valores de cada variable
    movie_titles = []
    movie_years = []
    movie_countries = []
    movie_ratings = []
    movie_rating_counts = []
    movie_directors = []
    movie_cast = []
    movie_links = []
    
    # Analizamos el HTML con lxml
    root = etree.HTML(str(obj_pelicula.get_html()))
    
    # Recopilo datos: recorro todos los div's con la clase "mc-info-container"
    for div in root.xpath('//div[@class="mc-info-container"]'):
        title_div = div.xpath('.//div[@class="mc-title"]')[0]
        full_text = title_div.xpath('string(.)').strip()
        
        # Obtenemos el título y el año
        title, year = full_text.rsplit('(', 1)
        year = year.rstrip(')')
        title = title.strip()
        
        # Obtenemos el país de origen
        country = title_div.xpath('.//img[@class="nflag"]/@alt')[0]
        
        # Obtenemos el director y el reparto
        director = div.xpath('.//div[@class="mc-director"]/div[@class="credits"]/span/a/text()')
        cast = div.xpath('.//div[@class="mc-cast"]/div[@class="credits"]/span/a/text()')
        
        # Obtenemos el enlace de la película
        link = div.xpath('.//div[@class="mc-title"]/a/@href')[0]
        
        movie_titles.append(title)
        movie_years.append(year)
        movie_countries.append(country)
        movie_directors.append(", ".join(director))
        movie_cast.append(", ".join(cast))
        movie_links.append(link)
    
    # Recopilo datos: recorro todos los li's con la clase "data"
    for li in root.xpath('//li[@class="data"]'):
        # Extraemos la puntuación media y el número de puntuaciones
        rating = li.xpath('.//div[@class="avg-rating"]/text()')[0]
        rating_count = li.xpath('.//div[@class="rat-count"]/text()')[0].strip()
        movie_ratings.append(rating)
        movie_rating_counts.append(rating_count)
    
    # Paso los datos recopilados al objeto de retorno
    obj_pelicula.set_movie_titles(movie_titles)
    obj_pelicula.set_movie_years(movie_years)
    obj_pelicula.set_movie_countries(movie_countries)
    obj_pelicula.set_movie_ratings(movie_ratings)
    obj_pelicula.set_movie_rating_counts(movie_rating_counts)
    obj_pelicula.set_movie_directors(movie_directors)
    obj_pelicula.set_movie_cast(movie_cast)
    obj_pelicula.set_movie_links(movie_links)
    return obj_pelicula






############## SE RASPAN EN EL DTO LOS DATOS ESPECÍFICOS DE CADA PELÍCULA ###########################

def scrape_movie_details(obj_pelicula, tuplas_de_datos_maximas):
    """
    Esta función se encarga de extraer detalles específicos de películas a partir de una lista de URLs previamente conseguida de la página de resumen.
    Gracias a las URL conseguidas, podemos acceder al interior de cada película de la página de resumen.
    Los datos concretos del interior de cada película son: título original, duración, género y sinopsis.
    
    Args:
        Objeto tipo "ClasePeliculaDTO": Objeto entrada como DTO con los enlaces a las películas para raspar.
        tuplas_de_datos_maximas: Filas de datos que queremos escribir en el fichero CSV (en el caso de esta práctica serán 1000).
    Return:
        Objeto tipo "ClasePeliculaDTO": Devolución del objeto entrante con los valores nuevos guardados.
    """
    
    print("Raspando datos específicos...")

    # Accedemos al DTO y cargamos los enlaces a las páginas de las películas
    url_list = obj_pelicula.get_movie_links()

    # Ponemos un límite al número de páginas para raspar
    if len(url_list) > tuplas_de_datos_maximas:
        url_list = url_list[:tuplas_de_datos_maximas]
    
    # Inicializamos listas vacías donde almacenaremos la información extraída
    movie_original_titles       = []
    movie_durations             = []
    movie_genres                = []
    movie_synopses              = []
    
    # Iteramos a través de cada URL en la lista
    for i, url in enumerate(url_list):
        print("Extrayendo información de la película {}/{}...".format(i+1, len(url_list)))
        
        # Gestión de errores general cuando falla la conexión web
        try:
            # Modificamos el user-agent para evitar detección
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

            # Hacemos una petición GET para obtener el contenido de la página
            response = requests.get(url, headers=headers)
            html_content = response.text
            
            # Utilizamos lxml para analizar el contenido HTML
            root = etree.HTML(html_content)
            
            # Utilizamos xpath para extraer estas 4 columnas: título_original, duración, género y sinopsis
            # Incluimos CONTROL DE ERRORES, para rellenar con "" si hay un error
            try:
                original_title = root.xpath('.//dt[text()="Título original"]/following-sibling::dd[1]/text()')[0].strip()
            except Exception as e_original:
                original_title = ""
            try:
                duration = root.xpath('.//dt[text()="Duración"]/following-sibling::dd[1]/text()')[0].split()[0].strip()
            except Exception as e_duration:
                duration = ""
            try:
                genre = root.xpath('.//dt[text()="Género"]/following-sibling::dd[1]//span[@itemprop="genre"]/a/text()')
            except Exception as e_genre:
                genre = ""
            try:
                synopsis = root.xpath('.//dt[text()="Sinopsis"]/following-sibling::dd[1]/text()')[0].strip()
            except Exception as e_synopsis:
                synopsis=""
        except Exception as e_connection:
            original_title, duration, genre, synopsis = "", "", "", ""
        
        # Añadimos la información extraída a las listas correspondientes
        movie_original_titles.append(original_title)
        movie_durations.append(duration)
        movie_genres.append(", ".join(genre))
        movie_synopses.append(synopsis)
        
        # Hacemos una pausa para no sobrecargar el servidor
        time.sleep(3)
    
    obj_pelicula.set_movie_original_titles(movie_original_titles)
    obj_pelicula.set_movie_durations(movie_durations)
    obj_pelicula.set_movie_genres(movie_genres)
    obj_pelicula.set_movie_synopses(movie_synopses)
    print("Extracción completa.")

    return obj_pelicula









###################### FUNCIÓN DE ESCRITURA DEL DATA SET COMPLETO EN ARCHIVO TXT ############################

def write_data_in_csv(obj_pelicula):
    """
    Función que escribe el DATASET definitivo en un archivo llamado "dataset_movie_info.csv"
    
    Args:
        obj_película:               Objeto tipo "ClasePeliculaDTO" con todos los datos conocidos del dataset.
        tuplas_de_datos_maximas:    Filas de datos que queremos escribir en el fichero CSV (en el caso de esta práctica serán 1000)
    Return:
        html: El código fuente HTML como una cadena de texto.
    """

    print("Escribiendo DATASET en archivo CSV...")
    
    # Escribimos todo en un archivo CSV
    ruta = "./documentos"
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    with open('./documentos/dataset_movie_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Título', 'Título Original', 'Año', 'Duración', 'Género', 'País', 'Puntuación Media', 'Número de Puntuaciones', 'Director', 'Reparto', 'Sinopsis', 'Enlace'])

        try:
            for i, (title, original_title, year, duration, genre, country, 
                    rating, rating_count, director, cast, synopsis, link) in enumerate(
                zip(
                    obj_pelicula.get_movie_titles(),
                    obj_pelicula.get_movie_original_titles(),
                    obj_pelicula.get_movie_years(),
                    obj_pelicula.get_movie_durations(),
                    obj_pelicula.get_movie_genres(),
                    obj_pelicula.get_movie_countries(),
                    obj_pelicula.get_movie_ratings(),
                    obj_pelicula.get_movie_rating_counts(),
                    obj_pelicula.get_movie_directors(),
                    obj_pelicula.get_movie_cast(),
                    obj_pelicula.get_movie_synopses(),
                    obj_pelicula.get_movie_links()
                )
            ):
                writer.writerow([title, original_title, year, duration, genre, country, rating, rating_count, director, cast, synopsis, link])

        except Exception as e:
            # Al llegar a un tope de tuplas superior a las disponible, entra aqui y para de escribir (sin abortar programa)
            pass