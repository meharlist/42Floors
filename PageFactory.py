"""
PageFactory uses the factory design pattern. 
get_page_object() returns the appropriate page object.
Add elif clauses as and when you implement new pages.
Pages implemented so far:
1. Home
2. Office Space
3. Co working
4. Listing

"""
from selenium import webdriver
from Home_Page import Home_Page
from Office_Space_Page import Office_Space_Page
from Coworking_Page import Coworking_Page
from Listing_Page import Listing_Page


def get_page_object(page_name,driver,base_url='https://42floors.com/'):
    "Return the appropriate page object based on page_name"
    test_obj = None
    page_name = page_name.lower()
    if page_name == "home":
        test_obj = Home_Page(driver,base_url=base_url)
    elif page_name == "office-space":
        test_obj = Office_Space_Page(driver,base_url=base_url)
    elif page_name == "coworking":
        test_obj = Coworking_Page(driver,base_url=base_url)
    elif page_name == "listing":
        test_obj = Listing_Page(driver,base_url=base_url)
    
    
    return test_obj
