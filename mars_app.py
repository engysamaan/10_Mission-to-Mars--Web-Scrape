from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def index():
    ## creat doc as empty string to host the latest outcome 
    doc = " "
    mars = mongo.db.collection.find()

    ## loop in mongo db to get the latest doc 
    for x in mars:
       doc = x

    print(doc)
    return render_template("index.html", mars = doc)


@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.insert_one(mars_data)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)