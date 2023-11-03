from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
from dtos import ClasePeliculaDTO
import csv





###########################################################################################################################
##################################### FUNCIÓN CON EL FLUJO GENERAL DEL PROGRAMA ###########################################
###########################################################################################################################

def ejecucion_programa():
    """
    Función de entrada al programa, donde se encuentra el flujo general del programa y las llamadas a las funcionalidades.
    
    Args:
        None.
    Return:
        None.
    """
    
    # capturo instante temporal inicial (t0)
    t0 = time.perf_counter_ns()

    # se inicializa objeto DTO de "ClasePeliculaDTO"
    url = "https://www.filmaffinity.com/"
    obj_detalles_peliculas = ClasePeliculaDTO("",[],[],[],[],[],[],[],[],[],[],[],[])

    # Abrir navegador Firefox y acceder a URL general
    options = webdriver.FirefoxOptions()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    time.sleep(5)

    # Busca el botón «ACEPTO» y lo clica automáticamente
    button = browser.find_element(By.CLASS_NAME, "css-v43ltw")
    button.click()

    # Navegación a la sección "TopFA" y recargar página con filtro [Películas, Años: 2013-2023]
    browser.find_element(By.XPATH, '/html/body/header/div[2]/div/ul/li[1]/a').click()
    time.sleep(3)
    browser.get("https://www.filmaffinity.com/es/topgen.php?genres=&chv=0&orderby=avg&movietype=movie%7C&country=&fromyear=2013&toyear=2023&ratingcount=3&runtimemin=0&runtimemax=4")

    # Realizar 33 veces scroll hasta conseguir 1020 películas generadas dinámicamente.
    # Luego guardar HTML de todo la página con las 1020 películas.
    html = return_html_after_scrape_movie_info_from_summary_page(browser, 33)
    obj_detalles_peliculas.set_html(html)

    # Tomo instante de tiempo (t1) después del raspado de la sumaryPage (con las 1020 películas)
    t1 = time.perf_counter_ns()
    tiempo_raspando_inicial = (t1 - t0) / 10**9

    # Recopilamos los datos de interés del HTML del sumaryPage (con las 1020 películas).
    # Datos recogidos se almacenan en objeto DTO "ClasePeliculaDTO"
    obj_detalles_peliculas = capture_data_from_sumaryPage(obj_detalles_peliculas)

    # Ahora recopilamos datos específicos de cada película.
    t2 = time.perf_counter_ns()
    obj_detalles_peliculas = scrape_movie_details(obj_detalles_peliculas)
    t3 = time.perf_counter_ns()
    tiempo_raspando_datos_especificos_de_cada_pelicula = (t3 - t2) / 10**9
    

    # Creación del DATASET
    # Dos parámetros de entra: 
    #                   1) el DTO con los datos de las 1020 películas
    #                   2) el nº de películas máximas que se quieren escribir en el dataset
    write_data_in_csv(obj_detalles_peliculas, 1000)

    # Se toma instante de tiempo t3 y se calcula el tiempo que cuesta escribir el dataset el fichero TXT
    t4 = time.perf_counter_ns()
    tiempo_escribiendo_csv = (t4 - t3) / 10**9
    print("-----------------------------------------------\nInformeme de tiempos:")
    print("El tiempo raspando SumaryPage: ",tiempo_raspando_inicial," (segundos)")
    print("El tiempo raspando datos específicos de cada película: ",tiempo_raspando_datos_especificos_de_cada_pelicula," (segundos)")
    print("El tiempo volcando tpdps los datos raspado, en fichero CSV: ",tiempo_escribiendo_csv," (segundos)")

####################################################### FIN PROGRAMA ####################################################












###########################################################################################################################
########################## FUNCIONES Y LIBRERÍAS PROPIAS PARA FUNCIONALIDAD ESPECÍFICA ####################################
###########################################################################################################################

############## SE GUARDAN EN EL DTO LOS DATOS GENERALES DE CADA PELÍCULA ###########################

def capture_data_from_sumaryPage(obj_pelicula):
    """
    A partir del HTML, extraido de SumaryPage, se localizan los datos de interés.
    
    Args:
        Objeto tipo "ClasePeliculaDTO": Objeto entrada como DTO para rellenar las propiedades de los datos recopilados.
    Return:
        Objeto tipo "ClasePeliculaDTO": Devolución del objeto entrante con los valores nuevos guardados.
    """
    
    print("Raspando datos de la Sumary Page...")
   
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






############## SE GUARDAN EN EL DTO LOS DATOS ESPECÍFICOS DE CADA PELÍCULA ###########################

def scrape_movie_details(obj_pelicula):
    """
    Esta función se encarga de extraer detalles específicos de películas a partir de una lista de URLs previamente conseguida de la SumaryPage.
    Gracias a las URL conseguidas, podemos acceder al interior de cada película de la SumaryPage.
    Los datos concretos del interior de cada película son: título original, duración, género y sinopsis.
    
    Args:
        input_csv (str): Ruta al archivo CSV que contiene la columna 'Enlace' con las URLs de las películas.
        output_csv (str): Ruta al archivo CSV donde se guardarán los detalles extraídos.
    Return:
        None: La función guarda los detalles directamente en un archivo CSV y no devuelve ningún valor.
    """
    
    print("Raspando datos específicos...")

    # Cargamos el archivo CSV que contiene los enlaces a las páginas de las películas
    # Convertimos la columna de enlaces en una lista
    # Inicializamos listas vacías donde almacenaremos la información extraída
    url_list = obj_pelicula.get_movie_links()
    
    movie_original_titles       = []
    movie_durations             = []
    movie_genres                = []
    movie_synopses              = []
    
    # Iteramos a través de cada URL en la lista
    for i, url in enumerate(url_list):
        print("Extrayendo información de la película {}/{}...".format(i+1, len(url_list)))
        
        # Gestión de errores general cuando falla la conexión web
        try:
            # Hacemos una petición GET para obtener el contenido de la página
            response = requests.get(url)
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
        except Exception as e_conection:
            original_title, duration, genre, synopsis = "", "", "", ""
        
        # Añadimos la información extraída a las listas correspondientes
        movie_original_titles.append(original_title)
        movie_durations.append(duration)
        movie_genres.append(", ".join(genre))
        movie_synopses.append(synopsis)
        
        # Hacemos una pausa para no sobrecargar el servidor
        time.sleep(3)
    
    obj_pelicula.set_titulo_original(movie_original_titles)
    obj_pelicula.set_duracion(movie_durations)
    obj_pelicula.set_genero(movie_genres)
    obj_pelicula.set_sinopsis(movie_synopses)
    print("Extracción completa.")

    return obj_pelicula







#################### SE CONSIGUE HTML DE LA SUMARY PAGE TRAS GENERAR LOS 1020 LINK DE PELÍCULAS #################

def return_html_after_scrape_movie_info_from_summary_page(browser, num_clics):
    """
    Función que obtiene el código fuente HTML tras la ejecución de JavaScript de la SumaryPage.
    
    Args:
        browser:    Con los datos de la conexión HTTP establecida y la web cargada.
        num_clics:  El número de veces para hacer clic en la flecha para cargar más películas.
                    Por defecto, se diseña para qye haga clic 33 veces y así cargar 1020 películas.
    Return:
        html: El código fuente HTML como una cadena de texto.
    """
    
    print("Generando HTML del código fuente del Sumary Page y almacenándolo en una variable...")

    # Bucle para hacer 33 veces scroll hacia abajo y click en la flecha que con javascrip sigue mostrando más películas
    for i in range(num_clics):
        # Esperamos para evitar sobrecargar el servidor
        time.sleep(3)

        # Hacemos clic en la flecha para cargar más películas
        button = browser.find_element(By.ID, "load-more-bt")
        browser.execute_script("arguments[0].scrollIntoView(true);", button)
        browser.execute_script("arguments[0].click();", button)
    
    # Esperamos para que las últimas 30 películas carguen
    time.sleep(3)
    
    # Obtenemos todo el código fuente (HTML) de la SumaryPage (con las 1020 películas ya generadas)
    html = browser.page_source

    # Cerramos el navegador para liberar recursos
    browser.quit()
    return html








###################### FUNCIÓN DE ESCRITURA DEL DATA SET COMPLETO EN ARCHIVO TXT ############################

def write_data_in_csv(obj_pelicula, tuplas_de_datos_maximas):
    """
    Función que escribe el DATA SET definitivo en un archivo llamado "dataset_movie_info.csv"
    
    Args:
        obj_película:               Objeto tipo "ClasePeliculaDTO" con todos los datos conocidos del dataset.
        tuplas_de_datos_maximas:    Filas de datos que queremos escribir en el fichero CSV (en el caso de esta práctica serán 1000)
    Return:
        html: El código fuente HTML como una cadena de texto.
    """

    print("Escribiendo DATASET en archivo CSV...")
    # Escribimos todo en un archivo CSV
    with open('dataset_movie_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Título', 'Año', 'País', 'Puntuación Media', 'Número de Puntuaciones', "Director", "Reparto", "Enlace", "Título Original", "Duración", "Género", "Sinopsis"])
        try:
            for i, (title, year, country, rating, rating_count, director, cast, link, originalTitle, duration, gender, synopsis) in enumerate(zip(obj_pelicula.get_movie_titles(), 
                                                                                                    obj_pelicula.get_movie_years(), 
                                                                                                    obj_pelicula.get_movie_countries(), 
                                                                                                    obj_pelicula.get_movie_ratings(), 
                                                                                                    obj_pelicula.get_movie_rating_counts(), 
                                                                                                    obj_pelicula.get_movie_directors(), 
                                                                                                    obj_pelicula.get_movie_cast(), 
                                                                                                    obj_pelicula.get_movie_links(), 
                                                                                                    obj_pelicula.get_titulo_original(), 
                                                                                                    obj_pelicula.get_duracion(), 
                                                                                                    obj_pelicula.get_genero(), 
                                                                                                    obj_pelicula.get_sinopsis())
                                                                                                    ):
                # Detenemos el proceso si hemos escrito 1000 filas
                if i >= tuplas_de_datos_maximas:
                    break
                writer.writerow([title, year, country, rating, rating_count, director, cast, link, originalTitle, duration, gender, synopsis])
        except Exception as e:
            # Al llegar a un tope de tuplas superior a las disponible, entra aqui y para de escribir (sin abortar programa)
            pass
        




