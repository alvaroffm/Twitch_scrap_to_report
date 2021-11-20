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

    views = stream['data'][0]['viewer_count']
    user = stream['data'][0]['user_name']

    return stream['data']


def check_online(STREAMER,DELAY_CHECK):
    current_directory = os.getcwd()
    ####################################
    #    check if streamer is ONLINE   #
    ####################################
    while True:
        clear_output(wait=True)
        try:
            DATA = download(STREAMER)
            print(f'Streaming ON - {STREAMER}')
            break
        except IndexError:
            print('Streaming OFF')
            time.sleep(DELAY_CHECK)

    ####################################
    #    create json file              #
    ####################################

    date = str(DATA[0]['started_at']).split(':')[0].replace('-','_')
    last_day=datetime.now().day
    filename = current_directory + f'/data/{STREAMER}_{date}.json'

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

        print('BIEN')
        time.sleep(DELAY- time.monotonic() % 1)




if __name__ == '__main__':

    STREAMER = 'zeling'
    now_time = datetime.now()
    twitch = login()

    download(STREAMER)
    filename = check_online(STREAMER, 5)
    MainLoop(STREAMER,filename,6)

