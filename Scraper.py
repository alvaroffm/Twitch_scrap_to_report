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
import matplotlib as mpl
from matplotlib import font_manager as fm,rcParams
from PIL import Image
from io import BytesIO
from secrets import CLIENT_ID,ACCESS_TOKEN
from misc import bcolors


def login():

    ####################################
    #              LOGIN               #
    ####################################



    twitch = Twitch(CLIENT_ID, ACCESS_TOKEN)
    twitch.authenticate_app([])



    return twitch


####################################
#        Scraping function         #
####################################

def download(STREAMER):
    twitch = login()
    stream = twitch.get_streams(user_login = STREAMER)
    # print(stream['pagination'])
    now_time = datetime.now()
    for item in stream['data']:
        item['hour']= str(now_time)


    return stream['data']


def check_online(STREAMER,DELAY_CHECK):
    current_directory = os.getcwd()
    ####################################
    #    check if streamer is ONLINE   #
    ####################################
    while True:

        try:
            DATA = download(STREAMER)
            date = str(DATA[0]['started_at']).split(':')[0].replace('-', '_')
            print(DATA)
            print(bcolors('OKGREEN', 'Streaming ON - '),f'{STREAMER}')
            break
        except IndexError:
            timee = str(datetime.now()).split(' ')[1].split('.')[0]
            print(bcolors('WARNING', 'Streaming OFF - ' ),  timee)
            time.sleep(DELAY_CHECK)

    ####################################
    #    create json file              #
    ####################################

    date = str(DATA[0]['started_at']).split(':')[0].replace('-','_')
    last_day=datetime.now().day
    filename = current_directory + f'/data/{date}_{STREAMER}.json'

    os.makedirs(os.path.dirname(filename), exist_ok=True)


    if not os.path.isfile(filename):

        data=[]

        with open(filename, 'w+', encoding="utf-8") as file_first:

            data.append(download(STREAMER))
            json.dump(data,file_first)

        print ("File  NOT existe")



    print ("File SI existe")

    return filename














####################################
#        MAIN LOOP                 #
####################################

def MainLoop(STREAMER, filename, DELAY):
    while True:
        now_time = datetime.now()
        now_day = now_time.day

        try:
            response = download(STREAMER)
            print(response[0]['user_name'])

        except IndexError:
            print('Scraping Acabado')
            os.rename(filename, filename.split('.')[0] + '_f.json')
            break

        with open(filename, 'r', encoding="utf-8") as file_read:

            data_read = json.load(file_read)
            file_read.close()

        with open(filename, 'w+', encoding="utf-8") as file:


            new_data = response
            data_read.append(new_data)
            data_json = json.dump(data_read,file, indent=2)

            print('n:',len(data_read))

        print(str(response[0]['hour']).split(' ')[1].split('.')[0])
        time.sleep(DELAY- time.monotonic() % 1)




if __name__ == '__main__':

    STREAMER = 'elxokas'
    now_time = datetime.now()
    twitch = login()

    download(STREAMER)
    filename = check_online(STREAMER, 5)
    print(filename)
    MainLoop(STREAMER,filename,6)

