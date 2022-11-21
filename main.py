import math
from tkinter import *
import time

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

SECONDS_IN_A_MINUTE = 60

reps = 1
check_text = ""
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_clicked():
    global check_text, reps
    reps = 1
    check_text = ""
    canvas.itemconfig(timer_text, text=f"00:00")
    timer_label.config(text="Timer")
    window.after_cancel(timer)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    if reps % 2 != 0:
        timer_value = WORK_MIN
        color = GREEN
        text = "Work"
    elif reps == 8:
        timer_value = LONG_BREAK_MIN
        color = RED
        text = "Long Break"
    else:
        timer_value = SHORT_BREAK_MIN
        color = PINK
        text = "Break"

    count_down(timer_value * SECONDS_IN_A_MINUTE)
    timer_label.config(text=text, fg=color)


def start_clicked():
    start_timer()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

# We can't make a loop to dismiss the time since then the GUI won't update this time
def count_down(count):
    global reps, check_text, timer
    min = math.floor(count / 60)
    sec = count % 60
    if min < 10:
        min = f"0{min}"
    if sec < 10:
        sec = f"0{sec}"

    canvas.itemconfig(timer_text, text=f"{min}:{sec}")
    if count > 0:
        timer = window.after(1000, count_down,
                             count - 1)  # wait an amount of time (in milliseconds) and do an action in buckle
    else:
        if reps % 2 != 0:
            check_text += "✓"
            check_label.config(text=check_text)
        reps += 1
        start_timer()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=50, pady=50, bg=YELLOW)

canvas = Canvas(width=210, height=224, bg=YELLOW, highlightthickness=0)  # canvas resized with the size of the image
# inside it
tomato_image = PhotoImage(file="tomato.png")  # create_image is waiting for a PhotoImage object
canvas.create_image(105, 112, image=tomato_image)  # position of the center of the image -> 100, 112 inside the canvas
timer_text = canvas.create_text(103, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

check_label = Label(font=(FONT_NAME, 20, "bold"), fg=GREEN, bg=YELLOW)
check_label.grid(row=3, column=1)

timer_label = Label(text="Timer", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=YELLOW)
timer_label.grid(row=0, column=1)

reset_button = Button(text="Reset", command=reset_clicked, highlightthickness=0)
reset_button.grid(row=2, column=2)

start_button = Button(text="Start", command=start_clicked, highlightthickness=0)
start_button.grid(row=2, column=0)

window.mainloop()  # looping every millisecond if something has changed into the GUI
