import csv
import pandas as pd
import os
import time 

#using web scraper to take satalite screenshots fron openstreetmaps
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
#screenshots and other image processing tools
from PIL import Image


airport_list = []
airfield_list = []

with open('./airport_WKT.csv', newline='') as csvfile:
    aiport_csv = csv.reader(csvfile, delimiter=',', quotechar="'")
    for row in aiport_csv:
        # also get rid of WKT for searching witht he coordinates because we did not end up needed that format
        airport_list.append(row[1][8:-2])


with open('./airfield_WKT.csv', newline='') as csvfile:
    airfield_csv = csv.reader(csvfile, delimiter=',', quotechar="'")
    for row in airfield_csv:
        airfield_list.append(row[1][8:-2])

#since airfields < airports, and we want the same amount of both types of data, we will take a slice of how many airfields there are of airports
# should now have a list of 531 coordinate locations for each list
airport_list_short = airport_list[200:(200+531)]
print(airport_list_short[0:10])
print('# of airport coords:', len(airport_list_short))
print('# of airfield coords:', len(airfield_list))

# specify web scraper browser size; sufficiently large to crop
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1920")

two_lists = [airport_list_short, airfield_list]
two_lists_names = ['airport', 'airfield']

#may return uneven lists do to random errors occuring for certain coordinates (for me i received 528 for airports and 525 for airfields; I deleted 3 from airport to be left with 525 each in the final dataset)
for curr_list in two_lists:
    j = two_lists.index(curr_list)
    for i in two_lists[j]:
        try:    
            #progress
            split = i.split()
            print(f"{two_lists[j].index(i) + 1}/{len(two_lists[j])} in {two_lists_names[j]} list at coords: {split}")

            if f"{i}.png" in os.listdir(f"./satalite_images/{two_lists_names[j]}"): 
                print("already done (or no coord data), skipping...")
                continue
            else:
                driver = Chrome(options=chrome_options)
                #map height chosen based off how good a small airport looked and if it fit much of JFK airport, 15 zoomed
                url = f"https://www.openstreetmap.org/search?query={split[0]}%20{split[1]}#map=15/{round(float(split[0]), 4)}/{round(float(split[1]), 4)}"
                driver.get(url)
                driver.implicitly_wait(20)
                location = f"./satalite_images/{two_lists_names[j]}/{i}.png"
                time.sleep(4)
                driver.save_screenshot(location)
                driver.close()
                #crop image
                im = Image.open(location)
                width, height = im.size
                (left, upper, right, lower) = (width*1/5, height*1/20, width*29/30, height*34/35)
                print((left, upper, right, lower))
                im = im.crop((left, upper, right, lower))
                im = im.resize((800,800))
                im.save(location)
        except Exception as e:
            print(e)
            continue
