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
# if it works, change dates to save multiple lists and then save to json
#  
back_months = {'January': '01', 'February': '02', 'March':'03', 'April':'04',
            'May':'05', 'June':'06', 'July':'07', 'August':'08',
            'September':'09', 'October':'10', 'November':'10', 'December':'12'}

months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
            '05': 'May', '06': 'June', '07': 'July', '08': 'August',
            '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
###############################################################################################




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
# def first_vars():
#     ##### - first publication url global var so this is not needed inside program
#     url = 'https://www.gocomics.com/the-adventures-of-business-cat/2020/06/04'
#     res = requests.get(url)
#     res.raise_for_status()
#     soup = bs4.BeautifulSoup(res.text, 'html.parser')
#     # find button for first comic page
#     first_page_button = soup.select('a[class="fa btn btn-outline-secondary btn-circle fa fa-backward sm"]')[0]
#     first_publication_url = 'https://www.gocomics.com/' + first_page_button.get('href')
#     print(first_publication_url)
#     year = first_publication_url[-10:-6]
#     print(year)
#     month = first_publication_url[-5:-3]
#     print(month)
#     return year, month
###############################################################################################
def download_comic_with_Selenium():
    Dates = []
    url = first_publication_url
    global current_year
    global current_month
    global current_date

    # current_year = url[-10:-6]
    # current_month = url[-5:-3]
    # # print(current_month)
    # current_date = current_year + '/' + current_month + url[-3:]
    # print(current_date)
    # selenium method with headless browser
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    browser = webdriver.Chrome() # options=chrome_options
    browser.get(url)
    sleep(20)

    # close banners
    cookies_banner = browser.find_element_by_xpath('//*[@id="cookieChoiceDismiss"]')
    cookies_banner.click() 
    sleep(3)
    try:
        continue_banner = browser.find_element_by_xpath('/html/body/div[10]/div[1]/div/div/div[4]/button[2]')
    except:
        sleep(3)
        continue_banner = browser.find_element_by_xpath('/html/body/div[10]/div[1]/div/div/div[4]/button[2]')
    continue_banner.click()
    
    actions = ActionChains(browser)
    for _ in range(1):
        actions.send_keys(Keys.SPACE).perform()
        sleep(3)
    # while True:
    try:
        calendar_button = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/nav/div[2]/div/input')
    except:
        sleep(3)
        calendar_button = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[1]/div/div[1]/nav/div[2]/div/input')
    calendar_button.click() # ElementClickInterceptedException
    # sleep(2)

    select_year_button = browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/div[2]/select')
    select_year = Select(select_year_button)
    # sleep(2)
    global first_publication_year
    global first_publication_month
    year = first_publication_year
    month = first_publication_month

    #####
    while int(year) < 2021:
        # sleep(5)
        try:
            select_year.select_by_visible_text(year)
        except:
            select_year_button = browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/div[2]/select')
            select_year = Select(select_year_button)
            select_year.select_by_visible_text(year)

        while int(month) <13: # try <12 and omit 142? - this loop runs indefinitely from month = 1 until month = 12

            select_month_button = browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/div[1]/select')
            select_month = Select(select_month_button)
            sleep(4)
            # convert month from url/loop to letters
            letter_month = months.get(month)
            print(letter_month)
            try:
                select_month.select_by_visible_text(letter_month)
            except:
                select_month_button = browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/div[1]/select')
                select_month = Select(select_month_button)
                # sleep(2)
                select_month.select_by_visible_text(letter_month)
                                                    
            sleep(3)
            print(month)
            dates_elements = browser.find_elements_by_class_name('ui-state-default') # list with all dates elements in calendar
            print(len(dates_elements)) # every date is an object so we need to check on href

            month_dates_yayornay = [] # list including none or (current) url members for each date of the month
            for i in dates_elements:
                x = i.get_attribute('href')
                month_dates_yayornay.append(x)

            indexPosList = getIndexPositions(month_dates_yayornay, None) # list of index number of each none element of the previous list
            print(indexPosList)
            if indexPosList:
                for i in range(len(month_dates_yayornay)): # this loop uses the none-objects' indexes to add the non-none objects' dates to Dates
                    if i not in indexPosList:
                        new_date = str('0' + str(int(i)+1)) # indexPosList has len 30-31, I extract dates for which value is not none
                        if len(str(new_date)) == 3:
                            new_date = new_date[1:] # I added 0 for one digit dates and I subtract 0 for two-digit dates
                        Dates.append(year + '-' + month + '-' + new_date) # if a calendar is full, indexPosList should be empty but month_dates_yayornay is normal
            else: # if calendar is full, month_dates_yayornay is full of hrefs and indexPosList is empty - so we use month_dates_yayornay's index instead
                for i in range(len(dates_elements)):
                    new_date = str('0' + str(int(i)+1))
                    if len(str(new_date)) == 3:
                        new_date = new_date[1:]
                    Dates.append(year + '/' + month + '/' + new_date)
            print(Dates)

            last_date = Dates[-1] # .replace('-', '/')
            print(last_date)
            print(current_date)
            if last_date == current_date:
                year = '2021'
                break

            # go to next month
            if int(month) <12:
                month = str('0' + str((int(month) + 1)))
                print(month)
                if len(str(month)) == 3: # I added 0 for one digit months and I subtract 0 for two-digit months
                    month = month[1:]
                    print(month)
                letter_month = months.get(month)
                print(letter_month)
            elif int(month) == 12: # without this, same dates of december get added forever
                break

        year = str(int(year) + 1) # important to proceed to next year
        print(year)
        month = '01'

    list_of_all_dates.append(Dates) # add to json
    with open(filename, 'w') as f_obj:
        json.dump(list_of_all_dates, f_obj)

################################################################################################################################

# comic_title_var = 'The Adventures of Business Cat'


# alt shift f to see json as list
filename = '.\\Downloaded Comics\\comic_dates.json'
try:
    with open(filename) as f_obj:
        list_of_all_dates = json.load(f_obj)
except FileNotFoundError:
    list_of_all_dates = []
    # for comic in comictitles
        # comic1dates = []
        # comic2dates = [] ...
    with open(filename, 'w') as f_obj:
        json.dump(list_of_all_dates, f_obj)
        print(list_of_all_dates)
else:
    print('json successfully loaded')
#     print(list_of_all_dates)
#      # for comic in comictitles
#         # comic1dates = list_of_all_dates[0]
#         # comic2dates = list_of_all_dates[1] ...


# # # we need to create a list for each comic
# comic1dates = []
# comic2dates = []
# comic3dates = []
# list_of_all_dates = [comic1dates, comic2dates, comic3dates]

#         list_of_all_dates.append(url)

#         with open(filename, 'w') as f_obj: # overwrites file
#             json.dump(list_of_all_dates, f_obj)

#         # print(list_of_all_dates)
        
#     list_of_all_dates.append(chosen_comic_url) # add to json
#     with open(filename, 'w') as f_obj:
#         json.dump(list_of_all_dates, f_obj)
#     print('ok')


#######################################################################################################
# download_comic_with_Selenium()


# create list with all comic titles
comic_title_list = []
comic_list_url = 'https://www.gocomics.com/comics/a-to-z'
# Download the page.
res = requests.get(comic_list_url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
list_link = soup.select('div > h4')
for i in list_link:
    comic_title_list.append(i.text)

for i in comic_title_list:
    # Get the comic current date url.
    comic_current_date_url = soup.select('a[class="gc-blended-link gc-blended-link--primary col-12 col-sm-6 col-lg-4"]')[comic_title_list.index(i)] # index must be comic_title_list index
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

    # vars used by selenium function
    global first_publication_year
    global first_publication_month
    first_publication_year = first_publication_url[-10:-6]
    first_publication_month = first_publication_url[-5:-3]
    global current_year
    global current_month
    global current_date
    current_year = chosen_comic_url[-10:-6]
    current_month = chosen_comic_url[-5:-3]
    current_date = chosen_comic_url[-10:]

    download_comic_with_Selenium()
