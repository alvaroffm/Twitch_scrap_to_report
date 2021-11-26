import time
import matplotlib.pyplot as plt
import numpy as np

def bcolors(weight, text):
    colors = dict(
            HEADER = '\033[95m',
            OKBLUE = '\033[94m',
            OKCYAN = '\033[96m',
            OKGREEN = '\033[92m',
            WARNING = '\033[93m',
            FAIL = '\033[91m',
            ENDC = '\033[0m',
            BOLD = '\033[1m',
            UNDERLINE = '\033[4m',
        )
    return colors[weight] + text + colors['ENDC']


class timer:
    def __init__(self):
        self.t0 = time.time()

    def __enter__(self):
        return

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print('time = %6.3f s' % (time.time() - self.t0,))
        print(bcolors('OKBLUE', 'time = %6.3f s' % (time.time() - self.t0,)))



def quickplot(x, y=None, ls='-', title=None, xlabel=None, ylabel=None, grid=True):

    _, ax = plt.subplots()

    if y is not None:
        ax.plot(x, y, ls)
    else:
        ax.plot(range(len(x)), x, ls)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(grid)



def ProgressBar(counter,total):
    n_bars_perc = int(np.ceil(counter/total * 100))

    n_rayas = 100 - n_bars_perc
    n_bars = n_bars_perc/5
    n_rayas = n_rayas/5

    print( str(n_bars_perc) + '%''[' + '\u25A0' * int(n_bars) + '.'*int(n_rayas) + ']' )

def Underscore(text):
    return '$_{%s}$' %text