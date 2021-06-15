#!/usr/bin/env python3

from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import pymongo 
import datetime as dt


def scrape():
	
	# initialize the splinter web browser
	ex_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **ex_path, headless=False)
	
	# --------- Main page scraping -------------
	url = 'https://redplanetscience.com/'
	browser.visit(url)
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	
	
	# find the latest news articles
	
	title_ = soup.find_all("div", class_="content_title")
	tease_ = soup.find_all("div", class_="article_teaser_body")
	
	articles = []
	for idx,title in enumerate(title_):
		articles.append({"title": title.text, "tease":tease_[idx].text})
		
	
	# --------- Main image scraping -------------
	imURL = "https://spaceimages-mars.com/"
	browser.visit(imURL)
	
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	
	x = soup.find("img", class_="headerimage")
	featured_image_url = imURL + x["src"]
	
	
	# --------- Mars Facts scraping -------------
	
	facts_url = "https://galaxyfacts-mars.com/"
	
	tables = pd.read_html(facts_url)
	fact_df = tables[1]
	fact_df.columns = ["Feature", "Value"]
	
	
	# --------- hemisphere scraping -------------
	hemi_url = "https://marshemispheres.com/"
	browser.visit(hemi_url)
	html = browser.html
	soup = BeautifulSoup(html, "html.parser")
	results = soup.find_all("div", class_="description")
	
	
	sites = []
	for result in results:
		
		title = result.a.text.strip()
		link_url = result.a['href']
		#print(f"title - {title}  and link: {link_url}")
		sites.append({"title": title, "url": hemi_url + link_url})
	
	hemi_sites = []
	
	for site in sites:
		# go site for each image
		browser.visit(site["url"])
		
		#click on the "open" button to expand the image
		browser.links.find_by_partial_text('Open').click()
		
		# git the html data
		img_html = browser.html
		
		# parce the html
		soup = BeautifulSoup(img_html, "html.parser")
		
		# find the url for the image
		img_url = soup.find("img", class_="wide-image")['src']
		
		#fix the title by removing the enhanced
		title = site["title"].replace(" Enhanced", "")
		img_url_full = hemi_url + img_url
		#store dictionary in list
		hemi_sites.append({'title':title, "img_url": img_url_full})
		print(img_url_full)
		
		# https://marshemispheres.com/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg
	#-----------done close the browser-------------	
	browser.quit()
	
	
	
	conn = 'mongodb://localhost:27017'
	client = pymongo.MongoClient(conn)
	db = client.Mars_db
	db.data.drop()
	
	
	db.data.insert_one({"articles": articles})
	db.data.insert_one({"image": featured_image_url})
	
	fact_dict = fact_df.to_dict("records")
	db.data.insert_one({"facts": fact_dict})
	db.data.insert_one({"hemi_images": hemi_sites })
	
	db.data.insert_one({"_id": 1, "updated": dt.datetime.today()})
	
if __name__ == "__main__":
	scrape()