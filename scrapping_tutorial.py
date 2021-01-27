import pathlib
from selenium import webdriver
import pandas as pd

web = 'https://sports.tipico.de/en/todays-matches'

# Tell the script were is the chrome driver
path = str(pathlib.Path().absolute()) + '/chromedriver'

# Set the driver instance
driver = webdriver.Chrome(path)
driver.get(web)

# Every time the betting site is opened, a popup will show up. We need to get
# rid of the popup to start scraping the website. We have to make Selenium
#  click the popup’s ‘accept’ button every time the website is opened.
accept = driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]')
accept.click()

"""
Scrapper
"""

teams = []
x12 = []  # 3-way
odds_events = []

# We'll check football matches
sport_title = driver.find_elements_by_class_name('SportTitle-styles-sport')

for sport in sport_title:
    # selecting only football
    if sport.text == 'Football':
        parent = sport.find_element_by_xpath('./..')
        grandparent = parent.find_element_by_xpath('./..')

       # Single row event
        single_row_events = grandparent.find_elements_by_class_name(
            'EventRow-styles-event-row')

        for match in single_row_events:
            odds_event = match.find_elements_by_class_name(
                'EventOddGroup-styles-odd-groups')
            odds_events.append(odds_event)
            # teams
            for team in match.find_elements_by_class_name('EventTeams-styles-titles'):
                teams.append(team.text)

            for odds_event in odds_events:
                for n, box in enumerate(odds_event):
                    rows = box.find_elements_by_xpath('.//*')
                    if n == 0:
                        x12.append(rows[0].text)

driver.quit()

#Storing lists within dictionary
dict_gambling = {'Teams': teams, '1x2': x12}
#Presenting data in dataframe
df_gambling = pd.DataFrame.from_dict(dict_gambling)
print(df_gambling)