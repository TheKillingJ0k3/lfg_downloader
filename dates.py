#! python3

# Third party imports
import requests, bs4, json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep


###############################################################################################
def getIndexPositions(listOfElements, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    indexPosList = []
    indexPos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            indexPos = listOfElements.index(element, indexPos)
            # Add the index position in list
            indexPosList.append(indexPos)
            indexPos += 1
        except ValueError:
            break
 
    return indexPosList
###############################################################################################
def download_comic_with_Selenium():
    Dates = []
    # selenium method with headless browser
    url = 'https://www.gocomics.com/the-adventures-of-business-cat/2020/05/28'
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    browser = webdriver.Chrome() # options=chrome_options
    browser.get(url)
    sleep(10)

    # while True:
    # find element
    continue_banner = browser.find_element_by_xpath('/html/body/div[10]/div[1]/div/div/div[4]/button[2]') # /html/body/div[10]/div[1]/div/div/div[4]/button[2]
    continue_banner.click()
    cookies_banner = browser.find_element_by_xpath('//*[@id="cookieChoiceDismiss"]')
    cookies_banner.click() 
    sleep(5)

    actions = ActionChains(browser)
    for _ in range(1):
        actions.send_keys(Keys.SPACE).perform()
        sleep(5)

    calendar_button = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/nav/div[2]/div/input') # calendar button
    calendar_button.click() # ElementClickInterceptedException
    sleep(2)
    select_year_button = browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/div[2]/select')
    select_year = Select(select_year_button)
    sleep(2)
    # select by visible text
    #####
    res = requests.get(url) # check if we have problems with global var
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # find button for first comic page
    first_page_button = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa fa-backward sm"]')[0]
    first_publication_url = 'https://www.gocomics.com/' + first_page_button.get('href')
    print(first_publication_url)
    year = first_publication_url[-10:-6]
    print(year)
    month = first_publication_url[-5:-3]
    print(month)
    # dict with months

    #####
    # year = '2015'
    select_year.select_by_visible_text(year)
    sleep(1)
    # for i in range(12)?
    select_month_button = browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/div[1]/select')
    select_month = Select(select_month_button)
    sleep(2)
    # select by visible text
    try:
        select_month.select_by_visible_text('January')
    except:
        try:
            select_month.select_by_visible_text('February')
        except:
            try:
                select_month.select_by_visible_text('March')
            except:
                select_month.select_by_visible_text('April')
    sleep(5)
    month = ''
    #TODO: see how to save month in variable to turn to number
    dates_elements = browser.find_elements_by_class_name('ui-state-default')
    # print(dates_elements)
    print(len(dates_elements))
    month_dates_yayornay = []

    for i in dates_elements:
        x = i.get_attribute('href') # #ui-datepicker-div > table > tbody > tr:nth-child(2) > td.undefined > a //////find_element_by_css_selector('a').
        print(x)
        month_dates_yayornay.append(x)
    for x in month_dates_yayornay:
        if x:
            Dates.append(year + '-' + 'April-' + str(int(month_dates_yayornay.index(x))+1))
    print(Dates)

####### same
    select_month_button = browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/div[1]/select')
    select_month = Select(select_month_button)
    sleep(2)
    # select by visible text
    select_month.select_by_visible_text('May')
    sleep(5)
    month = ''
    dates_elements = browser.find_elements_by_class_name('ui-state-default')
    # print(dates_elements)
    print(len(dates_elements))
    month_dates_yayornay = []

    for i in dates_elements:
        x = i.get_attribute('href') # #ui-datepicker-div > table > tbody > tr:nth-child(2) > td.undefined > a 
        print(x)
        month_dates_yayornay.append(x)
    print(month_dates_yayornay)
    # for y in month_dates_yayornay:
    #     if y != 'None':
    #         print(month_dates_yayornay.index(y))
    #         fockinglist.append(y)
    #         Dates.append(year + '-' + 'May-' + str(int(month_dates_yayornay.index(y))+1))
    #         print(Dates)

# index only finds first occurence of value that's why I only get 0 and 3
    indexPosList = []
    indexPos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            indexPos = month_dates_yayornay.index(None, indexPos)
            # Add the index position in list
            indexPosList.append(indexPos)
            indexPos += 1
        except ValueError:
            break

    print(indexPosList)
    for i in range(len(indexPosList)):
        if i not in indexPosList:
            Dates.append(year + '-' + 'May-' + str(int(i)+1))
    print(Dates)






################################################################################################################################



# # alt shift f to see json as list
# filename = '.\\Downloaded Comics\\comic_urls.json'
# try:
#     with open(filename) as f_obj:
#         list_of_all_urls = json.load(f_obj) 
# except FileNotFoundError:
#     list_of_all_urls = []
#     with open(filename, 'w') as f_obj:
#         json.dump(list_of_all_urls, f_obj)
#         print(list_of_all_urls)
# else:
#     print('json successfully loaded')



# # download 'https://www.gocomics.com/comics/a-to-z'
# comic_list_url = 'https://www.gocomics.com/comics/a-to-z'
# # Download the page.
# res = requests.get(comic_list_url)
# res.raise_for_status()
# soup = bs4.BeautifulSoup(res.text, 'html.parser')
# list_link = soup.select('div > h4')
# # create list of all comic titles
# comic_title_list = []
# for i in list_link:
#     comic_title_list.append(i.text)


# # parse through all comic titles
# for i in comic_title_list:
#     if int(comic_title_list.index(i)) > 13:
#         print(i)
#         if i == 'Andy Capp':
#                     # Download the page.  If I do not use this, res & soup get overwritten by chosen url
#             res = requests.get(comic_list_url)
#             res.raise_for_status()
#             soup = bs4.BeautifulSoup(res.text, 'html.parser')

#             # Get the comic current date url.
#             comic_current_date_url = soup.select('a[class="gc-blended-link gc-blended-link--primary col-12 col-sm-6 col-lg-4"]')[comic_title_list.index(i)] # index must be comic_title_list index
#             chosen_comic_url = 'https://www.gocomics.com/' + comic_current_date_url.get('href') # list index out of range when choosing new title
#             print(chosen_comic_url)
#             # download current page of chosen comic
#             res = requests.get(chosen_comic_url) # check if we have problems with global var
#             res.raise_for_status()
#             soup = bs4.BeautifulSoup(res.text, 'html.parser')
#             # find button for first comic page
#             first_page_button = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa fa-backward sm"]')[0]
#             first_publication_url = 'https://www.gocomics.com/' + first_page_button.get('href')
#             print(first_publication_url)

#             # save a list with all urls of a comic regardless of year - program will read only the ones of the year we want
#             url = "https://www.gocomics.com//andycapp/2009/08/29" # this must be the next one of the last saved
#             # print(url)
#             while url != chosen_comic_url: # loop condition: url not current url - SOS last url already saved
#                 # Download the page.
#                 # print('Downloading page %s...' % url)
#                 res = requests.get(url)
#                 res.raise_for_status()
#                 soup = bs4.BeautifulSoup(res.text, 'html.parser')
#                 list_of_all_urls.append(url)

#                 with open(filename, 'w') as f_obj: # overwrites file
#                     json.dump(list_of_all_urls, f_obj)

#                 # print(list_of_all_urls)
#                 # Get the Next button's url.
#                 nextLink = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')[0]
#                 url = 'https://www.gocomics.com/' + nextLink.get('href')
#                 # print(url)
#             list_of_all_urls.append(chosen_comic_url) # add to json
#             with open(filename, 'w') as f_obj:
#                 json.dump(list_of_all_urls, f_obj)
#             print('ok')

#         else:
#             # open comic page, go to first and start moving forward / save each url/date to a list -> save list to json

#             # Download the page.  If I do not use this, res & soup get overwritten by chosen url
#             res = requests.get(comic_list_url)
#             res.raise_for_status()
#             soup = bs4.BeautifulSoup(res.text, 'html.parser')

#             # Get the comic current date url.
#             comic_current_date_url = soup.select('a[class="gc-blended-link gc-blended-link--primary col-12 col-sm-6 col-lg-4"]')[comic_title_list.index(i)] # index must be comic_title_list index
#             chosen_comic_url = 'https://www.gocomics.com/' + comic_current_date_url.get('href') # list index out of range when choosing new title
#             print(chosen_comic_url)
#             # download current page of chosen comic
#             res = requests.get(chosen_comic_url) # check if we have problems with global var
#             res.raise_for_status()
#             soup = bs4.BeautifulSoup(res.text, 'html.parser')
#             # find button for first comic page
#             first_page_button = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa fa-backward sm"]')[0]
#             first_publication_url = 'https://www.gocomics.com/' + first_page_button.get('href')
#             print(first_publication_url)

#             # save a list with all urls of a comic regardless of year - program will read only the ones of the year we want
#             url = first_publication_url
#             # print(url)
#             while url != chosen_comic_url: # loop condition: url not current url - SOS last url already saved
#                 # Download the page.
#                 # print('Downloading page %s...' % url)
#                 res = requests.get(url)
#                 res.raise_for_status()
#                 soup = bs4.BeautifulSoup(res.text, 'html.parser')
#                 list_of_all_urls.append(url)

#                 with open(filename, 'w') as f_obj: # overwrites file
#                     json.dump(list_of_all_urls, f_obj)

#                 # print(list_of_all_urls)
#                 # Get the Next button's url.
#                 nextLink = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa-caret-right sm"]')[0]
#                 url = 'https://www.gocomics.com/' + nextLink.get('href')
#                 # print(url)
#             list_of_all_urls.append(chosen_comic_url) # add to json
#             with open(filename, 'w') as f_obj:
#                 json.dump(list_of_all_urls, f_obj)
#             print('ok')
#######################################################################################################
download_comic_with_Selenium()
