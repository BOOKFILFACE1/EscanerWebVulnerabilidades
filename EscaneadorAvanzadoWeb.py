import requests
import re
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Definir argumentos de línea de comandos
parser = argparse.ArgumentParser(description='Escaneo de vulnerabilidades de páginas web')
parser.add_argument('-u', '--url', help='URL del sitio web a escanear', required=True)
parser.add_argument('-t', '--tipo', help='Tipo de escaneo (1-3)', type=int, choices=[1, 2, 3], required=True)
args = parser.parse_args()

# Obtener el dominio del sitio web
url = urlparse(args.url)
dominio = url.netloc

# Definir patrones de expresión regular para encontrar vulnerabilidades
patron_sql_inyeccion = re.compile(r"(error|warning|you have an error in your sql syntax)", re.IGNORECASE)
patron_xss = re.compile(r"(document\.cookie|alert\()", re.IGNORECASE)
patron_csrf = re.compile(r"(input.*?hidden.*?name|input.*?type.*?hidden)", re.IGNORECASE)

# Función para encontrar vulnerabilidades SQLi
def encontrar_sql_inyeccion(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.find(string=patron_sql_inyeccion):
            print(f'[+] SQLi detectado en {url}')

# Función para encontrar vulnerabilidades XSS
def encontrar_xss(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.find(string=patron_xss):
            print(f'[+] XSS detectado en {url}')

# Función para encontrar vulnerabilidades CSRF
def encontrar_csrf(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.find(string=patron_csrf):
            print(f'[+] CSRF detectado en {url}')

# Escanear el sitio web según el tipo de escaneo seleccionado
if args.tipo == 1:
    # Escaneo básico
    print('[*] Iniciando escaneo básico...')
    for link in BeautifulSoup(requests.get(args.url).text, 'html.parser').findAll('a', href=True):
        if link['href'].startswith('http'):
            encontrar_sql_inyeccion(link['href'])
            encontrar_xss(link['href'])
            encontrar_csrf(link['href'])
elif args.tipo == 2:
    # Escaneo avanzado
    print('[*] Iniciando escaneo avanzado...')
    for link in BeautifulSoup(requests.get(args.url).text, 'html.parser').findAll('a', href=True):
        if link['href'].startswith('http'):
            encontrar_sql_inyeccion(link['href'])
            encontrar_xss(link['href'])
            encontrar_csrf(link['href'])
        elif link['href'].startswith('/'):
            encontrar_sql_inyeccion(f'{url.scheme}://{dominio}{link["href"]}')
            encontrar_xss(f'{url.scheme}://{dominio}{link["href"]}')
            encontrar_csrf(f'{url.scheme}://{dominio}{link["href"]}')
elif args.tipo == 3:
    # Escaneo exhaustivo
    print('[*] Iniciando escaneo exhaust
