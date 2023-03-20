import tkinter
import time
from tkinter import *
from PIL import ImageTk, Image

class opcion3:

    global photo_Class

    def __init__(self):

        super().__init__()
        self.master = tkinter.Tk()
        self.master.geometry(f'{700}x{350}')
        self.master.resizable(width=0, height=0)

        self.canvas = tkinter.Canvas(self.master)
        self.canvas.configure(bg="black")

        self.python_image = tkinter.PhotoImage(file = 'imagen_canon.png')
        self.canvas.create_image(40,250,image = self.python_image)

    def graficar(self):

        def start():

            self.bullet = self.canvas.create_oval(60, 220,80 ,240, width=2, fill='white',outline='red')
            t = 1

            while True:

                bullet_pos = self.canvas.coords(self.bullet)
                xl,yl,xr,yr = bullet_pos

                if xl > 700  or yl > 350:
                    self.canvas.delete(self.bullet)
                    self.bullet = self.canvas.create_oval(60, 220,80 ,240, width=2, fill='white',outline='red')
                    t = 1

                if xl > 350 and xl <= 360:
                    self.canvas.move(self.bullet,7*t ,0)

                elif xl >360:
                    self.canvas.move(self.bullet,7*t ,3*t**2)

                else:
                    self.canvas.move(self.bullet,7*t , -3* t**2 )

                self.master.update()
                time.sleep(0.1)
                t += 0.01

        def exit():

            self.master.quit()
            self.master.destroy()
            return

        self.cancel_Button = Button(self.master,text="EXIT",command=exit)
        self.cancel_Button.place(x= 400 , y= 320,width=110)

        self.start_Button = Button(self.master,text="START ANIMACION",command=start)
        self.start_Button.place(x= 150,y = 320)

        self.canvas.pack(fill="both", expand=True)
        mainloop()


