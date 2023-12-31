#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import datetime

URL_LOGIN = 'https://www.saucedemo.com/'
URL_INVENTORY = 'https://www.saucedemo.com/inventory.html'
URL_CART = 'https://www.saucedemo.com/cart.html'

def log_status(text):
    """log_status log status including timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {text}")

def login(driver, user, password):
    """Login to the website"""
    log_status('Navigating to the demo page to login.')
    driver.get(URL_LOGIN)
    driver.find_element("id", "user-name").send_keys(user)
    #driver.find_element_by_id("user-name").send_keys(user)
    driver.find_element("id", "password").send_keys(password)
    #driver.find_element_by_id("password").send_keys(password)
    driver.find_element("id", "login-button").click()
    #driver.find_element_by_id("login-button").click()
    assert URL_INVENTORY in driver.current_url
    log_status(f"Login with username {user} and password {password} successful")


def add_items(driver):
    """Add items to the cart"""
    cart = []
    log_status('Add all items to the cart')
    items = driver.find_elements(By.CLASS_NAME,"inventory_item")
    for item in items:
        item_name = item.find_element(By.CLASS_NAME,"inventory_item_name").text
        cart.append(item_name)
        item.find_element(By.CLASS_NAME,"btn_inventory").click()
        log_status(f'Added {item_name}')
    cart_item = driver.find_element(By.CLASS_NAME,"shopping_cart_badge")
    assert int(cart_item.text) == len(items)

    driver.find_element(By.CLASS_NAME,"shopping_cart_link").click()
    assert URL_CART in driver.current_url

    for item in driver.find_elements(By.CLASS_NAME,"inventory_item_name"):
        assert item.text in cart
    log_status('Finished testing adding items to the cart')


def remove_items(driver):
    """Remove items from the cart"""
    driver.find_element(By.CLASS_NAME,"shopping_cart_link").click()
    assert URL_CART in driver.current_url

    cart_items = len(driver.find_elements(By.CLASS_NAME,"cart_item"))

    log_status(f"Number of items in the cart = {cart_items}")
    for item in driver.find_elements(By.CLASS_NAME,"cart_item"):
        item_name = item.find_element(By.CLASS_NAME,"inventory_item_name").text
        item.find_element(By.CLASS_NAME,"cart_button").click()
        log_status(f'Removed {item_name}')

    cart_items = len(driver.find_elements(By.CLASS_NAME,"cart_item"))
    assert cart_items == 0
    log_status('Finshed testing removing items from the cart')


def run_tests():
    """Run the test"""
    log_status("Starting the browser...")
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    log_status('Browser started successfully.')
    log_status('Login')
    login(driver, "standard_user", "secret_sauce")
    log_status('Add items')
    add_items(driver)
    log_status('Remove items')
    remove_items(driver)
    log_status("Tests Completed")


if __name__ == "__main__":
    run_tests()
