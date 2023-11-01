from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
import csv
from dtos import ClasePeliculaDTO
from libreria_funciones_propias import return_html_after_scrape_movie_info_from_summary_page, recoger_detalles_concretos_pelicula_HTML, capture_data_from_sumaryPage, write_data_in_csv
from threading import Thread



def capture_details_from_all_filmPage(obj_pelicula):
    links = obj_pelicula.get_movie_links()
    cantidadLink = len(links)
    division = cantidadLink / 30
    i = 0
    pos_links = 0
    while i < division:
        hilos = []
        for i in range(30):
            obj_pelicula = hilos.append(Thread(target=recoger_detalles_concretos_pelicula_HTML, args=(str(links[pos_links]), "ficheroDesdeMain.txt", obj_pelicula)))

        for hilo in hilos:
            hilo.start()

        for hilo in hilos:
            hilo.join()

        print("Todos los hilos han terminado")
   
    return obj_pelicula






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

# Recopilamos los datos detallados de cada película
obj_detalles_peliculas = multiHilos(obj_detalles_peliculas)

# Creación del DATASET
write_data_in_csv(obj_detalles_peliculas)

# Tomamos tiempos midiento retardos escribiendo DATASET (csv)
t2 = time.perf_counter_ns()
tiempo_escribiendo_csv = (t2 - t1) / 10**9

# Imprimo información de los costes temporales por consola
print("El tiempo que tardamos en raspar todos los datos generales es de: ",tiempo_raspando_inicial," (segundos)")
print("El tiempo que tardamos en volcar los datos raspados a fichero CSV: ",tiempo_escribiendo_csv," (segundos)")

# 
url = str(obj_detalles_peliculas.get_movie_links()[0])
html = captura_detalle_pelicula_HTML(url, "0.txt")


