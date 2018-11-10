#dependencies 
from flask import Flask, render_template, redirect
from bs4 import BeautifulSoup as bs
import pandas as pd
import flask
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time
# create instance of Flask app
app = Flask(__name__)

newsurl = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
# Retrieve page with the requests module
response = requests.get(newsurl)
soup = bs(response.text, 'lxml')

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
browser.visit(url)
time.sleep(5)

news_p = browser.find_by_css('div[class="article_teaser_body"]').text
browser.quit()
news_title = soup.find("div", class_='content_title').text.strip()

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)
browser.click_link_by_partial_text('FULL IMAGE')
featured_image_url = browser.find_by_css('img.fancybox-image')['src']
browser.quit()

factsurl = 'https://space-facts.com/mars/'
tables = pd.read_html(factsurl)
facts = tables[0]
facts = facts.rename(columns= {0: 'Description', 1: 'Value'})
facts = facts.set_index('Description')
factsHTML = facts.to_html()

tweeturl = 'https://twitter.com/marswxreport?lang=en'
response = requests.get(tweeturl)
soup = bs(response.text, 'lxml')
mars_weather = soup.find("div", class_='js-tweet-text-container').text.strip()

hemispheres = ['Valles Marineris Hemisphere', 'Cerberus Hemisphere','Schiaparelli Hemisphere','Syrtis Major Hemisphere']
hemisphere_image_urls = []
for elt in hemispheres:
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    hemiurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemiurl)
    browser.click_link_by_partial_text(elt)
    browser.click_link_by_partial_text('Open')
    image = browser.find_by_css('img.wide-image')['src']
    browser.quit()
    name = elt.replace(' ', '')
    d = {'ref':name,'title': elt, 'img_url': image}
    hemisphere_image_urls.append(d)


# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo


# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.mars.drop()

# Creates a collection in the database and inserts two documents
db.mars.insert_many(
    [
        {
            'news_title' : news_title,
            'news_desc' : news_p,
            'weather': mars_weather,
            'feature_image': featured_image_url,
            'hemispheres' : hemisphere_image_urls,
            'facts': factsHTML
        }
    ]
)


# Set route
@app.route('/')
def index():
    # Store the entire team collection in a list
    mars = list(db.mars.find())
    print(mars)

    # Return the template with the teams list passed in
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
    newsurl = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    response = requests.get(newsurl)
    soup = bs(response.text, 'lxml')

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(5)

    news_p = browser.find_by_css('div[class="article_teaser_body"]').text
    browser.quit()
    news_title = soup.find("div", class_='content_title').text.strip()

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    featured_image_url = browser.find_by_css('img.fancybox-image')['src']
    browser.quit()

    factsurl = 'https://space-facts.com/mars/'
    tables = pd.read_html(factsurl)
    facts = tables[0]
    facts = facts.rename(columns= {0: 'Description', 1: 'Value'})
    facts = facts.set_index('Description')
    factsHTML = facts.to_html()

    tweeturl = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(tweeturl)
    soup = bs(response.text, 'lxml')
    mars_weather = soup.find("div", class_='js-tweet-text-container').text.strip()

    hemispheres = ['Valles Marineris Hemisphere', 'Cerberus Hemisphere','Schiaparelli Hemisphere','Syrtis Major Hemisphere']
    hemisphere_image_urls = []
    for elt in hemispheres:
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        hemiurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemiurl)
        browser.click_link_by_partial_text(elt)
        browser.click_link_by_partial_text('Open')
        image = browser.find_by_css('img.wide-image')['src']
        browser.quit()
        name = elt.replace(' ', '')
        d = {'ref':name,'title': elt, 'img_url': image}
        hemisphere_image_urls.append(d)


    # Import our pymongo library, which lets us connect our Flask app to our Mongo database.
    import pymongo


    # Create connection variable
    conn = 'mongodb://localhost:27017'

    # Pass connection to the pymongo instance.
    client = pymongo.MongoClient(conn)

    # Connect to a database. Will create one if not already available.
    db = client.mars_db

    # Drops collection if available to remove duplicates
    db.mars.drop()

    # Creates a collection in the database and inserts two documents
    db.mars.insert_many(
        [
            {
                'news_title' : news_title,
                'news_desc' : news_p,
                'weather': mars_weather,
                'feature_image': featured_image_url,
                'hemispheres' : hemisphere_image_urls,
                'facts': factsHTML
            }
        ]
    )
    return redirect("/", code=302)
if __name__ == "__main__":
    app.run(debug=True)
