from splinter import Browser
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
        
    browser = init_browser()
    # creat a Dic to run in flask, mars_app.py
    mars_data = {}

    #scrapping latest news about mars from nasa
    mars_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(mars_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # getting the latest title and text
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    ## insert the outcome to the dic
    mars_data [ "mars_news"] = {"title": news_title , "paragraph" : news_p}

    #### get image url of JPL
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    jpg = soup.find('a', class_="button fancybox")['data-fancybox-href']
    featured_image_url = urljoin(jpl_url, jpg)

    ## insert the outcome to the dic
    mars_data [ "jpl_img" ] = featured_image_url

     # #### Mars Weathe
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    p_weather = soup.find_all('p', class_="tweet-text")
    mars_weather = p_weather[1].text

    ## insert the outcome to the dic
    mars_data ["mars_weather"] = mars_weather

    # #### Mars Facts
    mars_fact = "https://space-facts.com/mars/"
    browser.visit(mars_fact)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    tables = pd.read_html(mars_fact)
    tables

    type(tables)
    df = tables[0]
    #df.columns = [" ","Value"]
    mars_facts_df = df
    mars_facts_df.columns = ["description", "Value"]
    mars_facts_htmltable = mars_facts_df.to_html(index= False)
    mars_facts_htmltable.replace("\n", "")

    ## insert the outcome to the dic
    mars_data ["mars_facts"] = mars_facts_htmltable



    #### Mars Hemispheres

    hemispher_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispher_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    results = soup.find_all("div" , class_="description")

    hemisphere_image_urls = []


    for result in results:
        # Error handling
        try:
            hemisphere_image_url = {}
            ## Identify and return titles of the imgs
            title = result.find("h3").text
            print(title)

            ## click on the title in h3 to go to the img_url
            browser.click_link_by_partial_text(title)
            #time.sleep(3)

            ## run the soup code in the 2nd pag
            html = browser.html 
            soup_img = BeautifulSoup(html, "html.parser")
            img_link = soup_img.find("div" , class_="downloads")
        # img_url = soup_img.find("a" , text = "sample")

            # selecting the href
            img_url = img_link.a["href"]
            #print(img_url["href"])

            ## append all the img title and ur in a dic
            #hemisphere_image_url['title'] = title
            #hemisphere_image_url["img_url"] = img_url
            hemisphere_image_url={"title":title,"img_url":img_url}

            ## insert the dic in a list
            hemisphere_image_urls.append(hemisphere_image_url)
            browser.back()
            print("end")


            
        except AttributeError as e:
            print(e)

    #print(hemisphere_image_urls)

    ## insert the outcome to the dic

    mars_data ["hemisphere"] = hemisphere_image_urls

    return mars_data

