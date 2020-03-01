#! python3
# lfg.py - Downloads every single lfg comic.

import requests, os, bs4

url = 'https://www.lfg.co/page/1/'               # starting url
os.makedirs('lfg', exist_ok=True)    # store comics in ./lfg  no exception if folder already exists
while url != 'https://www.lfg.co/page/1378/':
    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find the URL of the comic image.
    comicElem = soup.select('#comic-img img') # <div id="comic-img"> <img src="xxx"> ---> Elem = soup.select('#id element')
    if comicElem == []: # if selector does not find any elements, it returns empty list 
        print('Could not find comic image.')
    else:
        comicUrl = comicElem[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (comicUrl))
        res = requests.get(comicUrl)
        res.raise_for_status()  

        # Save the image to ./lfg.
        imageFile = open(os.path.join('lfg', os.path.basename(comicUrl)),
'wb') # call os.path.basename() with comicUrl, and it will return just the last part of the URL, 'blabla.png' /// join for Windows & Linux
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    # Get the Prev button's url.
    prevLink = soup.select('.comic-nav-next')[0] # selector '.comic-nav-next' identifies the class
    url = prevLink.get('href')

print('Done.')
