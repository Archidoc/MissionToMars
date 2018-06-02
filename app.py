# from activity LessonPlans/13-Web-Scraping-and-Document-Databases/3/Activities/09-Ins_Scrape_And_Render/Solved/app.py
# use app.py and modify it
# import librairies + dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create flask instance 
app = Flask(__name__)

mongo = PyMongo(app)

#  create route to render index.html template
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)