import tkinter
import  time
from tkinter import *


class GFG:

    def __init__(self):

        self.master = tkinter.Tk()
        self.master.geometry(f'{700}x{350}')

        self.x = 1
        self.y = 0

        self.canvas = tkinter.Canvas(self.master)
        self.canvas.configure(bg="white")
        self.canvas.pack(fill="both", expand=True)

        #DIBUJO

        self.head = self.canvas.create_oval(60, 10, 120, 80, width=2, fill='white')
        self.body = self.canvas.create_line(90,80,90,260,width=2),
        self.hands = self.canvas.create_line(60,130,120,130,width=2),
        self.foot_left = self.canvas.create_line(90,258,60,300,width=2),
        self.foot_right =  self.canvas.create_line(90,258,120,300,width=2)

    def graficar(self):

        def start():

            while True:

              ball_pos = self.canvas.coords(self.head)
              # unpack array to variables
              xl,yl,xr,yr = ball_pos

              if xl < abs(5) or xr > 700-abs(5):
                  self.canvas.coords(self.head,60,10,120,80)
                  self.canvas.coords(self.body,90,80,90,260)
                  self.canvas.coords(self.hands,60,130,120,130)
                  self.canvas.coords(self.foot_left,90,258,60,300)
                  self.canvas.coords(self.foot_right,90,258,120,300)
                  break

              else:

                  self.canvas.move(self.head,5,0)
                  self.canvas.move(self.body,5,0)
                  self.canvas.move(self.hands,5,0)
                  self.canvas.move(self.foot_left,5,0)
                  self.canvas.move(self.foot_right,5,0)

              self.master.update()
              time.sleep(0.1)

        def exit():
            self.master.quit()
            self.master.destroy()
            return

        start_Button = Button(self.master,text="START ANIMACION",command=start)
        start_Button.place(x= 150,y = 320)

        stop_Button = Button(self.master,text="STOP ANIMACION ")
        stop_Button.place(x= 280 , y= 320)

        cancel_Button = Button(self.master,text="EXIT",command=exit)
        cancel_Button.place(x= 400 , y= 320,width=110)

        mainloop()



