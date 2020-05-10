#! python3
# Cyanide&Happiness_Downloader.py - Downloads every single The Cyanide & Happiness comic.

import requests, os, bs4

url = 'http://explosm.net/comics/oldest'               # starting url
os.makedirs('The Cyanide & Happiness', exist_ok=True)    # store comics in ./The Cyanide & Happiness  no exception if folder already exists
while not url.endswith('latest'):
    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find the URL of the comic image.
    comicElem = soup.select('#comic-wrap img') # <div id="comic-wrap"> <img src="xxx"> ---> Elem = soup.select('#id element')
    if comicElem == []: # if selector does not find any elements, it returns empty list 
        print('Could not find comic image.')
    else:
        comicUrl = 'https:' + comicElem[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (comicUrl))
        res = requests.get(comicUrl)
        res.raise_for_status()  

        # Save the image to ./The Cyanide & Happiness.
        imageFile = open(os.path.join('The Cyanide & Happiness', os.path.basename(comicUrl)), # #comic-under > div.comic-nav > a.nav-next > img
'wb') # call os.path.basename() with comicUrl, and it will return just the last part of the URL/// join for Windows & Linux


# crushes on:
# #Downloading page https://explosm.net//comics/407/...
# Downloading image https://files.explosm.net/comics/Rob/alamo.jpg?t=6C2A15...

        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    # Get the Prev button's url.
    prevLink = soup.select('a[title="Next comic"]')[0] # selector 'a[rel="prev"]' identifies the <a> element with the rel attribute set to prev
    url = 'https://explosm.net/' + prevLink.get('href')

print('Done.')
