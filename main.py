from Scraper import download
from Scraper import check_online
from Scraper import MainLoop
from PostProcess import Data_frame
from PostProcess import Graph
import locale
import json
import requests
from twitchAPI.twitch import Twitch
import time
from datetime import datetime
import os
from IPython.display import clear_output
import pandas as pd
import matplotlib.pyplot as plt
import os
from misc import timer
from misc import bcolors
from report.latex_report import PythonLatex
import shutil
import matplotlib as mpl
from matplotlib import font_manager as fm,rcParams
from PIL import Image
from io import BytesIO
from secrets import CLIENT_ID,ACCESS_TOKEN


"""""""""""""""
INPUTS

"""""""""""""""
STREAMER = 'ERNESBARBEQ'
DELAY = 180

""""""""""""""""""
#
# locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')
now_time = datetime.now()
day_of_week = now_time.strftime("%A").capitalize()
day = now_time.day
month = now_time.strftime('%B').capitalize()
year = now_time.year


FECHA = f'{day_of_week}, {day} de {month} de {year}'
print(FECHA)

while True:

    now_time = datetime.now()

    download(STREAMER)
    filename = check_online(STREAMER, DELAY_CHECK=180)
    print(filename)
    MainLoop(STREAMER ,filename, DELAY)
    # filename = r'C:\Users\Buzz\PycharmProjects\Twitch_scrap_to_report/data/2022_01_24T18_elxokas.json'
    # UNCOMMENT TO CHECK WITHOUT RUNNING THE LOOP
    Data_frame(filename)
    df = Data_frame(filename)
    ST = df['user_login'].iloc[1]
    image, games_df ,profile_img = Graph(ST,df,flag_plot=True)
    print(games_df)

    with timer():

        PL = PythonLatex(ST , portada='portada2.pdf', logo='artic_boa_logo.pdf')
        PL.Preamble('artic_boa_logo.pdf',profile_img)
        PL.Add_color('prueba_color', 255, 0, 0)
        PL.Add_color('otra_prueba', 1, 200, 0, flag_print=False)

        # PL.Titlepage(TITLE2='ANÁLISIS DE MERCADO DE SEGUNDA MANO', MAIN_TITLE='VOLKSWAGEN ARTEON', TITLE3='INFORME DE RESULTADOS')

        # PL.Add_chapter('Análiticas de la transmisión')
        PL.Add_section(FECHA)
        PL.Add_image(profile_img, SIZEREL=0.2)
        PL.Add_image(image, 'Numero de viewers durante la retransmisión', SIZEREL=1)


        PL.Write()


    with timer():
        print('Compilando archivo TEX')
        os.system('xelatex -quiet report/output_latex.tex')
        print(bcolors('OKGREEN', '\n #################################### \n # Archivo PDF creado correctamente # \n ####################################'))
        file = filename.split('/data/')[1].split('.json')[0]
        shutil.move('output_latex.pdf', f'report/{file}.pdf')


        to_delete=['output_latex.log','output_latex.out','output_latex.aux']
        for item in to_delete:
            os.remove(item)

    # os.system(r'C:\Users\Buzz\PycharmProjects\Twitch_scrap_to_report\report\%s.pdf' %file)

    break


