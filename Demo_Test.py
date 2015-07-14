"""
Test case for 42floors functionality.

Our automated test will do the following:
    #1.Choose the market
    #2.Filter by size on office space page
    #3.Open a listing on coworking page
"""
import os,PageFactory,Test_Rail,Conf_Reader
from optparse import OptionParser
from DriverFactory import DriverFactory

def check_file_exists(file_path):
    #Check if the config file exists and is a file
    conf_flag = True
    if os.path.exists(file_path):
        if not os.path.isfile(file_path):
            print '\n****'
            print 'Config file provided is not a file: '
            print file_path
            print '****'
            conf_flag = False
    else:
        print '\n****'
        print 'Unable to locate the provided config file: '
        print file_path
        print '****'
        conf_flag = False

    return conf_flag


def check_options(options):
    "Check if the command line options are valid"
    options.config_file = os.path.abspath(options.config_file)
    return check_file_exists(options.config_file)


def run_demo_test(browser,conf,tconf,base_url,test_run_id=None,sauce_flag=None,browser_version=None,platform=None):
    "Demo Test Run"
       
    #Setup a driver
    driver_obj = DriverFactory()
    driver = driver_obj.get_web_driver(browser,sauce_flag,browser_version,platform)
    driver.implicitly_wait(10) # Some elements are taking long to load
    driver.maximize_window()

    #Result flag which will check if testrail.conf is present
    tconf_flag = check_file_exists(tconf)

    #Result flag used by TestRail
    result_flag = False
    
    #1. Create a home page object and choose Market
    #Create a login page object
    home_obj = PageFactory.get_page_object("home",driver)
    city_name = Conf_Reader.get_value(conf,'CITY_NAME')
    result_flag = home_obj.choose_market(city_name)
    if (result_flag):
        msg = "Market was set to %s"%city_name
    else:
        msg = "Could not set market to  %s"%city_name
    home_obj.write(msg)
    
    #Update TestRail
    #Get the case id from tesrail.conf file
    if tconf_flag:
        case_id = Conf_Reader.get_value(tconf,'CHOOSE_MARKET')
        Test_Rail.update_testrail(case_id,test_run_id,result_flag,msg=msg)


    #2. Filter by size on office space page
    #Create project space page object
    office_space_obj = PageFactory.get_page_object("office-space",driver)
    min_sqft = Conf_Reader.get_value(conf,'MIN_SQFT')
    max_sqft = Conf_Reader.get_value(conf,'MAX_SQFT')
    expected_result =Conf_Reader.get_value(conf,'EXPECTED_RESULT_FOR_SIZE')
    result_flag = office_space_obj.filter_by_size(min_sqft,max_sqft,expected_result)
    if (result_flag):
        msg = "Search results for filter by size matched the expected result of %s space(s)"%expected_result
    else:
        msg = "Actual result did not match the expected result %s space"%expected_result
    office_space_obj.write(msg)
    
    #Update TestRail
    #Get the case id from tesrail.conf file
    if tconf_flag:
        case_id = Conf_Reader.get_value(tconf,'OFFICESPACE_FILTER_SIZE')
        Test_Rail.update_testrail(case_id,test_run_id,result_flag,msg=msg) 
    

    #3.Open a listing on co-working page
    #Create co-working page object
    coworking_obj = PageFactory.get_page_object("coworking",driver)
    listing_name = Conf_Reader.get_value(conf,'LISTING_NAME_20MISSION')
    listing_href = Conf_Reader.get_value(conf,'LISTING_HREF_20MISSION')
    
    result_flag1 = coworking_obj.verify_listing(listing_name,listing_href)

    if result_flag1:
        result_flag2 = coworking_obj.click_listing(listing_href)
        if result_flag2:
            listing_obj = PageFactory.get_page_object("listing",driver)
            result_flag = listing_obj.verify_listing_name(listing_name)
    if (result_flag):
        msg = "Listing matched for %s"%listing_name
    else:
        msg = "Listing did not match or '0' coworking spaces"
    coworking_obj.write(msg)
    
    #Update TestRail
    #Get the case id from tesrail.conf file
    if tconf_flag:
        case_id = Conf_Reader.get_value(tconf,'COWORKING_LISTING')
        Test_Rail.update_testrail(case_id,test_run_id,result_flag,msg=msg)
          

    #Teardown
    home_obj.wait(3)
    home_obj.teardown() #You can use any page object to teardown  
    
#---START OF SCRIPT
if __name__=='__main__':
    print "Script start"
    #This script takes an optional command line argument for the TestRail run id
    usage = "\n----\n%prog -b <OPTIONAL: Browser> -c <OPTIONAL: configuration_file> -u <OPTIONAL: APP URL> -r <Test Run Id> -t <OPTIONAL: testrail_configuration_file> -s <OPTIONAL: sauce flag>\n----\nE.g.: %prog -b FF -c .conf -u https://app.fiscalnote.com -r 2 -t testrail.conf -s Y\n---"
    parser = OptionParser(usage=usage)

    parser.add_option("-b","--browser",
                      dest="browser",
                      default="firefox",
                      help="Browser. Valid options are firefox, ie and chrome")                      
    parser.add_option("-c","--config",
                      dest="config_file",
                      default=os.path.join(os.path.dirname(__file__),'data.conf'),
                      help="The full or relative path of the test configuration file")
    parser.add_option("-u","--app_url",
                      dest="url",
                      default="https://42floors.com/",
                      help="The url of the application")
    parser.add_option("-r","--test_run_id",
                      dest="test_run_id",
                      default=None,
                      help="The test run id in TestRail")
    parser.add_option("-s","--sauce_flag",
                      dest="sauce_flag",
                      default="N",
                      help="Run the test in Sauce labs: Y or N")
    parser.add_option("-v","--version",
                      dest="browser_version",
                      help="The version of the browser: a whole number",
                      default=None)
    parser.add_option("-p","--platform",
                      dest="platform",
                      help="The operating system: Windows 7, Linux",
                      default="Windows 7")
    parser.add_option("-t","--testrail_caseid",
                      dest="testrail_config_file",
                      default=os.path.join(os.path.dirname(__file__),'testrail.conf'),
                      help="The full or relative path of the testrail configuration file")
    
    (options,args) = parser.parse_args()
    if check_options(options): 
        #Run the test only if the options provided are valid
        run_demo_test(browser=options.browser,
                    conf=os.path.abspath(options.config_file),
                    base_url=options.url,
                    test_run_id=options.test_run_id,
                    sauce_flag=options.sauce_flag,
                    browser_version=options.browser_version,
                    platform=options.platform,
                    tconf=os.path.abspath(options.testrail_config_file))
    else:
        print 'ERROR: Received incorrect input arguments'
        print parser.print_usage()
