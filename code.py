import math
from tkinter import *


WIDTH  = 800
HEIGHT = 600
SIDE = 1
minx = -6.3
maxx = 6.3
miny = 2
maxy = -2

class Main(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.plot_line = None
        self.f = lambda x: math.sin(x)

    def key(self, event):
        if event.char == '1':
            self.f = lambda x: x * math.sin(x)
        elif event.char == '2':
            self.f = lambda x: math.sin(x**2)
        elif event.char == '3':
            self.f = lambda x: math.sin(x)
        elif event.char == '4':
            self.f = lambda x: x**2

    def click(self, event):
        self.prevx = event.x
        self.prevy = event.y

    def mouse_wheel(self, event):
        global SIDE
        if SIDE < .1:
            SIDE = .1
        if event.num == 5 or event.delta == -120:
            SIDE -= .3
        if event.num == 4 or event.delta == 120:
            SIDE += .3

    def drag(self, event):
        global minx, maxx
        global miny, maxy
        deltax = -(event.x - self.prevx) / WIDTH * (maxx - minx)
        deltay = -(event.y - self.prevy) / HEIGHT * (maxy - miny)
        minx += deltax
        maxx += deltax
        miny += deltay
        maxy += deltay
        self.prevx = event.x
        self.prevy = event.y
        self.draw()

    def draw(self):
        points = []

        for x in range(800):
            tx = (minx + (maxx - minx) * x / WIDTH)*SIDE
            ty = self.f(tx)/SIDE 
            y = (ty - miny) * HEIGHT / (maxy - miny)
            points.append((x, y))

        if self.plot_line is not None:
            myCanvas.delete(self.plot_line)
        self.plot_line = myCanvas.create_line(points)

        x = (0 - minx) * WIDTH / (maxx - minx)
        myCanvas.coords(self.y_axis, [x, 0, x, HEIGHT])
        y = (0 - miny) * HEIGHT / (maxy - miny)
        myCanvas.coords(self.x_axis, [0, y, WIDTH, y])


root = Tk()
root.geometry(str(WIDTH)+"x"+str(HEIGHT)+"+200+200")
root.title("График")
root.resizable(False, False)
app = Main(root)
app.pack()

myCanvas = Canvas(root, width=WIDTH, height=HEIGHT, bg = '#FFF')
myCanvas.pack()

myCanvas.bind("<ButtonPress-1>", app.click)
myCanvas.bind("<B1-Motion>", app.drag)
myCanvas.bind("<Button-4>", app.mouse_wheel)
myCanvas.bind("<Button-5>", app.mouse_wheel)
root.bind("<Key>", app.key)

app.y_axis = myCanvas.create_line(0, 0, 0, 0, arrow=FIRST)
app.x_axis = myCanvas.create_line(0, 0, 0, 0, arrow=LAST)

app.draw()

root.mainloop()
