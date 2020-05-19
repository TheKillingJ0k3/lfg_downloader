#! python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from openpyxl import *
import os, shutil


#GLOBAL VARIABLES
comic_title_var = ''
year_var = ''
OneDrive_var = ''

#####################################################


# how functions work: I create button/widget with command=function and I put it on the grid
##################################  FUNCTIONS  ##################################################

#creates  folder inside wd, if it doesn't already exist
def createFolder(path):
        os.makedirs(path, exist_ok=True)

######################################################

def function():
    global comic_title_var
    global year_var
    global OneDrive_var
    print(comic_title_var)
    print(year_var)
    print(OneDrive_var)

def set_comic_title_var(event):
    global comic_title_var
    comic_title_var = comic_title_selector.get()
    print (comic_title_var)

def set_year_var(event):
    global year_var
    year_var = year_selector.get()
    print (year_var)

def Set_OneDrive_var():
    global OneDrive_var
    if OneDrive_button_var.get() == '1':
        OneDrive_var = 'Yes'
        print(OneDrive_var)
    else:
        OneDrive_var = 'No'
        print(OneDrive_var)


#############################################################################################

# year_var = StringVar()

###################### main GUI - Button creation #########################################

root = Tk()
root.title('Comic Downloader')
# root.state('zoomed')
# root.option_add('*tear0ff', False) #opens fullscreen

frame = Frame(root, borderwidth=5, relief="sunken", width=1000, height=200)
frame.pack()

#first line
first_line = Label(frame, text='Comic Downloader', bg='gray')
first_line.pack()
#second line
ComicTitle = Label(frame, text='Comic Title', bg='yellow')
ComicYear = Label(frame, text='Year', bg='yellow')
OneDriveUpload = Label(frame, text='Upload to OneDrive', bg='yellow')
#third line
# comic_title_var = StringVar() # TypeError: 'StringVar' object is not callable
comic_title_selector = ttk.Combobox(frame, width='30', textvariable=comic_title_var)
comic_title_selector['values'] = ("The Adventures of Business Cat", "Andy Capp", "Calvin and Hobbes", "Catana Comics", "Fowl Language", "Garfield", "Peanuts")
# comic_title_selector.current("The Adventures of Business Cat")
comic_title_selector.bind('<<ComboboxSelected>>', set_comic_title_var)

year_selector = ttk.Combobox(frame, width='10')
year_selector['values'] = ('1950', '1951', '1952', '1953', '1954', '1955', '1956', '1957')
# year.current(1950)
year_selector.bind('<<ComboboxSelected>>', set_year_var)

submit = Button(frame, text='Download', command=function) 

OneDrive_Upload_Frame = Frame(frame)
OneDrive_button_var = StringVar() #if booleanvar -> unchecked!!!!
Checkbutton(OneDrive_Upload_Frame, text='Yes', variable=OneDrive_button_var, command=Set_OneDrive_var).pack(side='right')


#########################      grid     ###################################################
frame.grid(column=0, row=0)
#first_line grid configuration
frame.grid(column=0, row=0, columnspan=16, rowspan=4)
#grid for first line
first_line.grid(column=0, row=1, columnspan=16, rowspan=1, sticky=(W))
# grid for second line
ComicTitle.grid(column=1, row=2, columnspan=1, rowspan=1, sticky=(W))
ComicYear.grid(column=2, row=2, columnspan=1, rowspan=1, sticky=(W))
OneDriveUpload.grid(column=3, row=2, columnspan=1, rowspan=1, sticky=(E))
#grid for third line
comic_title_selector.grid(column=1, row=3, columnspan=1, rowspan=1, sticky=(W))
year_selector.grid(column=2, row=3, columnspan=1, rowspan=1, sticky=(W))
OneDrive_Upload_Frame.grid(column=3, row=3, columnspan=1, rowspan=1, sticky=(W))
submit.grid(column=4, row=3, columnspan=1, rowspan=1, sticky=(E))


######################################################################################


##############################   MENU  #############################################
menubar = Menu(root) #creates menubar
root.config(menu = menubar) #same as frame['menu'] = menubar, doesn't need menu=menu_file etc inside cascade

#creating submenus in frame menu/menubar
menu_app = Menu(menubar, tearoff=False) #first_lineises new submenu
menubar.add_cascade(label='New', menu=menu_app) #creates name of new submenu
menubar.add_cascade(label='Save', command=function) #adds option to submenu
# menu_app.add_command(label='Save app', command=save_excel) #adds option to submenu

# menu_app.add_command(label='Generate Random Test', command=importapp) #adds option to submenu


menu_exit = Menu(menubar)
menubar.add_cascade(label='Exit', command=frame.quit)
######################################################################################

root.mainloop()
