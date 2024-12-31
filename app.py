from flask import Flask, render_template, request, send_file
import pandas as pd
import io
from bs4 import BeautifulSoup
import requests

# Tu función de webscraping aquí
def scrape_ticket(url):
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd

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
        
        precio_limpio = None
        if precio:
            precio_limpio = precio.text.strip().replace("$", "")
        # Manejar casos donde los datos podrían no existir
        productos.append({
            'Nombre': nombre.text.strip() if nombre else None,
            'Precio': precio_limpio,
            'Código': codigo.text.strip() if codigo else None,
            'Motivo Descuento': motivo_descuento.text.strip() if motivo_descuento else None,
            'Descuento': descuento.text.strip() if descuento else None,
            'Precio por Cantidad': precio_por_cantidad.text.strip() if precio_por_cantidad else None
        })

    # Imprimir los datos en formato de tabla

    df = pd.DataFrame(productos)
    print(df)
    
    return pd.DataFrame(df)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    try:
        # Obtener la URL desde el formulario
        link = request.form.get('link')
        if not link:
            return "URL no proporcionada", 400

        # Simulación de scraping y creación de datos (esto puede ser reemplazado por tu código de scraping real)
        df = scrape_ticket(link)

        # Convertir DataFrame a diccionario para pasarlo al template
        table_data = df.to_dict(orient='records')

        # Renderizar el template con los datos procesados
        return render_template('index.html', table_data=table_data)
    except Exception as e:
        return f"Error: {e}", 500
# Si no anda, borrar preview
@app.route('/download', methods=['POST'])
def download_csv():
    link = request.form['link']
    if not link:
        return "Por favor ingresa un link válido", 400
    
    # Obtener los datos usando tu función de scraping
    df = scrape_ticket(link)

    # Convertir DataFrame a CSV en memoria
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Enviar archivo al cliente
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='productos.csv'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
