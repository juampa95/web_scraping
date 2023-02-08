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
URL = 'https://supermercado.laanonimaonline.com/'
S
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
  element = driver.find_element(By.CSS_SELECTOR, 
                                '#maq_cabezal_content > div > div.cabezal_derecho > div.sucursal_actual.izq') 
  driver.execute_script("arguments[0].click();", element) 
  time.sleep(1)
  popup = driver.find_element(By.CSS_SELECTOR, "body > div.modal-wrapper > div.modal-content")
  lista = popup.find_element(By.ID , 'sel_provincia').find_elements(By.TAG_NAME , 'option')
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
  precios = []
  for i in prov_loc:
    try:
      driver.refresh()
      time.sleep(1)
      element = driver.find_element(By.CSS_SELECTOR, 
                                    '#maq_cabezal_content > div > div.cabezal_derecho > div.sucursal_actual.izq')
      driver.execute_script("arguments[0].click();", 
                            element) 
      popup = driver.find_element(By.CSS_SELECTOR, "body > div.modal-wrapper > div.modal-content")
      time.sleep(0.5)
      sel_prov = Select(popup.find_element(By.CSS_SELECTOR, '#sel_provincia'))
      sel_prov.select_by_visible_text(i[1])
      time.sleep(0.5)
      sel_suc = Select(popup.find_element(By.ID, 'sel_localidad_'+ i[0])) 
      sel_suc.select_by_visible_text(i[3])
      time.sleep(0.5)
      popup.find_element(By.CSS_SELECTOR, '#vtn_mostrar > div > div.text_center > div.btn.estandar.cursor_pointer').click()     
      time.sleep(0.5)
      buscador = driver.find_element(By.ID, "buscar")   
      buscador.click()
      buscador.send_keys('0228801' + Keys.ENTER)  
      card = driver.find_elements(By.CLASS_NAME, 'contenedor-plus')  
      precio = card[0].text
      now = datetime.now()- timedelta(hours= +3)
      precios.append([now.strftime('%Y/%m/%d'),now.strftime('%H:%M:%S'),i[1],i[3], precio])
    except:
      pass
  df = pd.DataFrame(precios)
  return(df)

def up_csv_s3(df):
  try:
    AWS_S3_BUCKET = "webscraperjp"
    AWS_ACCESS_KEY_ID = "ID"
    AWS_SECRET_ACCESS_KEY  = "Key"
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    s3_object = s3_client.get_object(Bucket="webscraperjp", Key='asd.csv')
    data_read = s3_object['Body'].read().decode('utf-8')
    string = StringIO(data_read)
    df_s3 = pd.read_csv(string, sep =",")
    df_s3 = df_s3.set_axis(['fecha','hora','provincia','localidad','precio'],axis=1)
    df_scraping = df.set_axis(['fecha','hora','provincia','localidad','precio'],axis=1)
    df_new = pd.concat([df_s3,df_scraping])
    df_csv = df_new.to_csv(index=False)
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
