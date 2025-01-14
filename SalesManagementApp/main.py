from tkinter import Tk, Label, Button, Entry, StringVar, Toplevel, Listbox, Scrollbar, END
from tkinter.ttk import Treeview
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, NUMERIC, ID
import os
import logging
from contants import DATABASE_PATH, LOGGING_PATH
from src.config.database import Database
from src.config.log import LogConfig


# Database setup
def setup_database():
    db = Database(DATABASE_PATH)
    db.init_tables()

def setup_logging():
    log = LogConfig(LOGGING_PATH)
    log.setup_logging()

# Whoosh Index setup
def setup_search_index():
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    schema = Schema(
        id=ID(stored=True, unique=True),
        ten_hang=TEXT(stored=True),
        ten_ncc=TEXT(stored=True),
        ten_khach_hang=TEXT(stored=True),
        ten_chi_phi=TEXT(stored=True)
    )
    create_in("indexdir", schema)

# Tkinter GUI Setup
class SalesManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Management System")
        self.root.geometry("800x600")

        Label(root, text="Sales Management System", font=("Arial", 20)).pack()
        Button(root, text="Manage Products", command=self.manage_products).pack(pady=10)
        Button(root, text="Manage Sales", command=self.manage_sales).pack(pady=10)
        Button(root, text="Manage Purchases", command=self.manage_purchases).pack(pady=10)
        Button(root, text="Manage Expenses", command=self.manage_expenses).pack(pady=10)
        Button(root, text="Reports", command=self.view_reports).pack(pady=10)

    def manage_products(self):
        self.open_window("Manage Products")

    def manage_sales(self):
        self.open_window("Manage Sales")

    def manage_purchases(self):
        self.open_window("Manage Purchases")

    def manage_expenses(self):
        self.open_window("Manage Expenses")

    def view_reports(self):
        self.open_window("Reports")

    def open_window(self, title):
        window = Toplevel(self.root)
        window.title(title)
        window.geometry("600x400")
        Label(window, text=title, font=("Arial", 16)).pack()
        # Placeholder for each section functionality
        Label(window, text="Functionality coming soon...", font=("Arial", 12)).pack()

if __name__ == "__main__":
    setup_logging()
    logging.info('Starting Sales Management System')
    setup_database()
    # setup_search_index()

    # root = Tk()
    # app = SalesManagementApp(root)
    # root.mainloop()
