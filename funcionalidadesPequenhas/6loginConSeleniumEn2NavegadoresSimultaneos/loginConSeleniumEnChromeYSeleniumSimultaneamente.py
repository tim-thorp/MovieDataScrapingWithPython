from selenium.webdriver.common.by import By
from selenium import webdriver
import threading
import time


def loginAmazonAutomaticoFirefox(usuario, password):
    # Abrir navegador Firefox y acceder a URL de login AMAZON
    driver = webdriver.Firefox()
    driver.get('https://www.amazon.es/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.es%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=esflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')
    time.sleep(5)
    # Acceder a campo de formulariio "user", escribir el user y clicar para enviar
    usuarioForm = driver.find_element(By.XPATH, '//*[@id="ap_email"]')
    usuarioForm.send_keys(usuario)
    boton = driver.find_element(By.XPATH, '//*[@id="continue"]').click()
    # Esperar 3 segundos para cargar nueva página
    time.sleep(3)
    # Acceder a campo de formulariio "password", escribir el password y clicar para enviar (y acceder a tu cuenta de AMAZON)
    passwordForm = driver.find_element(By.XPATH, '//*[@id="ap_password"]')
    passwordForm.send_keys(password)
    entrar = driver.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()
    time.sleep(60)
    driver.close()

def loginAmazonAutomaticoChrome(usuario, password):
    # Abrir navegador Chrome y acceder a URL de login AMAZON
    driver = webdriver.Chrome()
    driver.get('https://www.amazon.es/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.es%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=esflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0')
    time.sleep(5)
    # Acceder a campo de formulariio "user", escribir el user y clicar para enviar
    usuarioForm = driver.find_element(By.XPATH, '//*[@id="ap_email"]')
    usuarioForm.send_keys(usuario)
    boton = driver.find_element(By.XPATH, '//*[@id="continue"]').click()
    # Esperar 3 segundos para cargar nueva página
    time.sleep(3)
    # Acceder a campo de formulariio "password", escribir el password y clicar para enviar (y acceder a tu cuenta de AMAZON)
    passwordForm = driver.find_element(By.XPATH, '//*[@id="ap_password"]')
    passwordForm.send_keys(password)
    entrar = driver.find_element(By.XPATH, '//*[@id="signInSubmit"]').click()
    time.sleep(60)
    driver.close()

def concurrencia2hilos(usuario, password):
     # Creamos dos hilos
    hilo1 = threading.Thread(target=loginAmazonAutomaticoFirefox, args=(usuario, password))
    hilo2 = threading.Thread(target=loginAmazonAutomaticoChrome, args=(usuario, password))

    # Iniciamos los hilos
    hilo1.start()
    hilo2.start()

    # Esperamos a que los hilos terminen
    hilo1.join()
    hilo2.join()

    # Colocacion de un retardo de 3 segundos para no saturar el servidor
    print("esperando 3 segundos")
    time.sleep(3)
    print("transcurridos 3 segundos")




# Ejecutamos la funcion anterior con mi usuario y password (entre comillas simples)
concurrencia2hilos('miUser', 'miPassword')


