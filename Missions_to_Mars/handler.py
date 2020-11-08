
import requests

from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import pandas as pd
import pymongo


def scrape_handler():
    url = 'https://mars.nasa.gov/news/'
    r = requests.get(url)
    r.text
    soup = BeautifulSoup(r.text, 'html.parser')
    titles = soup.findAll("div", {"class": "content_title"})
    titles = [titles[i].findChildren()[0].text.replace("\n","") for i in range(len(titles))]
    texts = soup.findAll("div", {"class": "rollover_description_inner"})
    texts = [texts[i].text.replace("\n","").strip() for i in range(len(texts))]
    text_dic = []
    for i in range(len(texts)):
        item={}
        item['type'] = "texttitle"
        item['title']=titles[i]
        item['text']=texts[i] 
        text_dic.append(item)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    r = requests.get(url)
    r.text
    soup = BeautifulSoup(r.text, 'html.parser')
    image_button = soup.find('a',{'id':'full_image'})
    featured_image_url = 'https://www.jpl.nasa.gov'+image_button['data-fancybox-href']
    url_mars = 'https://space-facts.com/mars/'
    r = requests.get(url_mars)
    r.text
    soup_mars = BeautifulSoup(r.text, 'html.parser')
    table = soup_mars.find("table",{"id":"tablepress-p-mars-no-2"})
    mars_table_dic={}
    mars_table = pd.read_html(str(table))[0]
    for index , row in mars_table.iterrows():
        mars_table_dic[row[0]]=row[1]
    #here im defining the URL 
    url_astro = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #extracting the contents of URL into Soup variable
    soup_mars = BeautifulSoup(requests.get(url_astro).text, 'html.parser')
    # Finding the interested variables in the Soup
    links = soup_mars.findAll("a",{"class":"itemLink product-item"})
    hemisphere_image_urls=[]
    for link in links:
        hemisphere_image_urls.append({"type":"titleimg","title":link.findChildren("div")[0].findChildren("h3")[0].text,"img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/"+link["href"].split("/")[-1]+".tif/full.jpg"})
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.scrape_db
    collection = db.mars
    collection.remove({})
    main_db={}
    main_db['table']=mars_table_dic

    main_db['title_text']=[]
    for item in text_dic:
        main_db['title_text'].append(item)
    main_db['hemisphere_images']=[]
    for item in hemisphere_image_urls:
        main_db['hemisphere_images'].append(item)
    main_db['featured_image_url']=featured_image_url
    collection.insert(main_db)
