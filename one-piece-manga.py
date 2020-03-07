#! python3
# one-piece.py - Downloads every single One Piece Chapter.

import requests, os, bs4

url = 'https://read-onepiece.com/manga/one-piece-chapter-973/'               # starting url
os.makedirs('One Piece', exist_ok=True)    # store comics in ./lfg  no exception if folder already exists
while url != 'https://read-onepiece.com/manga/onepiece-chapter-1/': #careful, layout & URL changes to one-piece-chapter-x
    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find the URL of the comic image.
    comicElem = soup.select('.separator img') # <div id="comic-img"> <img src="xxx"> ---> Elem = soup.select('#id element')
    # print(comicElem)
    # print(len(comicElem))
    if comicElem == []: # if selector does not find any elements, it returns empty list 
        print('Could not find comic image.')
    else:
        for i in range(0, len(comicElem)):
            comicUrl = comicElem[i].get('src')
            # Download the image.
            print('Downloading image %s...' % (comicUrl))
            res = requests.get(comicUrl)
            res.raise_for_status()  

            # Save the image to ./One Piece.
            imageFile = open(os.path.join('One Piece', os.path.basename(comicUrl)),
    'wb') # call os.path.basename() with comicUrl, and it will return just the last part of the URL, 'heartbleed_explanation.png' /// join for Windows & Linux
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

        # Get the Prev button's url.
        prevLink = soup.select('a[rel="prev"]')[0] # selector 'a[rel="prev"]' identifies the <a> element with the rel attribute set to prev
        url = prevLink.get('href') # next page = none

print('Done.')
