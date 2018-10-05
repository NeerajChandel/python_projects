#   Coding a simple text editor, using Python
#   Date/Day: 6th October 2018/Saturday
#   Author: Neeraj
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.messagebox import askyesno
from tkinter import messagebox
from tkinter import filedialog
import datetime
import time
import webbrowser


#   --------------- FILE MENU FUNCTIONS ----------------
def new_file():
    if askyesno("NELL-Edit", "Do you want to save the changes made?"):  # if clicked on yes, this condition will be true
        file_name = filedialog.asksaveasfilename()
        if file_name:   # if file_name exists
            all_text = text_box.get(1.0, END)   # get entire text -> from the 1st line to the last!
            open(file_name, 'w').write(all_text)    # create a file, and write the entire text inside it

    # ask if the user wants to open a new file:
    if askyesno("NELL-Edit", "Open an existing file?"):
        text_box.delete(1.0, END)   # clear the text
        file = open(filedialog.askopenfilename(), "r")  # open the file in read mode
        if file != "":  # if file not an empty file
            read_text = file.read() # read the file that's opened
            text_box.insert(INSERT, read_text) # and insert it to text_box to read
        else:
            pass
    else:   # if user doesn't want to open an existing file
        text_box.delete(1.0, END)   # simply delete the text_box contents


def open_file():
    # first, delete all the text!
    text_box.delete(1.0, END)
    file_open = open(filedialog.askopenfilename(), "r")
    if file_open != "": # if file_open not empty!
        read_text = file_open.read()
        text_box.insert(INSERT, read_text)
    else:
        pass


def save_as():
    file_name = filedialog.asksaveasfilename()
    if file_name:   # if exists
        entire_text = text_box.get(1.0, END)
        open(file_name, 'w').write(entire_text)


def close_file():
    if askyesno("NELL-Edit", "Do you want to save the changes made?"):  # if clicked on yes, this condition will be true
        file_name = filedialog.asksaveasfilename()
        if file_name:   # if file_name exists
            all_text = text_box.get(1.0, END)   # get entire text -> from the 1st line to the last!
            open(file_name, 'w').write(all_text)    # create a file, and write the entire text inside it
        if messagebox.askokcancel("Quit", "Do you really want to quit?"): # ask if the user really wants to quit?
            root.destroy()  # if ok pressed, destroy the window
    else:
        if messagebox.askokcancel("Quit", "Do you really want to quit?"): # ask if the user really wants to quit?
            root.destroy()  # if ok pressed, destroy the window


#   -----------------------------------------------------


#   --------------- EDIT MENU FUNCTIONS ----------------
def cut():
    # to clear the clipboard of any previously copied text, we first do:
    text_box.clipboard_clear()
    # then we append to the clipboard the selected text:
    text_box.clipboard_append(text_box.selection_get()) # append selected text to the clipboard
    # get the text from the starting of the selection to the ending
    select_text = text_box.get(SEL_FIRST, SEL_LAST)
    # since we are cutting, delete the selected text (after copying it to the clipboard!)
    text_box.delete(SEL_FIRST, SEL_LAST)


def copy():
    # to clear the clipboard of any previously copied text:
    text_box.clipboard_clear()
    text_box.clipboard_append(text_box.selection_get())


def paste():
    try:
        paste_text = text_box.selection_get(selection = 'CLIPBOARD')    # select the text from the clipboard to be pasted
        text_box.insert(INSERT, paste_text) # paste the text (insert it) to the text-box
    except:
        pass


def erase():
    selected_text = text_box.get(SEL_FIRST, SEL_LAST)
    text_box.delete(SEL_FIRST, SEL_LAST)    # erase only the selected portion of the text


def clear_screen():
    text_box.delete(1.0, END)   # delete the entire contents of the text-box
#   -----------------------------------------------------


#   --------------- INSERT MENU FUNCTIONS ----------------
def current_date():
    data = datetime.date.today()
    text_box.insert(INSERT, data)


def current_time():
    data = time.asctime()
    text_box.insert(INSERT, data)
#   -----------------------------------------------------


#   --------------- FORMAT MENU FUNCTIONS ----------------
def text_color():
    # triple -> takes r, g, b values, together as a string
    (triple, color) = askcolor()
    if color:
        text_box.config(foreground = color)


def no_format():
    text_box.config(font = ("Times New Roman", 16))


def bold_text():
    current_tags = text_box.tag_names("sel.first")
    if "bt" in current_tags:
        text_box.tag_remove("bt", "sel.first", "sel.last")
        text_box.tag_config("bt", font = ("Times New Roman", 16, "bold"))
    else:
        text_box.tag_add("bt", "sel.first", "sel.last")
        text_box.tag_config("bt", font = ("Times New Roman", 16, "bold"))


def italicise_text():
    current_tags = text_box.tag_names("sel.first")
    if "bt" in current_tags:
        text_box.tag_remove("bt", "sel.first", "sel.last")
        text_box.tag_config("bt", font = ("Times New Roman", 16, "italic"))
    else:
        text_box.tag_add("bt", "sel.first", "sel.last")
        text_box.tag_config("bt", font = ("Times New Roman", 16, "italic"))


def underline_text():
    # current_tags = text_box.tag_names("sel.first")
    # if "bt" in current_tags:
    #     text_box.tag_remove("bt", "sel.first", "sel.last")
    #     text_box.tag_config("bt", font = ("Times New Roman", 16, "underline"))
    # else:
    #     text_box.tag_add("bt", "sel_first", "sel_last")
    #     text_box.tag_config("bt", font = ("Times New Roman", 16, "underline"))
    text_box.tag_add("here", "sel.first", "sel.last")
    text_box.tag_config("here", font = ("Times New Roman", 16, "underline"))


def highlight_text():
    text_box.tag_add("here", "sel.first", "sel.last")
    text_box.tag_config("here", background = "black", foreground = "white")
#   -----------------------------------------------------


#   --------------- PERSONALIZE MENU FUNCTIONS ----------------
def background():
    (triple, color) = askcolor()
    if color:
        text_box.color(background = color)


# def full_screen():
#     # Following is the fullscreen code
#     root.attributes('-fullscreen', True)
#     root.bind('<Escape>', lambda e: root.destroy())
#     #OR:
#     #root.geometry("%dx%d+0+0" % (SW, SH))
#   -----------------------------------------------------


#   --------------- HELP MENU FUNCTIONS ----------------
def about():
    messagebox.showinfo("About", "Just Another Text Editor.\n Copyright:\n No rights left to reserve.")


def online_help():
    webbrowser.open("https://github.com/NeerajChandel")
#   -----------------------------------------------------


#   main() function
if __name__ == "__main__":
    # create an object of the Tkinter class
    root = Tk() # root -> like a handle to our window
    # name our window/text-editor
    root.title("NELL-Edit")

    # get width-height of the screen
    SCREEN_WIDTH = root.winfo_screenwidth()
    SCREEN_HEIGHT = root.winfo_screenheight()

    #   ----------- FILE MENU ------------
    # create the menu object (for menu bar) from the tkinter class
    main_menu = Menu(root)
    # create the object for the sub-menu commands
    file_command = Menu(root)

    root.config(menu = main_menu)

    # adding cascaded menus:
    main_menu.add_cascade(label = "File", menu = file_command)
    # we'll add elements/objects/attributes to the label 'File'
    # after clicking on the label 'New File', the new_file() function will be called
    file_command.add_command(label = "New File", command = new_file)
    file_command.add_command(label = "Open", command = open_file)
    file_command.add_command(label = "Save As", command = save_as)
    file_command.add_separator()
    file_command.add_command(label = "Quit", command = close_file)

    #   ----------- EDIT MENU ------------
    edit_command = Menu(root)
    main_menu.add_cascade(label = "Edit", menu = edit_command)
    edit_command.add_command(label = "Cut", command = cut)
    edit_command.add_command(label = "Copy", command = copy)
    edit_command.add_command(label = "Paste", command = paste)
    # add a seperator
    edit_command.add_separator()
    edit_command.add_command(label = "Delete", command = erase)  # deletes selected text
    edit_command.add_command(label = "Clear Screen", command = clear_screen)

    #   ----------- INSERT MENU ------------
    insert_command = Menu(root)
    main_menu.add_cascade(label = "Insert", menu = insert_command)
    insert_command.add_command(label = "Current Date", command = current_date)
    insert_command.add_command(label = "Current Time", command = current_time)

    #   ----------- FORMAT MENU ------------
    format_command = Menu(root) # to change the font's formatting
    main_menu.add_cascade(label = "Format", menu = format_command)
    format_command.add_command(label = "Font", command = text_color)
    # add a seperator after Font
    format_command.add_separator()
    format_command.add_command(label = "No Format", command = no_format)
    format_command.add_separator()
    format_command.add_command(label = "Bold", command = bold_text)
    format_command.add_command(label = "Italic", command = italicise_text)
    format_command.add_command(label = "Underline", command = underline_text)
    format_command.add_command(label = "Highlight", command = highlight_text)

    #   ----------- PERSONALIZE MENU ------------
    # personalizing will contain changing colors(background et al.)
    personalize_command = Menu(root)
    main_menu.add_cascade(label = "Personalize", menu = personalize_command)
    personalize_command.add_command(label = "Background", command = background)
    # personalize_command.add_command(label = "View Fullscreen", command = full_screen)

    #   ----------- HELP MENU ------------
    user_help = Menu(root)
    main_menu.add_cascade(label = "Help", menu = user_help)
    user_help.add_command(label = "About", command = about)
    user_help.add_separator()
    user_help.add_command(label = "Online Help", command = online_help)

    # defining text-box attributes
    text_box = Text(root, height = "20", width = "80", font = ("Times New Roman", 16))
    # add a scrollbar vertically (y-axis):
    y_scrollbar = Scrollbar(root, command = text_box.yview)
    y_scrollbar.config(command = text_box.yview)
    text_box.config(yscrollcommand = y_scrollbar.set)
    y_scrollbar.pack(side = RIGHT, fill = Y)

    # # add a scrollbar horizontally (x-axis):
    # x_scrollbar = Scrollbar(root, command = text_box.xview)
    # x_scrollbar.config(command = text_box.xview)
    # text_box.config(xscrollcommand = x_scrollbar.set)
    # x_scrollbar.pack(side = BOTTOM, fill = X)

    text_box.pack()
    # make window unresizable, so that text-box does nto stand out
    root.resizable(0, 0)

    root.mainloop()


