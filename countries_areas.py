### **Obteniendo Dataset de paises del mundo con su población y superficie**

# importando librerias
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

# Enlace con la tabla de todos los paises del mundo con su población y superficie
url_countries_areas = 'https://www.worldometers.info/geography/how-many-countries-are-there-in-the-world/'

# Obteniendo la tabla (scraping)
class TableScraper_areas:
    results = []

    def fetch(self, url_countries_areas):
      return requests.get(url_countries_areas)

    def parse(self, html):
      content = BeautifulSoup(html, 'lxml')
      table = content.find('div', class_='table-responsive')
      rows = table.findAll('tr')
      self.results.append([header.text for header in rows[0].findAll('th')])
      
      for row in rows:
        if len(row.findAll('td')):
          self.results.append([data.text for data in row.findAll('td')])
   
    def to_csv(self):
        with open('countries_areas.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.results)
   
    def run(self):
        response = self.fetch(url_countries_areas)
        self.parse(response.text)
        self.to_csv()

if __name__ == '__main__':
    scraper = TableScraper_areas()
    scraper.run()

# Comprobar countries_areas.csv
pd.read_csv('countries_areas.csv')

# countries_areas.csv a DataFrame
df_countries_areas = pd.DataFrame(pd.read_csv('countries_areas.csv'))

# Comprobar DataFrame
df_countries_areas

# Eliminando índice duplicado
df_countries_areas = df_countries_areas.drop(columns=['#'])

# Ver DataFrame
df_countries_areas


### **Obteniendo Dataset con las subregiones de los paises del mundo**

#Enlaces con las tablas de los paises por subregión continental
urls_subregs_by_continents = [
    "https://www.worldometers.info/geography/how-many-countries-in-africa/",
    "https://www.worldometers.info/geography/how-many-countries-in-asia/",
    "https://www.worldometers.info/geography/how-many-countries-in-europe/",
    "https://www.worldometers.info/geography/how-many-countries-in-latin-america/",
    "https://www.worldometers.info/geography/how-many-countries-in-oceania/",
    "https://www.worldometers.info/geography/how-many-countries-in-northern-america/"]

#Obteniendo la tabla (scraping)
class TableScraper_subregs_by_continents:
    results = []

    def fetch(self, url):
      return requests.get(url)

    def parse(self, html):
      content = BeautifulSoup(html, 'lxml')
      table = content.find('div', class_='table-responsive')
      rows = table.findAll('tr')
      self.results.append([header.text for header in rows[0].findAll('th')])
      
      for row in rows:
        if len(row.findAll('td')):
          self.results.append([data.text for data in row.findAll('td')])
   
    def to_csv(self):
        with open('subregs_by_continents.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.results)
   
    def run(self):
      for url in urls_subregs_by_continents:
        response = self.fetch(url)
        self.parse(response.text)
        self.to_csv()

if __name__ == '__main__':
    scraper = TableScraper_subregs_by_continents()
    scraper.run()

#Comprobar subregs_by_continents.csv
pd.read_csv('subregs_by_continents.csv')

#Convirtiendo subregs_by_continents.csv a DataFrame
df_subregs_by_continents = pd.DataFrame(pd.read_csv('subregs_by_continents.csv'))

#Comprobar DataFrame
df_subregs_by_continents

#Eliminando las cabeceras duplicadas de las tablas extraidas
df_subregs_by_continents = df_subregs_by_continents.drop_duplicates()

#Comprobar eliminación de cabeceras duplicadas
df_subregs_by_continents

#Eliminar 54va fila correspondiente a cabecera remanente
df_subregs_by_continents = df_subregs_by_continents.drop(54)

#Ver DataFrame
df_subregs_by_continents

### **Fusionando y limpiando los DataFrames**

#Fusionando
merged_countries_table = pd.merge(df_countries_areas, df_subregs_by_continents, 'outer', 'Country')

#Comprobar fusión
merged_countries_table

#Renombrando columna de población
renamed_merged_table = merged_countries_table.rename(columns = {'Population(2020)_x': 'Population (2020)'})

#Comprobar renombrado
renamed_merged_table

#Eliminando columnas de índice y población repetidas
almost_done_table = renamed_merged_table.drop(columns =['#', 'Population(2020)_y'])

#Comprobar eliminación de las columnas
almost_done_table

#Eliminando filas de cabeceras remanentes
final_countries_table = almost_done_table.drop_duplicates()

#Tabla final limpiada
final_countries_table
