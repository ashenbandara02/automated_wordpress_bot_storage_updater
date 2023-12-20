import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


# Admin-Data- Wpshop
username = ''
password = '@'

# Admin-Data- WordPress
wordpress_url = ''
username_wp = '@gmail.com'
password_wp = ''

# Login to WpShop Account / Cookie Set up / Verification
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

session = requests.Session()
login_response = session.get('https://wpshop.net/my-account/')
soup = BeautifulSoup(login_response.text, 'lxml')
csrf_token = soup.find('input', {'name': 'woocommerce-login-nonce'})['value'] #obtain CSRF token after login using requests

login_data = {
    'username': username,
    'password': password,
    'rememberme': 'forever', 
    'woocommerce-login-nonce': csrf_token,
    '_wp_http_referer': '/my-account/',
    'login': 'Log in',
}

login_response = session.post("https://wpshop.net/my-account/", data=login_data) # Perform the login request using requests and validation check
if 'Dashboard' in login_response.text:
    print("Login to Wpshop successful! [ \u2713 ]")
else:
    print("Login failed.")
    session.close()
    exit()


# Login to Wordpress with Selenium 
options_cd = Options()
# options_cd.add_argument("--headless") # headless mode *
driver = webdriver.Chrome(options=options_cd) # Initialize the webdriver
driver.maximize_window()
driver.get(wordpress_url)

driver.implicitly_wait(10)

username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user_login')))
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'user_pass')))
username_input.clear()
username_input.send_keys(username_wp)
password_input.clear()
password_input.send_keys(password_wp)

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "rememberme"))).click() # remember me button to avoid wordpress from logging out

login_button_locator = (By.ID, 'wp-submit') # Find the login button and click it
login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(login_button_locator))
login_button.click()
print("Wordpress Login [ \u2713 ]")


# moving to wpshop with selenium
driver.get("https://wpshop.net/my-account/")
cookies_dict = session.cookies.get_dict() # We must use the request cookies and transfer them to driver
for key, value in cookies_dict.items():
    driver.add_cookie({
        'name': key,
        'value': value,
        'domain': 'wpshop.net',  
        'path': '/',  
    })


def remove_special_characters(input_string): # very important func
    """Removes Unnessasry symbols to avoid crashing during saving a file"""
    translation_table = str.maketrans("", "", "/|\\<>?:\"*")
    result_string = input_string.translate(translation_table)

    return result_string.replace(" ", "")


def publish_to_wordpress(product_title, product_version, product_lastupdate, product_price, demo_link, product_type, product_url):
    """Passes Data to Wordpress and Then Adds perticular product"""
    # webdriver_path = '/path/to/chromedriver' incase required


    filename = f'{remove_special_characters(product_title)}_{remove_special_characters(product_version)}_wptoolmart.zip'

    product_image_path = f'F:/Work/UPLOADERBOT/products/{remove_special_characters(product_title)}.avif'
    product_downloadable_file_path = f'F:/Work/UPLOADERBOT/products/{filename}'


    # Navigate to the Products page
    driver.get('https://wptoolmart.com/wp-admin/edit.php?post_type=product')

    WebDriverWait(driver, 10).until( # Click on the "Add New" button
        EC.element_to_be_clickable((By.LINK_TEXT, 'Add New'))).click() 

    WebDriverWait(driver, 10).until(  # Title
        EC.element_to_be_clickable((By.NAME, 'post_title'))).send_keys(product_title)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'product-version'))).send_keys(product_version) # Version, update, demo
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'product-last-updated'))).send_keys(product_lastupdate)

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'live-preview'))).send_keys(demo_link)
    

    if product_type == "Theme":
        category = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'in-product_cat-63')))
        driver.execute_script("arguments[0].click();", category)

        # sub_category = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//li[@id="product_cat-63"]//label[text()=" {product_type[1]}"]')))
        # driver.execute_script("arguments[0].click();", sub_category)

    elif product_type == "Plugin":
        category = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'in-product_cat-15')))
        driver.execute_script("arguments[0].click();", category)

        # sub_category = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f'//li[@id="product_cat-15"]//ul[@class="children"]//label[text()=" {product_type[1]}"]')))
        # driver.execute_script("arguments[0].click();", sub_category)
        

    ###############add elif for phpscripts as well ####################3



    # Upload part of Image File
    set_image = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'set-post-thumbnail')))
    driver.execute_script("arguments[0].click();", set_image)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'menu-item-upload'))).click()

    input_tag = "//input[starts-with(@id,'html5_')]" # Identifies the Upload Field (Very Important)
    
    while True:
        try:
            driver.find_element(By.XPATH, input_tag).send_keys(product_image_path)
            break
        except:
            pass
        time.sleep(1)

    driver.implicitly_wait(10) # Awaits Untill the Picture Uploads

    set_image_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Set product image')]"))
    )
    set_image_button.click()


    # Fill out the product price
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, '_regular_price'))).send_keys(product_price)


 # Select the file Apply download etc/( Gdrive if needed )
    virtual_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, '_virtual'))) # ----- virtual checkbox -------
    driver.execute_script("arguments[0].click();", virtual_button)
    
    downloadable_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, '_downloadable'))) # ----- downloadable checkbox -------
    driver.execute_script("arguments[0].click();", downloadable_button)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "insert"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "upload_file_button"))).click()

    select_upload_section = driver.find_element(By.ID, "menu-item-upload")
    driver.execute_script("arguments[0].click();", select_upload_section)

    input_tag_file_zip = "//input[starts-with(@id,'html5_')]" # Identifies the Upload Field for downloadable (Very Important)
    while True:
        try:
            driver.find_element(By.XPATH, input_tag_file_zip).send_keys(product_downloadable_file_path)
            break
        except:
            pass
        time.sleep(5)
        
    print("Uploading the Zip File ...")

    turn = 0
    while True: # Check if file is uploaded to goto next step !
        try:
            progress_bar = driver.find_element(By.CSS_SELECTOR, '.thumbnail- .media-progress-bar div')
            print("Uploaded : ", progress_bar.get_attribute('style')[-4:])
            turn += 1
            if turn >= 10:
                with open("uploaderror.txt", "w", encoding="utf-8") as uploaderrorfile:
                    uploaderrorfile.write(f"{product_url}\n")
                break

            if 'width: 100%' in progress_bar.get_attribute('style'):
                break
        except Exception as e:
            pass 
        time.sleep(1)  # Wait for 1 second before checking again


    if turn < 10:
        insert_file_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Insert file URL')]"))
        )
        insert_file_button.click()

        file_download_name_change = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "file_name"))).find_element(By.CLASS_NAME, "input_text") # removing filename and adding Download as name
        file_download_name_change.clear()
        file_download_name_change.send_keys("Download")

        print("[ \u2713 ] Zip File Uploaded")


        # Setting Limit Purchases to 1 Item Only 
        inventory_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "inventory_options"))).find_element(By.TAG_NAME, "a")
        driver.execute_script("arguments[0].click();", inventory_button)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "_sold_individually"))).click()

        # Save the product / Publishing
        time.sleep(10) # -- Important --
        publish_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'publish')))
        driver.execute_script("arguments[0].click();", publish_button)

        print("[ \u2713 ] Product Added")

        with open('logfile.txt', 'a', encoding="utf-8") as logfile:
            logfile.write("[ \u2713 ] {}\n".format(product_url))
    else:
        try:
            submitdelete = driver.find_element(By.CLASS_NAME, "submitdelete")
            driver.execute_script("arguments[0].click();", submitdelete)
        except:
            print("Draft Wasnt Deleted")

    os.remove(product_image_path)
    os.remove(product_downloadable_file_path)


def product_scrapper(product_url, product_type):
    """This Perticular Function Runs Visits Each Product in the 3 subcategories the selenium web driver borrows the cookies
    from the requests library in order to send the products to the users cart and closes the driver after that"""
    
    # Scraping the Product Info 
    element = requests.get(product_url)
    parsed_element = BeautifulSoup(element.content, 'lxml')

    p_title = parsed_element.find('h1', class_="product_title entry-title").text

    product_details_div = parsed_element.find('div', class_='woocommerce-product-details__short-description')

    try:
        p_version = product_details_div.find_all('li')[-3].text.split(":")[1]
    except:
        p_version = ''

    try:
        p_last_update = product_details_div.find_all('li')[-2].text.split(":")[1]
    except:
        p_last_update = ''

    default_price = "3.99"

    try:
        demo_link = parsed_element.find("div", class_="woocommerce-product-details__short-description").find("p").find("a")['href']
    except AttributeError:
        demo_link = ''
        print("Current Item Has No Demo Link !")

    picture = parsed_element.find('div', class_="woocommerce-product-gallery__image").find('a')['href']


    driver.get(product_url)

    try:
        element2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.yith-wcmbs-product-download-box__downloads a.yith-wcmbs-download-button'))
            )
        zip_check = "K" 
    except:
        zip_check = "X"

    if zip_check == "K":
        zip_file = element2.get_attribute('href')
        
        print(f"[ \u2713 ] Fetch -> {p_title}")

        # Saving the Pic of the Product & downloading the file
        get_image = session.get(picture)
        get_file = session.get(zip_file)
        if get_image.status_code == 200:
            if get_file.status_code == 200:
                image_path = f"products/{remove_special_characters(p_title)}.avif"
                file_path = f"products/{remove_special_characters(p_title)}_{remove_special_characters(p_version)}_wptoolmart.zip" # write a code for renaming
                with open(image_path, 'wb') as image_file:
                    image_file.write(get_image.content)
                print("[ \u2713 ] Image Download")
                with open(file_path, 'wb') as content_file:
                    content_file.write(get_file.content)
                print("[ \u2713 ] Zip File Download")

                publish_to_wordpress(p_title, p_version, p_last_update, default_price, demo_link, product_type, product_url)

            else:
                with open("datalog.txt", 'a', encoding="utf-8") as log_file:
                    log_file.write(f"[ \u2717 ] File Download Error : {p_title}")
        else:
            with open("datalog.txt", 'a', encoding="utf-8") as log_file:
                log_file.write(f"[ \u2717 ] Image Download Error : {p_title}")
    elif zip_check == "X":
        with open('logfile.txt', 'a', encoding="utf-8") as logfile:
            logfile.write("[ \u2717 ] {}\n".format(product_url))
        

# # WebScraping the Product Links
# themes = "https://wpshop.net/product-category/wordpress-themes/"
# plugins = "https://wpshop.net/product-category/wordpress-plugins/"


# #check to see if already downloaded
# already_downloaded = []
# with open("logfile.txt", 'r', encoding="utf-8") as urls:
#     for url in urls:
#         already_downloaded.append(url.strip().replace("[ \u2713 ] ", "").replace("[ \u2717 ] ", ""))


# containers = {"Theme": themes, "Plugin": plugins}

# for the_main_category, section_url in containers.items():
#     print("Scraping: ",the_main_category)
#     section = session.get(section_url)
#     section_soup = BeautifulSoup(section.content, 'lxml')

#     try:
#         pagination = section_soup.find("nav", class_="woocommerce-pagination").find_all("li")
#         page_no = [no.text for no in pagination]
#     except:
#         page_no = ["1"]

#     try: # incase only 1 page present
#         last_page_no = int(page_no[-2])
#     except IndexError:
#         last_page_no = int(page_no[0])

#     for the_page in range(0, last_page_no):
#         print("\n>Page : ", str(the_page + 1))
#         goto_page = section_url+"page"+str(the_page + 1)+"/"
#         scrapper = BeautifulSoup(session.get(goto_page).content, 'lxml')

#         products = [product_link.find("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")['href'] 
#                     for product_link in scrapper.find(id="grid-view").find_all("li")]
            
#         for product in products:
#             if product not in already_downloaded:
#                 product_scrapper(product, the_main_category) # Here we send the link of product to the scrapper
#                 print("[ \u2713 ] Done, Moving to Next File !!")
#                 os.system('clear')
#             else:
#                 print(f"Skipping {product}, Already Present !")


product_scrapper("https://wpshop.net/shop/publisher-newspaper-magazine-amp/", "Theme")

driver.quit()
session.close()
