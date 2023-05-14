import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os


def save_drawing(canvas, root):
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    print(file_path)
    if file_path:
        psFilename ="temp.ps"
        
        # Save the current state of the turtle
        turtle_state = canvas.t.pen()
        turtle_isdown = canvas.t.isdown()

        canvas.t.clear()

        # Draw a rectangle over the entire canvas with the background color
        canvas.t.penup()
        canvas.t.goto(canvas.turtle_screen.cv.canvasx(0), -canvas.turtle_screen.cv.canvasy(0))
        canvas.t.color(canvas.canvas["bg"])
        canvas.t.begin_fill()
        for _ in range(2):
            canvas.t.forward(canvas.canvas.winfo_width())
            canvas.t.right(90)
            canvas.t.forward(canvas.canvas.winfo_height())
            canvas.t.right(90)
        canvas.t.end_fill()

        # Redraw all the stored lines
        canvas.redraw(True)

        # Save the canvas as a postscript file
        canvas.canvas.postscript(file=psFilename)
        
        # Restore the turtle to its previous state
        canvas.t.pen(turtle_state)
        if turtle_isdown:
            canvas.t.pendown()
        else:
            canvas.t.penup()

        # Open the postscript file and save it as a PNG
        psimage = Image.open(psFilename)
        psimage.save(file_path)

        # Remove the postscript file
        os.remove(psFilename)


def confirm_close(root):
    if messagebox.askokcancel("Confirm Exit", "Are you sure you want to exit?"):
        root.destroy()


def setup_menu(root, canvas):
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Save", command=lambda: save_drawing(canvas, root))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: confirm_close(root))

    edit_menu = tk.Menu(menubar)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Pen Size", command=lambda: canvas.set_pen_size())
    edit_menu.add_command(label="Pen Color", command=lambda: canvas.set_pen_color())
    edit_menu.add_command(label="Background Color", command= lambda: canvas.set_bg_color())
    edit_menu.add_command(label="Clear All", command=lambda: canvas.clear())
    edit_menu.add_checkbutton(label="Eraser", command=lambda: canvas.toggle_eraser())