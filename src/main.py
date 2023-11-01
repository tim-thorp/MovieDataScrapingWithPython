from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from dtos import ClasePeliculaDTO
from libreria_funciones_propias import return_html_after_scrape_movie_info_from_summary_page, scrape_movie_details, capture_details_from_all_filmPage, capture_data_from_sumaryPage, write_data_in_csv
from threading import Thread



################## Ejecución ###################
# tiempo inicial
t0 = time.perf_counter_ns()

# inicializo objetos de pelicula y web
url = "https://www.filmaffinity.com/"
obj_detalles_peliculas = ClasePeliculaDTO("",[],[],[],[],[],[],[],[],[],[],[],[])

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

# realizo raspado inicial y guardo html devuelto
html = return_html_after_scrape_movie_info_from_summary_page(browser, 33)
obj_detalles_peliculas.set_html(html)

# Tomo instantes de tiempo después del raspado inicial
t1 = time.perf_counter_ns()
tiempo_raspando_inicial = (t1 - t0) / 10**9

# Recopilamos los datos del sumaryPage
obj_detalles_peliculas = capture_data_from_sumaryPage(obj_detalles_peliculas)
print("El tiempo que tardamos en raspar todos los datos generales es de: ",tiempo_raspando_inicial," (segundos)")

# Recopilamos los datos detallados de cada película
obj_detalles_peliculas = scrape_movie_details(obj_detalles_peliculas)

# Creación del DATASET
write_data_in_csv(obj_detalles_peliculas)

# Tomamos tiempos midiento retardos escribiendo DATASET (csv)
t2 = time.perf_counter_ns()
tiempo_escribiendo_csv = (t2 - t1) / 10**9

# Imprimo información de los costes temporales por consola
print("El tiempo que tardamos en volcar los datos raspados a fichero CSV: ",tiempo_escribiendo_csv," (segundos)")


