import requests
from urllib import request
from bs4 import BeautifulSoup
import os
import tkinter as tk
import tkinter.ttk as ttk



headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "https://www.google.com/"
    }

### TKinter Interface
main_window = tk.Tk()
main_window.title("Khinsider Downloader")

text_label = tk.Label(main_window, text="Enlace del album a descargar:")
text_label.pack()
text = tk.Text(main_window, height=3)
text.pack()

start_button = tk.Button(main_window, text="Siguiente", command=lambda: process_page(str(text.get("1.0",tk.END)).strip("\n")))
start_button.pack()

option_window = tk.Toplevel()
option_window.title("Options")
option_window.withdraw()

download_last = tk.BooleanVar()
download_last_switch = tk.Checkbutton(option_window, variable=download_last, text="Listar primero")
download_last_switch.pack()

decide = tk.BooleanVar()
decide_switch = tk.Checkbutton(option_window, variable=decide,text='Descargar determinados archivos')
decide_switch.pack()

album_size = 20 ####GET
ran = range(1,album_size+1)
def update_ran():
    ran = range(int(ran_l.get()),int(ran_r.get())+1)
    ran_l.config(to=ran[-1])
    ran_r.config(from_=ran[0])

range_label=tk.Label(option_window,text="Rango de archivos a descargar")
range_label.pack()
ran_l = tk.Spinbox(option_window,from_=1,to=ran[-1],command=update_ran) #TO RAN_R
ran_l.pack()
ran_r = tk.Spinbox(option_window, from_=ran[0], to=album_size,command=update_ran) ##FIX
ran_r.pack()

format_label=tk.Label(option_window,text="Formato a descargar")
format_label.pack()
file_format = ".mp3"
mp3_rb = tk.Radiobutton(option_window,text="mp3",value='.mp3',variable=file_format,)
mp3_rb.pack()
flac_rb = tk.Radiobutton(option_window,text="flac",value='.flac',variable=file_format)
flac_rb.pack()

download_window = tk.Toplevel()
download_window.minsize(300,100)
download_window.title("Download")
download_window.withdraw()

def update_progress(file, downloaded, total_size):
    progress = (downloaded/total_size)*100.
    download_file_label.config(text=f"File:{file}")
    download_progress_label.config(text=f"Progress:{progress:.2f}% ({(downloaded/1024):.2f}/{(total_size/1024):.2f} kB)")
    download_progress_bar.config(value=round(progress))
    download_window.update_idletasks()

download_file_label = tk.Label(download_window, text="File:")
download_file_label.pack()
download_progress_label = tk.Label(download_window, text="Progress:")
download_progress_label.pack()

download_progress_bar = ttk.Progressbar(download_window, length=250, value=0)
download_progress_bar.pack()

links = []
st = {"set"}
to_download = []

folder_name = 'VideoGameMusic'

def download(url, name, number):
    decision = True
    if number in ran:
        if decide.get():
            print('Deseas descargar \''+name+'\'? (y/n)')
            decision = (True if input().lower() == 'y' else False)
        
        if decision:
            print('Descargando: '+name)

            # Streaming, so we can iterate over the response.
            response = requests.get(url, stream=True)

            total_size = int(response.headers.get("content-length", 0))
            block_size = 1024
            downloaded = 0
            progress = 0
            with open('./'+folder_name+'/'+name, "wb") as file:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    update_progress(name,downloaded,total_size)
                    file.write(data)

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
        
def process_page(_url):
    
    response = requests.get(_url, headers=headers)
    if response.status_code == 200: 
        main_window.withdraw()
        option_window.deiconify()
        
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')
        global album_size
        album_size = int(str(soup.find(id="songlist_footer").find_previous('tr').td.find_next('td').text).removesuffix("."))
        title = soup.find_all('title')[0].get_text()

        endtitle =  title.find('MP3')-1
        
        title = title[:endtitle]
        global folder_name
        folder_name = title
        global links
        links = soup.find_all('a')  
    else:
        print('Error al acceder a la página:', response.status_code)

def start_download():
    download_window.deiconify()
    download_button.config(text="Descargando...")
    if not os.path.isdir('./'+folder_name):
        os.mkdir('./'+folder_name)
    
    linksfile = open('./'+folder_name+'/'+'links.txt', 'a')

    # Encontrar todos los enlaces en la página
    
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
                    get_list_of_files('https://downloads.khinsider.com'+sref, counter, file_format)

                    st.add(sref)
                    counter+=1

    if download_last.get():
        for file in to_download:
            download(file[0], file[1])

download_button = tk.Button(option_window, text="Descargar", command=start_download)
download_button.pack()

main_window.mainloop()

print('Descarga finalizada')
