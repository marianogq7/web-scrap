from bs4 import BeautifulSoup
import requests
import pandas as pd

url = input("Ingresar URL:")
#'http://apps01.coto.com.ar/TicketMobile/Ticket/NDQ0Ny8zNDQ1LzIwMjQxMTMwLzE1OC8wMDAwMTYxNjcwOQ=='
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

#Equipos

productosTicket = soup.find_all('h2', class_='width-80 info-producto-h2')
preciosTicket = soup.find_all('div', class_='width-20 info-producto-price')
descuentosTicket = soup.find_all('div', class_='width-20 precio-descuento desc-banco')

#print(soup)
#test = soup.find_all('h1', class_='main-title')
#texto = test[0].text
#print(texto)
listaProductos = list()
for producto in productosTicket:
    listaProductos.append(producto.text)

listaPrecios = list()
for precio in preciosTicket:
    listaPrecios.append(precio.text)
listaDescuentos = list()
for descuento in descuentosTicket:
    listaDescuentos.append(descuento.text)


df = pd.DataFrame({'Producto':listaProductos,'Precio':listaPrecios, 'Descuento': listaDescuentos})
print(df)