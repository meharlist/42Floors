"""
Page object model for the office space page
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from Page import Page


class Office_Space_Page(Page):
    "Page object for the Office Space page"
    
    def start(self):
        self.url = "office-space"
        self.open(self.url) 
        # Assert Title of the Office Space Page
        self.assertIn("Office Space", self.driver.title)      

        "Xpath of all the field"
        self.size_link = "//span[@class='field-label'][text()='Size']"
        self.minsize_input ="//input[@placeholder='Min sqft']"
        self.maxsize_input = "//input[@placeholder='Max sqft']"
        self.search_button = "//div[@class='field-search']/descendant::button[@type='submit']"
        self.search_result = "//div[@class='results-count']"

    def filter_by_size(self,min_sqft,max_sqft,expected_result):
        #Search as per the given min and max size
        self.click_element(self.size_link)
        self.set_text(self.minsize_input,min_sqft)
        self.set_text(self.maxsize_input,max_sqft)
        self.click_element(self.search_button)

        return self.verify_result(expected_result)  
        

    def verify_result(self,expected_result):
        #Verifies the actual result with the expected result for the filter
        actual_num_results = self.get_text(self.search_result)
        actual_num_results = actual_num_results.split("office spaces")[0]
        actual_num_results = actual_num_results.strip()

        if int(expected_result) == int(actual_num_results):
            return True
        else:
            self.write("OBTAINED result for number of office spaces: " + actual_num_results)
            return False
        
    
