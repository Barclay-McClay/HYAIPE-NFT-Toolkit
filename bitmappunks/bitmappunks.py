import csv
from tkinter import *
from tkinter import filedialog , ttk
import webbrowser

SORT_ORDER = {}
viewURL = "https://bitfeed.live/block/height/"

#Create an instance of tkinter frame
window = Tk()
window.title("Bitmap Punk QuickView")

# Function to open the file dialog
def open_file_dialog():
    # Open the file dialog
    return filedialog.askopenfilename()

def openBrowser(event):
    print("hello")
    selected_item = tree.selection()
    print(selected_item)
    if selected_item:
        print("hello again")
        column_value = tree.set(selected_item, 2)
        webbrowser.open_new_tab(viewURL+column_value)

def remove_non_digits(string):
    return ''.join(char for char in string if char.isdigit())

def sort_treeview(column):
    # Clear existing items in the Treeview
    tree.delete(*tree.get_children())
    # Get the index of the selected column
    column_index = tree["columns"].index(column)
    # Sort the data based on the selected column and sort order
    rev = False if SORT_ORDER[column] == 'asc' else True
    sorted_data = sorted(OUTPUT, key=lambda x: x[column_index], reverse=rev)
    # Insert sorted data into the Treeview
    for i, item in enumerate(sorted_data):
        tree.insert(
            "",
            index=END,
            text=str(i + 1),
            values=item
        )
    
def on_header_click(event, column):
  # Get the current sort order of the column
    current_order = SORT_ORDER.get(column, "")
    # Toggle the sort order between ascending and descending
    new_order = "asc" if current_order == "desc" else "desc"
    # Clear the existing sort indicator arrow
    for col in tree["columns"]:
        tree.heading(col, text=col)
    # Add the sort indicator arrow to the clicked column
    arrow = " ▲" if new_order == "asc" else " ▼"
    tree.heading(column, text=column + arrow)
    # Update the sort order for the clicked column
    SORT_ORDER[column] = new_order
    # Sort the Treeview based on the clicked column and order
    sort_treeview(column)


#############################################################################################################################################

with open(open_file_dialog(), 'r', encoding='utf-8') as file:
    data = csv.reader(file)
    OUTPUT=list(data)
    for row in data:
        timestamp, bitmapInscriptionID, bitmapBlockNumber, date, sizeByValue, sizeByBytes, transactions, subKrange, negativePunk, historicalPunk, perfectPunk = row[:11]
        bitmapBlockNumber = remove_non_digits(bitmapBlockNumber)
frLeft = Frame(window)
frLeft.pack()

# Create a Treeview widget to display the data
tree = ttk.Treeview(window)
tree["columns"] = (
    "timestamp",
    "inscription_id",
    "block_number",
    "date",
    "size_value",
    "size_bytes",
    "transactions",
    "sub_k_range",
    "negative_punk",
    "historical_punk",
    "perfect_punk"
)
# Define column headings
tree.heading("#0", text="Index")
tree.heading("timestamp", text="Timestamp")
tree.heading("inscription_id", text="Bitmap Inscription ID")
tree.heading("block_number", text="Bitmap Block Number")
tree.heading("date", text="Date")
tree.heading("size_value", text="Size By Value")
tree.heading("size_bytes", text="Size By Bytes")
tree.heading("transactions", text="Transactions")
tree.heading("sub_k_range", text="Sub K and Range")
tree.heading("negative_punk", text="Negative Punk")
tree.heading("historical_punk", text="Historical Punk")
tree.heading("perfect_punk", text="Perfect Punk")

# Define column widths
tree.column("#0", width=50, minwidth=50, anchor=CENTER)
tree.column("timestamp", width=150, minwidth=100, anchor=CENTER)
tree.column("inscription_id", width=150, minwidth=100, anchor=CENTER)
tree.column("block_number", width=150, minwidth=100, anchor=CENTER)
tree.column("date", width=100, minwidth=80, anchor=CENTER)
tree.column("size_value", width=100, minwidth=80, anchor=CENTER)
tree.column("size_bytes", width=100, minwidth=80, anchor=CENTER)
tree.column("transactions", width=100, minwidth=80, anchor=CENTER)
tree.column("sub_k_range", width=150, minwidth=100, anchor=CENTER)
tree.column("negative_punk", width=100, minwidth=80, anchor=CENTER)
tree.column("historical_punk", width=100, minwidth=80, anchor=CENTER)
tree.column("perfect_punk", width=100, minwidth=80, anchor=CENTER)

# Insert data into the Treeview
for i, item in enumerate(OUTPUT):
    tree.insert(
        "",
        index=END,
        text=str(i + 1),
        values=item
    )

# Create clickable column headers
for i, column in enumerate(tree["columns"]):
    tree.heading(column, text=column)
    tree.heading(column, command=lambda col=column: on_header_click(event=None, column=col))

tree.bind("<<TreeviewSelect>>", openBrowser)

# Add Treeview to a Scrollbar
scrollbar = Scrollbar(window, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
# Pack the Treeview and Scrollbar
tree.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)


window.mainloop()