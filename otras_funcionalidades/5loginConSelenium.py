from selenium.webdriver.common.by import By
from selenium import webdriver
import time


def login_FilmAffinity_Automatico(url, usuario, password):
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

    # Clic en el elemento que me lleva al login
    browser.find_element(By.XPATH, '/html/body/header/div[1]/div/div[3]/div/a[1]/strong').click()

    # usuario login
    usuarioForm = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/main/div[2]/div[1]/form/div[1]/input')
    usuarioForm.send_keys(usuario)
    
    # password login
    passwordForm = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/main/div[2]/div[1]/form/div[2]/input')
    passwordForm.send_keys(password)

    # envio login
    entrar = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/main/div[2]/div[1]/form/input[3]').click()
    time.sleep(3)

    # navegación a la sección "TopFA"
    irTopFA = browser.find_element(By.XPATH, '/html/body/header/div[2]/div/ul/li[1]/a').click()
    time.sleep(10)
    
    browser.close()
    return browser
    

# Ejecutamos la funcion anterior con mi usuario y password (entre comillas simples)
url = "https://www.filmaffinity.com/"
usuario = "jtoracanouoc"
password = "1234aA"
login_FilmAffinity_Automatico(url, usuario, password)


