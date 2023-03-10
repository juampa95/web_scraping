# -*- coding: utf-8 -*-
try:
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    import boto3
    import csv
    from io import StringIO
    from datetime import datetime
    from datetime import timedelta
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.keys import Keys
    import pandas as pd 
    import time
    print("All Modules are ok ...")

except Exception as e:
    print("Error in Imports ")
# esta es la URL usada para recopilar datos. 
URL = 'https://supermercado.laanonimaonline.com/'

class WebDriver(object):

    def __init__(self):
        self.options = Options()
        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')

    def get(self):
        driver = Chrome('/opt/chromedriver', options=self.options)
        return driver

def get_prov(driver):
  # Se busca el elemento para hacer click a traves del selector CSS
  element = driver.find_element(By.CSS_SELECTOR, 
                                '#maq_cabezal_content > div > div.cabezal_derecho > div.sucursal_actual.izq')
  # Click en boton para seleccionar sucursal   
  driver.execute_script("arguments[0].click();", element) 

  time.sleep(1)

  # Aparece una ventana emergente en donde debemos seleccionar provincia y sucursal
  popup = driver.find_element(By.CSS_SELECTOR, "body > div.modal-wrapper > div.modal-content")
  # Guardo en una lista todas las provincias 
  lista = popup.find_element(By.ID , 'sel_provincia').find_elements(By.TAG_NAME , 'option')
  # con este bucle recorro las sucursales que hay en cada provincia y las guardo 
  # en una nueva lista llamada prov_loc conformada por la Provincia + localidad de sucursal 
  prov_loc = []
  for i in range(1,len(lista)):
    localidad = popup.find_element(By.ID , 'sel_localidad_' + lista[i].get_attribute('value')).find_elements(By.TAG_NAME , 'option')
    for j in range(1,len(localidad)):
      try:
        loc = localidad[j].get_attribute("textContent")
        id_loc = localidad[j].get_attribute("value")
        prov_loc.append((lista[i].get_attribute('value'),lista[i].text,id_loc, loc))
      except:
        pass
  return(prov_loc)

def get_precios(driver,prov_loc):
  # Buscamos en cada provincia y sucursal almacenadas en la lista prov_loc los 
  # precios del item. 
  precios = []
  for i in prov_loc:
    try:
      driver.refresh()

      time.sleep(1)

      # Se busca el elemento para hacer click
      element = driver.find_element(By.CSS_SELECTOR, 
                                    '#maq_cabezal_content > div > div.cabezal_derecho > div.sucursal_actual.izq')
      # Click en boton para seleccionar sucursal
      driver.execute_script("arguments[0].click();", 
                            element) 
      # Aparece una ventana emergente en donde debemos seleccionar provincia y sucursal
      popup = driver.find_element(By.CSS_SELECTOR, "body > div.modal-wrapper > div.modal-content")

      time.sleep(0.5)
      # En esa ventana emergente, selecionamos la provincia 
      sel_prov = Select(popup.find_element(By.CSS_SELECTOR, '#sel_provincia'))
      sel_prov.select_by_visible_text(i[1])

      time.sleep(0.5)
      # Una vez en esa provincia, seleccionamos la localidad. 
      sel_suc = Select(popup.find_element(By.ID, 'sel_localidad_'+ i[0])) 
      sel_suc.select_by_visible_text(i[3])

      # No vamos a seleccionar ninguna sucursal ya que solo hay una por localidad
      time.sleep(0.5)
      # Hacemos click en confirmar
      popup.find_element(By.CSS_SELECTOR, '#vtn_mostrar > div > div.text_center > div.btn.estandar.cursor_pointer').click()
      
      time.sleep(0.5)
      # Hacemos click en la barra del buscador
      buscador = driver.find_element(By.ID, "buscar")   
      buscador.click()
      # ingresamos el sku del item "0228801" y apretamos ENTER
      # en esta oportunidad el SKU corresponde a una Coca Cola regular de 2.5L
      buscador.send_keys('0228801' + Keys.ENTER)  
      # Guardamos la card del producto como un elemento y buscamos el contenedor-plus que tiene el precio
      card = driver.find_elements(By.CLASS_NAME, 'contenedor-plus')  
      # Guardamos el valor del item en la variable precio
      precio = card[0].text
      # obtenemos la hora del momento en que se adquieren estos datos y los 
      # guardamos junto con el precio en la lista precios 
      now = datetime.now()- timedelta(hours= +3)
      precios.append([now.strftime('%Y/%m/%d'),now.strftime('%H:%M:%S'),i[1],i[3], precio])
    except:
      pass
  # Cuando terminamos de armar la lista con todas las sucursales la pasamos a 
  # un DataFramee de pandas. 
  df = pd.DataFrame(precios)
  return(df)

def up_csv_s3(df):
# Para ingresar a el Bucket de S3 donde tengo almacenado el archivo CSV es necesario 
# hacerlo mediante una KEY privada que voy a tener que borrar. Ya que la misma
# da acceso a leer y escribir dentro del bucket. 
  try:
    AWS_S3_BUCKET = "webscraperjp"
    AWS_ACCESS_KEY_ID = "ID"
    AWS_SECRET_ACCESS_KEY  = "Key"
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    # Vamos a leer el archivo anterior para ir apilando informacion sobre este 
    s3_object = s3_client.get_object(Bucket="webscraperjp", Key='asd.csv')
    data_read = s3_object['Body'].read().decode('utf-8')
    string = StringIO(data_read)
    df_s3 = pd.read_csv(string, sep =",")
    df_s3 = df_s3.set_axis(['fecha','hora','provincia','localidad','precio'],axis=1)
    df_scraping = df.set_axis(['fecha','hora','provincia','localidad','precio'],axis=1)
    # Una vez que leemos el archivo lo concatenamos con el nuevo. 
    df_new = pd.concat([df_s3,df_scraping])
    df_csv = df_new.to_csv(index=False)
    # Cuando esta concatenado lo volvemos a subir al bucket s3 
    s3_client.put_object(Body=df_csv, Bucket='webscraperjp', Key='asd.csv')
  except:
    pass

def lambda_handler(event,context):
    instance_ = WebDriver()
    driver = instance_.get()
    driver.get(URL)
    print('Fetching the page') 
    localidades = get_prov(driver)
    precios = get_precios(driver,localidades)
    
    driver.close()
    driver.quit()

    up_csv_s3(precios)

    return('precios actualizados')

if __name__ == "__main__":
    lambda_handler(None, None)
