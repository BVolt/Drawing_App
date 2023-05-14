import tkinter as tk
import turtle
from tkinter import simpledialog, colorchooser

class TurtleCanvas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.pack(fill=tk.BOTH, expand=True)
        self.update()

        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.t = turtle.RawTurtle(self.turtle_screen)
        self.t.speed(0)
        self.t.pendown()

        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<Button-1>", self.update_coordinates)   

        self.eraser_on = False
        self.previous_pen_color = self.t.pencolor()
        self.previous_pen_size = self.t.pensize()
        self.previous_bg_color = "white"
        self.drawing_data = []

    def update_coordinates(self, event):
        self.canvas.unbind("<Button-1>")
        x, y = self.turtle_screen.cv.canvasx(event.x), self.turtle_screen.cv.canvasy(event.y)
        # Check if the x-coordinate is outside the canvas
        if x < 0:
            x = 0
        elif x > self.canvas.winfo_width():
            x = self.canvas.winfo_width()

        # Check if the y-coordinate is outside the canvas
        if y < 0:
            y = 0
        elif y > self.canvas.winfo_height():
            y = self.canvas.winfo_height()


        self.t.penup()
        self.t.goto(x,-y)
        self.t.pendown()
        self.canvas.bind("<Button-1>", self.update_coordinates)

    def draw_line(self, event):
        self.canvas.unbind("<B1-Motion>")
        x, y = self.turtle_screen.cv.canvasx(event.x), self.turtle_screen.cv.canvasy(event.y)
        self.t.goto(x, -y)

        if self.eraser_on:
            self.t.pencolor(self.canvas["bg"])
            self.t.pensize(20)
        else:
            self.t.pencolor(self.previous_pen_color)
            self.t.pensize(self.previous_pen_size)

        if self.drawing_data:
            prev_data = self.drawing_data[-1]
            prev_x, prev_y = prev_data["x"], prev_data["y"]
        else:
            prev_x, prev_y = x, -y

        self.drawing_data.append({
            "x": x, 
            "y": -y, 
            "prev_x": prev_x, 
            "prev_y": prev_y, 
            "color": self.t.pencolor(), 
            "size": self.t.pensize(), 
            "pendown": self.t.isdown(), 
            "eraser": self.eraser_on
        })

        self.canvas.bind("<B1-Motion>", self.draw_line)

    def set_pen_size(self):
        size = simpledialog.askinteger("Pen Size", "Enter pen size:", minvalue=1, maxvalue=100)
        if size is not None:
            self.previous_pen_size = size
            self.t.pensize(size)

    def set_pen_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.previous_pen_color = color
            self.t.pencolor(color)

    def redraw(self, save=False):
        if not save:
            self.t.clear()
        self.turtle_screen.tracer(0) 
        for data in self.drawing_data:
            self.t.penup()
            self.t.goto(data["prev_x"], data["prev_y"])
            if data["pendown"]:
                self.t.pendown()
            else:
                self.t.penup()
            self.t.pencolor(data["color"])
            self.t.pensize(data["size"])
            self.t.goto(data["x"], data["y"])
        self.turtle_screen.tracer(1)

    def set_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.canvas.config(bg=color)
            self.turtle_screen.bgcolor(color)

            for data in self.drawing_data:
                if data["eraser"]:
                    data["color"] = color

            self.previous_bg_color = color
            self.redraw()

            if self.eraser_on:
                self.t.pencolor(color)

    def toggle_eraser(self):
        self.eraser_on = not self.eraser_on

        if self.eraser_on:
            self.t.pencolor(self.canvas["bg"])
            self.t.pensize(20)
        else:
            self.t.pencolor(self.previous_pen_color)
            self.t.pensize(self.previous_pen_size)

    def clear(self):
        self.t.clear()