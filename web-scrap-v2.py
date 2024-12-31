from bs4 import BeautifulSoup
import requests
import pandas as pd

url = input("Ingresar URL:")
#'http://apps01.coto.com.ar/TicketMobile/Ticket/NDQ0Ny8zNDQ1LzIwMjQxMTMwLzE1OC8wMDAwMTYxNjcwOQ=='
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

productos = []
for item in soup.find_all('li', class_='product-li'):
    # Extraer los datos requeridos
    nombre = item.find('h2', class_='width-80 info-producto-h2')
    precio = item.find('div', class_='width-20 info-producto-price')
    codigo = item.find('span', class_='lean text-light-grey')
    motivo_descuento = item.find('div', class_='width-80 info-descuento desc-banco')
    descuento = item.find('div', class_='width-20 precio-descuento desc-banco')
    precio_por_cantidad = item.find('div', class_='width-80 text-light-grey info-cant')

    # Manejar casos donde los datos podrían no existir
    productos.append({
        'Nombre': nombre.text.strip() if nombre else None,
        'Precio': precio.text.strip() if precio else None,
        'Código': codigo.text.strip() if codigo else None,
        'Motivo Descuento': motivo_descuento.text.strip() if motivo_descuento else None,
        'Descuento': descuento.text.strip() if descuento else None,
        'Precio por Cantidad': precio_por_cantidad.text.strip() if precio_por_cantidad else None
    })

# Imprimir los datos en formato de tabla

df = pd.DataFrame(productos)
print(df)