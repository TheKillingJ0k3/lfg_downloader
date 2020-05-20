#! python3
# peanuts_downloader.py - Downloads every single Peanuts comic.

# Standard library imports
import shutil, os, subprocess
# Third party imports
import requests, bs4
# Local app imports
# import Tkinter_GUI_Skeleton

# url = 'https://www.gocomics.com/peanuts/1950/10/02'               # starting url
# url = 'https://www.gocomics.com/peanuts/1984/01/01'               # starting url

#GLOBAL VARIABLES
year = ''
url = ''
OneDriveUpload = ''
#####################################################

##################################  FUNCTIONS  ##################################################
def choose_year():
    global year
    global url
    year = input('Pick a year between 1950 and current year:') # year 1950 starts from 02/10
    if year == '1950':
        url = 'https://www.gocomics.com/peanuts/1950/10/02' # starting url for 1950
    else:
        url = 'https://www.gocomics.com/peanuts/{}/01/01' .format(year) # starting url


def OneDrive_upload():
    global OneDriveUpload
    OneDriveUpload = input('Do you want to upload your newly created folder to Onedrive? \nPress: Y for Yes, N for No: ')
    if OneDriveUpload == 'Y':
        shutil.copytree(os.path.join('Peanuts', year), os.path.join('OneDrive', 'Comics', 'Peanuts', year))
        subprocess.Popen(os.path.join('AppData', 'Local', 'Microsoft', 'OneDrive', 'OneDrive.exe'))
    elif OneDriveUpload == 'N':
        pass
    else:
        print('I SAID Press: Y for Yes, N for No')
#############################################################################################

os.makedirs('Peanuts', exist_ok=True)    # store comics in ./Peanuts  no exception if folder already exists

choose_year()

while year in str(url[-10:-6]): # loop condition: year that user picked should be in URL
    os.makedirs(os.path.join('Peanuts', year), exist_ok=True)

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
        imageFile = open(os.path.join('Peanuts', year, os.path.basename(filename + '.jpg')), # comicUrl does not end with .jpg, so we add it manually
'wb') # call os.path.basename() with comicUrl, and it will return just the last part of the URL /// join for Windows & Linux
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    # Get the Prev button's url.
    prevLink = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')[0]
    url = 'https://www.gocomics.com/' + prevLink.get('href')

print('Done.')

OneDrive_upload()
