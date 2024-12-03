import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Función para hacer scraping del precio
try:
        # Realizar la solicitud al sitio web
    url = input("ingrese url:")
    response = requests.get(url)
    response.raise_for_status()
        
        # Parsear el contenido HTML
    soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar el elemento con la clase 'precio'
    precio_elemento = soup.find('h1', class_='main-title')
    if precio_elemento:
        print(precio_elemento)
        
        
    else:
        print("No se encontró el elemento de precio.")
        
except Exception as e:
    print(f"Error al obtener el precio: {e}")
    
