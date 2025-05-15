import requests
from bs4 import BeautifulSoup

def buscar_producto(palabra):
    # URL de búsqueda en Mercado Libre
    url = f"https://listado.mercadolibre.com.co/{palabra.replace(' ', '-')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    # Solicitud HTTP
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Buscar productos
    productos = soup.select('li.ui-search-layout__item')
    print(f"\nResultados para: '{palabra}' en Mercado Libre Colombia\n")
    if not productos:
        print("No se encontraron productos.")
        return
    # Mostrar los primeros 5 productos
    for i, producto in enumerate(productos[:5]):
        try:
            # Título
            titulo_tag = producto.select_one('h2.ui-search-item__title')
            if not titulo_tag:
                titulo_tag = producto.select_one('h2')
            titulo = titulo_tag.text.strip() if titulo_tag else "Sin título"

            # Precio
            precio_entero = producto.select_one('span.andes-money-amount__fraction')
            precio_decimal = producto.select_one('span.andes-money-amount__cents')
            precio = precio_entero.text if precio_entero else "?"
            if precio_decimal:
                precio += f",{precio_decimal.text}"
            # Enlace
            enlace_tag = producto.select_one('a.ui-search-link')
            enlace = enlace_tag['href'] if enlace_tag else "Sin enlace"
            print(f"{i + 1}. {titulo} - ${precio}")
            print(f"   🔗 {enlace}")
        except Exception as e:
            print(f"{i + 1}. Error al procesar producto: {e}")
# Bucle para permitir nuevas búsquedas
while True:
    palabra = input("\nIngresa una palabra clave a buscar (o escribe 'salir' para terminar): ").strip()
    if palabra.lower() == 'salir':
        print("Programa finalizado.")
        break
    elif palabra == '':
        print("Debes ingresar una palabra.")
    else:
        buscar_producto(palabra)
