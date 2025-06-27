import requests
from urllib import request
from bs4 import BeautifulSoup
import os
import tkinter as tk

# Crear una ventana
ventana = tk.Tk()
ventana.title("Khinsider Downloader")

text_label = tk.Label(ventana, text="Enlace del album a descargar:")
text_label.pack()
text = tk.Text(ventana, height=3)
text.pack()


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "https://www.google.com/"
    }

download_last = tk.BooleanVar()
download_last_switch = tk.Checkbutton(ventana, variable=download_last, text="Listar primero")
download_last_switch.pack()

decide = tk.BooleanVar()
decide_switch = tk.Checkbutton(ventana, variable=decide,text='Descargar determinados archivos')
decide_switch.pack()

album_size = 20 ####GET
ran = range(1,album_size+1)
def update_ran():
    ran = range(int(ran_l.get()),int(ran_r.get())+1)
    ran_l.config(to=ran[-1])
    ran_r.config(from_=ran[0])

range_label=tk.Label(ventana,text="Rango de archivos a descargar")
range_label.pack()
ran_l = tk.Spinbox(ventana,from_=1,to=ran[-1],command=update_ran) #TO RAN_R
ran_l.pack()
ran_r = tk.Spinbox(ventana, from_=ran[0], to=album_size,command=update_ran) ##FIX
ran_r.pack()

format_label=tk.Label(ventana,text="Formato a descargar")
format_label.pack()
file_format = ".mp3"
mp3_rb = tk.Radiobutton(ventana,text="mp3",value='.mp3',variable=file_format,)
mp3_rb.pack()
flac_rb = tk.Radiobutton(ventana,text="flac",value='.flac',variable=file_format)
flac_rb.pack()

download_button = tk.Button(ventana, text="Descargar", command=lambda: download_files(str(text.get("1.0",tk.END)).strip("\n"),file_format))
download_button.pack()

#
##
###
#ARREGLAR %%%%%%%%%%%%%%%%%%
###
##
#

st = {"set"}
to_download = []

folder_name = 'VideoGameMusic'

def download(_link, _name, _number):
    decision = True
    if _number in ran:
        if decide.get():
            print('Deseas descargar \''+_name+'\'? (y/n)')
            decision = (True if input().lower() == 'y' else False)
        
        if decision:
            print('Descargando: '+_name)
            request.urlretrieve(_link, './'+folder_name+'/'+_name)

def get_list_of_files(_url, _number, format):
    response = requests.get(_url, headers=headers)
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
                if(sref.find(format)!=-1):
                    if(not (sref in st)):

                        name = sref[sref.rfind('/')+1:len(sref)]
                        name = name.replace('%20', ' ')

                        to_download.append((sref, name, _number))
                        if not download_last.get():
                            download(sref,name,_number)
    else:
        print('Error al acceder al archivo:', response.status_code)
def download_files(_url, format):
    download_button.config(text="Descargando...")
    response = requests.get(_url, headers=headers)
    if response.status_code == 200: 
        print(response.content)
        print('OK')
        
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find_all('title')[0].get_text()

        endtitle =  title.find('MP3')-1
        print(title, "<<<<")
        
        title = title[:endtitle]

        global folder_name
        folder_name = title

        os.mkdir('./'+folder_name)
        
        linksfile = open('./'+folder_name+'/'+'links.txt', 'a')

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
                        get_list_of_files('https://downloads.khinsider.com'+sref, counter, format)

                        st.add(sref)
                        counter+=1

        if download_last.get():
            for file in to_download:
                download(file[0], file[1])
        
    else:
        print('Error al acceder a la página:', response.status_code)

ventana.mainloop()

print('Descarga finalizada')
