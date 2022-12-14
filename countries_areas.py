### **Obteniendo Dataset de Países del mundo con su Población y Superficie**

# Importando librerías
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

# Enlace con la tabla de todos los Países del mundo con su Población y Superficie
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

# Revisar countries_areas.csv
pd.read_csv('countries_areas.csv')

# Convirtiendo countries_areas.csv a DataFrame
df_countries_areas = pd.DataFrame(pd.read_csv('countries_areas.csv'))

# Revisar DataFrame
df_countries_areas

# Eliminando índice duplicado
df_countries_areas = df_countries_areas.drop(columns=['#'])

# Revisar DataFrame
df_countries_areas


### **Obteniendo Dataset con las Subregiones continentales de los Países del mundo**

# Enlaces de las tablas de los Países por Subregión continental
urls_subregs_by_continents = [
    "https://www.worldometers.info/geography/how-many-countries-in-africa/",
    "https://www.worldometers.info/geography/how-many-countries-in-asia/",
    "https://www.worldometers.info/geography/how-many-countries-in-europe/",
    "https://www.worldometers.info/geography/how-many-countries-in-latin-america/",
    "https://www.worldometers.info/geography/how-many-countries-in-oceania/",
    "https://www.worldometers.info/geography/how-many-countries-in-northern-america/"]

# Obteniendo tabla de Países por Subregión continental (scraping)
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

# Revisar archivo subregs_by_continents.csv
pd.read_csv('subregs_by_continents.csv')

# Convirtiendo subregs_by_continents.csv a DataFrame
df_subregs_by_continents = pd.DataFrame(pd.read_csv('subregs_by_continents.csv'))

# Revisar DataFrame de Países por Subregión continental
df_subregs_by_continents

# Eliminando las cabeceras duplicadas de las tablas extraídas
df_subregs_by_continents = df_subregs_by_continents.drop_duplicates()

# Revisar eliminación de cabeceras duplicadas
df_subregs_by_continents

# Eliminando 54va fila correspondiente a cabecera remanente
df_subregs_by_continents = df_subregs_by_continents.drop(54)

# Revisar DataFrame de Países por Subregión continental
df_subregs_by_continents


### **Fusionando y limpiando los DataFrames**

# Fusionando datasets
merged_countries_table = pd.merge(df_countries_areas, df_subregs_by_continents, 'outer', 'Country')

# Revisar fusión de datasets
merged_countries_table

# Renombrando columnas
renamed_merged_table = merged_countries_table.rename(columns = {'Population(2020)_x': 'Population_2020', 'World Share': 'World_Share', 'Land Area (Km²)': 'Land_Area_(Km²)'})

# Revisar renombrado de columnas
renamed_merged_table

# Eliminando columnas de índice y población repetidas
almost_done_table = renamed_merged_table.drop(columns =['#', 'Population(2020)_y'])

# Revisar eliminación de las columnas
almost_done_table

# Eliminando filas de cabeceras remanentes
final_countries_table = almost_done_table.drop_duplicates()

# Revisar Tabla final limpia
final_countries_table


## *Importando NumPy para manipular columnas y poder graficarlas posteriormente*
import numpy as np

# Creación de una copia del Dataset como array
countries_table_arr = np.array(final_countries_table)

# Revisar copia del Dataset como array
countries_table_arr

# Trasposición del array para obtención de columnas
countries_table_arr = countries_table_arr.T

# Revisar trasposición
countries_table_arr

# Obtención y asignación de columnas
Paises = countries_table_arr[0]
Poblacion_2020 = countries_table_arr[1]
Porcentaje_del_Total = countries_table_arr[2]
Superficie = countries_table_arr[3]
Subregion = countries_table_arr[4]


### **Preparación, formateo de Tipo de dato y normalización de columnas para EDA**

## *Obteniendo columna Countries de tipo Object ('O') y transformándola a tipo string 'Unicode' ('<U10')*

# Obteniendo columna Countries (['Country']) tipo 'Object' ('O')
Countries = final_countries_table['Country']

# Revisar tipo de dato
Countries.dtype

# Transformando columna Countries de tipo Object ('O') a array tipo string 'Unicode' ('<U10')
Countries_str = Countries.to_string()
# Eliminando espacios vacíos
Countries_str = Countries_str.split()
# Transformando string "Paises_str" en 'array' con NumPy
Countries_arr = np.array(Countries_str)

# Comprobar transformación de tipo y eliminación de espacios vacíos en el array Countries_arr
Countries_arr

# Comprobar cantidad de elementos de columna "Countries_arr"
len(Countries_arr)

# Creando rango de números correspondiente a los índices a excluir del array Countries_arr
num_range_arr_str = np.arange(0,195).astype('str')

# Revisar rango creado
num_range_arr_str

# Eliminando números de índice incluidos por defecto en el array Countries_arr y pasando el mismo a una lista Countries_list
Countries_list = []
Countries_list = Countries_arr.tolist()
for i in num_range_arr_str:
    if i in Countries_list:
        Countries_list.remove(i)
        
# Revisar lista Countries_list limpia
Countries_list

# Creando lista de nombres compuestos a eliminar
to_clean = ["States", "Congo", "Kingdom", "Africa", "Korea", "Arabia", "d'Ivoire", "Korea" "Lanka", "Faso", "Sudan", "Republic", "Republic", "(Czechia)", 
            "Arab", "Emirates", "New", "Guinea" "Leone", "Salvador", "of", "Palestine", "Rica", "African", "Republic", "Zealand", "and", "Herzegovina", 
            "Macedonia", "Guinea", "and", "Tobago", "Islands", "Verde", "Tome", "&", "Principe", "Lucia", "Vincent", "&", "Granadines", "and", "Barbuda", 
            "Islands", "Kitts", "&", "Nevis", "Marino", "See"]

# Definiendo función que elimina los nombres compuestos
Countries_clean = Countries_list
def cleaning(Countries_clean):
  for i in to_clean:
    if i in Countries_clean:
      Countries_clean.remove(i)

# Aplicando tres veces la función de limpieza de nombres compuestos debido a "Guinea" repetido
cleaning(Countries_clean)
cleaning(Countries_clean)
cleaning(Countries_clean)

# Comprobar limpieza de nombres compuestos
Countries_clean

# Añadiendo a Guinea eliminado en el paso anterior en su respectivo índice
Countries_clean.insert(73, 'Guinea')

# Renombrando Countries de nombre compuesto
Countries = Countries_clean
Countries[2] = "United States"
Countries[15] = "DR Congo"
Countries[20] = "United Kingdom"
Countries[24] = "South Africa"
Countries[27] = "South Korea"
Countries[40] = "Saudi Arabia"
Countries[52] = "Côte d'Ivoire"
Countries[53] = "North Korea"
Countries[56] = "Sri Lanka"
Countries[57] = "Burkina Faso"
Countries[82] = "South Sudan"
Countries[83] = "Dominican Republic"
Countries[84] = "Czech Republic (Czechia)"
Countries[91] = "United Arab Emirates"
Countries[96] = "Papua New Guinea"
Countries[101] = "Sierra Leone"
Countries[109] = "El Salvador"
Countries[118] = "State of Palestine"
Countries[119] = "Costa Rica"
Countries[122] = "Central African Republic"
Countries[123] = "New Zealand"
Countries[132] = "Bosnia and Herzegovina"
Countries[144] = "North Macedonia"
Countries[149] = "Equatorial Guinea"
Countries[150] = "Trinidad and Tobago"
Countries[161] = "Solomon Islands"
Countries[165] = "Cabo Verde"
Countries[175] = "Sao Tome & Principe"
Countries[177] = "Saint Lucia"
Countries[180] = "St. Vincent & Grenadines"
Countries[183] = "Antigua and Barbuda"
Countries[186] = "Marshall Islands"
Countries[187] = "Saint Kitts & Nevis"
Countries[190] = "San Marino"
Countries[194] = "Holy See"

# Revisar longitud de la lista Countries: ok
len(Countries)

# Revisar lista Countries: ok
Countries

## *Obteniendo columna Population de tipo Object ('O') y transformándola a tipo string 'Unicode' ('<U10'), eliminando separador de miles "," y luego a tipo entero ('int32')*

# Obteniendo columna Population tipo Object ('O'), transformando a tipo string 'Unicode' ('<U10') y eliminando separador de miles ","
Population_str = final_countries_table['Population_2020'].to_string().replace(',', '')
# Eliminando espacios vacíos
Population_str = Population_str.split()
# Transformando string "Population_str" en 'array' con NumPy
Population_arr = np.array(Population_str)
# Descartando índice contenido en cada elemento del array
Population_arr_x = Population_arr[1:-2:2]
# Añadiendo elemento Population correspondiente a la Santa Sede ('Holy See') al array, previamente excluído del rango de indexación en el paso anterior
Population = np.append(Population_arr_x, Population_arr[-1])
# Transformando Poblacion de tipo string Unicode ('<U10') a tipo entero ('int32')
Population_2020 = Population.astype('int32')

# Revisar el tipo de dato del array Population:
Population_2020.dtype

# Convirtiendo el array Population en una lista
Population_2020.tolist()

# Revisar longitud de la lista Population: ok
len(Population_2020)

# Revisar lista Population: ok
Population_2020

## *Obteniendo columna Land_Area_Km² de tipo Object ('O') y transformándola a tipo string 'Unicode' ('<U10'), eliminando separador de miles "," y luego a tipo entero ('int32')*

# Obteniendo columna Land_Area_Km² tipo Object ('O'), transformando a tipo string 'Unicode' ('<U10') y eliminando separador de miles ","
Land_Area_Km2_str = final_countries_table['Land_Area_(Km²)'].to_string().replace(',', '')
# Eliminando espacios vacíos
Land_Area_Km2_str = Land_Area_Km2_str.split()
# Transformando string "Population_str" en 'array' con NumPy
Land_Area_Km2_arr = np.array(Land_Area_Km2_str)
# Descartando índice contenido en cada elemento del array
Land_Area_Km2_arr_x = Land_Area_Km2_arr[1:-2:2]
# Añadiendo elemento Population correspondiente a la Santa Sede ('Holy See') al array, previamente excluído del rango de indexación en el paso anterior
Land_Area_Km2 = np.append(Land_Area_Km2_arr_x, Land_Area_Km2_arr[-1])
# Transformando Poblacion de tipo string Unicode ('<U10') a tipo entero ('int32')
Land_Area_Km2 = Land_Area_Km2.astype('int32')

# Revisar el tipo de dato del array Land_Area_Km2:
Land_Area_Km2.dtype

# Convirtiendo el array Land_Area_Km2 en una lista
Land_Area_Km2.tolist()

# Revisar longitud de la lista Land_Area_Km2: ok
len(Land_Area_Km2)

# Revisar lista Land_Area_Km2: ok
Land_Area_Km2

## *Obtención de Subregiones*

# Clasificando Subregion por continente al que pertenece
Africa = []
for subregion in final_countries_table['Subregion']:
  if 'Africa' in subregion:
    Africa.append(subregion)

Asia = []
for subregion in final_countries_table['Subregion']:
  if 'Asia' in subregion:
    Asia.append(subregion)

Europe = []
for subregion in final_countries_table['Subregion']:
  if 'Europe' in subregion:
    Europe.append(subregion)

South_America = []
for subregion in final_countries_table['Subregion']:
  if 'South America' in subregion or 'Caribbean' in subregion or 'Central America' in subregion:
    South_America.append(subregion)

Oceania = []
for subregion in final_countries_table['Subregion']:
  if 'Melanesia' in subregion or 'Micronesia' in subregion or 'Polynesia' in subregion or 'Australia and New Zealand' in subregion:
    Oceania.append(subregion)

Northern_America = []
for subregion in final_countries_table['Subregion']:
  if 'Northern America' in subregion:
    Northern_America.append(subregion)
    
# Subegiones del contienente africano
Africa

# Subegiones del continente asiático
Asia

# Subegiones del continente europeo
Europe

# Subegiones del continente sudamericano
South_America

# Subegiones del continente oceánico
Oceania

# Subregiones del continente norteamericano
Northern_America


### EDA básico

# Ver cantidad de filas x columnas del DataFrame
final_countries_table.shape

# Información general del DataFrame
final_countries_table.info()

# Descripción general del DataFrame (count, unique, top, freq)
final_countries_table.describe()

# Descripción general de Países (count, unique, top, freq)
final_countries_table['Country'].describe()

#Descripción general de Población (count, unique, top, freq)
final_countries_table['Population_2020'].describe()

# Población mínima de un país ('Holy See' - Vaticano)
Population_2020.min()

# Población máxima de un país ('China')
Population_2020.max()

# Superficie mínima de un país ('Holy See' - Vaticano)
Land_Area_Km2.min()

# Superficie máxima de un país ('Russia')
Land_Area_Km2.max()
