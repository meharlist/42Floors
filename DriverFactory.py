"""
DriverFactory class
NOTE: Change this class as you add support for:
1. SauceLabs/BrowserStack
2. More browsers like Opera
"""
import dotenv,os
from selenium import webdriver

class DriverFactory():
    
    def __init__(self,browser='ff',sauce_flag='N',browser_version=None,platform=None):
        self.browser=browser
        self.sauce_flag=sauce_flag
        self.browser_version=browser_version
        self.platform=platform
        
        
    def get_web_driver(self,browser,sauce_flag,browser_version,platform):
        if (sauce_flag == 'Y'):
            web_driver = self.run_sauce(browser,sauce_flag,browser_version,platform)             
                            
        elif (sauce_flag == 'N'):
            web_driver = self.run_local(browser,sauce_flag,browser_version,platform)
        
        else:
            print "DriverFactory does not know the browser: ",browser
            web_driver = None
        return web_driver     
    

    def run_sauce(self,browser,sauce_flag,browser_version,platform):
        " Run the test in Sauce Labs is sauce flag is 'Y'"
        # Get the sauce labs credentials from sauce.credentials file
        PY_SCRIPTS_PATH=os.path.dirname(__file__)
        dotenv.load_dotenv(os.path.join(PY_SCRIPTS_PATH,"sauce.credentials"))
        USERNAME = os.environ['sauce_username']
        PASSWORD = os.environ['sauce_key']
        if browser.lower() == 'ff' or browser.lower() == 'firefox':
            desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
            desired_capabilities['version'] = browser_version
            desired_capabilities['platform'] = platform
        elif browser.lower() == 'ie':
            desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER
            desired_capabilities['version'] = browser_version
            desired_capabilities['platform'] = platform
        elif browser.lower() == 'chrome':
            desired_capabilities = webdriver.DesiredCapabilities.CHROME
            desired_capabilities['version'] = browser_version
            desired_capabilities['platform'] = platform
        desired_capabilities['name'] = 'Testing End to END Basecamp Test'
        return webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor="http://%s:%s@ondemand.saucelabs.com:80/wd/hub"%(USERNAME,PASSWORD)
        )

    def run_local(self,browser,sauce_flag,browser_version,platform):
        if self.browser.lower() == "ff" or self.browser.lower() == 'firefox':
            return webdriver.Firefox()    
        elif  self.browser.lower() == "ie":
            return webdriver.Ie()
        elif self.browser.lower() == "chrome":
            return webdriver.Chrome()
