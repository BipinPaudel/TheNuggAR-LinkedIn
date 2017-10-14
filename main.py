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

def search_by_filter(filters):
    """
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
    


def main():
    if len(sys.argv) != 3:
        print("Please pass username and password as arguments through command line.")
        sys.exit()

    if not linkedin_login(sys.argv[1], sys.argv[2]):
        sys.exit()

    search_by_filter()

if __name__ == '__main__':
    main()
