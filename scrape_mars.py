from selenium import webdriver
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_title_p():
    
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.
    chrome_path = "resources/chromedriver"
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    driver = webdriver.Chrome(chrome_path)
    driver.get(url);
    
    time.sleep(5) #time in seconds
    
    #Selenium
    results_titles = driver.find_elements_by_class_name("content_title")
    results_p = driver.find_elements_by_class_name("article_teaser_body")
    
    # Variable for recent title
    news_title = results_titles[0].text
    
    # Variable for recent <p>
    news_p = results_p[0].text
    
    print(news_title)
    print(news_p)
    
    #Store in Dictionary
    title_and_p = {
        "news": news_title,
        "paragraph": news_p
    }
    
    return title_and_p
    
# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# ------------------------------------------------------------------------------#
#JPL Mars Space Images - Featured Image
#Visit the url for JPL's Featured Space Image here. Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url. Make sure to find the image url to the full size .jpg image. Make sure to save a complete url string for this image.
   
def scrape_mars_image():
   
   # Initialize browser
   browser = init_browser()
   
   # Visit the Website
   url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
   browser.visit(url)
   
   # Scrape page into soup
   html = browser.html
   soup = BeautifulSoup(html, 'html.parser')
   articles = soup.find_all('div', class_='img')
   
   #Using beautiful soup to find url strin
   href = articles[0].find('img')['src']
   articles[0].find('img')['src']
   
   #Save complete url string 
   featured_image_url = 'https://www.jpl.nasa.gov/' + href
   
   print(featured_image_url)
   
   featured_image_url_d = {
       "img_url":featured_image_url
   }
  
   return featured_image_url_d

# ------------------------------------------------------------------------------#
# Mars Weather
# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

def scrape_twitter():

    # Initialize browser
    browser = init_browser()
    
    # Visit the Website
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    tweets = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    
    tweet_text = str(tweets[0].text)
    
    print(tweet_text)
    
    tweet_d = {
        "tweet":tweet_text
    }
    
    return tweet_d

# Mars Facts
#Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.Use Pandas to convert the data to a HTML table string.
def scrape_table():

    url = 'https://space-facts.com/mars/'
    
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Information', 'Data']
    html_table = df.to_html()
    html_table.replace('\n', '')
    df.to_html('table.html')
    
    return df

# Mars Hemisperes
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

# Mars Hemisperes
# Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

def scrape_hemispheres():
    
    # Initialize browser
    browser = init_browser()
    
    # Visit the website
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Scrape page with soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = soup.find_all('div', class_='item')
    
    i = 0
    d = {}
    hemisphere_image_urls = []

    for x in hemispheres:
    
        #finding the title 
        text = hemispheres[i].find('h3').text
    
        #going to the page via the header title/text
        browser.click_link_by_partial_text(text)
        
        #going to image page
        # browser.click_link_by_partial_href('.tif/full.jpg')
        
        # Get the current website url
        url = browser.url
    
        # Scrape page with soup
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        #getting url and giving it a variable
        current_img = soup.find_all('div', class_="downloads")
        img_url = current_img[0].find('li').find('a')['href']
    
        #create key and value for dictionary d
        d.update({'img_url': img_url,'title': text})
        
        #add dictionary to list
        hemisphere_image_urls.append(d.copy())
    
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
    
        i += 1
        print(text)
    
    return(hemisphere_image_urls)


# def scrape():
    
#     # Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. Assign the text to variables that you can reference later.
#     chrome_path = "resources/chromedriver"
#     url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
#     driver = webdriver.Chrome(chrome_path)
#     driver.get(url);
    
#     time.sleep(5) #time in seconds
    
#     #Selenium
#     results_titles = driver.find_elements_by_class_name("content_title")
#     results_p = driver.find_elements_by_class_name("article_teaser_body")
    
#     # Variable for recent title
#     news_title = results_titles[0].text
    
#     # Variable for recent <p>
#     news_p = results_p[0].text
    
#     print(news_title)
#     print(news_p)
    
#     # ------------------------------------------------------------------------------#
#     #JPL Mars Space Images - Featured Image
#     #Visit the url for JPL's Featured Space Image here. Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url. Make sure to find the image url to the full size .jpg image. Make sure to save a complete url string for this image.
    
#     #Splinter / Browser
#     executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
#     browser = Browser('chrome', **executable_path, headless=False)
    
#     url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#     browser.visit(url)
    
#     html = browser.html
#     soup = BeautifulSoup(html, 'html.parser')
#     articles = soup.find_all('div', class_='img')
    
#     #Using beautiful soup to find url strin
#     href = articles[0].find('img')['src']
#     articles[0].find('img')['src']
    
#     #Save complete url string 
#     featured_image_url = 'https://www.jpl.nasa.gov/' + href
    
#     print(featured_image_url)
    
#     # ------------------------------------------------------------------------------#
#     # Mars Weather
#     # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.
    
#     url = 'https://twitter.com/marswxreport?lang=en'
#     browser.visit(url)
    
#     html = browser.html
#     soup = BeautifulSoup(html, 'html.parser')
#     tweets = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    
#     tweet_text = str(tweets[0].text)
    
#     print(tweet_text)
    
#     # ------------------------------------------------------------------------------#
#     # Mars Facts
#     #Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.Use Pandas to convert the data to a HTML table string.
    
#     url = 'https://space-facts.com/mars/'
    
#     tables = pd.read_html(url)
#     df = tables[0]
#     df.columns = ['Information', 'Data']
#     html_table = df.to_html()
#     html_table.replace('\n', '')
#     df.to_html('table.html')
    
#     # ------------------------------------------------------------------------------#
#     # Mars Hemisperes
#     # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.Save both the image url string for the full resolution hemipshere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

#     url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#     browser.visit(url)
    
#     html = browser.html
#     soup = BeautifulSoup(html, 'html.parser')
#     hemispheres = soup.find_all('div', class_='item')
    
#     i = 0
#     d = {}
#     hemisphere_image_urls = []

#     for x in hemispheres:
    
#         #finding the title 
#         text = hemispheres[i].find('h3').text
    
#         #going to the page via the header title/text
#         browser.click_link_by_partial_text(text)
#         #going to image page
#         browser.click_link_by_partial_href('.tif/full.jpg')
#         #getting url and giving it a variable
#         img_url = browser.url
    
#         #create key and value for dictionary d
#         d.update({'img_url': img_url,'title': text})
#         #add dictionary to list
#         hemisphere_image_urls.append(d.copy())
    
#         url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#         browser.visit(url)
    
#         i += 1
#         print(text)
    
#     print(hemisphere_image_urls)

