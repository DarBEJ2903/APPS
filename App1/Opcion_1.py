import PySimpleGUI as sg
from matplotlib import  animation
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import time


class grafica_barras:

    def __init__(self):

        self.layout = [[sg.Text('COMPRA DE AUTOS EN 2022', size=(40, 1),
                           justification='center', font='Helvetica 20')],
                  [sg.Canvas(size=(640, 480), key='-CANVAS-')],
                  [sg.Button('Exit', size=(10, 1), pad=((280, 0), 3), font='Helvetica 14')]]

        self.window = sg.Window('Grafico De Barras',
                           self.layout, finalize=True)

        self.canvas_elem = self.window['-CANVAS-']
        self.canvas = self.canvas_elem.TKCanvas

        self.y2022=[40, 100]
        self.y2023=[20, 150]
        self.year=['2022','2023']
        self.mes=['Enero','Febrero']
        self.vector_pos = np.arange(len(self.year))

        self.Ancho_barra = 0.4
        self.fig, self.ax = plt.subplots()

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        self.fig_agg = self.draw_figure(self.canvas, self.fig)


    def graficar(self):
        i = 0
        while True:
            event, values = self.window.read(timeout=10)
            if self.y2023[0] > 250:
                i = 0
            else:
                i += 1
            if event in ('Exit', None):
                self.window.close()
                return

            self.ax.cla()
            self.y2023[0] += 10*i
            self.y2023[1] += 2*i

            self.ax.bar(self.vector_pos+self.Ancho_barra,self.y2022,self.Ancho_barra,color='red',edgecolor='black')
            self.ax.bar(self.vector_pos,self.y2023,self.Ancho_barra,color='blue',edgecolor='black')
            self.ax.set_xticks(self.vector_pos, self.mes)
            self.ax.set_xlabel('Mes', fontsize=16)
            self.ax.set_ylabel('Numero de vehiculos', fontsize=16)
            self.ax.set_title('Compras de vehiculos',fontsize=18)
            self.ax.legend(self.year,loc=2)
            self.fig_agg.draw()
            time.sleep(0.2)

    def draw_figure(self,canvas, figure, loc=(0, 0)):

        figure_canvas_agg = FigureCanvasTkAgg(figure,canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg








