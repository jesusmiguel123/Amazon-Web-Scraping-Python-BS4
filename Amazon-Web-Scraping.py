from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_title(soup):
   h1_title = soup.find_all(
      'h1',
      attrs={
         'id': 'title'
      }
   )[0]
   title = h1_title.find_all(
      'span',
      attrs={
         'id': 'productTitle'
      }
   )[0].text.strip()
   sufix = ""
   words_title = title.split()
   if len(words_title) > 5:
      words_title = words_title[:5]
      sufix = "..."
   return " ".join(words_title) + sufix

def get_currency(soup):
   price_currency = soup.find_all(
      'span',
      attrs={
         'class': 'a-price-symbol'
      }
   )[0].text.strip()
   return price_currency

def get_price(soup):
   price_int = soup.find_all(
      'span',
      attrs={
         'class': 'a-price-whole'
      }
   )[0].text.strip()

   price_dec = soup.find_all(
      'span',
      attrs={
         'class': 'a-price-fraction'
      }
   )[0].text.strip()
   return price_int + price_dec

def get_rating(soup):
   rating = soup.find_all(
      'span',
      attrs={
         'class': 'a-icon-alt'
      }
   )[0].text.strip()
   words_rating = rating.split()
   return words_rating[0]

def get_delivery_date(soup):
   delivery_date = soup.find_all(
      'div',
      attrs={
         'id': 'mir-layout-DELIVERY_BLOCK'
      }
   )[0].find_all(
      'span',
      attrs={
         'class': 'a-text-bold'
      }
   )[0].text.strip()
   return delivery_date

def main():
   print('Web Scraping a Amazon')
   AMAZON_URL = 'https://www.amazon.com'
   URL = 'https://www.amazon.com/s?k=grafica&__mk_es_US=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1HHI6WRXO7GCO&sprefix=grafica%2Caps%2C200&ref=nb_sb_noss_1'
   HEADERS = ({
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
      'Accept-Language': 'es-US, es; q=0.5'
   })
   
   print('Obteniendo HTML de lista de productos...')

   html = requests.get(URL, headers=HEADERS)
   
   print('HTML de lista de productos obtenido exitosamente')
   print('Convirtiendo HTML a BS Object...')

   soup = BeautifulSoup(html.content, 'html.parser')
   
   print('Conversion de HTML a BS Object exitosa')
   print('Obteniendo enlace de productos...')

   links = soup.find_all(
      'a',
      attrs={
         'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'
      }
   )

   print('Enlaces obtenidos')

   d = {
      'Titulo': [],
      'Moneda': [],
      'Precio': [],
      'Calificacion /5': [],
      'Fecha de entrega': []
   }
   
   print('Obteniendo caracteristicas de los productos...')

   for ix, link in enumerate(links):
      url_product = AMAZON_URL + link.get('href')
      html_product = requests.get(url_product, headers=HEADERS)
      soup_product = BeautifulSoup(html_product.content, 'html.parser')
      d['Titulo'].append(get_title(soup_product))
      d['Moneda'].append(get_currency(soup_product))
      d['Precio'].append(get_price(soup_product))
      d['Calificacion /5'].append(get_rating(soup_product))
      d['Fecha de entrega'].append(get_delivery_date(soup_product))
      print(f'\r   Procesados {ix+1}/{len(links)} productos...', end="")

   print('\nCreando DataFrame con las caracteristicas de los productos...')
   
   df_products = pd.DataFrame(d)

   print('DataFrame creado exitosamente')

   return df_products

if __name__ == '__main__':
   df = main()
   print('Guardando DataFrame en "AmazonWebScraping.csv"...')
   df.to_csv('AmazonWebScraping.csv', index=False)
   print('DataFrame guardado exitosamente\nFin')