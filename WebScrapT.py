
# import these two modules bs4 for selecting HTML tags easily
from bs4 import BeautifulSoup
import requests
# requests module is easy to operate some people use urllib but I prefer this one because it is easy to use.
from urllib.request import urlopen as uReq


# ## scrap data from wikipedia
print("------------------------------------------------------------------------------------")
print("WEB SCRAPING EXAMPLE 1: SCRAPE WIKIPEDIA LINK WITH ITS TITLE AND TABLE CONTENTS")
print("------------------------------------------------------------------------------------")
wiki = requests.get(
    "https://en.wikipedia.org/wiki/Charotar_University_of_Science_and_Technology")
soup = BeautifulSoup(wiki.text, 'html')
print(soup.find('title'))


# ### find html tags with classes
print("This is a demo to show the desired formatted data of CHARUSAT University")
print("-----------------------------------------------------------------------------")
unicontents = soup.find_all("div", class_='toc')
for i in unicontents:
    print(i.text)


overview = soup.find_all('table', class_='infobox vevent')
for z in overview:
    print(z.text)

print("------------------------------------------------------------------------------------")

# To scrape user specific wikipedia link
urld = input(
    "Enter a wikipedia link of your choice to scrape its data in a similiar manner:")

wiki1 = requests.get(urld)
soup1 = BeautifulSoup(wiki1.text, 'html')
print(soup1.find('title'))

unicontentss = soup1.find_all("div", class_='toc')
for i in unicontentss:
    print(i.text)


overviews = soup1.find_all('table', class_='infobox vevent')
for z in overviews:
    print(z.text)

print("-----------------------------------------------------------------------------------------------------------------------")

print("WEB SCRAPING EXAMPLE 2: SCRAPE PRODUCTS LIST OF A WEBSITE WITH THEIR PRICES AND SHIPPING RATES AND STORE IT INTO A EXCEL FILE IN .CSV FORMAT")
print("------------------------------------------------------------------------------------------------------------------------")
# URl to web scrap from.
# scraping graphics cards from Newegg.com
page_url = "http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&N=-1&IsNodeId=1&Description=GTX&bop=And&Page=1&PageSize=36&order=BESTMATCH"

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = BeautifulSoup(uClient.read(), "html.parser")
uClient.close()

# finds each product from the store page
containers = page_soup.findAll("div", {"class": "item-container"})

# name the output file to write to local disk
out_filename = "graphics_cards.csv"
# header of csv file to be written
headers = "brand,product_name,shipping \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

# loops over each product and grabs attributes about
# each product
for container in containers:
    # Finds all link tags "a" from within the first div.
    make_rating_sp = container.div.select("a")

    # Grabs the title from the image title attribute
    # Then does proper casing using .title()
    brand = make_rating_sp[0].img["title"].title()

    # Grabs the text within the second "(a)" tag from within
    # the list of queries.
    product_name = container.div.select("a")[2].text

    # Grabs the product shipping information by searching
    # all lists with the class "price-ship".
    # Then cleans the text of white space with strip()
    # Cleans the strip of "Shipping $" if it exists to just get number
    shipping = container.findAll(
        "li", {"class": "price-ship"})[0].text.strip().replace("$", "").replace(" Shipping", "")

    # prints the dataset to console
    print("brand: " + brand + "\n")
    print("product_name: " + product_name + "\n")
    print("shipping: " + shipping + "\n")

    # writes the dataset to file
    f.write(brand + ", " + product_name.replace(",", "|") + ", " + shipping + "\n")

f.close()  # Close the file
