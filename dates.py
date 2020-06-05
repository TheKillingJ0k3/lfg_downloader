#! python3

# Third party imports
import requests, bs4, json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep

back_months = {'January': '01', 'February': '02', 'March':'03', 'April':'04',
            'May':'05', 'June':'06', 'July':'07', 'August':'08',
            'September':'09', 'October':'10', 'November':'10', 'December':'12'}

months = {'01': 'January', '02': 'February', '03': 'March', '04': 'April',
            '05': 'May', '06': 'June', '07': 'July', '08': 'August',
            '09': 'September', '10': 'October', '11': 'November', '12': 'December'}
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
def first_vars():
    ##### - first publication url global var so this is not needed inside program
    url = 'https://www.gocomics.com/the-adventures-of-business-cat/2020/06/04'
    res = requests.get(url)
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
    return year, month
###############################################################################################
def download_comic_with_Selenium():
    Dates = []
    # selenium method with headless browser
    #(global first publication url)
    url = 'https://www.gocomics.com/the-adventures-of-business-cat/2020/06/04'
    current_year = url[-10:-6]
    current_month = url[-5:-3]
    # print(current_month)
    current_date = current_year + '/' + current_month + url[-3:]
    # print(current_date)
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
    year, month = first_vars()

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
            sleep(2)
            # convert month from url/loop to letters
            letter_month = months.get(month)
            print(letter_month)
            try:
                select_month.select_by_visible_text(letter_month)
            except:
                select_month_button = browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/div[1]/select')
                select_month = Select(select_month_button)
                sleep(2)
                # select by visible text
                # letter_month = months.get(month)
                # print(letter_month)
                # sleep(2)
                select_month.select_by_visible_text(letter_month)
                                                    
            sleep(3)
            print(month)
            dates_elements = browser.find_elements_by_class_name('ui-state-default') # list with all dates elements in calendar
            print(len(dates_elements))

            month_dates_yayornay = [] # list including none or (current) url members for each date of the month
            for i in dates_elements:
                x = i.get_attribute('href')
                month_dates_yayornay.append(x)

            indexPosList = getIndexPositions(month_dates_yayornay, None) # list of the position of each none element of the previous list
            print(indexPosList)
            for i in range(len(indexPosList)):
                if i not in indexPosList:
                    new_date = str('0' + str(int(i)+1)) # indexPosList has len 30-31, I extract dates for which value is not none
                    if len(str(new_date)) == 3:
                        new_date = new_date[1:] # I added 0 for one digit dates and I subtract 0 for two-digit dates
                    Dates.append(year + '-' + month + '-' + new_date)
            print(Dates)

            last_date = Dates[-1].replace('-', '/')
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
        # if year == '2021':
        #     break
        month = '01'
        # if int(year) == int(current_year):
        #     if int(month) > int(current_month):
        #         break
            # else:
                # month = '01'

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



#                 list_of_all_urls.append(url)

#                 with open(filename, 'w') as f_obj: # overwrites file
#                     json.dump(list_of_all_urls, f_obj)

#                 # print(list_of_all_urls)
#                 
#             list_of_all_urls.append(chosen_comic_url) # add to json
#             with open(filename, 'w') as f_obj:
#                 json.dump(list_of_all_urls, f_obj)
#             print('ok')

#         else:

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
