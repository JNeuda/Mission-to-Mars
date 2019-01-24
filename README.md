

```python
import pandas as pd
import requests

from selenium import webdriver
from splinter import Browser
from bs4 import BeautifulSoup
```

### NASA Mars News


```python
#Mars News url
news_url = 'https://mars.nasa.gov/news'

#browser setup
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome')
browser.visit(news_url)

#create BeautifulSoup object and parse
soup = BeautifulSoup(browser.html, 'html.parser')
```


```python
#find the latest news title and remove newline characters
news_title = soup.find(class_='content_title').get_text(strip=True)

news_title
```




    'NASA Briefing on First Mission to Study Mars Interior'




```python
#find the latest news paragraph text and remove newline characters
news_p = soup.find(class_='rollover_description_inner').get_text(strip=True)

news_p
```




    'NASA’s next mission to Mars will be the topic of a media briefing Thursday, March 29, at JPL. The briefing will air live on NASA Television and the agency’s website.'



### JPL Mars Space Images - Featured Image


```python
#JPL Mars images url
img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
img_base_url = 'https://www.jpl.nasa.gov'

#retrieve
result = requests.get(img_url)

#check if okay
result.ok
```




    True




```python
#make it text
html = result.text

#create BeautifulSoup object and parse
soup = BeautifulSoup(html, 'html.parser')

```


```python
#select the part that contains the image urls
fancy_box = soup.select('li.slide a.fancybox')

#make a list of just the data-fancybox-hrefs
img_list = [i.get('data-fancybox-href') for i in fancy_box]

#combine the base url with the first img url
featured_image_url = img_base_url + img_list[0]   

print(featured_image_url)
```

    https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA22405_hires.jpg
    

### Mars Weather





```python
#scrape the latest Mars weather tweet from the Mars Weather twitter account
twit_url = 'https://twitter.com/marswxreport?lang=en'
result = requests.get(twit_url)
result.ok
```




    True




```python
#make it text
html = result.text

#create BeautifulSoup object and parse
soup = BeautifulSoup(html, 'html.parser')
```


```python
#get the weather from the newest tweet
mars_weather = soup.find(class_='tweet-text').get_text()
mars_weather
```




    'Saturn’s planet-sized moon Titan, its encircling atmosphere backlit by the Sun, as seen 12 years ago today. Details: https://go.nasa.gov/2HadMcO\xa0 #SaturnSaturdaypic.twitter.com/zeVCa1N2vd'



### Mars Facts


```python
#Mars space facts url
facts_url = 'https://space-facts.com/mars/'

#use Pandas to scrape the planet profile
profile = pd.read_html(facts_url)
profile               
```




    [                      0                              1
     0  Equatorial Diameter:                       6,792 km
     1       Polar Diameter:                       6,752 km
     2                 Mass:  6.42 x 10^23 kg (10.7% Earth)
     3                Moons:            2 (Phobos & Deimos)
     4       Orbit Distance:       227,943,824 km (1.52 AU)
     5         Orbit Period:           687 days (1.9 years)
     6  Surface Temperature:                  -153 to 20 °C
     7         First Record:              2nd millennium BC
     8          Recorded By:           Egyptian astronomers]




```python
#make a df
profile_df = profile[0]

#set index to the 0 column
profile_df.set_index(0, inplace=True)

#delete the index name
profile_df.index.names = [None]

#delete the column name
profile_df.columns = ['']

profile_df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Equatorial Diameter:</th>
      <td>6,792 km</td>
    </tr>
    <tr>
      <th>Polar Diameter:</th>
      <td>6,752 km</td>
    </tr>
    <tr>
      <th>Mass:</th>
      <td>6.42 x 10^23 kg (10.7% Earth)</td>
    </tr>
    <tr>
      <th>Moons:</th>
      <td>2 (Phobos &amp; Deimos)</td>
    </tr>
    <tr>
      <th>Orbit Distance:</th>
      <td>227,943,824 km (1.52 AU)</td>
    </tr>
    <tr>
      <th>Orbit Period:</th>
      <td>687 days (1.9 years)</td>
    </tr>
    <tr>
      <th>Surface Temperature:</th>
      <td>-153 to 20 °C</td>
    </tr>
    <tr>
      <th>First Record:</th>
      <td>2nd millennium BC</td>
    </tr>
    <tr>
      <th>Recorded By:</th>
      <td>Egyptian astronomers</td>
    </tr>
  </tbody>
</table>
</div>




```python
#convert the data to a HTML table string
html_table = profile_df.to_html()

#clean it up
html_table = html_table.replace('\n', '')

html_table
```




    '<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th></th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>Equatorial Diameter:</th>      <td>6,792 km</td>    </tr>    <tr>      <th>Polar Diameter:</th>      <td>6,752 km</td>    </tr>    <tr>      <th>Mass:</th>      <td>6.42 x 10^23 kg (10.7% Earth)</td>    </tr>    <tr>      <th>Moons:</th>      <td>2 (Phobos &amp; Deimos)</td>    </tr>    <tr>      <th>Orbit Distance:</th>      <td>227,943,824 km (1.52 AU)</td>    </tr>    <tr>      <th>Orbit Period:</th>      <td>687 days (1.9 years)</td>    </tr>    <tr>      <th>Surface Temperature:</th>      <td>-153 to 20 °C</td>    </tr>    <tr>      <th>First Record:</th>      <td>2nd millennium BC</td>    </tr>    <tr>      <th>Recorded By:</th>      <td>Egyptian astronomers</td>    </tr>  </tbody></table>'



### Mars Hemispheres


```python
#visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres

#USGS url
usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

#visit
browser.visit(usgs_url)

#create BeautifulSoup object and parse
soup = BeautifulSoup(browser.html, 'html.parser')
```


```python
#get the 4 hemispheres (class of 'item')
hemispheres = soup.select('div.item')

hemispheres
```




    [<div class="item"><a class="itemLink product-item" href="/search/map/Mars/Viking/cerberus_enhanced"><img alt="Cerberus Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/dfaf3849e74bf973b59eb50dab52b583_cerberus_enhanced.tif_thumb.png"/></a><div class="description"><a class="itemLink product-item" href="/search/map/Mars/Viking/cerberus_enhanced"><h3>Cerberus Hemisphere Enhanced</h3></a><span class="subtitle" style="float:left">image/tiff 21 MB</span><span class="pubDate" style="float:right"></span><br/><p>Mosaic of the Cerberus hemisphere of Mars projected into point perspective, a view similar to that which one would see from a spacecraft. This mosaic is composed of 104 Viking Orbiter images acquired…</p></div> <!-- end description --></div>,
     <div class="item"><a class="itemLink product-item" href="/search/map/Mars/Viking/schiaparelli_enhanced"><img alt="Schiaparelli Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/7677c0a006b83871b5a2f66985ab5857_schiaparelli_enhanced.tif_thumb.png"/></a><div class="description"><a class="itemLink product-item" href="/search/map/Mars/Viking/schiaparelli_enhanced"><h3>Schiaparelli Hemisphere Enhanced</h3></a><span class="subtitle" style="float:left">image/tiff 35 MB</span><span class="pubDate" style="float:right"></span><br/><p>Mosaic of the Schiaparelli hemisphere of Mars projected into point perspective, a view similar to that which one would see from a spacecraft. The images were acquired in 1980 during early northern…</p></div> <!-- end description --></div>,
     <div class="item"><a class="itemLink product-item" href="/search/map/Mars/Viking/syrtis_major_enhanced"><img alt="Syrtis Major Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/aae41197e40d6d4f3ea557f8cfe51d15_syrtis_major_enhanced.tif_thumb.png"/></a><div class="description"><a class="itemLink product-item" href="/search/map/Mars/Viking/syrtis_major_enhanced"><h3>Syrtis Major Hemisphere Enhanced</h3></a><span class="subtitle" style="float:left">image/tiff 25 MB</span><span class="pubDate" style="float:right"></span><br/><p>Mosaic of the Syrtis Major hemisphere of Mars projected into point perspective, a view similar to that which one would see from a spacecraft. This mosaic is composed of about 100 red and violet…</p></div> <!-- end description --></div>,
     <div class="item"><a class="itemLink product-item" href="/search/map/Mars/Viking/valles_marineris_enhanced"><img alt="Valles Marineris Hemisphere Enhanced thumbnail" class="thumb" src="/cache/images/04085d99ec3713883a9a57f42be9c725_valles_marineris_enhanced.tif_thumb.png"/></a><div class="description"><a class="itemLink product-item" href="/search/map/Mars/Viking/valles_marineris_enhanced"><h3>Valles Marineris Hemisphere Enhanced</h3></a><span class="subtitle" style="float:left">image/tiff 27 MB</span><span class="pubDate" style="float:right"></span><br/><p>Mosaic of the Valles Marineris hemisphere of Mars projected into point perspective, a view similar to that which one would see from a spacecraft. The distance is 2500 kilometers from the surface of…</p></div> <!-- end description --></div>]




```python
#Loop through each hemisphere

hemisphere_image_urls = []

for h in hemispheres:
    title = (h.find('h3').text).replace(' Enhanced', '')
        
    #click the hemisphere
    browser.click_link_by_partial_text(title)
    
    #make new soup of that page
    soup = BeautifulSoup(browser.html, 'html.parser')
    
    #find the full image
    full = soup.find('a', text='Sample')
    
    #get the img url
    img_url = full['href']
    
    #make a dict and append to the list
    hemisphere_image_urls.append({'title': title, 'img_url': img_url})
    
    #go back 
    browser.back()

#close browser
browser.quit()    

hemisphere_image_urls
```




    [{'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
      'title': 'Cerberus Hemisphere'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
      'title': 'Schiaparelli Hemisphere'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
      'title': 'Syrtis Major Hemisphere'},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg',
      'title': 'Valles Marineris Hemisphere'}]


