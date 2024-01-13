import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

class ExpenseTracker:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("500x500")  
        self.root.configure(background='pink')  # Set background color

        # Database initialization
        self.conn = sqlite3.connect(':memory:')  # Using in-memory database for this 
        self.create_tables()

        # GUI elements
        # Labels and combobox for category
        self.label_category = ttk.Label(root, text="Category:", width=15, font=('Arial', 14))
        self.category_var = tk.StringVar()

        ttk.Style().configure('TCombobox', font=('Arial', 14))

        self.category_combobox = ttk.Combobox(root, textvariable=self.category_var, width=15, font=('Arial', 14))
        self.category_combobox['values'] = ('Food', 'Transportation', 'Entertainment', 'Others')
        self.category_combobox.set('Others')

        # Labels and entry for amount
        self.label_amount = ttk.Label(root, text="Amount:", width=15, font=('Arial', 14))
        self.entry_amount = ttk.Entry(root, width=15, font=('Arial', 14))

        # Labels and entry for description
        self.label_description = ttk.Label(root, text="Description:", width=15, font=('Arial', 14))
        self.entry_description = ttk.Entry(root, width=15, font=('Arial', 14))

        # Buttons for adding expense and showing summary
        self.btn_add = ttk.Button(root, text="Add Expense", command=self.add_expense, width=25, style='TButton')
        self.btn_summary = ttk.Button(root, text="Show Summary", command=self.show_summary, width=25, style='TButton')

        # Treeview for displaying expenses
        self.tree = ttk.Treeview(root, columns=('ID', 'Amount', 'Description', 'Category', 'Date'), show='headings')
        self.tree.heading('ID', text='ID', anchor=tk.CENTER)
        self.tree.heading('Amount', text='Amount', anchor=tk.CENTER)
        self.tree.heading('Description', text='Description', anchor=tk.CENTER)
        self.tree.heading('Category', text='Category', anchor=tk.CENTER)
        self.tree.heading('Date', text='Date', anchor=tk.CENTER)

        # Scrollbars for treeview
        scrollbar_y = ttk.Scrollbar(root, orient='vertical', command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(root, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

        # Configure style for treeview cells
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 12))

        style.configure('ID_tag', font=('Arial', 14))
        style.configure('Amount_tag', font=('Arial', 14))
        style.configure('Description_tag', font=('Arial', 14))
        style.configure('Date_tag', font=('Arial', 14))

        self.load_expenses()

        # Layout
        self.label_category.grid(row=0, column=0, padx=15, pady=5, sticky=tk.W)
        self.category_combobox.grid(row=0, column=1, padx=15, pady=5)

        self.label_amount.grid(row=1, column=0, padx=15, pady=5, sticky=tk.W)
        self.entry_amount.grid(row=1, column=1, padx=15, pady=5)

        self.label_description.grid(row=2, column=0, padx=15, pady=5, sticky=tk.W)
        self.entry_description.grid(row=2, column=1, padx=15, pady=5)

        self.btn_add.grid(row=3, column=0, columnspan=2, pady=10)
        self.btn_summary.grid(row=4, column=0, columnspan=2, pady=10)

        self.tree.grid(row=5, column=0, columnspan=2, padx=15, pady=15, sticky='nsew')
        scrollbar_y.grid(row=5, column=2, pady=15, sticky='ns')
        scrollbar_x.grid(row=6, column=0, columnspan=2, padx=15, sticky='ew')

        self.tree.bind('<Double-1>', self.edit_expense)

        ttk.Style().configure('TButton', font=('Arial', 14))

        # Configure grid row and column weights
        root.grid_rowconfigure(5, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def create_tables(self):
        # Create database tables if not exist
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                description TEXT,
                category TEXT,
                date TEXT
            )
        ''')
        self.conn.commit()

    def add_expense(self):
        # Add expense to the database
        category = self.category_var.get()
        amount = self.entry_amount.get()
        description = self.entry_description.get()

        if amount and description:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO expenses (amount, description, category, date) VALUES (?, ?, ?, ?)',
                           (amount, description, category, date))
            self.conn.commit()

            # Clear entry fields
            self.category_combobox.set('Others')
            self.entry_amount.delete(0, tk.END)
            self.entry_description.delete(0, tk.END)

            # Reload expenses in the treeview
            self.load_expenses()
        else:
            # Show error message if fields are not filled
            self.show_error_message("Please fill in all fields.")

    def load_expenses(self):
        # Load expenses from the database and display in the treeview
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM expenses')
        rows = cursor.fetchall()

        # Clear existing treeview items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert expenses into treeview
        for row in rows:
            self.tree.insert('', 'end', values=row, tags=('ID_tag', 'Amount_tag', 'Description_tag', 'Category', 'Date_tag'))

        # Adjust the height of the treeview based on the number of records
        num_records = len(rows)
        if num_records > 5:
            self.tree['height'] = 5
        else:
            self.tree['height'] = num_records

    def edit_expense(self, event):
        # Edit expense on double-click in the treeview
        selected_item = self.tree.selection()
        if selected_item:
            # Extract expense data from the selected item
            item_data = self.tree.item(selected_item)['values']

            # Open a new window for editing
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Expense")

            # Create and position entry fields
            ttk.Label(edit_window, text="ID:", width=20, font=('Arial', 14)).grid(row=0, column=0, padx=15, pady=10, sticky=tk.W)
            ttk.Label(edit_window, text="Amount:", width=20, font=('Arial', 14)).grid(row=1, column=0, padx=15, pady=10, sticky=tk.W)
            ttk.Label(edit_window, text="Description:", width=20, font=('Arial', 14)).grid(row=2, column=0, padx=15, pady=10, sticky=tk.W)
            ttk.Label(edit_window, text="Category:", width=20, font=('Arial', 14)).grid(row=3, column=0, padx=15, pady=10, sticky=tk.W)
            ttk.Label(edit_window, text="Date:", width=20, font=('Arial', 14)).grid(row=4, column=0, padx=15, pady=10, sticky=tk.W)

            id_label = ttk.Label(edit_window, text=item_data[0], width=30, font=('Arial', 14))
            id_label.grid(row=0, column=1, padx=15, pady=10)

            amount_entry = ttk.Entry(edit_window, width=30, font=('Arial', 14))
            amount_entry.insert(0, item_data[1])
            amount_entry.grid(row=1, column=1, padx=15, pady=10)

            description_entry = ttk.Entry(edit_window, width=30, font=('Arial', 14))
            description_entry.insert(0, item_data[2])
            description_entry.grid(row=2, column=1, padx=15, pady=10)

            category_entry = ttk.Entry(edit_window, width=30, font=('Arial', 14))
            category_entry.insert(0, item_data[3])
            category_entry.grid(row=3, column=1, padx=15, pady=10)

            date_label = ttk.Label(edit_window, text=item_data[4], width=30, font=('Arial', 14))
            date_label.grid(row=4, column=1, padx=15, pady=10)

            # Update expense on button click
            ttk.Button(edit_window, text="Update Expense",
                       command=lambda: self.update_expense(selected_item, amount_entry.get(), description_entry.get(),
                                                           category_entry.get(), edit_window)).grid(row=5, column=0, columnspan=2, pady=20)

    def update_expense(self, selected_item, amount, description, category, edit_window):
        # Update expense in the database
        if amount and description:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor = self.conn.cursor()
            cursor.execute('UPDATE expenses SET amount=?, description=?, category=?, date=? WHERE id=?',
                           (amount, description, category, date, selected_item[0]))
            self.conn.commit()

            # Close the edit window
            edit_window.destroy()

            # Reload expenses in the treeview
            self.load_expenses()

    def show_summary(self):
        # Calculate monthly expenses and category-wise expenditure
        cursor = self.conn.cursor()
        cursor.execute('SELECT strftime("%Y-%m", date) as month, SUM(amount) FROM expenses GROUP BY month')
        monthly_expenses = cursor.fetchall()

        cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
        category_expenditure = cursor.fetchall()

        # Display the summary in a new window
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Expense Summary")

        ttk.Label(summary_window, text="Monthly Expenses:", width=20, font=('Arial', 14)).grid(row=0, column=0, padx=15, pady=10, sticky=tk.W)
        ttk.Treeview(summary_window, columns=('Month', 'Total Expense')).grid(row=1, column=0, padx=15, pady=10)

        ttk.Label(summary_window, text="Category-wise Expenditure:", width=25, font=('Arial', 14)).grid(row=2, column=0, padx=15, pady=10, sticky=tk.W)
        category_tree = ttk.Treeview(summary_window, columns=('Category', 'Total Expense'))
        category_tree.grid(row=3, column=0, padx=15, pady=10)

        for row in monthly_expenses:
            summary_tree = summary_window.winfo_children()[1]
            summary_tree.insert('', 'end', values=row)

        for row in category_expenditure:
            category_tree.insert('', 'end', values=row)

    def show_error_message(self, message):
        # Show error message in a new window
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")

        ttk.Label(error_window, text=message, font=('Arial', 14), foreground='red').grid(row=0, column=0, padx=15, pady=10)

        ttk.Button(error_window, text="OK", command=error_window.destroy).grid(row=1, column=0, padx=15, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
