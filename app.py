from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_data = mongo.db.mars.find()

    # return template and data
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():

    # Run scraped functions
    title_p = scrape_mars.scrape_title_p()
    jpl_image = scrape_mars.scrape_mars_image()
    tweet = scrape_mars.scrape_twitter()
    # table1 = scrape_mars.scrape_table()
    hemisphere = scrape_mars.scrape_hemispheres()

    # Store results into a dictionary
    mars = {
       "news_title": title_p['news'],
       "news_p": title_p["paragraph"],
       "jpl_img_url": jpl_image["img_url"],
       "tweet_data": tweet["tweet"],
       "hemisphere1_title": hemisphere[0]["title"],
       "hemisphere1_img": hemisphere[0]["img_url"],
       "hemisphere2_title": hemisphere[1]["title"],
       "hemisphere2_img": hemisphere[1]["img_url"],
       "hemisphere3_title": hemisphere[2]["title"],
       "hemisphere3_img": hemisphere[2]["img_url"],
       "hemisphere4_title": hemisphere[3]["title"],
       "hemisphere4_img": hemisphere[3]["img_url"]
    }

    # Insert forecast into database
    mongo.db.mars.insert_one(mars)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)