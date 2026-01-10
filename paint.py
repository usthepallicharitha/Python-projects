from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageTk
import math

# ---------------- WINDOW ----------------
root = Tk()
root.title("Untitled - Paint")
root.geometry("1400x800")

# ---------------- STATE ----------------
tool = "pencil"
current_color = "black"
brush_size = 4
fill_mode = False
start_x = start_y = None
polygon_points = []

# ---------------- IMAGE BUFFER ----------------
WIDTH, HEIGHT = 2000, 1500
image = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(image)
tk_img = ImageTk.PhotoImage(image)

# ---------------- FUNCTIONS ----------------
def select_tool(t):
    global tool
    tool = t
    status.set(f"Tool: {tool.upper()}")

def set_color(c):
    global current_color
    if c:
        current_color = c

def toggle_fill():
    global fill_mode
    fill_mode = not fill_mode

def clear_canvas():
    global image, draw
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    redraw()

def change_brush(v):
    global brush_size
    brush_size = int(v)

def redraw():
    global tk_img
    tk_img = ImageTk.PhotoImage(image)
    canvas.itemconfig(img_id, image=tk_img)

# ---------------- MENU ----------------
menubar = Menu(root)
root.config(menu=menubar)
menubar.add_cascade(label="File", menu=Menu(menubar, tearoff=0))

# ---------------- RIBBON ----------------
ribbon = Frame(root, bg="#1e1e1e", height=120)
ribbon.pack(fill=X)

# -------- TOOLS --------
tools_frame = LabelFrame(ribbon, text="Tools", fg="white", bg="#1e1e1e")
tools_frame.pack(side=LEFT, padx=10)

Button(tools_frame, text="Pencil",
       command=lambda: select_tool("pencil")).pack(fill=X)
Button(tools_frame, text="Brush",
       command=lambda: select_tool("brush")).pack(fill=X)
Button(tools_frame, text="Eraser",
       command=lambda: select_tool("eraser")).pack(fill=X)

# -------- BRUSH SIZE --------
brush_frame = LabelFrame(ribbon, text="Brush", fg="white", bg="#1e1e1e")
brush_frame.pack(side=LEFT, padx=10)

Scale(brush_frame, from_=1, to=20,
      orient=VERTICAL, command=change_brush).pack()

# -------- SHAPES --------
shapes_frame = LabelFrame(ribbon, text="Shapes", fg="white", bg="#1e1e1e")
shapes_frame.pack(side=LEFT, padx=10)

shapes = [
    ("Line", "line"),
    ("Rect", "rect"),
    ("Oval", "oval"),
    ("Triangle", "triangle"),
    ("Arrow", "arrow"),
    ("Polygon", "polygon")
]

r = c = 0
for text, shape in shapes:
    Button(shapes_frame, text=text, width=8,
           command=lambda s=shape: select_tool(s)
           ).grid(row=r, column=c, padx=2, pady=2)
    c += 1
    if c == 3:
        c = 0
        r += 1

# -------- COLORS --------
colors_frame = LabelFrame(ribbon, text="Colours", fg="white", bg="#1e1e1e")
colors_frame.pack(side=LEFT, padx=10)

for c in ["black", "red", "green", "blue", "yellow", "orange", "purple"]:
    Button(colors_frame, bg=c, width=3,
           command=lambda col=c: set_color(col)).pack(side=LEFT, padx=2)

Button(colors_frame, text="+",
       command=lambda: set_color(colorchooser.askcolor()[1])
       ).pack(side=LEFT)

# -------- ACTIONS --------
actions_frame = LabelFrame(ribbon, text="Actions", fg="white", bg="#1e1e1e")
actions_frame.pack(side=LEFT, padx=10)

Button(actions_frame, text="Fill", command=toggle_fill).pack(fill=X)
Button(actions_frame, text="Clear", command=clear_canvas).pack(fill=X)

# ---------------- STATUS BAR ----------------
status = StringVar(value="Tool: PENCIL")
Label(root, textvariable=status, relief=SUNKEN, anchor=W).pack(fill=X)

# ---------------- CANVAS ----------------
canvas = Canvas(root, bg="white", cursor="cross")
canvas.pack(fill=BOTH, expand=True)

img_id = canvas.create_image(0, 0, anchor=NW, image=tk_img)

# ---------------- DRAWING ----------------
def mouse_down(e):
    global start_x, start_y
    start_x, start_y = e.x, e.y
    if tool == "polygon":
        polygon_points.append((e.x, e.y))

def mouse_drag(e):
    global start_x, start_y
    if tool in ("pencil", "brush", "eraser"):
        color = "white" if tool == "eraser" else current_color
        width = brush_size * 2 if tool == "brush" else brush_size
        draw.line((start_x, start_y, e.x, e.y),
                  fill=color, width=width)
        start_x, start_y = e.x, e.y
        redraw()

def mouse_up(e):
    x, y = e.x, e.y

    if tool == "line":
        draw.line((start_x, start_y, x, y),
                  fill=current_color, width=brush_size)

    elif tool == "rect":
        draw.rectangle((start_x, start_y, x, y),
                       outline=current_color,
                       fill=current_color if fill_mode else None,
                       width=brush_size)

    elif tool == "oval":
        draw.ellipse((start_x, start_y, x, y),
                     outline=current_color,
                     fill=current_color if fill_mode else None,
                     width=brush_size)

    elif tool == "triangle":
        draw.polygon([start_x, y, (start_x + x)//2, start_y, x, y],
                     outline=current_color,
                     fill=current_color if fill_mode else None)

    elif tool == "arrow":
        draw.line((start_x, start_y, x, y),
                  fill=current_color, width=brush_size)
        angle = math.atan2(start_y - y, start_x - x)
        size = 15
        p1 = (x + size * math.cos(angle + 0.3),
              y + size * math.sin(angle + 0.3))
        p2 = (x + size * math.cos(angle - 0.3),
              y + size * math.sin(angle - 0.3))
        draw.polygon([x, y, *p1, *p2], fill=current_color)

    redraw()

def finish_polygon(e):
    global polygon_points
    if len(polygon_points) > 2:
        draw.polygon(polygon_points,
                     outline=current_color,
                     fill=current_color if fill_mode else None)
        polygon_points = []
        redraw()

# ---------------- BINDINGS ----------------
canvas.bind("<ButtonPress-1>", mouse_down)
canvas.bind("<B1-Motion>", mouse_drag)
canvas.bind("<ButtonRelease-1>", mouse_up)
canvas.bind("<Double-Button-1>", finish_polygon)

root.mainloop()
