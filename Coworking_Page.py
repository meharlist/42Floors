"""
Page object model for the coworking page
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from Page import Page


class Coworking_Page(Page):
    "Page object for the Office Space page"
    
    def start(self):
        self.url = "coworking"
        self.open(self.url) 
        # Assert Title of the Office Space Page
        self.assertIn("Coworking Spaces", self.driver.title)
        
        "Xpath of all the field"
        self.search_result = "//div[@class='results-count']"
        self.listing_href = "//a[@href='%s']/descendant::div[@class='name']"

        #Verify if there are coworking spaces available
        if '0 coworking spaces' in self.get_text(self.search_result):
            self.write(self.get_text(self.search_result))
            self.coworking_available = False
        else:
            self.coworking_available = True
    

    def verify_listing(self,listing_name,listing_href):
        "Verify the listing on a the co-working page"
        if self.coworking_available :
            if listing_name in self.get_text(self.listing_href%listing_href):
                self.write("Listing name matches with the listing href")
                return True
            else:
                self.write("Listing name does not matches with the listing href")
                return False
        else:
            self.write("No coworking listing available")
            return False
        

    def click_listing(self,listing_href):
        return self.click_element(self.listing_href%listing_href)
        
        
        
    
