# web_scraping

## Table of Contents
1. [Información General](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Collaboration](#collaboration)
5. [FAQs](#faqs)
### Información General
***
Este proyecto comenzo por curiosidad. La idea era lograr armar una base de datos de información en tiempo real, que luego 
seria usada en algun modelo de inteligencia artificial para lograr predecir el precio de un item. 
En este caso, esos precios son obtenidos de la pagina web de diferentes sucursales de La Anonima. 
[Supermercado La Anonima] https://supermercado.laanonimaonline.com/

Para que esto funcione fue necesario seguir los siguientes pasos:
*[Crear Web Scraper]
Esto lo hice con Selenium ya que me ofrecia una gran versatilidad para navegar por paginas como las de un supermercado
en donde toda iteraccion se hace a traves de ventanas emergentes o listas desplegables.
*[Automatizar el proceso]
Esto se dividio en varias partes y decidi implementarlo en AWS con la ayuda de las funciones Lambda y el almacenamiento
en Buckets S3. 
**[Funciones Lambda]
Con esto podemos ejecutar scripts de python en AWS.
**[Buckets S3]
En este se almacena el csv resultado.
**[EventBridge]
Con este creamos un "gatillo" que dispara la funcion Lambda una vez por dia.
**[IAM]
En el creamos los permisos necesarios para que la funcion lambda acceda al Bucket S3 para leer y escribir archivos. 

### Screenshot
![Image text](https://www.united-internet.de/fileadmin/user_upload/Brands/Downloads/Logo_IONOS_by.jpg)
## Technologies
***
Lista de tecnologias usadas en el proyecto:
* [Python: Pandas ](https://example.com): Version 12.3 
* [Technologie name](https://example.com): Version 2.34
* [Library name](https://example.com): Version 1234
## Installation
***
A little intro about the installation. 
```
$ git clone https://example.com
$ cd ../path/to/the/file
$ npm install
$ npm start
```
Side information: To use the application in a special environment use ```lorem ipsum``` to start
## Collaboration
***
Give instructions on how to collaborate with your project.
> Maybe you want to write a quote in this part. 
> It should go over several rows?
> This is how you do it.
## FAQs
***
A list of frequently asked questions
1. **This is a question in bold**
Answer of the first question with _italic words_. 
2. __Second question in bold__ 
To answer this question we use an unordered list:
* First point
* Second Point
* Third point
3. **Third question in bold**
Answer of the third question with *italic words*.
4. **Fourth question in bold**
| Headline 1 in the tablehead | Headline 2 in the tablehead | Headline 3 in the tablehead |
|:--------------|:-------------:|--------------:|
| text-align left | text-align center | text-align right |