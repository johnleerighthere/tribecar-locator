from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import time

start_time = time.time()
chrome_options = Options()

# detach means visible chrome is visible
chrome_options.add_experimental_option("detach", True)

# to make chrome invisible, use headless
# chrome_options.add_argument('--headless')

# load chrome
driver = webdriver.Chrome(options=chrome_options)

# navigate to login page
driver.get("https://tribecar.com/login")

# key in username, password and submit
username = driver.find_element(By.ID, "username")
username.send_keys("youremail@email.com")
password = driver.find_element(By.ID, "password")
password.send_keys("mysuperduperhardtocrackpassword")
driver.find_element(By.ID, "_submit").click()

# find date 21 days from today
start_date = str(datetime.date.today())
date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
end_date = str(date_1 + datetime.timedelta(days=21))
addtwentyonedays = end_date.split(" ")[0]

# wait for page to load because if next step executes immediately, it will be unable to find element on page
driver.implicitly_wait(3)
# there is also the option of waiting for certain elements on the page to load
# elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "pickupDate")))

# find rental start time dropdown and select it
timedropdown = driver.find_element(By.CSS_SELECTOR, "#searchCarForm > form > div > div.col-md-1.pickup-time-field > div > div > button")
timedropdown.click()
select_time = driver.find_element(By.CSS_SELECTOR, "#searchCarForm > form > div > div.col-md-1.pickup-time-field > div > div > div > ul > li:nth-child(5)")
select_time.click()

# find duration dropdown and select it
durationdropdown = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div/form/div/div[4]/div/div/button")
durationdropdown.click()
select_duration = Select(driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div[2]/div/div/form/div/div[4]/div/div/select"))
select_duration.select_by_index(3)

# change pickup date to 21 days from now - so during search there will be higher chance of finding a vehicle
driver.execute_script(f"document.getElementById('pickupDate').value='{addtwentyonedays}'")

# select phv
vehicletype = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div/form/div/div[8]/div/div[2]/button")
vehicletype.click()
selectvehicle = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div/form/div/div[8]/div/div[3]/div/div[6]/div[2]/input")
selectvehicle.click()

# find submit button and click it
submit_button = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div/div[2]/div/div/form/div/div[9]/div/button")
submit_button.click()

# wait for page to load because if next step executes immediately, it will be unable to find element on page
driver.implicitly_wait(3)

# find an element using a loop with a timeout
def find_element_with_timeout(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except:
        return None

my_element = None

# keep looking until there is no more loading button
while not my_element:
    # my_element = find_element_with_timeout(driver, By.CLASS_NAME, 'margin-bottom hide')
    # elem = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "margin-bottom")))
    # if elem:
    #     elem.click()
    time.sleep(1.3)
    loadingbutton = driver.find_element(By.CLASS_NAME, "margin-bottom")
    print(loadingbutton.is_displayed())
    if loadingbutton.is_displayed():
        loadingbutton.click()
    else:
        break
    
    # driver.implicitly_wait(0.3)
    

# wait for page to load because if next step executes immediately, it will be unable to find element on page
driver.implicitly_wait(3)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "carDiv")))

# parse page
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# find all carDivs on the page
carDivs_selector = soup.find_all('div', class_='carDiv')

# compile all the urls of each individual car in an array
car_urls = []
for links in carDivs_selector:
    #find links
    getall_links = links.find('a', class_="btn btn-block bg-tribeorange")
    #individual cars
    carlink = getall_links.get("href")
    car_urls.append(carlink)

driver.implicitly_wait(3)

# access the url of each car in the array above
carAndAddress = []
for accesslink in car_urls:
    driver.get(f"https://tribecar.com/{accesslink}")
    carname = driver.find_element(By.CSS_SELECTOR, "#main-content > form > div > div.row > div.col-sm-5.col-sm-push-7 > div > div > div:nth-child(1) > div > div:nth-child(2)").text
    address = driver.find_element(By.CSS_SELECTOR, "#address-link").text
    carAndAddress.append({'car': carname, 'address': address})
    time.sleep(0.3)

# write the results into excel file
df = pd.DataFrame(carAndAddress)
df.to_excel(f"tribecarlocations_{start_date}.xlsx", index=False)

# Close the browser
driver.quit()

# measure how long it takes to find the whole list
print("--- %s seconds ---" % (time.time() - start_time))


