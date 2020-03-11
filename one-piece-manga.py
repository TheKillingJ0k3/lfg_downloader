#! python3
# one-piece.py - Downloads every single One Piece Chapter.

import requests, os, bs4

#TODO: how to handle server error without crushing -> reload page and try again, if not, go to next page

url = 'https://read-onepiece.com/manga/onepiece-chapter-973/'               # starting url
os.makedirs('One Piece', exist_ok=True)    # store comics in ./lfg  no exception if folder already exists
while url != 'https://read-onepiece.com/manga/onepiece-chapter-1/': #careful, layout & URL changes to one-piece-chapter-x
    # Download the page.
    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find the URL of the comic image.
    comicElem = soup.select('.separator img') # <div id="comic-img"> <img src="xxx"> ---> Elem = soup.select('#id element')
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
            fileName = url[-4:-1] + '_' + str(i+1)
            print(fileName)
            imageFile = open('.\\One Piece\\%s.jpg' % fileName,
    'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

        # Get the Prev button's url.
        prevLink = soup.select('a[rel="prev"]')[0] # selector 'a[rel="prev"]' identifies the <a> element with the rel attribute set to prev
        url = prevLink.get('href')

    # print('Done.')

# chapter 967 ---> photos do not load in site
# raise HTTPError(http_error_msg, response=self)
# requests.exceptions.HTTPError: 403 Client Error: Forbidden
# for url: https://1.bp.blogspot.com/-mFxjKPPC5yw/XhC24wPfPRI/AAAAAAAAi_E/CUfY0zjJ8EgVbicJ0f2HqXlmQXRqAQWngCLcBGAsYHQ/s1600/onepiece1.jpg

# chapter 778
# requests.exceptions.ChunkedEncodingError: ("Connection broken: OSError(10051, 'A socket operation was attempted to an unreachable network', None, 10051, None)",
# OSError(10051, 'A socket operation was attempted to an unreachable network', None, 10051, None))

# up to 249 runs ok - could not find comic image

# chapter 1 has another URL:
url = 'https://onlineonepiece.com/manga/one-piece-chapter-1/'
print('Downloading page %s...' % url)
res = requests.get(url)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, 'html.parser')

# Find the URL of the comic image.
comicElem = soup.select('.separator img') # <div id="comic-img"> <img src="xxx"> ---> Elem = soup.select('#id element')
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
        fileName = url[-4:-1] + '_' + str(i+1)
        print(fileName)
        imageFile = open('.\\One Piece\\%s.jpg' % fileName,
'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    # Get the Prev button's url.
    prevLink = soup.select('a[rel="prev"]')[0] # selector 'a[rel="prev"]' identifies the <a> element with the rel attribute set to prev
    url = prevLink.get('href')
    
    print('Done.')
