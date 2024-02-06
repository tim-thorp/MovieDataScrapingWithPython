# PR1: Web scraping

(See below for English translation)

# CASTELLANO

## Descripción

En este repositorio encontrará los códigos relacionados con la práctica PR1, centrada en la aplicación de técnicas de *web scraping* usando Python. Esta práctica formó parte de la asignatura "Tipología y ciclo de vida de los datos" de la UOC.

El objetivo final es obtener un dataset de películas con diferentes columnas o atributos de interés. Inicialmente, se recopilan los atributos generales de aproximadamente 1000 películas y el enlace a cada una; después, se utiliza cada enlace para recoger datos específicos. Finalmente, se integran todos los datos recopilados en el dataset final, que se guarda en un fichero CSV.

La web de referencia y central de nuestro proyecto es: _https://www.filmaffinity.com/_

## ¿Quiénes realizamos la práctica?

- **Juan Antonio Tora Cánovas**
- **Tim Thorp**

## ¿Dónde puede encontrar el dataset?

1. **En Zenodo:** a través del siguiente enlace DOI: _https://doi.org/10.5281/zenodo.10072733_
2. **En este repositorio de GitHub:** bajo el directorio `/data` desde la raíz de este repositorio, donde encontrará el fichero CSV correspondiente a nuestro dataset.

## Directorios

- **/src**: Aquí se encuentra todo el código fuente de la práctica PR1.
- **/data**: Aquí se encuentra el archivo CSV con los datos extraídos.
- **/docs**: Directorio donde se puede encontrar la `memoria.pdf` junto con los ficheros utilizados para su creación.

## Archivos

### - De /src -

- **/src/main.py**: Es el punto de entrada del programa central de la PR1, y es responsable de llamar a otros dos archivos .py.
- **/src/librerias_propias.py**: Aquí se encuentran todas las funciones propias creadas durante la PR1.
- **/src/dtos.py**: Aquí se define el objeto/clase llamado `ClasePeliculaDTO`, que se utiliza como un Data Transfer Object (DTO) en `libreria_funciones_propias.py`.

### - De /data -

- **dataset_movie_info.csv**: Este archivo corresponde a nuestro dataset generado con nuestro código.

### - De /docs -

- **memoria.rmd**: Plantilla codificada en R Markdown.
- **memoria.pdf**: Memoria de la práctica PR1 en formato PDF, que es también el resultado de compilar el archivo `memoria.rmd`.
- **requirements.txt**: Fichero que incluye todas las librerías utilizadas en este proyecto: `requests`, `selenium` y `lxml`.

## Ejecución y uso del código


El código principal puede ejecutarse desde `/src/main.py`. No requiere parámetros de entrada y genera como salida el dataset en formato CSV, ubicado en el directorio `/data`.

## Bibliografía utilizada

1. Bristi, W. R., Zaman, Z., & Sultana, N. (2019). Predicting IMDb rating of movies by machine learning techniques. *2019 10th International Conference on Computing, Communication and Networking Technologies (ICCCNT)*, 1-5. IEEE.
2. Creative Commons. (2023). Licencia Creative Commons Atribución-CompartirIgual 4.0 Internacional (CC BY-SA 4.0). Recuperado de https://creativecommons.org/licenses/by-sa/4.0/deed.es
3. Firmanto, A., & Sarno, R. (2018). Prediction of movie sentiment based on reviews and score on Rotten Tomatoes using SentiWordNet. *2018 International Seminar on Application for Technology of Information and Communication*, 202-206. IEEE.
4. Harish, B. S., Kumar, K., & Darshan, H. K. (2019). Sentiment analysis on IMDb movie reviews using hybrid feature extraction method.
5. Lawson, R. (2015). Scraping the Data. En *Web Scraping with Python* (Capítulo 2). Packt Publishing Ltd.
6. Selenium. (2023). Getting started. Recuperado de https://www.selenium.dev/documentation/webdriver/getting_started/
7. Subirats, L., & Calvo, M. (2018). *Web Scraping*. Editorial UOC.


# ENGLISH

## Description

In this repository, you will find the code related to the practical assignment PR1, focused on the application of web scraping techniques using Python. This assignment was part of the "Data Lifecycle Management" subject at the Open University of Catalonia (UOC).

The ultimate goal is to obtain a dataset of movies with different columns or attributes of interest. Initially, general attributes of about 1000 movies and the link to each one are collected; then, each link is used to gather specific data. Finally, all the collected data are integrated into the final dataset, which is saved in a CSV file.

The central reference website for our project is: https://www.filmaffinity.com/

## Who are we?

- **Juan Antonio Tora Cánovas**
- **Tim Thorp**

## Where can I find the dataset?

1. **On Zenodo:** through the following DOI link: _https://doi.org/10.5281/zenodo.10072733_
2. **In this GitHub repository:** under the `/data` directory from the root of this repository, where you will find the CSV file corresponding to our dataset.

## Directories

- **/src**: Here is all the source code for PR1.
- **/data**: Here is the CSV file with the extracted data.
- **/docs**: Directory where you can find the `memoria.pdf` along with the files used for its creation.

## Files

### - From /src -

- **/src/main.py**: This is the entry point of the main program for PR1 and is responsible for calling two other .py files.
- **/src/librerias_propias.py**: Here are all the custom functions created during PR1.
- **/src/dtos.py**: Here the object/class called `ClasePeliculaDTO` is defined, which is used as a Data Transfer Object (DTO) in `libreria_funciones_propias.py`.

### - From /data -

- **dataset_movie_info.csv**: This file corresponds to our generated dataset with our code.

### - From /docs -

- **memoria.rmd**: Template coded in R Markdown.
- **memoria.pdf**: Report of the PR1 assignment in PDF format, which is also the result of compiling the `memoria.rmd` file.
- **requirements.txt**: File that includes all the libraries used in this project: `requests`, `selenium`, and `lxml`.

## Code execution

The main code can be run from `/src/main.py`. It does not require input parameters and generates as output the dataset in CSV format, located in the `/data` directory.

## Bibliography

1. Bristi, W. R., Zaman, Z., & Sultana, N. (2019). Predicting IMDb rating of movies by machine learning techniques. *2019 10th International Conference on Computing, Communication and Networking Technologies (ICCCNT)*, 1-5. IEEE.
2. Creative Commons. (2023). Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0). Retrieved from https://creativecommons.org/licenses/by-sa/4.0/deed.en
3. Firmanto, A., & Sarno, R. (2018). Prediction of movie sentiment based on reviews and score on Rotten Tomatoes using SentiWordNet. *2018 International Seminar on Application for Technology of Information and Communication*, 202-206. IEEE.
4. Harish, B. S., Kumar, K., & Darshan, H. K. (2019). Sentiment analysis on IMDb movie reviews using hybrid feature extraction method.
5. Lawson, R. (2015). Scraping the Data. In *Web Scraping with Python* (Chapter 2). Packt Publishing Ltd.
6. Selenium. (2023). Getting started. Retrieved from https://www.selenium.dev/documentation/webdriver/getting_started/
7. Subirats, L., & Calvo, M. (2018). *Web Scraping*. Editorial UOC.