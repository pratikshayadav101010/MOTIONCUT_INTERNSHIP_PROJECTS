import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import random

# List of questions
questions = [
    "What is the largest ocean in the world?",
    "Which planet is known as the Red Planet?",
    "Who wrote the play Romeo and Juliet?",
    "What is the currency of Japan?",
    "What is the largest organ in the human body?",
]

# List of answer choices for each question
answer_choice = [
    ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
    ["Venus", "Mars", "Jupiter", "Saturn"],
    ["William Shakespeare", "Jane Austen", " Charles Dickens", "F. Scott Fitzgerald"],
    [" Euro", "Dollar", " Yen", "Rupee"],
    ["Heart", "Liver", "Brain", "Skin"],
]

# List of correct answers
answers = [3, 1, 0, 2, 3]

# List to store user's answers
user_answer = []

# List to store randomly generated indexes for questions
indexes = []

# Function to generate unique random indexes for questions
def gen():
    global indexes
    while len(indexes) < 5:
        x = random.randint(0, 4)
        if x in indexes:
            continue
        else:
            indexes.append(x)

# Function to display the final score and feedback
def showresult(score):
    # Clear all widgets from the window
    for widget in root.winfo_children():
        widget.destroy()

    # Set the background color for the entire window
    root.config(background="pink")

    # Display final score and feedback
    result_str = f"Your Final Score: {score}/5\n\n"
    for i in range(5):
        is_correct = user_answer[i] == answers[indexes[i]]
        result_str += f"Question {i + 1}: {'Correct' if is_correct else 'Incorrect'}"
        if not is_correct:
            result_str += f" (Correct Answer: {answer_choice[indexes[i]][answers[indexes[i]]]})"
        result_str += "\n"

    result_label = Label(root, text=result_str, font=("Arial", 16), background="pink")
    result_label.pack(pady=(50, 50))

    thank_you_label = Label(root, text="Thank You For Participating!", font=("arial black", 24), background="pink")
    thank_you_label.pack(pady=(0, 50))

# Function to calculate the final score
def calc():
    global indexes, user_answer
    x = 0
    score = 0
    for i in indexes:
        if user_answer[x] == answers[i]:
            score += 1
        x += 1
    showresult(score)

# Variable to keep track of the current question
ques = 1

# Function to handle user's answer selection
def selected():
    global radiovar, user_answer, lblquestion, r1, r2, r3, r4, ques
    x = radiovar.get()
    user_answer.append(x)
    radiovar.set(-1)
    if ques < 5:
        lblquestion.config(text=questions[indexes[ques]])
        r1['text'] = answer_choice[indexes[ques]][0]
        r2['text'] = answer_choice[indexes[ques]][1]
        r3['text'] = answer_choice[indexes[ques]][2]
        r4['text'] = answer_choice[indexes[ques]][3]
        ques += 1
    else:
        calc()

# Function to initialize the quiz
def startquiz():
    global lblquestion, r1, r2, r3, r4, radiovar
    lblquestion = Label(
        root,
        text=questions[indexes[0]],
        font=("arial", 16),
        width=580,
        justify="center",
        wraplength=400,
        background="#aaffcc",  # Set your desired background color for the question window
    )
    lblquestion.pack(pady=(100, 30))

    # Set the background color for the entire window
    root.config(background="light yellow")

    # Rest of the code with modified background colors for options
    radiovar = IntVar()
    radiovar.set(-1)  # not by default checked

    r1 = Radiobutton(
        root,
        text=answer_choice[indexes[0]][0],
        font=("arial", 14),
        value=0,
        variable=radiovar,
        command=selected,
        background="pink",  # Set your desired background color for option 1
    )
    r1.pack(pady=5)

    r2 = Radiobutton(
        root,
        text=answer_choice[indexes[0]][1],
        font=("arial", 14),
        value=1,
        variable=radiovar,
        command=selected,
        background="pink",  # Set your desired background color for option 2
    )
    r2.pack(pady=5)

    r3 = Radiobutton(
        root,
        text=answer_choice[indexes[0]][2],
        font=("arial", 14),
        value=2,
        variable=radiovar,
        command=selected,
        background="pink",  # Set your desired background color for option 3
    )
    r3.pack(pady=5)

    r4 = Radiobutton(
        root,
        text=answer_choice[indexes[0]][3],
        font=("arial", 14),
        value=3,
        variable=radiovar,
        command=selected,
        background="pink",  # Set your desired background color for option 4
    )
    r4.pack(pady=5)

# Function to handle the start button press
def startispressed():
    label.destroy()
    lblinstruction.destroy()
    lblinstruction.destroy()
    lblrules.destroy()
    btn_start.destroy()
    gen()
    startquiz()

# Create the main window
root = tk.Tk()
root.title("QuizMaster")
root.geometry("700x600")
root.config(background="lavender")
root.resizable(0, 0)

# Open and convert the image to a format compatible with Tkinter
img_pil = Image.open("C:/Users/Pratiksha/Desktop/MOTIONCUT PYTHON INTERNSHIP/quiz image.jpg")
img = ImageTk.PhotoImage(img_pil)


# Assuming img is a PhotoImage object
label = Label(root, image=img)
label.pack(padx=0, pady=25)

# Open and convert the second image
img_start_pil = Image.open("C:/Users/Pratiksha/Desktop/MOTIONCUT PYTHON INTERNSHIP/start.jpg")
# Resize the image to the desired width and height
img_start_pil_resized = img_start_pil.resize((250, 100), Image.ANTIALIAS)
img_start = ImageTk.PhotoImage(img_start_pil_resized)

# Decrease the size of the button
btn_start = Button(root, image=img_start, command=startispressed)
btn_start.pack(padx=0, pady=15)

lblinstruction = Label(
    root,
    text="Read the Rules and \n Click Quiz to Start the Quiz Once You are Ready !!",
    background="lavender",
    font=("Arial black", 13),
    justify="center",
)
lblinstruction.pack(padx=0, pady=25)

lblrules = Label(
    root,
    text="This quiz conatains 5 Questions \n Once you select a radio button that will be a final choice \nHence think before you select\n All The Best!! ",
    width=100,
    font=("ARIAL", 13),
    background="#000000",
    foreground="yellow",
)

lblrules.pack()

root.mainloop()
