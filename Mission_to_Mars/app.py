#!/usr/bin/env python

from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
import datetime as dt
import pymongo
from scrape_mars import scrape

app = Flask(__name__)



# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.Mars_db

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    
    try:
        articles_db = db.data.find({},{"_id": 0, "articles": 1})
        #articles = articles_db['articles']
    #    feat_image_url = db.data.find("image")
    #    fact_dict = db.data.find("facts")
    #    hemi_images = db.data.find("hemi_images")
        count = 0
        
        #print(f"doc = {articles_db[0]}")
        articles = articles_db[0]['articles']
        
    #    for x in articles:
    #        count += 1
    #        print(f"{count} = {x['title']}\n\n")
        
        fact_doc = db.data.find({"facts": {"$exists": True}})
        fact_array = fact_doc[0]["facts"]
        
        for fact in fact_array:
            
            print(f"{fact['Feature']}:  {fact['Value']}")
            
            
        img_doc = db.data.find({"image": {"$exists": True}})
        img_path = img_doc[0]["image"]
    #    print(f"this is the path ====== {img_path}")
    
        hemi_doc = db.data.find({"hemi_images": {"$exists": True}})
        img_array = hemi_doc[0]["hemi_images"]
        
        
        update_doc =  db.data.find({"updated":{"$exists": True}},{"_id":0, "updated":1})
        update = update_doc[0]['updated']
    except:
        articles = []
        img_path = ""
        fact_array = []
        img_array = []
        update=""
    
#    for img in img_array:
#        
#        print(f"{img}\n\n")
        
    
        # mars_data = {'articles': articles, 'feat_image_url': feat_image_url, 'facts': fact_dict, "hemi_images": hemi_images}
    
    return render_template("index.html", articles = articles, 
        img_path = img_path, 
        facts=fact_array, 
        img_array = img_array,
        update=update)

@app.route("/scrape")
def scraper():
    scrape()
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
    
        