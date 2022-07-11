import pdb
import time
import urllib

from .formatting import *

from seleniumwire import webdriver
# from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from webdriver_manager.chrome import ChromeDriverManager

def login_to_newrelic(email, username, password, staging=False):

    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome()

    # login
    login_url = "https://login.newrelic.com/login" if not staging else "https://staging-login.newrelic.com/login"
    driver.get(login_url)

    if email:
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "form#login > input"))
            )
            email_input[0].send_keys(email)
            
            time.sleep(1)

            submit_button = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "form#login > button"))
            )
            submit_button[0].click()

            if username:
                username_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#okta-signin-username"))
                )
                username_input[0].send_keys(username)
                time.sleep(1)

                password_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#okta-signin-password"))
                )
                password_input[0].send_keys(password)
                time.sleep(1)

                submit_login_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#okta-signin-submit"))
                )
                submit_login_button[0].click()

        except Exception as  e:
            print_warning('Could not auto-complete login info.\n{}'.format(e))
            pass


    try:
        print('waiting for login...')
        # Wait until user is logged in (we use the Projects text to be indicative of a successful login)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "APM")))
    except:
        print_error('Did not login in time. Please restart script.')
        raise Exception('Did not login in time. Script exiting.')

    print('Logged in!')

    return driver

def wait_for_page_load(driver, max_wait):
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".query-builder-search"))
        )
    except Exception as e:
        print_error('Could not find query box.\n{}'.format(e))
        return False
    return True

def click_run_query_button(driver, max_wait):
    try:
        json_widgets = WebDriverWait(driver, max_wait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".execute-button"))
        )
        json_widgets[0].click()
        time.sleep(3)
    except Exception as e:
        print_error('Could not click json widget.\n{}'.format(e))
        return False
    return True



def set_to_product_visibility(driver, max_wait):
    try:

        # pdb.set_trace()
        visibility_el = WebDriverWait(driver, max_wait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".toolbar-button[title=\'Schema visibility mode\']"))
        )
        visibility_el[0].click()
        time.sleep(2)
        product_vis_el = WebDriverWait(driver, max_wait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[title='The product-facing schema']"))
        )
        product_vis_el[0].click()
        time.sleep(3)
        
    except Exception as e:
        print_error('Error setting visibility to product: \nError: {}'.format(e))

def get_query_response_from_driver_requests(driver_requests):
    response_bodies = []
    # cookie = ''
    for request in driver_requests:
        if request.response:
            # NOTE: It is possible that you create a graphql request that doesn't produce data
            #       in which case, you would remove this second condition
            try:
                body = request.response.body.decode("utf-8")
                if 'graphql' in request.path and 'data' in body and 'VisibleAccountFilter' not in body and 'mutation' not in body:
                    # cookie = request.headers.get('Cookie')
                    response_bodies.append(body)
            except Exception as e:
                print_warning("Could not decode response body in response list:\n{}".format(e))

    # print('cookie = {}'.format(cookie))
    # pdb.set_trace()
    if len(response_bodies):
        return (response_bodies[0], True)
    else:
        return (None, None, False)

def wait_for_query_to_load(driver, max_wait):
    WebDriverWait(driver, max_wait).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cm-s-graphiql"))
    )

def scrape_query_for_account(driver, change_visibility, id_, query, max_wait, staging=False):
    success = False
    try:
        query = query.replace("{{ID}}", id_)
        query_string = urllib.parse.urlencode({'query': query})
        url_base = 'https://api.newrelic.com/graphiql?#' if not staging else 'https://staging-api.newrelic.com/graphiql?#'
        url =  '{}{}'.format(url_base, query_string)
        # pdb.set_trace()
        driver.get(url)
        driver.refresh()
        response_json = ''

        wait_for_page_load(driver, max_wait)
        if change_visibility:
            set_to_product_visibility(driver, max_wait)
        prev_driver_requests = len(driver.requests)
        if not click_run_query_button(driver, max_wait):
            print('RETRYING Once')
            time.sleep(2)
            prev_driver_requests = len(driver.requests)
            click_run_query(driver, max_wait)
        wait_for_query_to_load(driver, 8)

        if len(driver.requests) > prev_driver_requests:
            response_json,  success = get_query_response_from_driver_requests(driver.requests[prev_driver_requests:])

        # r = scrape_query_for_account_with_cookie(query, cookie)
        # response_json, success = parse_response_panel(driver, max_wait)
        if not success:
            print_error('Could not parse json widget response. The analysis will fail for this key!\n')
        return response_json, True
    except Exception as e:
        print_error('Error parsing query response for account: {}. Details: {}'.format(id_, e))
    return ({}, success)