"""
Page object model for the listing page
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from Page import Page


class Listing_Page(Page):
    "Page object for the Listing page"
    
    def start(self):
        self.url = ""
        #self.open(self.url) 
        # Assert Title of the Home Page
        #self.assertIn("Office Space Listings - Commercial Real Estate", self.driver.title)      

        "Xpath of all the field"
        self.listing_header = "//div[@class='property-header']/descendant::h1[@itemprop='name']"

    def get_listing_header(self):
        return self.get_text(self.listing_header)

    def verify_listing_name(self,listing_name):
        if (listing_name == self.get_listing_header()):
            return True
        else:
            return False
