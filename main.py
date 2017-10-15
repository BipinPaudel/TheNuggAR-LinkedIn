from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import sys
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

browser = webdriver.Chrome()
browser.maximize_window()
sheet_range = 1


def connect_with_spreadsheet(clientsecrets, store, scopes=('https://www.googleapis.com/auth/spreadsheets',)):
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


def write_row_to_spreadsheet(sheets, sheet_id, rows, spreadsheet_range, value_input_option="RAW"):
    """
    :param sheets:
    :param sheet_id:
    :param rows:
    :param spreadsheet_range:
    :param value_input_option:
    :return:
    """
    body = {
        'values': rows
    }
    result = sheets.spreadsheets().values().update(
        spreadsheetId=sheet_id, range=spreadsheet_range,
        valueInputOption=value_input_option, body=body).execute()
    print(result)


def navigate_next_page():
    """
    :return:
    """
    try:
        next_button = WebDriverWait(browser, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, "next"))
        )
    except TimeoutException:
        print("No more pages to traverse.")
        sys.exit()
    next_button.click()
    time.sleep(2)


def get_first_degree_email(individual_url):
    """
    :param individual_url:
    :return:
    """
    js_cmd = 'window.open("' + individual_url + '", "_blank");'
    browser.execute_script(js_cmd)
    browser.switch_to.window(browser.window_handles[-1])
    try:
        contact_details_btn = WebDriverWait(browser, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, "contact-see-more-less"))
        )
    except TimeoutException:
        print("Although 1st degree connection, email not available for %s", individual_url)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return ""

    contact_details_btn.click()
    try:
        profile_personal_section = WebDriverWait(browser, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, "pv-profile-section__section-info"))
        )
    except TimeoutException:
        print("Can't find personal info section")
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return ""

    email_addr = profile_personal_section.find_elements_by_xpath('//a[contains(@href, "mailto:")]')
    email_addr = email_addr[-1].text
    print(email_addr)
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    return email_addr


def get_personal_info(individual):
    """
    :param individual:
    :return:
    """
    individual_name = individual.find_element_by_class_name("actor-name").text
    job_title = individual.find_element_by_class_name("subline-level-1").text
    profile_url = individual.find_element_by_tag_name("a").get_attribute("href")
    connection_distance = individual.find_element_by_class_name("dist-value").text

    print(individual_name)
    print(connection_distance)
    if connection_distance != "1st":
        return "", individual_name, profile_url, job_title

    return [get_first_degree_email(profile_url), individual_name, profile_url, job_title]


def url_constructor(base_url='https://linkedin.com/search/results/people/?origin=GLOBAL_SEARCH_HEADER', **kwargs):
    """
    :param base_url:
    :param kwargs:
    :return:
    """
    for key, value in kwargs.iteritems():
        base_url += "&" + key + "=" + value
    return base_url


def search_by_filter(sheets):
    """
    :param sheets:
    :return:
    """
    global sheet_range
    try:
        search_result_ul = WebDriverWait(browser, 15).until(
            ec.presence_of_element_located((By.CLASS_NAME, "results-list"))
        )
    except TimeoutException:
        print("Could not get results for the given search filters.")
        sys.exit()

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    results_details = [get_personal_info(people) for people in search_result_ul.find_elements_by_tag_name('li')]
    write_row_to_spreadsheet(sheets, '1_BQBY9sinWoUD1LXaYMP7rsOIr2zDgG7bUfsczYU140', results_details, 'A' + str(sheet_range))
    sheet_range += len(results_details)


def linkedin_login(username, password):
    """
    :param username:
    :param password:
    :return: bool
    """
    browser.get("https://linkedin.com")
    try:
        email_field = WebDriverWait(browser, 15).until(
            ec.presence_of_element_located((By.ID, "login-email"))
        )
    except TimeoutException:
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
    print(sys.argv[1])
    print(sys.argv[2])

    if not linkedin_login(sys.argv[1], sys.argv[2]):
        sys.exit()

    # browser.get(url_constructor(facetNetwork='["F"%2C"S"%2C"O"]', keywords='data miner%2Cscientist', company='facebook',
    #                             facetNonprofitInterest='["volunteer"%2C"nonprofitboard"]'))
    browser.get(url_constructor(facetNetwork='["F"%2C"S"%2C"O"]', keywords='meditation',
                                facetNonprofitInterest='["volunteer"%2C"nonprofitboard"]'))
    sheets = connect_with_spreadsheet(
        "client_secret_391502371883-ucq6afoq80m5h6gj3k9mur3ankfa5go6.apps.googleusercontent.com.json",
        file.Storage('storage.json'))
    while True:
        search_by_filter(sheets)
        navigate_next_page()

        # search_by_filter(url_constructor(facetNetwork='["F"%2C"S"%2C"O"]', keywords='data miner%2Cscientist', company='facebook', facetNonprofitInterest='["volunteer"%2C"nonprofitboard"]'))


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
