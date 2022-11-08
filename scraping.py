# **Obteniendo Dataset de paises del mundo con su población y superficie**

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