# Step 1 - Scraping

# Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

# Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.

# NASA Mars News

# Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.

from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import requests
import tweepy
import time

# load tweeter api keys
from config import consumer_key, consumer_secret, access_token, access_token_secret


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()


    # ----create a dictionary to hold all the data (steps covered from mission_to_mars.py)
    mars_data = {}

    #mars nasa web news page
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # find the title and paragraph
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div",class_="article_teaser_body").text
    news_date = soup.find("div", class_="list_date").text

    #----add to dict ----
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p


    # JPL Mars Space Images - Featured Image
    # Visit the url for JPL's Featured Space Image here.
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Make sure to find the image url to the full size .jpg image.
    # Make sure to save a complete url string for this image.

    #JPL Mars Space Images - featured image
    url_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_img)

    #scrape browser to find the image
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('article', class_="carousel_item").get('style')
    #thanks kat
    image = image.split("('", 1)[1].split("')")[0]
    featured_image_url = "https://jpl.nasa.gov" + image
    full_image_url = featured_image_url

    #----add to dict----
    mars_data["full_image_url"] =  full_image_url


    # Mars Weather
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called mars_weather.

    # Twitter credentials and APi authentification
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    # find the target user
    target_user = "MarsWxReport"
    mars_tweet = api.user_timeline(target_user , count = 1)
    latest_mars_weather=mars_tweet[0]['text']


    #----add to dict----
    mars_data["latest_mars_weather"] =  latest_mars_weather


    # Mars Facts
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    url_facts= "https://space-facts.com/mars/"
    browser.visit(url_facts)

    table = pd.read_html(url_facts)
    table[0]

    # add headers to the columns to replace 0 and 1
    df_mars_table = table [0]
    df_mars_table.columns = ["Mars Variables", "Data"]
    # reset index to Variables
    df_mars_table.set_index(["Mars Variables"])

    mars_table_html = df_mars_table.to_html()
    mars_table_html = mars_table_html.replace("\n", "")

    #----add to dict----
    mars_data["df_mars_table"] =  mars_table_html


    # Mars Hemispheres
    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # Mars hemispheres
    url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url_hemisphere)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # create hemisphere list
    mars_hemispheres = []

    # grab the different hemispheres
    # looping through the pages
    # use find by tag http://splinter.readthedocs.io/en/latest/finding.html
    for i in range (4):
        time.sleep(2)
        hemisphere_images = browser.find_by_tag ("h3")
        hemisphere_images [i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_product = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ img_product

    # Append the dictionary with the image url string and the hemisphere title to a list.
        hemisphere_image_dict={"title":img_title,"img_url":img_url}
        mars_hemispheres.append(hemisphere_image_dict)
        browser.back()

    #----add to dict----
    mars_data["mars_hemispheres"] =  mars_hemispheres


    # return the dictionnary of each steps
    return mars_data

    # from pprint import pprint
    # pprint (mars_data)