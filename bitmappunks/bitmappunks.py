import csv
from tkinter import *
from tkinter import filedialog
import webbrowser

OUTPUT = []
viewURL = "https://bitfeed.live/block/height/"

#Create an instance of tkinter frame
window = Tk()
window.title("Bitmap Punk QuickView")

# Function to open the file dialog
def open_file_dialog():
    # Open the file dialog
    return filedialog.askopenfilename()


def openBrowser(event):
   selected_item = listbox.get(listbox.curselection())
   webbrowser.open_new_tab(viewURL+selected_item)

def remove_non_digits(string):
    return ''.join(char for char in string if char.isdigit())

#############################################################################################################################################


with open(open_file_dialog(), 'r', encoding='utf-8') as file:
    data = csv.reader(file)

    for row in data:
        timestamp, bitmapInscriptionID, bitmapBlockNumber, date, sizeByValue, sizeByBytes, transactions, subKrange, negativePunk, historicalPunk, perfectPunk = row[:11]
        bitmapBlockNumber = remove_non_digits(bitmapBlockNumber)
        if bitmapBlockNumber.isdigit():
            OUTPUT.append(bitmapBlockNumber)

frLeft = Frame(window)

frLeft.grid(row=0,column=0)

# Create a scrollbar
scrollbar = Scrollbar(frLeft)
# Create a Listbox
listbox = Listbox(frLeft, yscrollcommand=scrollbar.set)
# Add items to the Listbox
for i in OUTPUT:
    listbox.insert(END, i)
# Bind the <<ListboxSelect>> event to the on_item_select function
listbox.bind("<<ListboxSelect>>",openBrowser)
# Configure the scrollbar to control the Listbox
scrollbar.config(command=listbox.yview)

# Pack the Listbox
listbox.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

window.mainloop()