from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
import csv
from dtos import ClasePeliculaDTO
import libreria_funciones_propias 



def login_FillmAffinity_And_Navegation_To_TopFA(url):
    # Abrir navegador Firefox y acceder a URL general
    options = webdriver.FirefoxOptions()
    options.headless = True
    
    # Instanciamos navegador Firefox con opciones definidas y navegamos a la URL deseada
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    time.sleep(5)

     # Buscamos el botón «ACEPTO» y lo clicamos
    button = browser.find_element(By.CLASS_NAME, "css-v43ltw")
    button.click()

    # navegación a la sección "TopFA"
    irTopFA = browser.find_element(By.XPATH, '/html/body/header/div[2]/div/ul/li[1]/a').click()
    time.sleep(3)
    
    # Cargo la página "TopFA" con filtro de búsqueda concreto
    browser.get("https://www.filmaffinity.com/es/topgen.php?genres=&chv=0&orderby=avg&movietype=movie%7C&country=&fromyear=2013&toyear=2023&ratingcount=3&runtimemin=0&runtimemax=4")
    return browser
    



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
    
    # Cerramos el navegador para liberar recursos
    browser.quit()

    return html




def write_in_file_the_dataset(obj):
    """
    A partir del HTML extraido, se localizan los datos de interés y se escriben en un fichero CSV.
    Parámetros:
        html: El código fuente en HTML que se extrajo de la web.
    Return:
        obj_detalles_peliculas: objeto de tipo "ClasePeliculasDTO"
    """

    # Analizamos el HTML con lxml
    root = etree.HTML(obj.get_html())
    
    # Creamos listas para guardar los valores de cada variable
    movie_titles = []
    movie_years = []
    movie_countries = []
    movie_ratings = []
    movie_rating_counts = []
    movie_directors = []
    movie_cast = []
    movie_links = []
    
    # Recorremos todos los divs con la clase "mc-info-container"
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
    
    # Guardo el valor de "movie_links" para devolverlo en el RETURN
    obj.set_movie_links(movie_links)

    # Recorremos todos los lis con la clase "data"
    for li in root.xpath('//li[@class="data"]'):
        # Extraemos la puntuación media y el número de puntuaciones
        rating = li.xpath('.//div[@class="avg-rating"]/text()')[0]
        rating_count = li.xpath('.//div[@class="rat-count"]/text()')[0].strip()
        
        movie_ratings.append(rating)
        movie_rating_counts.append(rating_count)

    # Escribimos todo en un archivo CSV
    with open('movie_info_from_summary_page.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Título', 'Año', 'País', 'Puntuación Media', 'Número de Puntuaciones', "Director", "Reparto", "Enlace"])

        for i, (title, year, country, rating, rating_count, director, cast, link) in enumerate(zip(movie_titles, movie_years, movie_countries, movie_ratings, movie_rating_counts, movie_directors, movie_cast, movie_links)):
            # Detenemos el proceso si hemos escrito 1000 filas
            if i >= 1000:
                break
            writer.writerow([title, year, country, rating, rating_count, director, cast, link])

    return obj





# Ejecución

obj_detalles_peliculas = ClasePeliculaDTO("",[])
t0 = time.perf_counter_ns()
url = "https://www.filmaffinity.com/"
current_url = login_FillmAffinity_And_Navegation_To_TopFA(url)
html = return_html_after_scrape_movie_info_from_summary_page(current_url, 33)
obj_detalles_peliculas.set_html(html)
t1 = time.perf_counter_ns()
tiempo_final_raspando = (t1 - t0) / 10**9


print("El tiempo que tardamos en raspar todos los datos generales es de: ",tiempo_final_raspando," (segundos)")
objeto_devuelto= write_in_file_the_dataset(obj_detalles_peliculas)
t2 = time.perf_counter_ns()
tiempo_escribiendo_csv = (t2 - t1) / 10**9
print("El tiempo que tardamos en volcar los datos raspados a fichero CSV: ",tiempo_escribiendo_csv," (segundos)")

html = libreria_funciones_propias.captura_detalle_pelicula_HTML(objeto_devuelto.get_movie_links[0], "0.txt")


