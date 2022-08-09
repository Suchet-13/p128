from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time
import csv
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("chromedriver")
browser.get(START_URL)
time.sleep(10)

headers = ["Proper name","Distance (ly)","Mass", "Radius"]
star_data = []

def scrape():
   
    for i in range(0, 428):
         while True:
            time.sleep(2)

            url = 'https://en.wikipedia.org/wiki/List_of_brown_dwarfs'
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            star_table = soup.find_all('table')
            table_rows = star_table[7].find_all('tr')

            #soup = BeautifulSoup(browser.page_source, "html.parser")

            for tr_tag in soup.find_all("tr", attrs={"class", "wikitable sortable jquery-tablesorter"}):
                td_tags = tr_tag.find_all("a")
                temp_list = []
                for index, td_tag in enumerate(td_tags):
                    if index == 0:
                        temp_list.append(td_tag.find_all("td")[0].contents[0])
                    else:
                        try:
                            temp_list.append(td_tag.contents[0])
                        except:
                            temp_list.append("")

                # Get Hyperlink Tag
                hyperlink_td_tag = td_tags[0]

                temp_list.append("https://en.wikipedia.org/wiki"+ hyperlink_td_tag.find_all("a", href=True)[0]["href"])
                
                star_data.append(temp_list)

         browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

         print(f"Page {i} scraping completed")


scrape()

new_stars_data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        new_stars_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

#Calling method

for index, data in enumerate(star_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(new_stars_data[0:10])

final_stars_data = []

for index, data in enumerate(star_data):
    new_stars_tag_data_element = new_stars_data[index]
    new_stars_data_element = [elem.replace("\n", "") for elem in new_stars_data_element]
    new_stars_data_element = new_stars_data_element[:7]
    final_stars_data.append(data + new_stars_data_element)

with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(final_stars_data)