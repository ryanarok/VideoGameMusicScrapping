import requests
from urllib import request
from bs4 import BeautifulSoup

print('Introduzca el enlace de la pagina para descargar:')

url = input()#'https://downloads.khinsider.com/game-soundtracks/album/the-last-story'

print('Deseas listar y luego descargar? (y/n)')

download_last = (True if input().lower() == 'y' else False)

print('Deseas decidir descargar solo determinados archivos? (y/n)')

decide = (True if input().lower() == 'y' else False)

print('Rango de archivos que quieres descargar:')
ran = range(int(input()),int(input())+1)

#
##
###
#ARREGLAR %%%%%%%%%%%%%%%%%%
###
##
#

st = {"set"}
to_download = []


def download(_link, _name, _number):
    decision = True
    if _number in ran:
        if decide:
            print('Deseas descargar \''+_name+'\'? (y/n)')
            decision = (True if input().lower() == 'y' else False)
        
        if decision:
            print('Descargando: '+_name)
            request.urlretrieve(_link, _name)

def get_list_of_mp3s(_url, _number):
    response = requests.get(_url)
    if response.status_code == 200: 
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los enlaces en la página
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')
            sref = str(href)
            # Imprimir el atributo href de cada enlace
            if(str(type(href))=='<class \'str\'>'):
                if(sref.find('.mp3')!=-1):
                    if(not (sref in st)):

                        name = sref[sref.rfind('/')+1:len(sref)]
                        name = name.replace('%20', ' ')

                        to_download.append((sref, name, _number))
                        if not download_last:
                            download(sref,name,_number)
                        
        
        
    else:
        print('Error al acceder al archivo:', response.status_code)

def download_mp3s(_url):
    response = requests.get(_url)
    if response.status_code == 200: 

        print('OK')
        linksfile = open('links.txt', 'a')
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar todos los enlaces en la página
        links = soup.find_all('a')
        counter = 1
        print('Archivos a descargar:')
        for link in links:
            
            href = link.get('href')
            sref = str(href)
            # Imprimir el atributo href de cada enlace
            if(str(type(href))=='<class \'str\'>'):
                if(sref.find('.mp3')!=-1):
                    if(not (sref in st)):
                        linksfile.write(href+'\n')
                        get_list_of_mp3s('https://downloads.khinsider.com'+sref, counter)

                        st.add(sref)
                        counter+=1

        if download_last:
            for file in to_download:
                download(file[0], file[1])
        
    else:
        print('Error al acceder a la página:', response.status_code)

download_mp3s(url)

print('Descarga finalizada')