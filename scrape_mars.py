# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

# Setting up chromedriver, located in same folder as this code.

# Putting this code in a function inspired by activity Ins_Scrape_And_Render 

def init_browser():
    # Note you should replace 'chromedriver.exe' with the path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():

    browser = init_browser()

    # Scraping Mars News

    final_dict = {}

    # Getting the html from the NASA Mars News site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Below largely pulled from activity Ins_Splinter

    html = requests.get(url).text
    soup = bs(html, 'html.parser')
    

    # Scraping the latest News Title
    results = soup.find_all("div", class_="content_title")

    title = results[0].text
    
    results = soup.find_all("div", class_="rollover_description_inner")
    
    paragraph = results[0].text
    

    final_dict["mars_news_title"] = title
    final_dict["mars_news_paragraph"] = paragraph

    


    # Scraping JPL Mars space Images

    # Getting the html from the JPL site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html

    # Create a Beautiful Soup object
    soup = bs(html, 'html.parser')

    # I notice a button link to the image with <a class="button fancybox"...id="full_image"...

    result = soup.find("a", id="full_image")

    address_end = result.get('data-fancybox-href')

    # Appending to get the full url

    featured_image_url = "https://jpl.nasa.gov" + address_end

    final_dict["jpl_url"] = featured_image_url

    




    # Scraping Mars Facts

    url = "https://space-facts.com/mars/"
    browser.visit(url)
    html = browser.html

    # Create a Beautiful Soup object
    soup = bs(html, 'html.parser')

    # Using pandas to get tabular data

    mars_tables = pd.read_html(url)

    # I see two commas, thus three items in the list. I only want the first item in the list
    # which should be a dataframe.

    mars_df = mars_tables[0]

    # Renaming the columns to attribute and value, setting index to attribute

    mars_df.columns = ['attribute', 'value']
    mars_df.set_index('attribute', inplace=True)

    # Converting the dataframe to an html table string

    html_table = mars_df.to_html()

    final_dict["mars_fact_table_html_string"] = html_table

    


    # Mars Hemispheres

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html

    # Create a Beautiful Soup object
    soup = bs(html, 'html.parser')

    #Making a list without duplicates

    addresses = []

    for link in soup.find_all('a', class_="itemLink product-item"):
        if f"https://astrogeology.usgs.gov{link.get('href')}" not in addresses:
            addresses.append(f"https://astrogeology.usgs.gov{link.get('href')}")
        
    # Looping through the above sites (I can't get the .click() thing in splinter to work at the moment)

    # Creating the list

    hemisphere_image_urls = []

    for row in addresses:
        browser.visit(row)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        # The high resolution image is the only image in the list of links with a .tif file type
        # Grabbing that, and the hemisphere name:

        title = soup.find("h2", class_="title").text
        
        for link in soup.find_all('a'):
            if ".tif" in link.get('href'):
            
                # Weed out the .jpg with .tif earlier in the url
                if ".jpg" not in link.get('href'):
                    #print(link.get('href'))
                
                    if {title:link.get('href')} not in hemisphere_image_urls:
                        
                        dict = {title:link.get('href')}
                        
                        hemisphere_image_urls.append(dict)
        
    final_dict["hemisphere_urls"] = hemisphere_image_urls

    

    browser.quit()

    return final_dict









