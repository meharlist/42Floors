"""
Page object model for the home page
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from Page import Page


class Home_Page(Page):
    "Page object for the Home page"
    
    def start(self):
        self.url = ""
        self.open(self.url) 
        # Assert Title of the Home Page
        self.assertIn("Office Space Listings - Commercial Real Estate", self.driver.title)      

        "Xpath of all the field"
        self.choose_market_dropdown = "//span[text()='Market']"
        self.select_city_name = "//ul[@class='markets-dropdown dropdown-menu']/descendant::a[contains(text(),'%s')]"
        #self.selected_market = "//a[@class='dropdown-toggle market']/text()[2]"
        self.selected_market = "//a[@class='dropdown-toggle market']"

    def choose_market(self,city_name):
        "Choose the given city from the drop down list"
        #San Francisco Office Space | 42Floors
        self.click_element(self.choose_market_dropdown)
        self.wait(2)
        self.click_element(self.select_city_name%city_name)
        self.wait(2)
        return self.verify_selected_market(city_name)


    def verify_selected_market(self,city_name):
        if city_name in self.get_text(self.selected_market):
            return True
        else:
            return False        


