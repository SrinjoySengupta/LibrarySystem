"""
LIBRARY MANAGEMENT SYSTEM
Developed by Srinjoy Sengupta

A beautiful blue-themed library management application with:
- Modern interface design
- Colorful interactive buttons
- Smooth user experience
"""

import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import tkinter.simpledialog as sd

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Library Management System")
        self.root.geometry("1100x650")
        self.root.configure(bg="#e6f2ff")
        self.root.resizable(False, False)
        
        # Custom colors
        self.bg_color = "#e6f2ff"  # Light blue background
        self.panel_color = "#cce0ff"  # Medium blue panels
        self.button_color = "#4d94ff"  # Bright blue buttons
        self.highlight_color = "#80b3ff"  # Button hover color
        self.text_color = "#003366"  # Dark blue text
        self.accent_color = "#ff9933"  # Orange accent
        
        # Fonts
        self.title_font = ("Verdana", 16, "bold")
        self.label_font = ("Verdana", 10)
        self.button_font = ("Verdana", 10, "bold")
        
        # Initialize variables
        self.bk_name = StringVar()
        self.bk_id = StringVar()
        self.author_name = StringVar()
        self.bk_status = StringVar(value='Available')
        self.card_id = StringVar()
        
        # Setup database
        self.initialize_database()
        self.populate_sample_data()
        
        # Configure UI
        self.configure_ui()
        self.display_records()

    def initialize_database(self):
        """Initialize database connection and create tables"""
        self.connector = sqlite3.connect('library.db')
        self.cursor = self.connector.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Library (
                BK_NAME TEXT, 
                BK_ID TEXT PRIMARY KEY NOT NULL, 
                AUTHOR_NAME TEXT, 
                BK_STATUS TEXT, 
                CARD_ID TEXT)
        ''')

    def populate_sample_data(self):
        """Insert sample book records if database is empty"""
        self.cursor.execute('SELECT COUNT(*) FROM Library')
        if self.cursor.fetchone()[0] == 0:
            sample_books = [
                ("Python Crash Course", "PY1001", "Eric Matthes", "Available", "N/A"),
                ("Deep Learning", "DL2002", "Ian Goodfellow", "Issued", "LIB1001"),
                ("The Pragmatic Programmer", "PP3003", "Andrew Hunt", "Available", "N/A"),
                ("Clean Code", "CC4004", "Robert Martin", "Issued", "LIB1002"),
                ("Design Patterns", "DP5005", "Erich Gamma", "Available", "N/A"),
                ("Algorithms", "AL6006", "Robert Sedgewick", "Available", "N/A"),
                ("Database Systems", "DB7007", "Raghu Ramakrishnan", "Issued", "LIB1003"),
                ("Computer Networks", "CN8008", "Andrew Tanenbaum", "Available", "N/A"),
                ("Operating Systems", "OS9009", "Abraham Silberschatz", "Issued", "LIB1004"),
                ("Artificial Intelligence", "AI1010", "Stuart Russell", "Available", "N/A")
            ]
            
            self.cursor.executemany(
                'INSERT INTO Library VALUES (?, ?, ?, ?, ?)',
                sample_books
            )
            self.connector.commit()

    def configure_ui(self):
        """Configure the beautiful user interface"""
        # Main header
        header = Frame(self.root, bg=self.button_color, height=80)
        header.pack(fill=X)
        
        title = Label(header, text="LIBRARY MANAGEMENT SYSTEM", 
                    font=self.title_font, bg=self.button_color, 
                    fg="white", pady=20)
        title.pack()
        
        # Main content frame
        main_frame = Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel - Controls
        left_panel = Frame(main_frame, bg=self.panel_color, 
                          bd=2, relief=GROOVE, padx=15, pady=15)
        left_panel.pack(side=LEFT, fill=Y)
        
        # Book Details Section
        detail_frame = LabelFrame(left_panel, text=" Book Details ", 
                                 font=self.label_font, bg=self.panel_color,
                                 fg=self.text_color, bd=2)
        detail_frame.pack(fill=X, pady=10)
        
        fields = [
            ("📖 Book Name", self.bk_name),
            ("🆔 Book ID", self.bk_id),
            ("✍️ Author", self.author_name)
        ]
        
        for text, var in fields:
            Label(detail_frame, text=text, bg=self.panel_color, 
                 font=self.label_font, fg=self.text_color).pack(anchor=W, pady=5)
            Entry(detail_frame, textvariable=var, font=self.label_font, 
                 bd=2, relief=GROOVE).pack(fill=X, pady=5)
        
        # Status Section
        status_frame = Frame(detail_frame, bg=self.panel_color)
        status_frame.pack(fill=X, pady=10)
        
        Label(status_frame, text="📌 Status", bg=self.panel_color, 
             font=self.label_font, fg=self.text_color).pack(side=LEFT, padx=5)
        
        status_menu = ttk.OptionMenu(status_frame, self.bk_status, 
                                   'Available', 'Available', 'Issued')
        status_menu.pack(side=LEFT, fill=X, expand=True)
        
        # Action Buttons
        button_frame = Frame(left_panel, bg=self.panel_color)
        button_frame.pack(fill=X, pady=20)
        
        buttons = [
            ("➕ Add Book", self.button_color, self.add_record),
            ("🔄 Update", "#4CAF50", self.update_record),
            ("🗑️ Delete", "#FF5733", self.delete_record),
            ("🧹 Clear", "#9C27B0", self.clear_fields),
            ("🔍 Search", "#FFC107", self.search_books)
        ]
        
        for text, color, command in buttons:
            btn = Button(button_frame, text=text, font=self.button_font,
                        bg=color, fg="white", activebackground=self.highlight_color,
                        bd=0, padx=10, pady=5, command=command)
            btn.pack(fill=X, pady=5, ipady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.highlight_color))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
        
        # Right Panel - Book List
        right_panel = Frame(main_frame, bg=self.bg_color)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
        
        list_frame = LabelFrame(right_panel, text=" Book Inventory ", 
                               font=self.label_font, bg=self.bg_color,
                               fg=self.text_color, bd=2)
        list_frame.pack(fill=BOTH, expand=True)
        
        # Treeview with scrollbar
        self.tree = ttk.Treeview(list_frame, columns=('Book Name', 'Book ID', 'Author', 'Status', 'Card ID'),
                                show='headings', height=15)
        
        # Configure columns
        columns = [
            ('Book Name', 250),
            ('Book ID', 100),
            ('Author', 150),
            ('Status', 100),
            ('Card ID', 100)
        ]
        
        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=CENTER)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", font=self.label_font, rowheight=25)
        style.configure("Treeview.Heading", font=("Verdana", 10, "bold"))
        style.map("Treeview", background=[('selected', self.highlight_color)])
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.tree.pack(fill=BOTH, expand=True)
        
        # Bind treeview selection
        self.tree.bind('<<TreeviewSelect>>', self.view_record)
        
        # Status bar
        self.status = Label(self.root, text="Ready", bd=1, relief=SUNKEN, 
                          anchor=W, font=("Verdana", 9), bg=self.button_color, fg="white")
        self.status.pack(fill=X)

    def display_records(self):
        """Display all books in the Treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for record in self.connector.execute('SELECT * FROM Library'):
            self.tree.insert('', END, values=record)
        
        self.status.config(text=f"Total Books: {len(self.tree.get_children())}")

    def add_record(self):
        """Add new book to database with validation"""
        if not self.validate_inputs():
            return
            
        if self.bk_status.get() == 'Issued':
            card_id = self.get_issuer_card()
            if not card_id:
                return
            self.card_id.set(card_id)
        
        try:
            self.cursor.execute(
                'INSERT INTO Library VALUES (?, ?, ?, ?, ?)',
                (self.bk_name.get(), self.bk_id.get(), 
                 self.author_name.get(), self.bk_status.get(), 
                 self.card_id.get())
            )
            self.connector.commit()
            self.display_records()
            self.clear_fields()
            mb.showinfo("Success", "Book added successfully")
            self.status.config(text="Book added successfully")
        except sqlite3.IntegrityError:
            mb.showerror("Error", "Book ID already exists!")
            self.status.config(text="Error: Book ID exists")

    def update_record(self):
        """Update existing book record"""
        if not self.validate_inputs():
            return
            
        if self.bk_status.get() == 'Issued' and not self.card_id.get():
            card_id = self.get_issuer_card()
            if not card_id:
                return
            self.card_id.set(card_id)
        
        self.cursor.execute(
            '''UPDATE Library SET 
            BK_NAME=?, AUTHOR_NAME=?, 
            BK_STATUS=?, CARD_ID=? 
            WHERE BK_ID=?''',
            (self.bk_name.get(), self.author_name.get(),
             self.bk_status.get(), self.card_id.get(), 
             self.bk_id.get())
        )
        self.connector.commit()
        self.display_records()
        mb.showinfo("Success", "Book updated successfully")
        self.status.config(text="Book updated successfully")

    def delete_record(self):
        """Delete selected book record"""
        selected = self.tree.focus()
        if not selected:
            mb.showerror("Error", "Please select a book to delete")
            self.status.config(text="Error: No book selected")
            return
            
        book_id = self.tree.item(selected)['values'][1]
        if mb.askyesno("Confirm", "Delete this book permanently?"):
            self.cursor.execute('DELETE FROM Library WHERE BK_ID=?', (book_id,))
            self.connector.commit()
            self.display_records()
            self.clear_fields()
            mb.showinfo("Success", "Book deleted successfully")
            self.status.config(text="Book deleted successfully")

    def search_books(self):
        """Search books by name or author"""
        search_term = sd.askstring("Search Books", "Enter book name or author:")
        if not search_term:
            return
            
        query = f'''
            SELECT * FROM Library 
            WHERE BK_NAME LIKE ? OR AUTHOR_NAME LIKE ?
        '''
        self.cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for record in self.cursor.fetchall():
            self.tree.insert('', END, values=record)
        
        self.status.config(text=f"Found {len(self.tree.get_children())} books matching '{search_term}'")

    def view_record(self, event):
        """Display selected record in fields"""
        selected_item = self.tree.focus()
        if not selected_item:
            return
            
        values = self.tree.item(selected_item, 'values')
        self.bk_name.set(values[0])
        self.bk_id.set(values[1])
        self.author_name.set(values[2])
        self.bk_status.set(values[3])
        self.card_id.set(values[4])
        self.status.config(text=f"Viewing: {values[0]}")

    def clear_fields(self):
        """Reset all input fields"""
        self.bk_name.set('')
        self.bk_id.set('')
        self.author_name.set('')
        self.bk_status.set('Available')
        self.card_id.set('')
        self.tree.selection_remove(self.tree.selection())
        self.status.config(text="Fields cleared")

    def validate_inputs(self):
        """Validate all input fields"""
        if not all([self.bk_name.get(), self.bk_id.get(), self.author_name.get()]):
            mb.showerror("Error", "Please fill all required fields")
            self.status.config(text="Error: Missing fields")
            return False
        return True

    def get_issuer_card(self):
        """Prompt for member card ID when issuing book"""
        card_id = sd.askstring("Member ID", "Enter member card ID:")
        if not card_id:
            mb.showerror("Error", "Member ID cannot be empty")
            self.status.config(text="Error: No member ID")
            return None
        return card_id

if __name__ == '__main__':
    root = Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()