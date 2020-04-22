import selenium
from selenium import webdriver
import pandas as pd
import matplotlib.pyplot as plt

#path of chromedriver object. If you are trying to test the code, ensure you point the path
#to the proper location
path = r'C:\Users\Philip\AppData\Local\Programs\Python\Python38-32/chromedriver.exe'

def getDates():
    #returns the date of every Trump tweet
    return [i.text[:12] for i in driver.find_elements_by_xpath('//span[@class="tweet-date ng-binding"]')]

def manipulateData(dateList):
    #grouping the number of tweets by setting the keys as the date and the value as number of daily tweets for that date
    dateDic = Counter(dateList)
    #data wrangling to dataframe format
    tweetDf = pd.DataFrame(dateDic, index=[0]).T.iloc[:list(dateDic.keys()).index('Jan 19, 2017')].rename(columns={0:'DailyTweetAmounts'})
    tweetDf.to_csv('dailytweets.csv')
    #reversing the dataframe to display results in chronological order
    return tweetDf.iloc[::-1]

def graphData(x_axis, y_axis):
    fig,ax = plt.subplots(figsize=(25,10))
    #creating bar graph with x axis as date and y axis at daily tweet amounts
    ax.bar(x_axis, y_axis)
    ax.set_title('Daily Trump Tweet Amounts', fontsize=23)
    ax.set_xlabel('Dates (Jan 2017 to April 2020)', fontsize=15)
    ax.set_ylabel('Daily Tweet Amount',fontsize=15)

def main(url='http://www.trumptwitterarchive.com/archive'):
    driver = webdriver.Chrome(path)
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.get(url)
    #make sure to scroll down to 2017 tweets
    tweetAmount = getDates()
    tweetDf = manipulateData(tweetAmount)
    graphData(tweetDf.index, tweetDf['DailyTweetAmounts'])

if __name__ == "__main__":
    main()
