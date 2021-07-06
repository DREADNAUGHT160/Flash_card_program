import pandas
from tkinter import *
import random

BACKGROUND_COLOR = "#B1DDC6"
# +++++++++++++++++++++++++++++++data extraction ++++++++++++++++++++++++++++++++#
try:
    data = pandas.read_csv("data/words_remains.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    french_words = data.to_dict(orient="records")
else:
    french_words = data.to_dict(orient="records")
random_word = {}


# ++++++++++++++++++++++++++++++++++flip card++++++++++++++++++++++++++++++++++++++#


def flip_card():
    flash_card.itemconfig(front_image, image=card_back)
    flash_card.itemconfig(fr_word, text=random_word["English"], fill="red")
    flash_card.itemconfig(title, text="English", fill="red")


# +++++++++++++++++++++++++++++++++++data_generating++++++++++++++++++++++++++++++#
def word_generator():
    global flip_timer, random_word
    window.after_cancel(flip_timer)
    random_word = random.choice(french_words)
    flash_card.itemconfig(title, text="French", fill="black")
    flash_card.itemconfig(fr_word, text=random_word["French"], fill="black")
    flash_card.itemconfig(front_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


# +++++++++++++++++++++++++++++++++++right answer++++++++++++++++++++++++++++++++++#
def is_known():
    french_words.remove(random_word)
    data1 = pandas.DataFrame(french_words)
    data1.to_csv("data/word_remains.csv", index=False)
    word_generator()


# ++++++++++++++++++++++++++++++++++++++++UX/UI++++++++++++++++++++++++++++++++++++#
window = Tk()
window.config(padx=50, pady=50)
window["background"] = BACKGROUND_COLOR
window.title("Flash Card(French edition)")

# windows.after is used to set timer instead of sleep function
flip_timer = window.after(3000, func=flip_card)

# flash card is a canvas
flash_card = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
front_image = flash_card.create_image(400, 263, image=card_front)
flash_card.grid(row=0, column=0, columnspan=2)
flash_card.config(bg=BACKGROUND_COLOR, highlightthickness=0)
fr_word = flash_card.create_text(400, 263, text="", font=("Ariel", 40, "italic"))
title = flash_card.create_text(400, 150, text="", font=("Ariel", 40, "bold"))

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=0, )

wrong_image = PhotoImage(file="images/wrong.png")
left_button = Button(image=wrong_image, highlightthickness=0, command=word_generator)
left_button.grid(row=1, column=1)
word_generator()
window.mainloop()
