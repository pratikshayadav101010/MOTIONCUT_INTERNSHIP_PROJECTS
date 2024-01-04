import tkinter as tk
from tkinter import messagebox

def count_words():
    input_text = text_widget.get("1.0", "end-1c").strip()  # Get text from the Text widget and remove leading/trailing spaces
    if not input_text:
        messagebox.showerror("Opps!!", "Please enter text before counting words.")
    else:
        words = input_text.split()
        word_count = len(words)
        result_label.config(text=f"Word Count: {word_count}")

window = tk.Tk()
window.title("WORD COUNT")
window.geometry("700x600")

# Set background color for the window
window.configure(bg="light cyan")

# Set background color and font color for Text widget
text_widget = tk.Text(window, height=20, width=60, font=("Arial", 12), bg="white", fg="black")  # Here fg is set to white
text_widget.pack(pady=20)

# Set background color and font color for Button
count_button = tk.Button(window, 
                         text="Count Words", 
                         command=count_words,
                         height=2, width=15,
                         bg='#0052cc', fg='white',  # Here fg is set to white
                         font=("Arial black", 15))
count_button.pack()

# Set background color and font color for Label
result_label = tk.Label(window, text="Word Count: ", font=("Arial black", 15), bg="black", fg="white")  # Here fg is set to white
result_label.pack(pady=10)

window.mainloop()
