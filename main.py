from Scraper import download
from Scraper import check_online
from Scraper import MainLoop
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


"""""""""""""""
INPUTS

"""""""""""""""
STREAMER = 'zeling'
DELAY = 6


""""""""""""""""""




now_time = datetime.now()

download(STREAMER)
filename = check_online(STREAMER, DELAY_CHECK=5)
MainLoop(STREAMER ,filename, DELAY)

