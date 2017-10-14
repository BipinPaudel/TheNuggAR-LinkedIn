from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

browser = webdriver.Chrome()


def connect_with_spreadsheet(credentials):
    pass


def write_row_to_spreadsheet(row):
    pass


def get_personal_info(individual):
    pass


def url_constructor(base_url='https://linkedin.com/search/results/people/?origin=GLOBAL_SEARCH_HEADER', **kwargs):
    """
    :param base_url:
    :param kwargs:
    :return:
    """
    for key, value in kwargs.iteritems():
        base_url += "&" + key + "=" + value
    return base_url



def search_by_filter(**kwargs):
    """
    :type filters: object
    :param filters:
    :return:
    """
    pass


def linkedin_login(username, password):
    """
    :param username:
    :param password:
    :return: bool
    """
    browser.get("https://linkedin.com")
    try:
        email_field = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.ID, "login-email"))
        )
    except:
        print("The login page did not load correctly.")
        return False
    password_field = browser.find_element_by_id("login-password")
    email_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    return True


def main():
    if len(sys.argv) != 3:
        print("Please pass username and password as arguments through command line.")
        sys.exit()

    if not linkedin_login(sys.argv[1], sys.argv[2]):
        sys.exit()

    search_by_filter()


if __name__ == '__main__':
    # print(url_constructor(facetNetwork='["F"%2C"S"%2C"O"]', keywords='data miner%2Cscientist', company='facebook', facetNonprofitInterest='["volunteer"%2C"nonprofitboard"]'))
    # sys.exit()
    main()

"""
Possible filters on search
connections: facetNetwork=["F"] , facetNetwork=["F"%2C"S"], facetNetwork=["F"%2C"S"%2C"O"]
Keywords: firstName=Bhishan , lastName=Bhandari, keywords=data miner%2Cscientist, company=facebook, school=Deerwalk Institute of Technology, title=Data Miner%2CSoftware Engineer
Connections of : facetConnectionOf=['sometoken']
Non profit interests: facetNonprofitInterest=["volunteer"%2C"nonprofitboard"]
Origin : origin=GLOBAL_SEARCH_HEADER
https://www.linkedin.com/search/results/people/?company=Facebook&facetNetwork=%5B%22F%22%2C%22S%22%2C%22O%22%5D&firstName=&keywords=data%20miner&lastName=Bhandari&origin=FACETED_SEARCH&title=Data%20miner
"""
