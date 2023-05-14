import tkinter as tk
from menu_actions import setup_menu, confirm_close
from turtle_canvas import TurtleCanvas
from PIL import Image, ImageTk


def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Drawing App")
    root.iconbitmap('draw.ico')

    root.protocol("WM_DELETE_WINDOW", lambda: confirm_close(root))

    canvas = TurtleCanvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)

    setup_menu(root, canvas)

    root.mainloop()

if __name__ == "__main__":
    main()