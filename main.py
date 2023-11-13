# Modules that will be used
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# using request module to get the url so that we use the bs4 module to get the html of the website we want to scrap
request = requests.get(url="https://appbrewery.github.io/Zillow-Clone/")
response = request.text
soup = BeautifulSoup(response, "html.parser")

link = soup.find_all('a', class_="StyledPropertyCardDataArea-anchor", href=True)
links = [link['href'] for link in soup.find_all('a', class_="StyledPropertyCardDataArea-anchor", href=True)]

"""We remove any non-dollar character then we append the clean price to an empty list"""

prices = []
for price in soup.find_all('span', class_="PropertyCardWrapper__StyledPriceLine"):
    price_text = price.text
    cleaned_price = ''.join(char for char in price_text if char.isdigit() or char in "$,")
    prices.append(cleaned_price)

addresses = []
for address in soup.find_all('address'):
    addresses.append(address.text.strip())  # We are using .strip() to remove any trailing whitespace

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
for n in range(len(links)):
    driver.get("https://forms.gle/GecKGyNydWNCAxBU6")
    time.sleep(3)
    address = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    address.send_keys(addresses[n])
    price.send_keys(prices[n])
    link.send_keys(links[n])
    submit_button.click()
