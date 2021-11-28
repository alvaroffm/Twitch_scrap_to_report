import time
import datetime
from datetime import date
from misc import bcolors
import os



class PythonLatex():

    TODAY = datetime.datetime.now()
    DAY = str(TODAY.day)
    MINUTE = str(TODAY.minute)

    def __init__(self, STREAMER, fontname = 'Montserrat', logo = 'logo.pdf', portada = 'portada.pdf', ):
        self.cwd = os.getcwd()
        self.preamble = []
        self.titlepage = []
        self.body = []
        self.colors = []
        self.STREAMER = STREAMER

        self.fontname = fontname
        self.logo = logo
        self.portada = portada

    def Change_font(self, fontname):

        self.preamble.append(r'\usepackage{fontspec}')
        self.preamble.append(r'\setmainfont{%s}' % fontname)


    def Preamble(self, LOGO, LOGO_STREAMER):
        TODAY = datetime.datetime.now()
        DAY = str(TODAY.day)
        YEAR = str(TODAY.year)
        MONTH = TODAY.strftime("%B")

        with open('report/latex_inputs/preamble.txt') as f:
            data = f.read().splitlines()
            for line in data:
                line = line.replace('STREAMER_NAME', self.STREAMER)
                if line.startswith('\setmainfont') and self.fontname not in line:
                    line_split = line.split("[")
                    line_split[1] = f'[{self.fontname}]'
                    line = str(line_split[0] + line_split[1])

                    print(bcolors('OKBLUE',f'Replacing font for {self.fontname}'))

                if 'LOGO_INDEX' in line:
                    line = line.replace('LOGO_INDEX', f'report/images/{LOGO}')
                if 'LOGO_STREAMER' in line:
                    line = line.replace('LOGO_STREAMER', f'{LOGO_STREAMER}')

                self.preamble.append(line)
                # print(line, file=None)

    def Titlepage(self, TITLE2 ='TITLE2', color1 ='capgemini_blue', MAIN_TITLE =' ', TITLE3 =' ', color2 = 'rodeo_grey', color3 ='rodeo_grey'):
        with open('latex_inputs/titlepage.txt') as f:
            data = f.read().splitlines()


            TODAY = datetime.datetime.now()
            DAY = str(TODAY.day)
            YEAR = str(TODAY.year)
            MONTH = TODAY.strftime("%B")


        for line in data:
            line = line.replace('TITLE2', TITLE2)
            line = line.replace('color2', color2)

            line = line.replace('color1', color1)
            line = line.replace('TITLE3', TITLE3)
            line = line.replace('color3', color3)
            line = line.replace('MAIN_TITLE', MAIN_TITLE)
            line = line.replace('LOGO', f'images/{self.logo}')
            line = line.replace('DATE', MONTH + ' ' + YEAR)
            line = line.replace('BACKGROUND', f'images/{self.portada}')
            self.titlepage.append(line)
            # print(line, file=None)


    def Add_image(self, IMAGE, CAPTION = ' ', SIZEREL=0.7, landscape=False):
        with open('report/latex_inputs/image.txt') as f:
            data = f.read()


            data = data.replace('CAPTION', CAPTION)
            data = data.replace('IMAGE', IMAGE)

        if landscape:

            self.body.append(r'\begin{landscape}')
            data = data.replace(r'SIZEREL\textwidth', '24cm')

        data = data.replace('SIZEREL', '%f' % SIZEREL)

        self.body.extend(data.splitlines())

        if landscape:
            self.body.append(r'\end{landscape}')







    def Add_chapter(self, TITLE, content_txt = None):
        self.body.extend(['\chapter*{%s}' % TITLE])
        self.body.append(r'\thispagestyle{fancy}')
        if content_txt != None:
            with open(r'latex_inputs/' + content_txt) as f:
                data = f.read()

                self.body.extend(data.splitlines())

    def Add_section(self, TITLE, content_txt = False):
        if content_txt:
            with open(r'report/latex_inputs/' + content_txt) as f:
                data = f.read()
                self.body.extend(['\section*{%s}' % TITLE])
                self.body.extend(data.splitlines())
        else:
            self.body.extend(['\section*{%s}' % TITLE])




    def Add_color(self,NAME,R,G,B, flag_print=False):
        self.colors = []
        for ii, line in enumerate(self.preamble[::-1]):
            if line.startswith('\definecolor'):
                if flag_print:
                    print(ii,line)
                self.colors.append(line)
                if flag_print:
                    print(bcolors('FAIL', f'eliminando : {line}' ))
                self.preamble.remove(line)
                if flag_print:
                    print(bcolors('OKCYAN',f'items_preambulo {len(self.preamble)}'))


        self.colors.append('\definecolor{%s}{rgb}{%s,%s,%s}' %(NAME,R/255,G/255,B/255))

        self.preamble.extend(self.colors)
        self.preamble.extend(' ')









    def Write(self, pathfile = f'report/output_latex.tex'):
        with open(pathfile, 'w+', encoding='utf-8') as f:

            for line in self.preamble:
                print(line, file=f)

            print(r'\begin{document}', file=f)

            for line in self.titlepage:
                print(line, file=f)


            for line in self.body:
                print(line, file=f)

            print(r'\end{document}', file=f)

        print(bcolors('OKBLUE', 'Archivo TEX creado correctamente'))





if __name__ == '__main__':

    from misc import timer
    import os


    with timer():

        PL = PythonLatex('elxokas',portada='portada2.pdf', logo='artic_boa_logo.pdf')
        PL.Preamble('artic_boa_logo_small_mono.pdf')
        PL.Add_color('prueba_color', 255, 0, 0)
        PL.Add_color('otra_prueba', 1, 200, 0, flag_print=False)

        # PL.Titlepage(TITLE2='ANÁLISIS DE MERCADO DE SEGUNDA MANO', MAIN_TITLE='VOLKSWAGEN ARTEON', TITLE3='INFORME DE RESULTADOS')
        PL.Add_chapter('Análiticas de la transmisión')
        PL.Add_section('Resumen', 'content.txt')
        PL.Add_image('evangelion0_2021_11_21.pdf', 'Numero de coches por color', SIZEREL=1)






        PL.Write()


    with timer():
        print('Compilando archivo TEX')
        os.system('xelatex -quiet output_latex.tex')
        print(bcolors('OKGREEN', 'Archivo PDF creado correctamente'))

        # os.system("mv file1 file2") # mover de archivo1  a archivo 2
