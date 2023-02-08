<div align="center">
 <h1>Web Scraping</h1>
 <i> Python + AWS </i>
</div>

<div align="center">
 <img alt ="estado-en-progreso" src = https://img.shields.io/badge/estado-en%20progreso-green/>
 <img alt ="version-python" src =https://img.shields.io/badge/Python-3.7-blue/>
</div>


## Tabla de contenido

[Información General](#Información-General)

[Tecnologia](#Tecnología)

[Resultado](#Resultado)

### Información General

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
<div align="center">
  <img src="/img/Lambda.png" width="80" height="80"/>
  <img src="/img/s3.png" width="80" height="80"/>
  <img src="/img/eventBridge.png" width="80" height="80"/>
  <img src="/img/IAM.png" width="80" height="80"/>
</div>

  *  ***Funciones Lambda***
  
Con esto podemos ejecutar scripts de python en AWS.

  *  ***Buckets S3***
  
En este se almacena el csv resultado.

  *  ***EventBridge***
  
Con este creamos un "gatillo" que dispara la funcion Lambda una vez por dia.

  *  ***IAM***
  
En el creamos los permisos necesarios para que la funcion lambda acceda al Bucket S3 para leer y escribir archivos. 


Al no contar con experiencia suficiente para lograr que todo esto funcione, busque en google para llegar al resultado final. Por ello llegue al post  de Medium de [Vinod Dhole](https://blog.jovian.com/automate-web-scraping-using-python-aws-lambda-amazon-s3-amazon-eventbridge-cloudwatch-c4c982c35fa9)

## Pasos a seguir 

Inicialmente debemos ingresar a la pagina e identificar que queremos realizar. En mi caso, era obtener el preecio de un unico articulo para cada una de las sucursales que posee esta cadena de supermercados dentro del pais.

Por ello realizo todos los pasos de forma manual para entender un poco que es lo que deberia ir haciendo el web scraper. 

1. Presionamos el boton para seleccionar sucursales, a la derecha del buscador. 

![Barra_buscador](https://user-images.githubusercontent.com/42218625/217662423-8e3c861c-3fa6-4092-91dc-916334a0777f.png)
> Nota: Esto hace que aparezca una ventana emergente

2. Seleccionamos la provincia y la sucursal
<div align="center">
 <img src="https://user-images.githubusercontent.com/42218625/217663562-66d114ed-81fe-433f-b99d-4b6bc6510668.png" width="300" height="280"/>
</div>

3. Presionamos Aceptar y luego de que la pagina cambie de sucursal ingresamos en la barra de busqueda el item que deseemos.

Este proyecto no tiene una finalidad especifica por lo que se seleccionó cualquier item. Algo que todos conocemos es una CocaCola y la que mas podemos encontrarnos en el dia a dia es la de 2.25L regular. Ingresamos el nombre y seleccionamos el producto. 

<div align="center">
 <img src="https://user-images.githubusercontent.com/42218625/217664785-bbaa5d83-ccdc-4503-ae2b-8b3710e5b182.png" width="650" height="280"/>
</div>

> Tip: En lugar de buscar por el nombre de un producto, es preferible hacerlo por su SKU, en este caso el mismo es `0228801` que se ve a la derecha de la imagen

4. Identificamos el dato que queremos extraer. En este caso el precio del producto. 
5. Una vez que ya conocemos todos los pasos podemos comenzar a codear el web scraper. Para ello no voy a entrar en muchos detalles ya que el codigo compleeto pueden enconrtarlo con todos los comentarios necesarios aca [`ACA`](web_scraper_object_git.py)

Si no es de su agrado ver codigo con tantos comentarios hay una version "limpia" en este otro [`LINK`](web_scraper_object_raw.py)

Una breve explicacion de que fue lo que se hizo en el codigo:

1. Creamos una instancia del WebDriver de Chrome 
    ```python
    class WebDriver(object):
    ```
2. Creamos una funcion que va a obtener todas las provincias y localidades que posee la cadena de supermercados 
    ```python
    def get_prov(driver):
    ...
    ...
    return(prov_loc)
    ```
3. Usamos ese parametro de entrada de una nueva funcion para obtener los precios del producto deseado en cada una de las localidades
    ```python
    def get_precios(driver,prov_loc):
    ...
    ...
    return(df)
    ```
4. Una ves que tengamos los precios y las localidades solo queda subirlo al bucket S3 que se designo para eso
    ```python
    def up_csv_s3(df):
    ```
    > Importante: Para configurar el bucket S3 vean el post que sugiero mas arriba. 
5. Por ultimo creamos el `lambda_handler` necesario para ejecutar la funcion en Lamnda de AWS. 
    ```python
    def lambda_handler(event,context):
    ```
6. Una vez que todo esto esta configurado de manera correcta, llega el momento de entrar en AWS para configurar la funcion Lambda y el gatillo que la disparara con EventBridge. Para ver un tutorial detallado de como hacerlo pueden ingresar [`AQUI`](https://blog.jovian.com/automate-web-scraping-using-python-aws-lambda-amazon-s3-amazon-eventbridge-cloudwatch-c4c982c35fa9)


## Tecnología
Todos estas librerias deben ser compatibles para la misma version de Python. En este caso se realizo en la version 3.7

Pueden descargarlas desde PYPI o desde este [enlace](Librerias)
| Tecnologia     |Versión                         |Link                         |
|----------------|-------------------------------|-----------------------------|
|Pandas          |1.3.5                          |https://pypi.org/project/pandas/1.3.5/            |
|Numpy           |1.19.0                         |https://pypi.org/project/numpy/1.19.0/            |
|Pytz            |2021.1                         |https://pypi.org/project/pytz/2021.1/|
|Selenium        |3.141.0                          |https://pypi.org/project/selenium/3.141.0/       |

## Resultado

Haciendo click en este [`LINK`](https://webscraperjp.s3.sa-east-1.amazonaws.com/asd.csv) podra descargar el archivo CSV que contiene los datos que el web scraper recolecta diariamente. 

> Nota: si descarga el archivo, notara que en algunos se recopilo informacion mas de una vez por dia. Esto se debe a que fue necesario ralizar algunos test del script en AWS, lo que genero que se cargara informacion durante el test y durante la ejecucion normal del dia. 

Si bien el archivo se encuentra en CSV. En su formato tabular se veria algo como lo siguiente:

| Fecha     | Hora      | Provincia     | Localidad   | Precio     | 
|------------|-----------|--------------|-------------|-----------|
|12/01/2023  | 23:50:45  | BUENOS AIRES  | 9 DE JULIO  | $ 382,50  |
|12/01/2023  | 23:50:49  | BUENOS AIRES  | AZUL  | $ 390,00  |
|12/01/2023  | 23:50:52  | BUENOS AIRES  | BRAGADO  | $ 390,00  |
|......  | ...... | ...... | ......  | $ ...... |
|12/01/2023  | 23:53:39  | TIERRA DEL FUEGO  | USHUAIA  | $ 409,00  |




