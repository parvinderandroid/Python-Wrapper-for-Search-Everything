from backend import search_xyz

from os import startfile

from subprocess import run

from tkinter import BOTH
from tkinter import BOTTOM
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import YES
from tkinter import Menu
from tkinter import StringVar
from tkinter import Tk

from tkinter.ttk import Entry
from tkinter.ttk import Label
from tkinter.ttk import Scrollbar
from tkinter.ttk import Style
from tkinter.ttk import Treeview


def search(*args):
    results.delete(*results.get_children())
    current_num_of_objects, value_items = search_xyz(entry_var.get())
    change_footer_text(current_num_of_objects)
    for value in value_items:
        results.insert("", "end", text="Listbox", values=value)


def call_on_startup():
    total_num_of_objects, value_items = search_xyz("")
    change_footer_text(total_num_of_objects)
    for value in value_items:
        results.insert("", "end", text="Listbox", values=value)


def open_path():
    run(["explorer.exe", "/select,", results.item(results.focus())["values"][1]])


def open_files(event):
    startfile(results.item(results.focus())["values"][1])


def change_footer_text(result_count):
    num_of_results.set(result_count)


def do_popup(event):
    item = results.identify_row(event.y)
    results.selection_set(item)
    try:
        context_menu.tk_popup(event.x_root, event.y_root, 0)
    finally:
        context_menu.grab_release()


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children("")]
    if col == "Size (KB)":
        l.sort(key=lambda x: int(x[0]), reverse=reverse)
    else:
        l.sort(key=lambda x: x[0].lower(), reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, "", index)

    # reverse sort next time
    tv.heading(
        col,
        text=col,
        command=lambda _col=col: treeview_sort_column(tv, _col, not reverse),
    )


root = Tk()
root.title("Flash Search")

# Adding theme
s = Style()
s.theme_use("winnative")

# Setting the window size
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w / 2, h / 2))
root.state("zoomed")  # This will launch the windows in maximized mode

entry_var = StringVar()
num_of_results = StringVar()

# Creating an entry for input using widget Entry
entry_field = Entry(
    root, font=("calibre", 10, "normal"), width=50, textvariable=entry_var
)

# Creating a listbox to display search results
columns = ("Name", "Path", "Size (KB)", "Extension", "Date Modified")
results = Treeview(root, columns=columns, selectmode="browse", show="headings")
for col in columns:
    results.heading(
        col,
        text=col,
        command=lambda _col=col: treeview_sort_column(results, _col, False),
    )

results.heading(columns[0], text=columns[0], anchor="sw")
results.heading(columns[1], text=columns[1], anchor="sw")
results.heading(columns[2], text=columns[2], anchor="se")
results.heading(columns[3], text=columns[3], anchor="sw")
results.heading(columns[4], text=columns[4], anchor="sw")

results.column(columns[0], width=100, anchor="sw")
results.column(columns[1], width=300, anchor="sw")
results.column(columns[2], width=30, anchor="se")
results.column(columns[3], width=30, anchor="sw")
results.column(columns[4], width=30, anchor="sw")

# Creating a scrollbar
scrollbar = Scrollbar(root)

# Creating a label for number of results
footer = Label(results, textvariable=num_of_results)

# Creating a right click menu
context_menu = Menu(root, tearoff=0)
context_menu.add_command(label="Open Path", command=open_path)

results.bind("<Button-3>", do_popup)

# Placing the entry in the required position using pack method
entry_field.focus()
entry_field.pack(fill=BOTH)

# Keep track of what is in the entry_field
entry_var.trace("w", search)

# Placing the results in the required position
results.pack(side=LEFT, fill=BOTH, expand=YES)

# Placing the number of results label at the bottom
footer.pack(side=BOTTOM, fill=BOTH)

# Binding open_files with double click and enter key
results.bind("<Double-1>", open_files)
results.bind("<Return>", open_files)

# Placing the results in the required position
scrollbar.pack(side=RIGHT, fill=BOTH)

# attach listbox to scrollbar
results.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=results.yview)

# Performing an infinite loop for the window to display
# root.wait_visibility()
call_on_startup()
root.mainloop()
