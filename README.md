# web_scraping

## Table of Contents
1. [Información General](#Información-General)
2. [Tecnologia](#Tecnología)
3. [Installation](#installation)
4. [Collaboration](#collaboration)
5. [FAQs](#faqs)
### Información General
***
Este proyecto comenzo por curiosidad. La idea era lograr armar una base de datos de información en tiempo real, que luego 
seria usada en algun modelo de inteligencia artificial para lograr predecir el precio de un item. 
En este caso, esos precios son obtenidos de la pagina web de diferentes sucursales de La Anonima.
 
**Supermercado La Anonima**:  https://supermercado.laanonimaonline.com/

Para que esto funcione fue necesario seguir los siguientes pasos:
 * **Crear Web Scraper**

Esto lo hice con Selenium ya que me ofrecia una gran versatilidad para navegar por paginas como las de un supermercado
en donde toda iteraccion se hace a traves de ventanas emergentes o listas desplegables.
 * **Automatizar el proceso**

Esto se dividio en varias partes y decidi implementarlo en AWS con la ayuda de las funciones Lambda y el almacenamiento
en Buckets S3. 

  *  ***Funciones Lambda***
Con esto podemos ejecutar scripts de python en AWS.

  *  ***Buckets S3***
En este se almacena el csv resultado.

  *  ***EventBridge***
Con este creamos un "gatillo" que dispara la funcion Lambda una vez por dia.

  *  ***IAM***
En el creamos los permisos necesarios para que la funcion lambda acceda al Bucket S3 para leer y escribir archivos. 


Al no contar con experiencia suficiente para lograr que todo esto funcione, busque en google para llegar al resultado final. Por ello llegue al post  de Medium de [Vinod Dhole](https://blog.jovian.com/automate-web-scraping-using-python-aws-lambda-amazon-s3-amazon-eventbridge-cloudwatch-c4c982c35fa9)

## Tecnología
Todos estas librerias deben ser compatibles para la misma version de Python. En este caso se realizo en la version 3.7

Pueden descargarlas desde PYPI o desde este [enlace](Librerias)
| Tecnologia     |Versión                         |Link                         |
|----------------|-------------------------------|-----------------------------|
|Pandas          |1.3.5                          |https://pypi.org/project/pandas/1.3.5/            |
|Numpy           |1.19.0                         |https://pypi.org/project/numpy/1.19.0/            |
|Pytz            |2021.1                         |https://pypi.org/project/pytz/2021.1/|
|Selenium        |3.141.0                          |https://pypi.org/project/selenium/3.141.0/       |
