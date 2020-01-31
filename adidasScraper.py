'''
    adidasScraper.py 
    Created By: Ryan Dunton
    September 27, 2016
'''

from bs4 import BeautifulSoup
from urllib2 import urlopen, Request
import ssl
import csv
import re

# Beginning URL
BASE_URL = "http://www.adidas.com/us/men-shoes"

# Lists of product titles and prices
productTitles = []
productPrices = []


def getPageInformation(url):
    '''
    Function to grab all the information with classes of title and salesprice
    '''
    # hdr added to verify to webpage we are not an unknown browser
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    response = page.read()

    # Create nested HTMl object to search through
    soup = BeautifulSoup(response, "html.parser")

    # Grab all titles and prices
    allTitles = soup.find_all(class_="title")
    allPrices = soup.find_all(class_="salesprice")

    # Iterate through allTitles. Clean up the formatting and add it to productTitles
    for i in allTitles:
        i = str(i)
        i = i.replace('<span class="title">', '')
        i = i.replace('</span>', '')
        productTitles.append(i)

    # Iterate through allPrices. Clean up formatting and add it to productPrices
    for i in allPrices:
        i = str(i)
        i = i.split('\t')
        del i[:6]
        del i[1:]
        i = ''.join(i)
        i = str(i)
        i = i.replace('\r', '')
        i = i.replace('\n', '')
        i = i.strip()
        productPrices.append(i)


def prepareLink(url):
    '''
    Function to find link in current webpage
    '''
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    page = urlopen(req)
    response = page.read()
    soup = BeautifulSoup(response, "html.parser")
    pageLink = soup.find(class_="right-arrow")
    return pageLink


def extractPageLink(nextPageLink):
    '''
    Function to extract link to next page in the webpage
    '''
    nextPageLink = str(nextPageLink)
    nextPageLink = nextPageLink.split(' ')
    # This checks to determine if this is the final page or not
    if len(nextPageLink) < 5:
        return False
    else:
        # There was a lot of formatting to do here. There is an 'unwrap' function and
        # possible RegEx techiques available, however there were some issues getting either
        # to work completely.
        del nextPageLink[:5]
        nextPageLink = ''.join(nextPageLink)
        nextPageLink = nextPageLink.replace('</a>', '')
        nextPageLink = nextPageLink.replace('</li>', '')
        extPageLink = nextPageLink.replace('\n', '')
        nextPageLink = nextPageLink.replace('>', '')
        nextPageLink = nextPageLink.replace('href=', '')
        nextPageLink = nextPageLink.replace('amp;', '')
        nextPageLink = nextPageLink.replace('"', '')
        nextPageLink = nextPageLink.strip()
        return nextPageLink


def webScraper(url):
    '''
    Function to scrape data from webpage and print it to console
    '''
    getPageInformation(url)
    print "Page 1 Done"
    # print len(productTitles)
    i = 1
    while True:
        # Check if this is the last page on the webpage list
        if not extractPageLink(prepareLink(url)):
             print "Scrape finished"
             break
        # Scrape from next page
        if extractPageLink(prepareLink(url)):
            i += 1
            getPageInformation(extractPageLink(prepareLink(url)))
            print "Page %s Done" % i
        # Set url for next page as url
        url = extractPageLink(prepareLink(url))
        # print len(productTitles)

    # Blank line for formatting
    print ""

    # Print item and price from productTitles and productPrices
    for x in xrange(len(productTitles)):
        print "Item: " + productTitles[x] + " | " + "Price: $" + productPrices[x]

# Call webScraper on BASE_URL
webScraper(BASE_URL)
            