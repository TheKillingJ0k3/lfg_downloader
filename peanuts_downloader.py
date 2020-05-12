#! python3
# peanuts_downloader.py - Downloads every single Peanuts comic.

# https://www.gocomics.com/little-moments-of-love/2018/09/24
# https://www.gocomics.com/cestlavie/2020/05/08
# https://www.gocomics.com/the-adventures-of-business-cat/2020/05/07
# https://www.gocomics.com/calvinandhobbes/2020/05/10
# https://www.gocomics.com/peanuts/2020/05/10

import requests, os, bs4

# url = 'https://www.gocomics.com/peanuts/1950/10/02'               # starting url
# url = 'https://www.gocomics.com/peanuts/1967/04/17'               # starting url
url = 'https://www.gocomics.com/peanuts/1979/01/12'               # starting url


os.makedirs('Peanuts', exist_ok=True)    # store comics in ./Peanuts  no exception if folder already exists

lastYear = ''
while not url.endswith('latest'): # no end condition on last comic - I can use today's date
    year = str(url[-10:-6])
    if year != lastYear:
        lastYear = year
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
    comicElem = soup.select('.item-comic-image img') # src="https://assets.amuniversal.com/3acf4280f867013014ce001dd8b71c47" ---> Elem = soup.select('#id element')
    if comicElem == []: # if selector does not find any elements, it returns empty list 
        print('Could not find comic image.')
    else:
        comicUrl = comicElem[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (comicUrl))
        res = requests.get(comicUrl)
        res.raise_for_status()  

        # Save the image to ./Peanuts.
        imageFile = open(os.path.join('Peanuts', year, os.path.basename(filename + '.jpg')), # comicUrl does not end with .jpg, so we add it manually
'wb') # call os.path.basename() with comicUrl, and it will return just the last part of the URL, 'heartbleed_explanation.png' /// join for Windows & Linux


        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    # Get the Prev button's url.
    prevLink = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')[0] # selector 'a[rel="prev"]' identifies the <a> element with the rel attribute set to prev
    url = 'https://www.gocomics.com/' + prevLink.get('href')

print('Done.')
