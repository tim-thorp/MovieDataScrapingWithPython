import threading
import sys
import time

########### Código para el import de carpeta superior a la actual ################
sys.path.append("C:\\Users\\Juan Antonio\\Desktop\\UOC\\entrega PR1\\PR1-WebScraping-TipologiaYCicloDeVidaDeLosDatos\\funcionalidadesPequenhas\\2descargaImagenes")
print(sys.path)
from descargaImagenes import descargar_imagenes_contenidas_en_html_source, consigueCodigoFuente



########### Código de paralelismo de 2 en 2 procesos a la vez ################

def procesadoConcurrente(x):
    #TODO: Aqui debe de hacerse la ejecucion funcional de interes en paralelo
    return 2 * x

def main():
    # Creamos dos hilos
    hilo1 = threading.Thread(target=procesadoConcurrente, args=(1,))
    hilo2 = threading.Thread(target=procesadoConcurrente, args=(2,))

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



if __name__ == "__main__":
    main()