from tkinter import *

class Window():

    def __init__(self, master):

        self.display1 = Canvas(master, width=150, height=80, relief=RAISED, bd=5)
        self.display1.grid(row=0,column=0)
        self.display1.create_rectangle(10, 10, 150, 80, fill='dark red')

        self.slider1 = Scale(master, from_=0, to=100, length=400,
                tickinterval=10, orient=HORIZONTAL, relief=SUNKEN, bd=5,
                bg='white', troughcolor='black', sliderrelief=RAISED, command = self.updateCanvas)
        self.slider1.grid(row=0,column=1)

        self.createdText = self.display1.create_text(50, 20, font = 'Helvatica 28', text = self.slider1.get(), fill = 'white', anchor = NW)

    def updateCanvas(self, sliderVal):

        self.display1.itemconfig(self.createdText, text = sliderVal)

master = Tk()
w = Window(master)
master.mainloop()