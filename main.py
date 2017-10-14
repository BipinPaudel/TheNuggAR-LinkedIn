from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import json

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

browser = webdriver.Chrome()



def connect_with_spreadsheet(clientsecrets, store, scopes=('https://www.googleapis.com/auth/spreadsheets')):
    """
    :param store:
    :param clientsecrets:
    :param scopes:
    :return:
    """
    credz = store.get()
    if not credz or credz.invalid:
        flow = client.flow_from_clientsecrets(clientsecrets, scopes)
        credz = tools.run_flow(flow, store)
    return discovery.build('sheets', 'v4', http=credz.authorize(Http()))


def write_row_to_spreadsheet(SHEETS, sheet_ID, rows, range, valueInputOption="RAW"):
    """
    :param rows:
    :return:
    """
    body = {
        'values': rows
    }
    result = SHEETS.spreadsheets().values().update(
    spreadsheetId=sheet_ID, range=range,
    valueInputOption=valueInputOption, body=body).execute()



def navigate_next_page():
    """
    :return:
    """
    try:
        next_button = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "next"))
        )
    except:
        print("No more pages to traverse.")
        sys.exit()
    next_button.click()



def get_first_degree_email(individual_url):
    """
    :param individual_url:
    :return:
    """
    browser.get(individual_url)
    try:
        contact_details_btn = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "contact-see-more-less"))
        )
    except:
        print("Although 1st degree connection, email not available for %s", individual_url)
        return ""

    contact_details_btn.click()
    try:
        profile_personal_section = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pv-profile-section__section-info"))
        )
    except:
        print("Can't find personal info section")
        return ""

    email_section = profile_personal_section.find_element_by_class_name("ci-email")
    email_addr = email_section.find_element_by_tag_name("a").text
    return email_addr


def get_personal_info(individual):
    """
    :param individual:
    :return:
    """
    profile_url = individual.find_element_by_tag_name("a").get_attribute("href")
    individual_name = individual.find_element_by_class_name("actor-name").text
    job_title = individual.find_element_by_class_name("subline-level-1").text
    connection_distance = individual.find_element_by_class_name("dist-value").text
    if connection_distance is not "1st":
        return "", individual_name, profile_url, job_title

    return get_first_degree_email(profile_url), individual_name, profile_url, job_title


def url_constructor(base_url='https://linkedin.com/search/results/people/?origin=GLOBAL_SEARCH_HEADER', **kwargs):
    """
    :param base_url:
    :param kwargs:
    :return:
    """
    for key, value in kwargs.iteritems():
        base_url += "&" + key + "=" + value
    return base_url



def search_by_filter(url):
    """
    :param kwargs:
    :return:
    """
    browser.get(url)
    try:
        search_result_ul = WebDriverWait(browser, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "results-list"))
        )
    except:
        print("Could not get results for the given search filters.")
        sys.exit()

    results_details = [get_personal_info(people) for people in search_result_ul.find_elements_by_tag_name('li')]


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

    search_by_filter(url_constructor(facetNetwork='["F"%2C"S"%2C"O"]', keywords='data miner%2Cscientist', company='facebook', facetNonprofitInterest='["volunteer"%2C"nonprofitboard"]'))


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


"""
Updating rows to spreadsheet.
values = [
    [
        # Cell values ...
    ],
    # Additional rows ...
]
body = {
  'values': values
}



result = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_name,
    valueInputOption=value_input_option, body=body).execute()

"""
