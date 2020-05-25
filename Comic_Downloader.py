#! python3

#TODO: Stop downloading on today's date without giving error
#TODO: most important problem is when downloading a middle year - not the first one / we always get error
#TODO: check program exit conditions, if bar is sill running, program cannot die
#TODO: if remote connection error, download pauses on last url - if user presses download again, it continues
#TODO: download whole comic option
#TODO: create json file to save starting point for each comic each year

#TODO: Process 2 does not recognize path to create folder, probably because all vars/code so far was made by another core

# Standard library imports
import shutil, os, threading, subprocess, time
# Third party imports
import requests, bs4
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
# Local app imports

#GLOBAL VARIABLES
url = ''
comic_title_var = ''
year_var = ''
OneDrive_var = 'No'
first_publication_url = ''

comic_title_list = []


comic_list_url = 'https://www.gocomics.com/comics/a-to-z'
# Download the page.
res = requests.get(comic_list_url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
list_link = soup.select('div > h4')
for i in list_link:
    comic_title_list.append(i.text)


year_list = []
for i in range(1950,2021):
    year_list.append(i)

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
    # url -> res -> parser -> with select I save element in list / var
    global res # for 'https://www.gocomics.com/comics/a-to-z'
    global soup # for 'https://www.gocomics.com/comics/a-to-z'

    # Download the page.  If I do not use this, res & soup get overwritten by chosen url
    global comic_list_url
    res = requests.get(comic_list_url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    global comic_title_list
    print(comic_title_list.index(comic_title_var))

    # Get the comic current date url.
    comic_current_date_url = soup.select('a[class="gc-blended-link gc-blended-link--primary col-12 col-sm-6 col-lg-4"]')[comic_title_list.index(comic_title_var)] # index must be comic_title_list index
    chosen_comic_url = 'https://www.gocomics.com/' + comic_current_date_url.get('href') # list index out of range when choosing new title
    print(chosen_comic_url)
    # download current page of chosen comic
    res = requests.get(chosen_comic_url) # check if we have problems with global var
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # find button for first comic page
    first_page_button = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa fa-backward sm"]')[0]
    global first_publication_url
    first_publication_url = 'https://www.gocomics.com/' + first_page_button.get('href')
    print(first_publication_url)

    # update year_list
    global year_list
    print(first_publication_url[-10:-6])
    year_list = []
    for i in range(int(first_publication_url[-10:-6]),2021):
        year_list.append(i)
    print(year_list)
    global year_selector
    year_selector['values'] = (year_list)
    print(year_selector['values'])

    # includes set_year_var code in case user lets previous year and does not set new one / maybe use if condition with newyear-oldyear vars
    global year_var
    global url
    year_var = year_selector.get()
    print (year_var)
    if str(year_var) in str(first_publication_url[-10:-6]): # if year chosen by user is the first publication year
        url = first_publication_url
        print(url)
    else:
        url = first_publication_url
        print(url)
        while str(year_var) not in str(url[-10:-6]): # loop condition: year that user picked should be in URL
            # Download the page.
            print('Downloading page %s...' % url)
            res = requests.get(url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            # Get the Next button's url.
            nextLink = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')[0] # usual index error
            url = 'https://www.gocomics.com/' + nextLink.get('href')
            print(url)

def set_year_var(event): # code of this function is also included in comic_title one for the case user does not pick new year after selecting new title
    global comic_title_var
    global year_var
    global url
    year_var = year_selector.get()
    print (year_var)
    global first_publication_url
    if str(year_var) in str(first_publication_url[-10:-6]): # if year chosen by user is the first publication year
        url = first_publication_url
        print(url)
    # elif int(year_var) < int(first_publication_url[-10:-6]):
    #     print('Oops! Too early for {}' .format(comic_title_var))
    else:
        url = first_publication_url
        print(url)
        while str(year_var) not in str(url[-10:-6]): # loop condition: year that user picked should be in URL
            # Download the page.
            print('Downloading page %s...' % url)
            res = requests.get(url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            # Get the Next button's url.
            nextLink = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')[0] # usual index error
            url = 'https://www.gocomics.com/' + nextLink.get('href')
            print(url)
        # url = 'https://www.gocomics.com/{}/{}/01/01' .format(comic_title_var, year_var) # starting url
        # print(url)


def Set_OneDrive_var():
    global OneDrive_var
    if OneDrive_button_var.get() == '1':
        OneDrive_var = 'Yes'
        print(OneDrive_var)
    else:
        OneDrive_var = 'No'
        print(OneDrive_var)

################################  MAIN FUNCTIONS  ###############################################

# def progressbar_multiprocessing(): #opens 2 new main windows
#     p1 = multiprocessing.Process(target=start_progress)
#     p2 = multiprocessing.Process(target=download_comic)
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()

# threading acts as if using two cores but it does not - python processes a couple of lines of each function at intervals
# multiprocessing uses 2 cores that do not share the same memory, so second process -download comic- does not work correctly

def threading_dl_and_progress(): # does not enter while loop
    threadObj1 = threading.Thread(target=download_comic) # does not enter while loop
    threadObj1.start()
    threadObj2 = threading.Thread(target=start_progress)
    time.sleep(5)
    threadObj2.start()


def download_comic(): # the adventures of business cat 2018 does not download anything
    global url
    global comic_title_var
    global year_var

    # threadObj = threading.Thread(target=start_progress)
    # threadObj.start()

    createFolder(os.path.join('Downloaded Comics', comic_title_var)) # multiprocessing does not recognize this var / cannot find path specified

    while year_var in str(url[-10:-6]): # loop condition: year that user picked should be in URL
        os.makedirs(os.path.join('Downloaded Comics', comic_title_var, year_var), exist_ok=True) # createFolder

        # Download the page.
        print('Downloading page %s...' % url)
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')

        # Find the URL of the comic image.
        date = str(url[-10:])
        filename = date.replace('/', '.')
        print(filename)
        comicElem = soup.select('.item-comic-image img') # src="https://assets.amuniversal.com/3acf4280f867013014ce001dd8b71c47"
        if comicElem == []: # if selector does not find any elements, it returns empty list 
            print('Could not find comic image.')
        else:
            comicUrl = comicElem[0].get('src')
            # Download the image.
            print('Downloading image %s...' % (comicUrl))
            res = requests.get(comicUrl)
            res.raise_for_status()  

            # Save the image to ./Peanuts/Year.
            imageFile = open(os.path.join('Downloaded Comics', comic_title_var, year_var, os.path.basename(filename + '.jpg')), # comicUrl does not end with .jpg, so we add it manually
    'wb') # call os.path.basename() with comicUrl, and it will return just the last part of the URL /// join for Windows & Linux
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

        # Get the Next button's url.
        nextLink = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')[0] # usual index error
        url = 'https://www.gocomics.com/' + nextLink.get('href')

    print('Done.')
    OneDrive_upload()


def OneDrive_upload():
    # global OneDriveUpload
    global OneDrive_var
    global comic_title_var
    # OneDriveUpload = input('Do you want to upload your newly created folder to Onedrive? \nPress: Y for Yes, N for No: ')
    if OneDrive_var == 'Yes':
        shutil.copytree(os.path.join('Downloaded Comics', comic_title_var, year_var), os.path.join('OneDrive', 'Comics', comic_title_var, year_var))
        subprocess.Popen(os.path.join('AppData', 'Local', 'Microsoft', 'OneDrive', 'OneDrive.exe'))
    elif OneDrive_var == 'No':
        pass
#############################################################################################


lst = []
combination_number = 200
for x in range(0, combination_number):
    lst.append(str(x+1))
    # print(self.lst)

def start_progress():
    # root = Tk()
    s = ProgressWindow('Comic Downloader', lst)
    root.wait_window(s)

class ProgressWindow(simpledialog.Dialog):
    def __init__(self, name, lst):
        ''' Init progress window '''
        Toplevel.__init__(self)
        self.name = name
        self.lst = lst
        self.length = 400
        #
        self.create_window()
        self.create_widgets()

    def create_window(self):
        ''' Create progress window '''
        self.focus_set()  # set focus on the ProgressWindow
        self.grab_set()  # make a modal window, so all events go to the ProgressWindow
        self.transient()  # show only one window in the task bar
        #
        self.title(u'Downloading for {}'.format(self.name))
        self.resizable(False, False)  # window is not resizable
        # self.close gets fired when the window is destroyed
        self.protocol(u'WM_DELETE_WINDOW', self.close)
        # Set proper position over the parent window
        # dx = (self.master.winfo_width() >> 1) - (self.length >> 1)
        # dy = (self.master.winfo_height() >> 1) - 50
        # self.geometry(u'+{x}+{y}'.format(x = self.master.winfo_rootx() + dx,
        #                                  y = self.master.winfo_rooty() + dy))
        self.geometry(u'+100+100')
        self.bind(u'<Escape>', self.close)  # cancel progress when <Escape> key is pressed

    def create_widgets(self):
        ''' Widgets for progress window are created here '''
        self.var1 = StringVar()
        self.var2 = StringVar()
        self.num = IntVar()
        self.maximum = len(self.lst) #combination_number here
        self.tmp_str = ' / ' + str(self.maximum)
        #
        # pady=(0,5) means margin 5 pixels to bottom and 0 to top
        ttk.Label(self, textvariable=self.var1).pack(anchor='w', padx=2)
        self.progress = ttk.Progressbar(self, maximum=self.maximum, orient='horizontal',
                                        length=self.length, variable=self.num, mode='determinate')
        self.progress.pack(padx=2, pady=2)
        ttk.Label(self, textvariable=self.var2).pack(side='left', padx=2)
        ttk.Button(self, text='Cancel', command=self.close).pack(anchor='e', padx=1, pady=(0, 1))
        #
        self.next()

    def next(self):
        ''' Take next file from the list and do something with it '''
        n = self.num.get()
        # self.do_something_with_file(n+1, self.lst[n])  # some useful operation
        # self.var1.set('File name: ' + self.lst[n])  # 1st einai ta arxeia: thelei allagi
        n += 1
        self.var2.set(str(n) + self.tmp_str)
        self.num.set(n)
        if n < self.maximum:
            self.after(500, self.next)  # call itself after some time
        else:
            self.close()  # close window

    # def do_something_with_file(self, number, name): #edw vazw "test x generated"
    #     print(number, name)

    def close(self, event=None):
        ''' Close progress window '''
        if self.progress['value'] == self.maximum:
            print('Ok: process finished successfully')
        else:
            print('Cancel: process is cancelled')
        # self.master.focus_set()  # put focus back to the parent window
        self.destroy()  # destroy progress window


###################### main GUI - Button creation #########################################
root = Tk()
# if __name__ == '__main__':
    
root.title('Comic Downloader')
root.geometry('500x350')
# root.state('zoomed')
# root.option_add('*tear0ff', False) #opens fullscreen

background_image = PhotoImage(file='Documents\\Python\\Comic downloader\\crowd-img.png')
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = Frame(root, borderwidth=5, relief="sunken", width=100, height=200)
frame.pack()


#first line
first_line = Label(frame, text='Comic Downloader', bg='gray')
first_line.pack()
#second line
ComicTitle = Label(frame, text='Comic Title', bg='pink')
ComicYear = Label(frame, text='Year', bg='pink')
OneDriveUpload = Label(frame, text='Upload to OneDrive', bg='pink')
#third line
# comic_title_var = StringVar() # TypeError: 'StringVar' object is not callable
comic_title_selector = ttk.Combobox(frame, width='30', textvariable=comic_title_var)
comic_title_selector['values'] = (comic_title_list)
comic_title_selector.bind('<<ComboboxSelected>>', set_comic_title_var)

year_selector = ttk.Combobox(frame, width='10')
year_selector['values'] = (year_list)
# year.current(1950)
year_selector.bind('<<ComboboxSelected>>', set_year_var)

submit = Button(frame, text='Download', command=threading_dl_and_progress)

OneDrive_Upload_Frame = Frame(frame)
OneDrive_button_var = StringVar() #if booleanvar -> unchecked and always stays no!!!!
c = Checkbutton(OneDrive_Upload_Frame, text='Yes', variable=OneDrive_button_var, command=Set_OneDrive_var)
c.pack(side='right')
c.deselect()


#########################      grid     ###################################################

frame.grid(column=0, row=0, columnspan=4, rowspan=4, padx=15)
#grid for first line
first_line.grid(column=0, row=1, columnspan=4, rowspan=1, sticky=(W))
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
# menu_app.add_command(Label='Save app', command=save_excel) #adds option to submenu

# menu_app.add_command(Label='Generate Random Test', command=importapp) #adds option to submenu


menu_exit = Menu(menubar)
menubar.add_cascade(label='Exit', command=frame.quit)
######################################################################################

root.mainloop()
