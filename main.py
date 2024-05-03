from tkinter import *
import tkinter as tk
from tkinter import filedialog, dialog
from matplotlib import colors
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageGrab

FONT_NAME = "Courier"

window = Tk()
window.title("Watermark")
window.config(bg="#4a4841")
window.resizable(False, False)

# Label
title_label = Label(text="WATERMARK", font=(FONT_NAME, 35, "bold"), bg="#4a4841")
title_label.grid(column=1, row=0)

canvas_picture = Canvas(width=700, height=700, highlightthickness=0, background="#4a4841")
canvas_picture.grid(column=0, row=1)

canvas_button = Canvas(width=200, height=700, highlightthickness=0, background="#4a4841")
canvas_button.grid(column=1, row=1)

photo_image = None
logo_image = None
entry_text = None
FONT_SIZE = 20
TEXT_COLOR = "black"
UP_DIRECTION = None
DOWN_DIRECTION = None
LEFT_DIRECTION = None
RIGHT_DIRECTION = None
OPACITY = 255
X_COR = 200
Y_COR = 200


# add_logo_button
def add_logo_action():
    global logo_image
    logo_file_path = filedialog.askopenfilename()
    if logo_file_path:
        # logo
        logo_original_image = Image.open(f"{logo_file_path}", mode="r")
        logo_resized_image = logo_original_image.resize((40, 40), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo_resized_image)
        window.logo = logo
        canvas_picture.create_image(50, 75, image=logo)



def save_canvas(canvas):
    # Update the canvas to ensure it's fully drawn
    canvas.update()

    # Get the bounds of the canvas
    x = canvas.winfo_rootx() + canvas.winfo_x()
    y = canvas.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    # Ask the user to select a folder for saving the image
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Construct the full file path
        file_path = f"{folder_path}/canvas_image.png"

        # Grab the image and crop to the canvas size
        ImageGrab.grab(bbox=(x, y, x1, y1)).save(file_path)
        print(f"Image saved to {file_path}")

def choose_photo_action():
    global photo_image
    photo_file_path = filedialog.askopenfilename()
    if photo_file_path:
        # Load the image
        original_image = Image.open(f"{photo_file_path}", mode="r")
        photo_resized_image = original_image.resize((650, 630), Image.Resampling.LANCZOS)
        # Convert the image to a format Tkinter can use
        photo = ImageTk.PhotoImage(photo_resized_image)
        window.photo = photo
        canvas_picture.create_image(340, 350, image=photo)


def color_to_rgb():
    fill_color = None
    if TEXT_COLOR == "red":
        fill_color = (255, 0, 0, OPACITY)
    elif TEXT_COLOR == "blue":
        fill_color = (0, 0, 255, OPACITY)

    elif TEXT_COLOR == "green":
        fill_color = (0, 255, 0, OPACITY)

    elif TEXT_COLOR == "yellow":
        fill_color = (255, 255, 0, OPACITY)

    elif TEXT_COLOR == "white":
        fill_color = (255, 255, 255, OPACITY)

    else:
        fill_color = (0, 0, 0, OPACITY)
    return fill_color


def change_opacity(opacity):
    global OPACITY
    if opacity == 1:
        OPACITY = min(255, OPACITY + 20)  # OPACITY değerini artır, ancak 255'i aşma
    elif opacity == -1:
        OPACITY = max(0, OPACITY - 20)  # OPACITY değerini azalt, ancak 0'ın altına düşme


def direction():
    global Y_COR, X_COR, UP_DIRECTION, DOWN_DIRECTION
    if 20 < Y_COR:
        Y_COR += UP_DIRECTION

    if Y_COR < 580:
        Y_COR += DOWN_DIRECTION

    if 20 < X_COR:
        X_COR += LEFT_DIRECTION

    if X_COR < 580:
        X_COR += RIGHT_DIRECTION


def add_text_action(text_color="black", font_size=20, up_direction=0, down_direction=0, left_direction=0,
                    right_direction=0, opacity=0):
    global entry_text, FONT_SIZE, TEXT_COLOR, UP_DIRECTION, DOWN_DIRECTION, LEFT_DIRECTION, RIGHT_DIRECTION, X_COR, Y_COR, OPACITY
    TEXT_COLOR = text_color
    FONT_SIZE = font_size
    UP_DIRECTION = up_direction
    DOWN_DIRECTION = down_direction
    LEFT_DIRECTION = left_direction
    RIGHT_DIRECTION = right_direction

    direction()

    entry_text = entry.get()

    # Create an image with transparent background
    img = Image.new('RGBA', (680, 680), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    # Set the font and size of the text
    font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    # Draw the text with desired opacity (alpha)

    change_opacity(opacity)
    print(OPACITY)
    draw.text((320, 320), entry_text, font=font, fill=color_to_rgb())
    # Convert the Image object to a format that Tkinter can use
    tk_img = ImageTk.PhotoImage(img)
    # Display the image on the canvas

    canvas_picture.create_image(X_COR, Y_COR, image=tk_img)
    print(f"X_cor: {X_COR} Y_cor: {Y_COR}")

    # Keep a reference to the image object
    canvas_picture.image = tk_img


# select photo
select_photo_button = Button(canvas_button, text="Select Files", command=choose_photo_action,
                             font=(FONT_NAME, 15, "bold"))
select_photo_button.configure(width=15, activebackground="#4a4841")
select_photo_button.place(x=0, y=0)


# add logo
add_logo_button = Button(canvas_button, text="Add Logo", command=add_logo_action, font=(FONT_NAME, 15, "bold"))
add_logo_button.configure(width=15, activebackground="#4a4841")
add_logo_button_window = canvas_button.create_window(100, 80, window=add_logo_button)
add_logo_button.place(x=0, y=45)

# Create an entry widget

entry_label = Label(canvas_picture, text="Text:", width=10, font=(FONT_NAME, 11, "bold"), bg="#4a4841", )
entry_label.place(x=0, y=0)

entry = Entry(canvas_picture, width=80, highlightthickness=3)
entry.insert(END, "Write text for adding image")
entry.place(x=70, y=0)

add_text_button = Button(canvas_button, text="Add Text",
                         command=lambda: add_text_action(opacity=OPACITY, text_color=TEXT_COLOR,
                                                         font_size=FONT_SIZE),
                         font=(FONT_NAME, 15, "bold"))
add_text_button.configure(width=15, activebackground="#4a4841")

add_text_button.place(x=0, y=90)


# save button
save_button = Button(canvas_button, text="Save Image", command=lambda: save_canvas(canvas_picture), font=(FONT_NAME, 15, "bold"))
save_button.configure(width=15, height=1, activebackground="#4a4841")
save_button_window = canvas_button.create_window(100, 80, window=save_button)
save_button.place(x=0, y=135)








# Color Buttons

# Red Button
add_red_color_button = Button(canvas_button, command=lambda: add_text_action(text_color="red",
                                                                             font_size=FONT_SIZE), bg="red")
add_red_color_button.configure(width=10, height=2, activebackground="#4a4841")
add_red_color_button.place(x=0, y=190)

# Blue Button
add_blue_color_button = Button(canvas_button, command=lambda: add_text_action(text_color="blue",
                                                                              font_size=FONT_SIZE), bg="blue")
add_blue_color_button.configure(width=10, height=2, activebackground="#4a4841")
add_blue_color_button.place(x=100, y=190)

# Green Button
add_green_button = Button(canvas_button, command=lambda: add_text_action(text_color="green",
                                                                         font_size=FONT_SIZE), bg="green")
add_green_button.configure(width=10, height=2, activebackground="#4a4841")
add_green_button.place(x=0, y=240)

# Yellow Button
add_yellow_button = Button(canvas_button, command=lambda: add_text_action(text_color="yellow",
                                                                          font_size=FONT_SIZE), bg="yellow")
add_yellow_button.configure(width=10, height=2, activebackground="#4a4841")
add_yellow_button.place(x=100, y=240)

# White Button
add_white_button = Button(canvas_button, command=lambda: add_text_action(text_color="white",
                                                                         font_size=FONT_SIZE), bg="white")
add_white_button.configure(width=10, height=2, activebackground="#4a4841")
add_white_button.place(x=0, y=290)

# Black Button
add_black_button = Button(canvas_button, command=lambda: add_text_action(text_color="black",
                                                                         font_size=FONT_SIZE), bg="black")
add_black_button.configure(width=10, height=2, activebackground="#4a4841")
add_black_button.place(x=100, y=290)

# Font Size Button (Spinbox)
font_size_label = Label(canvas_button, text="Font Size:", width=10, font=(FONT_NAME, 10, "bold"), bg="#4a4841")
font_size_label.place(x=0, y=350)
font_size_button = Spinbox(canvas_button, from_=20, to=50, width=10,
                           command=lambda: add_text_action(font_size=int(font_size_button.get()),
                                                           text_color=TEXT_COLOR))
font_size_button.place(x=90, y=350)

# Opacity Button
opacity_label = Label(canvas_button, text="Opacity:", width=10, font=(FONT_NAME, 11, "bold"), bg="#4a4841", )
opacity_label.place(x=0, y=390)

opacity_button_up = Button(canvas_button, text="🔼", command=lambda: add_text_action(opacity=1, text_color=TEXT_COLOR,
                                                                                    font_size=FONT_SIZE),
                           font=(FONT_NAME, 20, "bold"))
opacity_button_up.configure(width=2, height=1, activebackground="#4a4841")
opacity_button_up.place(x=90, y=390)

opacity_button_down = Button(canvas_button, text="🔽",
                             command=lambda: add_text_action(opacity=-1, text_color=TEXT_COLOR,
                                                             font_size=FONT_SIZE),
                             font=(FONT_NAME, 20, "bold"))
opacity_button_down.configure(width=2, height=1, activebackground="#4a4841")
opacity_button_down.place(x=90, y=440)

# Direction Button


Direction_label = Label(canvas_button, text="Direction:", width=10, font=(FONT_NAME, 11, "bold"), bg="#4a4841", )
Direction_label.place(x=0, y=500)

# Up Button
up_button = Button(canvas_button, text="🔼", command=lambda: add_text_action(up_direction=-10, text_color=TEXT_COLOR,
                                                                            font_size=FONT_SIZE),
                   font=(FONT_NAME, 20, "bold"))
up_button.configure(width=2, height=1, activebackground="#4a4841")
up_button.place(x=90, y=530)

# Down Button
down_button = Button(canvas_button, text="🔽", command=lambda: add_text_action(down_direction=10, text_color=TEXT_COLOR,
                                                                              font_size=FONT_SIZE),
                     font=(FONT_NAME, 20, "bold"))
down_button.configure(width=2, height=1, activebackground="#4a4841")
down_button.place(x=90, y=580)

# Left Button
left_button = Button(canvas_button, text="◀", command=lambda: add_text_action(left_direction=-10, text_color=TEXT_COLOR,
                                                                              font_size=FONT_SIZE),
                     font=(FONT_NAME, 20, "bold"))

left_button.configure(width=1, height=1, activebackground="#4a4841")
left_button.place(x=64, y=550)

# Right Button
right_button = Button(canvas_button, text="▶",
                      command=lambda: add_text_action(right_direction=10, text_color=TEXT_COLOR,
                                                      font_size=FONT_SIZE),
                      font=(FONT_NAME, 20, "bold"))
right_button.configure(width=1, height=1, activebackground="#4a4841")
right_button.place(x=132, y=550)









window.mainloop()
