import pandas as pd
import json
import os
import json
import requests
from twitchAPI.twitch import Twitch
import time
from datetime import datetime
import os
from IPython.display import clear_output
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
from matplotlib import font_manager as fm,rcParams
from PIL import Image
from io import BytesIO
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MultipleLocator
import matplotlib.ticker as tck
from scipy.interpolate import make_interp_spline
import numpy as np
from datetime import timedelta
from textwrap import wrap




def Data_frame(filename):
    filename_f = filename.split('.')[0] + '_f.json'



    with open(filename_f, 'r') as f:
        data_dict = json.load(f)

    new_list = []
    for item in data_dict:
        for ii in item:
            new_list.append(ii)


    df = pd.DataFrame(new_list)
    df['hour'] = pd.to_datetime(df['hour'], utc=True)
    df['started_at'] = pd.to_datetime(df['started_at'], utc=True) +  pd.DateOffset(hours=1)


    return df

def Graph(STREAMER, df):

    row_max_viewers = df['viewer_count'].idxmax()
    color = '#18bc9c'

    fpath = os.path.join(mpl.get_data_path(),
                         r"C:\Users\Buzz\PycharmProjects\Cochesnet_Latex\fonts\Montserrat-Regular.ttf")
    fpath2 = os.path.join(mpl.get_data_path(),
                          r"C:\Users\Buzz\PycharmProjects\Cochesnet_Latex\fonts\Montserrat-SemiBold.ttf")

    prop = fm.FontProperties(fname=fpath, weight='bold')
    prop_bold = fm.FontProperties(fname=fpath2, weight='bold', size=13)

    figure1, ax3 = plt.subplots(1, 1, figsize=(10, 7))

    df_clean = df
    # scatter = ax3.scatter(df_clean['hour'], df_clean['viewer_count'], marker='.', edgecolors='#233440', linewidths=0.01,
    #                       alpha=0.4)


    views_change = df_clean["viewer_count"].shift() != df["viewer_count"]
    points_to_plot = list(df_clean[views_change].index)

    ax3.plot(df_clean['hour'], df_clean['viewer_count'], color=color)

    # legend1 = ax3.legend(handletextpad=1.5, labelspacing = 1.5, framealpha = 0.4)
    # ax3.add_artist(legend1)

    ax3.set_ylabel('Viewers', fontproperties=prop_bold)
    ax3.set_xlabel('Hour', fontproperties=prop_bold)
    ax3.xaxis.set_ticks_position('bottom')

    # ax3.set_yticks([1200,1110,1220], minor=True)

    ax3.tick_params(which='major', width=1.00, length=7, )
    ax3.tick_params(which='minor', width=0.5, length=2.5)

    # ax3.set_xlim(0,df['km'].max()*1.02)
    # ax3.set_ylim(df['price'].min()*0.9, df['price'].max()*1.05)
    titulo_streamer_name = df_clean['user_name'][row_max_viewers]
    ax3.set_title(r"$\bf{" + titulo_streamer_name + "}$" + '\n' + '\n'.join(wrap(df_clean['title'][row_max_viewers])))
    ax3.set_ylim(0, )

    # @ticker.FuncFormatter
    def major_formatter(x, pos):
        # return f'{str(x)[:-5]} k'
        return f'{str(x / 1000)} k'

    # def major_formatter2(x,pos):
    #     # return f'{str(x)[:-5]} k'
    #     return f'{x} h'

    plt.xticks(rotation=0)
    # legend1.set_title('Streamer', prop=prop_bold)

    # ax3.xaxis.set_major_formatter(major_formatter2)
    ax3.yaxis.set_major_formatter(major_formatter)

    for tick in ax3.get_xticklabels():
        tick.set_fontproperties(prop)
    for tick in ax3.get_yticklabels():
        tick.set_fontproperties(prop)

    ax3.fill_between(df_clean['hour'][points_to_plot], df_clean['viewer_count'][points_to_plot], 0, color=color,
                     alpha=0.04, )

    df.started = df_clean['started_at'][0]

    df.started = pd.to_datetime(df.started)

    print(df.started)

    df.last = df_clean.iloc[-1]

    df.last = pd.to_datetime(df.last['hour'])

    print(df.last)

    streaming_minutes = int((df.last - df.started).total_seconds() / 60)
    streaming_hours = round(streaming_minutes / 60, 2)

    max_viewers = df_clean.viewer_count.max()

    print(f'{streaming_hours = } hours')
    print(f'{streaming_minutes = } minutes')
    print(f'{max_viewers = } max viewers')

    game = df_clean['game_name'][0]
    print(game)

    prop = fm.FontProperties(fname=fpath, weight='bold')
    prop_game = fm.FontProperties(fname=fpath, size=13)
    prop_metrics = fm.FontProperties(fname=fpath, size=11)

    # insertar nuevo juego
    # df_evan['game_name'][1200:2400] = 'Minecraft'

    my_column_changes = df_clean["game_name"].shift() != df["game_name"]

    arg_game_change = list(df_clean[my_column_changes].index)

    for index in arg_game_change:
        plt.vlines(x=df_clean['hour'][index], ymin=0, ymax=df_clean['viewer_count'].max() * 1.1, color='#cd0033',
                   linestyles='dashed', linewidth=0.5)
        plt.text(df_clean['hour'][index],
                 (df_clean['viewer_count'].max() * 0.03) if index != 0 else df_clean['viewer_count'].max() * 1.03,
                 df_clean['game_name'][index], rotation=270, verticalalignment='bottom' if index != 0 else 'top',
                 color='#cd0033', fontproperties=prop_game)

    lenght = len(df_clean.index)

    plt.axhline(y=df_clean['viewer_count'].max(), xmin=0, xmax=1, color=color, linewidth=1, alpha=0.5,
                linestyle='dotted')

    plt.axhline(y=df_clean['viewer_count'].mean(), xmin=0, xmax=1, color='#210a68', linewidth=1, alpha=0.5,
                linestyle='dotted')

    ax3.annotate('MAX' + '\n' + str(int(df_clean['viewer_count'].max())), (1, 1),
                 xytext=(1.01, df_clean['viewer_count'].max() / df_clean['viewer_count'].max()),
                 xycoords='axes fraction', color=color, fontproperties=prop_metrics, verticalalignment='center',
                 horizontalalignment='left')

    ax3.annotate('AVG' + '\n' + str(int(df['viewer_count'].mean())), (1, 1),
                 xytext=(1.01, df_clean['viewer_count'].mean() / df_clean['viewer_count'].max()),
                 xycoords='axes fraction', color='#210a68', fontproperties=prop_metrics, verticalalignment='center',
                 horizontalalignment='left')

    ax3.xaxis.set_major_formatter(DateFormatter('%H:%M'))

    time = streaming_hours

    hours = int(time)
    minutes = (time * 60) % 60

    duration = "%dh %02dm" % (hours, minutes)
    print(duration)

    ax3.annotate('STREAM DURATION' + '\n' + r"$\bf{" + duration + "}$", (1, 1), xytext=(0.94, 0.08),
                 xycoords='axes fraction', color='red', fontproperties=prop_metrics, verticalalignment='top',
                 horizontalalignment='right')

    imagename = f'data/{STREAMER}_{datetime.now().year:04}_{datetime.now().month:02}_{datetime.now().day:02}.pdf'

    plt.interactive(True)
    plt.savefig(imagename, bbox_inches='tight')

    return imagename


if __name__ == '__main__':
    STREAMER = 'elxokas'
    df = Data_frame(f'data/elxokas_2021_11_20T17.json')
    Graph(STREAMER,df)
