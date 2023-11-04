# PR1: Web scraping

## Descripción

En este repositorio podrá encontrar los códigos relacionados con la práctica PR1, que se centra en poner en práctica técnicas de Web Scraping, usando Python.
Esta práctica está dentro de la asignatura "Tipología y ciclo de Vida de los Datos", de la UOC. 

El objetivo final de nuestra práctica es "conseguir un DataSet de películas, con diferentes columnas o atributos de interés, siendo este DataSet escrito en un fichero CSV.
Inicialmente se recopian los atributos generales de aproximadamente 1000 películas y el link a cada película; después se usa el link de cada película para recopilar datos concretos de cada película.
Finalmente, se unifican todos los datos recopilados de todas las películas y se escribe el dataset final, en un fichero CSV.

La web de referencia y central de nuestro proyecto es: _https://www.filmaffinity.com/_

## ¿Quiénes realizamos la práctica?

* **Juan Antonio Tora Cánovas** 
* **Tim Thorp**

## DIRECTORIOS
* **src/main**: aquí se encuentra todo el código fuente de la práctica PR1.
* **src/otras_funcionalidades**: aquí se encuentra todo el código que, aun quedando fuera de la PR1, ha sido de utilidad para la MEMORIA.PDF o practicar para la PR1.
* **documentos**: directorio donde puede encontrarse la memoria.pdf, requirements.txt (con info de librerías) y el dataset.

## ARCHIVOS
### -De src/main-
* **src/main/main.py**: es el punto de entrada del programa central de la PR1, y el responsable de llamar a otros 2 archivos .py.
* **src/main/librerias_propias.py**: aquí se encuentran todas las funciones propias, creadas por nosotros durante la PR1. 
* **src/main/dtos.py**: aquí se define el objeto/clase llamado "ClasePeliculaDTO". Se utilizará como objeto DTO (Data Tansfer Object) en "libreria_funciones_propias.py".
### -De src/otras_funcionalidades-
* **Los 3 primeros códigos**: creados para probar tiempos y funcionalidades entre Selenium y métodos básicos.
* **Los códigos 4 y 5**: realizados para crear las 2 funciones de raspado de datos que posteriormente se añadieron a la PR1.
* **El código 6**: código para obtener la tecnología del sitio web y los datos del propietario, información útil que se usa en la MEMORIA.PDF.


## Bibliografía Utilizada

1. Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC.
2. Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2.
Scraping the Data
