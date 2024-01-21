from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time

urlWTD = 'https://finviz.com/screener.ashx?v=141&f=cap_smallover,sh_avgvol_o1000&o=-perf1w'
urlYTD = 'https://finviz.com/screener.ashx?v=141&f=cap_smallover,sh_avgvol_o1000&o=-perfytd'
urlMTD = 'https://finviz.com/screener.ashx?v=141&f=cap_smallover,sh_avgvol_o1000&o=-perf4w'
urlWebull='https://app.webull.com/stocks'
tickerList = list()

options = Options()
options.add_experimental_option('detach',True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                        options = options)
driver.maximize_window()
driver.execute_script("window.open('', '_blank');")
actions = ActionChains(driver)
time.sleep(2)

def loginWebull():
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(urlWebull)
    x = driver.find_element('xpath',"//i[@class='jss458 webull-cancel_ jss459 jss2']")
    x.click()
    time.sleep(2)
    x = driver.find_element('xpath',"//i[@class='jss458 webull-cancel_ jss459 jss376']")
    x.click()
    time.sleep(1)
    login = driver.find_element('xpath',"//span[contains(text(),'Login')]")
    login.click()
    time.sleep(1)
    id = driver.find_element('xpath',"//input[@type='tel']")
    id.click()
    id.send_keys('')
    pwd = driver.find_element('xpath',"//input[@type='password']")
    pwd.click()
    pwd.send_keys('')
    login = driver.find_element('xpath',"//span[contains(text(), 'Log In')]")
    login.click()
    time.sleep(30)

def addToWebull(watchlist_type):
    driver.switch_to.window(driver.window_handles[-1])
    watchlist_dropdown = driver.find_element('xpath','//span[@class="jss213 jss203"]')
    watchlist_dropdown.click()
    time.sleep(5)
    if watchlist_type=='wtd':
        watchlist_element = driver.find_element('xpath',"//div[contains(text(),'Finviz WTD')]")
        watchlist_element.click()
        
    elif watchlist_type == 'mtd':
       watchlist_element = driver.find_element('xpath',"//div[contains(text(),'Finviz MTD')]")
       watchlist_element.click()
        
    elif watchlist_type == 'ytd':
        watchlist_element= driver.find_element('xpath',"//div[contains(text(),'Finviz YTD')]")
        watchlist_element.click()
        
    else:
        print('WATCHLIST TYPE NOT FOUND')
    time.sleep(1)

    watchlist_len  = len(driver.find_elements('xpath','//div[@class="jss160"]//div[@class="simplebar-content-wrapper"]//li'))
    num = 0
    while num<=watchlist_len and watchlist_len>1:
        current_ticker_element= driver.find_element('xpath',f'//div[@class="jss160"]//div[@class="simplebar-content-wrapper"]//li[{num+1}]')
        current_ticker= driver.find_element('xpath',f'//div[@class="jss160"]//div[@class="simplebar-content-wrapper"]//li[{num+1}]/div[2]/div/div/span').text
        if current_ticker not in tickerList:
            actions.context_click(current_ticker_element).perform()
            driver.execute_script("arguments[0].scrollIntoView(true);", current_ticker_element)
            time.sleep(3)
            delete_element = driver.find_element('xpath',"//div[contains(text(),'Delete')]")
            delete_element.click()
            time.sleep(1)
            num-=1
        else:
            duplicateTickerIndex = tickerList.index(current_ticker)
            tickerList.pop(duplicateTickerIndex)
            num +=1
        watchlist_len  = len(driver.find_elements('xpath','//div[@class="jss160"]//div[@class="simplebar-content-wrapper"]//li'))

    #tickerList is global variable
    for x in tickerList:
        searchbar = driver.find_element('xpath',"//input[@placeholder='Symbol/Name']")
        searchbar.click()
        searchbar.send_keys(Keys.CONTROL + "A")
        searchbar.send_keys(Keys.DELETE)
        time.sleep(2)
        searchbar.send_keys(x)
        time.sleep(3)
        star = driver.find_element('xpath',f"//span[contains(text(),'{x}')]/parent::div/parent::div/parent::div//*[@xmlns='http://www.w3.org/2000/svg']")
        star.click()
        time.sleep(2)
        if watchlist_type =='wtd':
            wtdwatchlist = driver.find_element('xpath',"//*[contains(text(),'Finviz WTD')]//*[@role='img']")
            wtdwatchlist.click()
        elif watchlist_type =='mtd':
            mtdwatchlist = driver.find_element('xpath',"//*[contains(text(),'Finviz MTD')]//*[@role='img']")
            mtdwatchlist.click()
        else:
            ytdwatchlist = driver.find_element('xpath',"//*[contains(text(),'Finviz YTD')]//*[@role='img']")
            ytdwatchlist.click()

def getDataFinviz(timeFrame,perfThreshold=5):
    driver.switch_to.window(driver.window_handles[0])
    if str(timeFrame).lower()=='wtd':
        driver.get(urlWTD)
    elif str(timeFrame).lower()=='mtd':
        driver.get(urlMTD)
    elif str(timeFrame).lower()=='ytd':
        driver.get(urlYTD) 
    else:
        print('Correct timeframe not entered')
        driver.quit()
    time.sleep(2)
    tickerList.clear()
    current_page = 1
    currentTickerPerfAmount = perfThreshold
    while current_page<=3 and currentTickerPerfAmount >=perfThreshold:
        all_tickers = driver.find_elements('xpath',"//table[@class='styled-table-new is-rounded is-tabular-nums w-full screener_table']//tbody/tr")
        halfway_point = driver.execute_script("return (document.body.scrollHeight)/8")
        driver.execute_script(f"window.scrollTo(0, {halfway_point});")
        for x in range(len(all_tickers)):
            currentTickerPerfAmount = driver.find_element('xpath',f"//table[@class='styled-table-new is-rounded is-tabular-nums w-full screener_table']//tbody/tr[{x+1}]/td[3]").text
            currentTickerPerfAmount=float(currentTickerPerfAmount.strip('%'))
            if float(currentTickerPerfAmount)>=perfThreshold:
                ticker = driver.find_element('xpath',f"//table[@class='styled-table-new is-rounded is-tabular-nums w-full screener_table']//tbody/tr[{x+1}]/td[2]").text
                tickerList.append(ticker)
        current_page+=1
        nextpage = driver.find_element('xpath','//*[@href="/assets/dist-icons/icons.svg?rev=10#arrowForward"]')
        nextpage.click()
        time.sleep(3)


loginWebull()
getDataFinviz(timeframe='wtd')
addToWebull(watchlist_type='wtd')
getDataFinviz(timeframe='mtd')
addToWebull(watchlist='mtd')
getDataFinviz(timeframe='ytd')
addToWebull(watchlist='ytd')



    


