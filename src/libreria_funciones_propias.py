from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
from dtos import ClasePeliculaDTO
import csv



def scrape_movie_details(obj_pelicula):
    """
    Esta función se encarga de extraer detalles específicos de películas a partir de una lista de URLs.
    Los detalles incluyen el título original, la duración, el género y el sinopsis de cada película.
    
    Args:
        input_csv (str): Ruta al archivo CSV que contiene la columna 'Enlace' con las URLs de las películas.
        output_csv (str): Ruta al archivo CSV donde se guardarán los detalles extraídos.
    
    Returns:
        None: La función guarda los detalles directamente en un archivo CSV y no devuelve ningún valor.
    """
    
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
        
        # Hacemos una petición GET para obtener el contenido de la página
        response = requests.get(url)
        html_content = response.text
        
        # Utilizamos lxml para analizar el contenido HTML
        root = etree.HTML(html_content)
        
        # Utilizamos xpath para extraer el título original, la duración, el género y el sinopsis
        original_title = root.xpath('.//dt[text()="Título original"]/following-sibling::dd[1]/text()')[0].strip()
        duration = root.xpath('.//dt[text()="Duración"]/following-sibling::dd[1]/text()')[0].split()[0].strip()
        genre = root.xpath('.//dt[text()="Género"]/following-sibling::dd[1]//span[@itemprop="genre"]/a/text()')
        synopsis = root.xpath('.//dt[text()="Sinopsis"]/following-sibling::dd[1]/text()')[0].strip()
        
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




def capture_details_from_all_filmPage(obj_pelicula):
    
    links = obj_pelicula.get_movie_links()
    titulo_original     = []
    duracion            = []
    genero              = []
    sinopsis            = []
    
    print("Recopilando datos de película específica, de la 0 a la 1029...")

    for i in range(len(links)):
        
        try:
            response = requests.get(links[i])
            soup = BeautifulSoup(response.content, "html.parser")
            html = soup.prettify()
            # Analizamos el HTML con lxml
            root = etree.HTML(html)
            
            try:
                # Consiguiendo valor de "Título original"
                value = root.xpath('/html/body/div[2]/div/div/main/div[2]/div/div[3]/dl[1]/dd[1]')[0].text
                value = value.replace(" ", "")
                value = value.replace("\n", "")
                titulo_original.append(value)
            except Exception as e:
                titulo_original.append("")
            
            try:
                # Consiguiendo valor de "Título original"
                value = root.xpath('/html/body/div[2]/div/div/main/div[2]/div/div[3]/dl[1]/dd[3]')[0].text
                value = value.replace(" ", "")
                value = value.replace("\n", "")
                duracion.append(value)
            except Exception as e:
                duracion.append("")

            try:
                # Conseguimos los generos
                value = root.xpath('/html/body/div[2]/div/div/main/div[2]/div/div[3]/dl[1]/dd[11]/span[@itemprop="genre"/a/text()')
                value = value.replace(" ", "")
                value = value.replace("\n", "")
                genero.append(value)
            except Exception as e:
                genero.append("")

            try:
                # Conseguimos la sinopsis
                value = root.xpath('/html/body/div[2]/div/div/main/div[2]/div/div[3]/dl[1]/dd[13]')[0].text
                value = value.replace("\n", "")
                sinopsis.append(value)
            except Exception as e:
                sinopsis.append("")
            finally:
                time.sleep(3)
                print("Analizada película ", i)
        except Exception as e:
            print("Ocurrió TimeOut en Película ", i)
    # Seteamos las listas de vuelta al objeto para retornarlas en él
    obj_pelicula.set_titulo_original(titulo_original)
    obj_pelicula.set_duracion(duracion)
    obj_pelicula.set_genero(genero)
    obj_pelicula.set_sinopsis(sinopsis)
    return obj_pelicula



def return_html_after_scrape_movie_info_from_summary_page(browser, num_clics):
    """
    Obtiene el código fuente HTML tras la ejecución de JavaScript y extrae los datos de las películas.
    Parámetros:
        browser: Con los datos de la conexión HTTP establecida y la web cargada.
        num_clics: El número de veces para hacer clic en la flecha para cargar más películas.
                   Por defecto, hacemos clic 33 veces para cargar 1020 películas.
    Return:
        html: El código fuente HTML como una cadena de texto.
    """
    
    
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
    
    # Obtenemos todo el código fuente HTML de la página con las 1000-1030 películas ya cargadas, incluidos los cambios realizados por JavaScript
    html = browser.page_source
    with open('html_sumary_page.txt', 'w', newline='', encoding='utf-8') as f:
        f.write(html)
    
    # Cerramos el navegador para liberar recursos
    browser.quit()

    return html








def capture_data_from_sumaryPage(obj_pelicula):
    """
    A partir del HTML extraido, se localizan los datos de interés y se escriben en un fichero CSV.
    Parámetros:
        html: El código fuente en HTML que se extrajo de la web.
    Return:
        obj_detalles_peliculas: objeto de tipo "ClasePeliculasDTO"
    """
    
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

def write_data_in_csv(obj_pelicula):

    # Escribimos todo en un archivo CSV
    with open('dataset_movie_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Título', 'Año', 'País', 'Puntuación Media', 'Número de Puntuaciones', "Director", "Reparto", "Enlace", "Título Original", "Duración", "Género", "Sinopsis"])

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
            if i >= 1000:
                break
            writer.writerow([title, year, country, rating, rating_count, director, cast, link, originalTitle, duration, gender, synopsis])
    



