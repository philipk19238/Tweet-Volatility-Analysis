import selenium
from selenium import webdriver
import pandas as pd
import matplotlib.pyplot as plt
import time

#path of chromedriver object. If you are trying to test the code, ensure you point the path
#to the proper location
path = r'C:\Users\Philip\AppData\Local\Programs\Python\Python38-32/chromedriver.exe'

def scrollBottom():
    #scrolls all the way down so scraper can access all data
    page = driver.find_element_by_tag_name('body')
    for i in range(200):
        page.send_keys(Keys.PAGE_DOWN)

def getData():
    symbolData = driver.find_elements_by_xpath('//td[@class="Py(10px) Pstart(10px)"]')
    #returns every sixth variable to exclude useless data
    volumecol = [symbolData[index].text for index in range(5,len(symbolData),6)]
    dates = [date.text for date in driver.find_elements_by_xpath('//td[@class="Py(10px) Ta(start) Pend(10px)"]')]
    return volumecol, dates

def manipulateData(date, volume):
    df = pd.DataFrame(volume, index = date).iloc[::-1].rename(columns={0:'volume'})
    #converting strings to float
    df['volume'] = df['volume'].apply(lambda row: float(row.replace(',',"")))
    #finding percentage change
    df = df.pct_change()
    #multiplying values by 100 to display in percentage notation
    df['volume'] = df['volume'].apply(lambda row: row * 100)
    return df

def graphData(data):
    fig,ax = plt.subplots(figsize=(25,10))
    ax.bar(df.index, df['volume'])
    ax.set_title('Change in Daily Volume since 2017', fontsize=23)
    ax.set_ylabel('Percent Change in Volume',fontsize = 15)
    ax.set_xlabel('Date (Jan 2017 to April 2020)',fontsize=15)

def main():
    driver = webdriver.Chrome(path)
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get('https://finance.yahoo.com/quote/%5EDJI/history?period1=1484870400&period2=1586649600&interval=1d&filter=history&frequency=1d')
    time.sleep(2)
    scrollBottom()
    data = getData()
    df = manipulateData(data[1], data[0])
    graphData(df)
    df.to_csv('volumechange.csv')

if __name__ == "__main__":
    main()
