from tkinter import *
from tkinter import messagebox
import string
import random
import pyperclip

# Declare length_box globally
length_box = None
password_field = None
choice = None

#generator function to generate password as per user choice
def generator():
    small_alpha = string.ascii_lowercase
    capital_alpha = string.ascii_uppercase
    numbers = string.digits
    special_char = string.punctuation

    password_length = int(length_box.get())
    
    if choice.get() == 1:
        password = ''.join(random.sample(small_alpha, password_length))
    elif choice.get() == 2:
        password = ''.join(random.sample(small_alpha + capital_alpha, password_length))
    elif choice.get() == 3:
        password = ''.join(random.sample(small_alpha + capital_alpha + numbers + special_char, password_length))
    else:
        password = messagebox.showerror("Error","Select radiobutton first for password type")

    password_field.delete(0, END)  # Clear previous password
    password_field.insert(0, password)

def copy():
    random_password = password_field.get()
    if random_password:
        pyperclip.copy(random_password)
        messagebox.showinfo("Success", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "Generate a password first before copying!")

def proceed_button_click():
    global choice  # Declare choice globally
    choice = IntVar()

    if choice.get() is None:
        messagebox.showerror("Error", "Select a password strength first!")
        return

    # Function to open a new window
    new_window = Toplevel(root)
    new_window.title("Password Generator")
    new_window.geometry("700x600")
    new_window.config(bg="gray20")

    Font = ("Helvetica", 18, "bold")

    # Add content to the new window
    label_in_new_window = Label(new_window, text="Password Generator", font=("Helvetica", 26, "bold"), bg="gray20", fg="yellow")
    label_in_new_window.pack(pady=20)

    weak_radiobutton = Radiobutton(new_window, text="Weak", value=1, variable=choice, font=Font, bg="gray20", fg="white")
    weak_radiobutton.pack(pady=5)

    medium_radiobutton = Radiobutton(new_window, text="Medium", value=2, variable=choice, font=Font, bg="gray20", fg="white")
    medium_radiobutton.pack(pady=5)

    strong_radiobutton = Radiobutton(new_window, text="Strong", value=3, variable=choice, font=Font, bg="gray20", fg="white")
    strong_radiobutton.pack(pady=5)

    length_label = Label(new_window, text="Password Length", font=Font, bg="gray20", fg="white")
    length_label.pack(pady=5)

    global length_box  # Move length_box outside the function to make it accessible to the generator function
    length_box = Spinbox(new_window, from_=5, to_=20, width=5, font=Font)
    length_box.pack(pady=15)

    #generate_button to generate password in textfield
    generate_button = Button(new_window, text="Generate Password", font=Font, bg="blue", fg="white", command=generator)
    generate_button.pack(pady=15)

    global password_field  # Move password_field outside the function for easier access
    password_field = Entry(new_window, width=25, bd=2, font=Font)
    password_field.pack(pady=15)

    #copy_button to copy password
    copy_button = Button(new_window, text="Copy Password", bg="green", fg="white", font=Font, command=copy)
    copy_button.pack(pady=15)

# Main window
root = Tk()
root.config(bg="gray20")
root.title("Password Generator UI")
root.geometry("700x600")

welcomelabel = Label(root, text="WELCOME TO", font=("Helvetica", 26, "bold"), bg="gray20", fg="white")
welcomelabel.grid(row=0, column=0, pady=10, sticky="nsew")  # Center both horizontally and vertically

# Use a PNG image for better compatibility with Tkinter
image_path = r"C:\Users\Pratiksha\Desktop\MOTIONCUT PYTHON INTERNSHIP\pass.png"

# Decrease the size of the image
img = PhotoImage(file=image_path).subsample(2, 2)  # Change the values to adjust the size

image_label = Label(root, image=img, bg="gray20")
image_label.grid(row=1, column=0, pady=10, sticky="nsew")  # Center both horizontally and vertically

# Add a smaller Proceed button
proceed_button = Button(root, text="Proceed", font=("Helvetica", 20, "bold"), command=proceed_button_click, height=1, width=5, bg="red", fg="white")
proceed_button.grid(row=2, column=0, pady=10, sticky="nsew")  # Center both horizontally and vertically

# Configure grid row and column weights to make the labels and button expand to the center
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
