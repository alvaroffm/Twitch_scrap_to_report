from Scraper import download
from Scraper import check_online
from Scraper import MainLoop
from PostProcess import Data_frame
from PostProcess import Graph
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
STREAMER = 'auronplay'
DELAY = 120

""""""""""""""""""


while True:

    now_time = datetime.now()

    download(STREAMER)
    filename = check_online(STREAMER, DELAY_CHECK=120)
    print(filename)
    MainLoop(STREAMER ,filename, DELAY)
    # filename = 'data/auronplay_2021_11_24T16.json'
    Data_frame(filename)
    df = Data_frame(filename)
    image = Graph(STREAMER,df)

    with timer():

        PL = PythonLatex(STREAMER , portada='portada2.pdf', logo='artic_boa_logo.pdf')
        PL.Preamble('artic_boa_logo.pdf')
        PL.Add_color('prueba_color', 255, 0, 0)
        PL.Add_color('otra_prueba', 1, 200, 0, flag_print=False)

        # PL.Titlepage(TITLE2='ANÁLISIS DE MERCADO DE SEGUNDA MANO', MAIN_TITLE='VOLKSWAGEN ARTEON', TITLE3='INFORME DE RESULTADOS')
        PL.Add_chapter('Análiticas de la transmisión')
        PL.Add_section('Resumen', 'content.txt')
        PL.Add_image(image, 'Numero de coches por color', SIZEREL=1)


        PL.Write()


    with timer():
        print('Compilando archivo TEX')
        os.system('xelatex -quiet report/output_latex.tex')
        print(bcolors('OKGREEN', 'Archivo PDF creado correctamente'))
        file = filename.split('/data/')[1].split('.json')[0]
        shutil.move('output_latex.pdf', f'report/{file}.pdf')



