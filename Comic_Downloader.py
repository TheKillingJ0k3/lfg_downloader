#! python3

# Standard library imports
import shutil, os, subprocess
# Third party imports
import requests, bs4
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# Local app imports


# url = 'https://www.gocomics.com/peanuts/1950/10/02'               # starting url
# url = 'https://www.gocomics.com/peanuts/1984/01/01'               # starting url

#GLOBAL VARIABLES
url = ''
# OneDriveUpload = ''

comic_title_var = ''
year_var = ''
OneDrive_var = ''
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
    global comic_title_list
    print(comic_title_list.index(comic_title_var))

    # Get the comic current date url.
    # chosen_comic_url = 'https://www.gocomics.com/{}/{}/01/01' .format(comic_title_var, year_var)
    comic_current_date_url = soup.select('a[class="gc-blended-link gc-blended-link--primary col-12 col-sm-6 col-lg-4"]')[comic_title_list.index(comic_title_var)] # index must be comic_title_list index
    chosen_comic_url = 'https://www.gocomics.com/' + comic_current_date_url.get('href') # correct
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


def set_year_var(event):
    global comic_title_var
    global year_var
    global url
    year_var = year_selector.get()
    print (year_var)
    global first_publication_url
    if year_var in str(first_publication_url[-10:-6]): # if year chosen by user is the first publication year
        url = first_publication_url
    elif int(year_var) < int(first_publication_url[-10:-6]):
        print('Oops! Too early for {}' .format(comic_title_var))
    else:
        url = 'https://www.gocomics.com/{}/{}/01/01' .format(comic_title_var, year_var) # starting url
    # if year_var == '1950':
    #     url = 'https://www.gocomics.com/{}/1950/10/02' .format(comic_title_var) # starting url for 1950
    # else:
    #     url = 'https://www.gocomics.com/{}/{}/01/01' .format(comic_title_var, year_var) # starting url

def Set_OneDrive_var():
    global OneDrive_var
    if OneDrive_button_var.get() == '1':
        OneDrive_var = 'Yes'
        print(OneDrive_var)
    else:
        OneDrive_var = 'No'
        print(OneDrive_var)

################################  MAIN FUNCTIONS  ###############################################

def download_comic():
    global url
    global comic_title_var
    global year_var
    createFolder(comic_title_var)
    while year_var in str(url[-10:-6]): # loop condition: year that user picked should be in URL
        os.makedirs(os.path.join(comic_title_var, year_var), exist_ok=True) # createFolder

        # Download the page.
        print('Downloading page %s...' % url)
        res = requests.get(url)
        res.raise_for_status()
    # 1967.04.17 requests.exceptions.HTTPError: 502 Server Error: Bad Gateway for url: https://assets.amuniversal.com/b7ac0120f892013014ff001dd8b71c47
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
            imageFile = open(os.path.join(comic_title_var, year_var, os.path.basename(filename + '.jpg')), # comicUrl does not end with .jpg, so we add it manually
    'wb') # call os.path.basename() with comicUrl, and it will return just the last part of the URL /// join for Windows & Linux
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

        # Get the Next button's url.
        nextLink = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')[0]
        url = 'https://www.gocomics.com/' + nextLink.get('href')

    print('Done.')
    OneDrive_upload()


def OneDrive_upload():
    # global OneDriveUpload
    global OneDrive_var
    global comic_title_var
    # OneDriveUpload = input('Do you want to upload your newly created folder to Onedrive? \nPress: Y for Yes, N for No: ')
    if OneDrive_var == 'Yes':
        shutil.copytree(os.path.join(comic_title_var, year_var), os.path.join('OneDrive', 'Comics', comic_title_var, year_var))
        subprocess.Popen(os.path.join('AppData', 'Local', 'Microsoft', 'OneDrive', 'OneDrive.exe'))
    elif OneDrive_var == 'No':
        pass
#############################################################################################

# os.makedirs('Peanuts', exist_ok=True)    # store comics in ./Peanuts  no exception if folder already exists


# OneDrive_upload()


# year_var = StringVar()

###################### main GUI - Button creation #########################################

root = Tk()
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
comic_title_selector['values'] = (comic_title_list) # "The Adventures of Business Cat", "Andy Capp", "Calvin and Hobbes", "Catana Comics", "Fowl Language", "Garfield", "Peanuts"
# comic_title_selector.current("The Adventures of Business Cat")
comic_title_selector.bind('<<ComboboxSelected>>', set_comic_title_var)

year_selector = ttk.Combobox(frame, width='10')
year_selector['values'] = (year_list)
# year.current(1950)
year_selector.bind('<<ComboboxSelected>>', set_year_var)

submit = Button(frame, text='Download', command=download_comic) 

OneDrive_Upload_Frame = Frame(frame)
OneDrive_button_var = StringVar() #if booleanvar -> unchecked!!!!
Checkbutton(OneDrive_Upload_Frame, text='Yes', variable=OneDrive_button_var, command=Set_OneDrive_var).pack(side='right')


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