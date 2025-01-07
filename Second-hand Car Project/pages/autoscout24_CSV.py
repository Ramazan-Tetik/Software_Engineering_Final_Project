from selenium import webdriver
from selenium.webdriver.chrome.service import  Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import random
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
#options.add_argument("--headless")
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=options)
driver.maximize_window()

website = 'https://www.autoscout24.com/'
path = f'{website}lst?atype=C&desc=0&page=1&search_id=2554r0bdct&sort=standard&source=listpage_pagination&ustate=N%2CU'
driver.get(path)


#TODO Accept the Pop Up
def pop_up_accept():
    try:
        pop_up_accept = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class = "_consent-accept_1lphq_114"]'))
        )
        pop_up_accept.click()
    except:
        pass
pop_up_accept()

#TODO COMPETED
# TODO ALL Brands
def find_all_brands_array():
    all_brands_array = []

    all_brand_input = driver.find_elements(By.XPATH, '//div[@class = "input-wrapper"]/input')

    brand_input = all_brand_input[0]
    brand_input.click()
    all_brands = driver.find_elements(By.XPATH, '//ul[@id= "make-input-primary-filter-suggestions"]/li')
    for brand in all_brands:
        if brand != all_brands[0]:
            final_letter_brand = ''
            brand_text = brand.text
            brand_text = brand_text.lower()
            for brand_letter in brand_text:
                if brand_letter == ' ':
                    brand_letter = '-'
                final_letter_brand = final_letter_brand + brand_letter

            all_brands_array.append(final_letter_brand)
    return all_brands_array


#TODO COMPETED
#TODO ALL BRANDS And Their Models
def find_all_brand_model_array():
    all_brand_model_array = []
    all_brands_array = find_all_brands_array()
    for brand_key in all_brands_array:
        page_url = f'{website}/lst/{brand_key}?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&powertype=kw&search_id=ppuu00tm4c&sort=standard&source=homepage_search-mask&ustate=N%2CU'
        driver.get(page_url)
        # TODO ALL Models

        time.sleep(1)
        all_brand_input_for_model = driver.find_elements(By.XPATH, '//div[@class = "input-wrapper"]/input')
        brand_input_for_model = all_brand_input_for_model[1]
        brand_input_for_model.click()
        try:
            all_models = driver.find_elements(By.XPATH, '//li[@role= "option"]')

            for model in all_models:
                model_text = model.text
                lower_text = model_text.lower()
                final_model_letter = ''
                for model_letter in lower_text:
                    if model_letter == ' ':
                        model_letter = '-'
                    final_model_letter = final_model_letter + model_letter
                all_brand_model_array.append(f'{brand_key}/{final_model_letter}')
                print(f'Current  = {brand_key}/{final_model_letter}')
        except:
            time.sleep(11111)
    return all_brand_model_array

#TODO COMPETED
def find_all_countries_array():
    all_countries_array = []
    country_url_format = 'D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL'
    all_countries_text = country_url_format.split('%2C')
    for each_country in all_countries_text:
        all_countries_array.append(each_country)

    return all_countries_array




#TODO COMPETED ---> CHECK
def find_mileage_array():
    # TODO  Set Mileage
    all_from_array = []
    all_to_array = []
    all_mileage_array = []
    time.sleep(0.5)
    mileage_from_input = driver.find_element(By.XPATH, '//button[@id= "mileageFrom-input"]')
    mileage_from_input.click()
    time.sleep(0.5)
    mileage_to_input = driver.find_element(By.XPATH, '//button[@id= "mileageTo-input"]')
    mileage_to_input.click()

    all_miles = driver.find_elements(By.XPATH, '//ul[@id= "mileageTo-input-suggestions"]/li')

    for mile in all_miles:

        if mile != all_miles[-1]:
            if mile == all_miles[0]:
                all_from_array.append('')

            from_text = ''
            for each_text_from in mile.text:
                if each_text_from == ',':
                    each_text_from = ""
                from_text = from_text + each_text_from
            all_from_array.append(from_text)

        to_text = ''
        for each_text_to in mile.text:
            if each_text_to == ',':
                each_text_to = ""
            to_text = to_text + each_text_to
        all_to_array.append(to_text)
    index = 0
    while index < len(all_to_array):
        if index == 0:
            mileage_text = f'-{all_to_array[index]}'
        else:
            mileage_text = f'{all_from_array[index]}-{all_to_array[index]}'
        all_mileage_array.append(mileage_text)
        index += 1
    return all_mileage_array

#TODO COMPETED --> CHECK LATER
def url_type_form_to_mileage(all_mileage):
    all_mileage_array = []
    all_mileage_low_array = []
    all_mileage_high_array = []

    for price in all_mileage:
        if price != all_mileage[-1]:
            all_mileage_low_array.append(price)
        if price != all_mileage[0]:
            all_mileage_high_array.append(price)
    mileage_index = 0
    while mileage_index < len(all_mileage_low_array):
        if mileage_index == 0:
            all_mileage_array.append(
                f'kmto={all_mileage_high_array[mileage_index]}')
        else:
            all_mileage_array.append(f'kmfrom={all_mileage_low_array[mileage_index]}&kmto={all_mileage_high_array[mileage_index]}')
        mileage_index += 1
    return all_mileage_array






#TODO COMPETED
def find_from_array():
    all_from_array = []
    time.sleep(1)
    mileage_from_input = driver.find_element(By.XPATH, '//button[@id= "mileageFrom-input"]')
    mileage_from_input.click()

    all_miles = driver.find_elements(By.XPATH, '//ul[@id= "mileageFrom-input-suggestions"]/li')

    for mile in all_miles:
        if mile != all_miles[-1]:
            if mile == all_miles[0]:
                all_from_array.append('')
            from_text = ''
            for each_text_from in mile.text:
                if each_text_from == ',':
                    each_text_from = ""
                from_text = from_text + each_text_from
            all_from_array.append(from_text)

    return all_from_array

#TODO COMPETED
def find_to_array():

    all_to_array = []
    time.sleep(1)
    mileage_to_input = driver.find_element(By.XPATH, '//button[@id= "mileageTo-input"]')
    mileage_to_input.click()
    all_miles = driver.find_elements(By.XPATH, '//ul[@id= "mileageTo-input-suggestions"]/li')

    for mile in all_miles:
        to_text = ''
        for each_text_to in mile.text:
            if each_text_to == ',':
                each_text_to = ""
            to_text = to_text + each_text_to
        all_to_array.append(to_text)
    return all_to_array

#TODO COMPETED
def find_all_mileage():
    all_mileage = ['']
    time.sleep(1)
    mileage_to_input = driver.find_element(By.XPATH, '//button[@id= "mileageTo-input"]')
    mileage_to_input.click()
    all_miles = driver.find_elements(By.XPATH, '//ul[@id= "mileageTo-input-suggestions"]/li')

    for mile in all_miles:
        to_text = ''
        for each_text_to in mile.text:
            if each_text_to == ',':
                each_text_to = ""
            to_text = to_text + each_text_to
        all_mileage.append(to_text)
    return all_mileage


#Completed-------------------------------------------------------------------------------
#TODO Find All Price To URL
def all_price_array_to_url(all_price):
    all_price_array = []
    all_price_form_array = []
    all_price_to_array = []

    for price in all_price:
        if price != all_price[-1]:
            all_price_form_array.append(price)
        if price != all_price[0]:
            all_price_to_array.append(price)
    price_index = 0
    while price_index < len(all_price_to_array):
        all_price_array.append(f'pricefrom={all_price_form_array[price_index]}&priceto={all_price_to_array[price_index]}')
        price_index += 1
    return all_price_array


#TODO COMPETED
def find_all_price():
    all_price_array = []
    time.sleep(10)
    all_price_button = driver.find_element(By.XPATH,'//button[@id = "price-from"]')

    all_price_button.click()

    all_price_elements = driver.find_elements(By.XPATH,'//li[@role= "option"]')
    for price in all_price_elements:
        price_text = price.text
        each_price_word = ''
        for each_price_letter in price_text:
            if each_price_letter == price_text[0]:
                each_price_letter = ''
            elif each_price_letter == ',':
                each_price_letter = ''
            each_price_word += each_price_letter
        if(int(each_price_word) >= 2000):
            all_price_array.append(each_price_word)
    return all_price_array

#Warning These process will take too much time! For that reason for data scrapin use found filtrations for improve usage!
def all_website_filtrations_for_url():
    all_brand_model = find_all_brand_model_array()

    all_price = all_price_array_to_url(find_all_price())

    all_mileage = url_type_form_to_mileage(find_all_mileage())

    all_country = find_all_countries_array()

    return all_brand_model, all_price, all_mileage, all_country




#TODO COMPETED
#TODO Random Search ID Generator
def generate_search_id():
    all_possible_element = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    counter = 0
    random_generated_id_search = ''
    while counter < 10:
        rand_element_index = random.randint(0,36)
        random_generated_id_search = random_generated_id_search + all_possible_element[rand_element_index]
        counter += 1
    return random_generated_id_search




def generate_url_not_price(brand_model, country, mileage):
    website = 'https://www.autoscout24.com/'
    current_page = f'{website}/lst/{brand_model}?atype=C&cy={country}&damaged_listing=exclude&desc=0&{mileage}&page=1&powertype=kw&search_id={generate_search_id()}&sort=standard&source=listpage_pagination&ustate=N%2CU'
    return current_page



#TODO COMPETED
def scrap_the_page_to_df(url):
    driver.get(url)
    all_headers = []
    all_features = []
    df_feature = {}
    try:
        # TODO Car Brand
        car_name = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//span[@class = "StageTitle_boldClassifiedInfo__sQb0l"]'))
        )

        df_feature['brand'] = car_name.text
    except:
        df_feature['brand'] = ''
    try:
        # TODO Car Model
        car_model = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//span[@class = "StageTitle_model__EbfjC StageTitle_boldClassifiedInfo__sQb0l"]'))
        )

        df_feature['model'] = car_model.text
    except:
        df_feature['model'] = ''

    try:
        # TODO Car Price
        car_price = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//span[@class = "PriceInfo_price__XU0aF"]'))
        )
        df_feature['price'] = car_price.text
    except:
        df_feature['price'] = ''

    try:
        # TODO General Feature
        first_feature_block = WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class = "VehicleOverview_containerMoreThanFourItems__691k2"]'))
        )
        first_feature_block_each_row = WebDriverWait(first_feature_block,5).until(
            lambda driver: driver.find_elements(By.XPATH,
                                                './/div[@class = "VehicleOverview_itemContainer__XSLWi"]')
        )
        #first_feature_block_each_row = first_feature_block.find_elements(By.XPATH,'.//div[@class = "VehicleOverview_itemContainer__XSLWi"]')
        for row in first_feature_block_each_row:
            first_row_header = row.find_element(By.XPATH, './/div[@class ="VehicleOverview_itemTitle__S2_lb"]').text
            first_row_feature = row.find_element(By.XPATH, './/div[@class ="VehicleOverview_itemText__AI4dA"]').text
            df_feature[first_row_header] = first_row_feature
    except:
        pass
    # -------------------------------------------------------------------------------------------------------------

    try:
        # TODO All Feature
        all_block = WebDriverWait(driver, 2).until(
            lambda driver: driver.find_elements(By.XPATH,
                                                '//dl[@class = "DataGrid_defaultDlStyle__xlLi_"]')
        )

        for each_block in all_block:
            all_headers_general = each_block.find_elements(By.XPATH, './dt')
            for header in all_headers_general:
                all_headers.append(header.text)

            all_features_general = each_block.find_elements(By.XPATH, './dd')
            for feature in all_features_general:
                all_features.append(feature.text)
    except:
        pass

    index = 0
    while index < len(all_features):
        df_feature[all_headers[index]] = all_features[index]
        index += 1
    df = pd.DataFrame([df_feature])

    return df

#TODO COMPETED
def find_last_page_num():

    try:
        pagination_bar = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_elements(By.XPATH, '//nav[@class ="scr-pagination FilteredListPagination_pagination__3WXZT"]/ul/li')
        )


        last_page = pagination_bar[-3]
        last_page_number = int(last_page.text)
    except:
        last_page_number = 1
    return last_page_number

#TODO COMPETED
def split_url_until_find_page_add_powertype(url):
    splitted_url = url.split('&powertype')
    splitted_elements = []
    for element in splitted_url:
        splitted_elements.append(element)
    return splitted_elements


#TODO COMPETED
def all_car_links(webpage_url):
    driver.get(webpage_url)

    try:
        possible_all_car_links = WebDriverWait(driver, 10).until(
            lambda driver: driver.find_elements(By.XPATH,
                                                '//div[@class = "ListItem_header__J6xlG ListItem_header_new_design__Rvyv_"]/a')
        )

        all_links = []
        for link in possible_all_car_links:
            car_link = link.get_attribute('href')
            all_links.append(car_link)
    except:
        all_links = []
    return all_links


#TODO COMPETED
def concat_all_urls_and_print_to_csv(all_df,file_name):
    if not all_df:
        return
    concated_df = pd.concat(all_df, ignore_index=True)
    concated_df.to_csv(f'{file_name}.csv', index=False)


#TODO Completed
#TODO Random Search ID Generator
def generate_search_id():
    all_possible_element = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    counter = 0
    random_generated_id_search = ''
    while counter < 10:
        rand_element_index = random.randint(0,36)
        random_generated_id_search = random_generated_id_search + all_possible_element[rand_element_index]
        counter += 1
    return random_generated_id_search


def generate_url(brand_model, country, mileage,price):
    website = 'https://www.autoscout24.com/'
    current_page = f'{website}/lst/{brand_model}?atype=C&cy={country}&damaged_listing=exclude&desc=0&{mileage}&page=1&powertype=kw&{price}&search_id={generate_search_id()}&sort=standard&source=listpage_pagination&ustate=N%2CU'

    return current_page

"""
all_brand_model_array = find_all_brand_model_array()
#all_brand_model_array = ['audi/100', 'audi/200', 'audi/50', 'audi/80', 'audi/90', 'audi/a1', 'audi/a2', 'audi/a3', 'audi/a4', 'audi/a4-allroad', 'audi/a5', 'audi/a6', 'audi/a6-allroad', 'audi/a7', 'audi/a8', 'audi/allroad', 'audi/cabriolet', 'audi/coupe', 'audi/e-tron', 'audi/e-tron-gt', 'audi/q1', 'audi/q2', 'audi/q3', 'audi/q4-e-tron', 'audi/q5', 'audi/q6', 'audi/q7', 'audi/q8', 'audi/q8-e-tron', 'audi/quattro', 'audi/r8', 'audi/rs', 'audi/rs-e-tron-gt', 'audi/rs-q3', 'audi/rs-q5', 'audi/rs-q8', 'audi/rs2', 'audi/rs3', 'audi/rs4', 'audi/rs5', 'audi/rs6', 'audi/rs7', 'audi/s1', 'audi/s2', 'audi/s3', 'audi/s4', 'audi/s5', 'audi/s6', 'audi/s7', 'audi/s8', 'audi/sq2', 'audi/sq3', 'audi/sq5', 'audi/sq6', 'audi/sq7', 'audi/sq8', 'audi/sq8-e-tron', 'audi/tt', 'audi/tt-rs', 'audi/tts', 'audi/v8', 'audi/others', 'bmw/1-series-(all)', 'bmw/114', 'bmw/116', 'bmw/118', 'bmw/120', 'bmw/123', 'bmw/125', 'bmw/128', 'bmw/130', 'bmw/135', 'bmw/140', 'bmw/2-series-(all)', 'bmw/214', 'bmw/216', 'bmw/218', 'bmw/220', 'bmw/223', 'bmw/225', 'bmw/228', 'bmw/230', 'bmw/235', 'bmw/240', 'bmw/2002', 'bmw/3-series-(all)', 'bmw/315', 'bmw/316', 'bmw/318', 'bmw/320', 'bmw/323', 'bmw/324', 'bmw/325', 'bmw/328', 'bmw/330', 'bmw/335', 'bmw/340', 'bmw/active-hybrid-3', 'bmw/4-series-(all)', 'bmw/418', 'bmw/420', 'bmw/425', 'bmw/428', 'bmw/430', 'bmw/435', 'bmw/440', 'bmw/5-series-(all)', 'bmw/518', 'bmw/520', 'bmw/523', 'bmw/524', 'bmw/525', 'bmw/528', 'bmw/530', 'bmw/535', 'bmw/540', 'bmw/545', 'bmw/550', 'bmw/active-hybrid-5', 'bmw/6-series-(all)', 'bmw/620', 'bmw/628', 'bmw/630', 'bmw/633', 'bmw/635', 'bmw/640', 'bmw/645', 'bmw/650', 'bmw/7-series-(all)', 'bmw/725', 'bmw/728', 'bmw/730', 'bmw/732', 'bmw/735', 'bmw/740', 'bmw/745', 'bmw/750', 'bmw/760', 'bmw/active-hybrid-7', 'bmw/8-series-(all)', 'bmw/830', 'bmw/840', 'bmw/850', 'bmw/i3', 'bmw/i4', 'bmw/i5', 'bmw/i7', 'bmw/i8', 'bmw/ix', 'bmw/ix1', 'bmw/ix2', 'bmw/ix3', 'bmw/m-series-(all)', 'bmw/1er-m-coupé', 'bmw/m1', 'bmw/m2', 'bmw/m3', 'bmw/m4', 'bmw/m5', 'bmw/m550', 'bmw/m6', 'bmw/m8', 'bmw/m850', 'bmw/x-series-(all)', 'bmw/active-hybrid-x6', 'bmw/x1', 'bmw/x2', 'bmw/x2-m', 'bmw/x3', 'bmw/x3-m', 'bmw/x4', 'bmw/x4-m', 'bmw/x5', 'bmw/x5-m', 'bmw/x6', 'bmw/x6-m', 'bmw/x7', 'bmw/x7-m', 'bmw/xm', 'bmw/z-series-(all)', 'bmw/z1', 'bmw/z3', 'bmw/z3-m', 'bmw/z4', 'bmw/z4-m', 'bmw/z8', 'bmw/others', 'ford/aerostar', 'ford/b-max', 'ford/bronco', 'ford/c-max', 'ford/capri', 'ford/connect-elekto', 'ford/consul', 'ford/cougar', 'ford/courier', 'ford/crown', 'ford/customline', 'ford/econoline', 'ford/econovan', 'ford/ecosport', 'ford/edge', 'ford/escape', 'ford/escort', 'ford/excursion', 'ford/expedition', 'ford/explorer', 'ford/express', 'ford/f-1', 'ford/f-100', 'ford/f-150', 'ford/f-250', 'ford/f-350', 'ford/f-360', 'ford/f-450', 'ford/f-550', 'ford/f-650', 'ford/f-super-duty', 'ford/fairlane', 'ford/falcon', 'ford/fiesta', 'ford/flex', 'ford/focus', 'ford/focus-c-max', 'ford/focus-cc', 'ford/freestar', 'ford/freestyle', 'ford/fusion', 'ford/galaxy', 'ford/gran-torino', 'ford/granada', 'ford/grand-c-max', 'ford/grand-tourneo', 'ford/gt', 'ford/ka/ka+', 'ford/kuga', 'ford/m', 'ford/maverick', 'ford/mercury', 'ford/mondeo', 'ford/mustang', 'ford/mustang-mach-e', 'ford/orion', 'ford/probe', 'ford/puma', 'ford/ranger-(all)', 'ford/ranger', 'ford/ranger-raptor', 'ford/rs-200', 'ford/s-max', 'ford/scorpio', 'ford/sierra', 'ford/sportka', 'ford/streetka', 'ford/taunus', 'ford/taurus', 'ford/thunderbird', 'ford/torino', 'ford/tourneo-(all)', 'ford/tourneo', 'ford/tourneo-connect', 'ford/tourneo-courier', 'ford/tourneo-custom', 'ford/transit-(all)', 'ford/e-transit', 'ford/transit', 'ford/transit-bus', 'ford/transit-connect', 'ford/transit-courier', 'ford/transit-custom', 'ford/windstar', 'ford/others', 'mercedes-benz/170', 'mercedes-benz/180', 'mercedes-benz/190', 'mercedes-benz/200', 'mercedes-benz/208', 'mercedes-benz/210/310', 'mercedes-benz/220', 'mercedes-benz/230', 'mercedes-benz/240', 'mercedes-benz/250', 'mercedes-benz/260', 'mercedes-benz/270', 'mercedes-benz/280', 'mercedes-benz/300', 'mercedes-benz/308', 'mercedes-benz/320', 'mercedes-benz/350', 'mercedes-benz/380', 'mercedes-benz/400', 'mercedes-benz/416', 'mercedes-benz/420', 'mercedes-benz/450', 'mercedes-benz/500', 'mercedes-benz/560', 'mercedes-benz/600', 'mercedes-benz/a-series-(all)', 'mercedes-benz/a-140', 'mercedes-benz/a-150', 'mercedes-benz/a-160', 'mercedes-benz/a-170', 'mercedes-benz/a-180', 'mercedes-benz/a-190', 'mercedes-benz/a-200', 'mercedes-benz/a-210', 'mercedes-benz/a-220', 'mercedes-benz/a-250', 'mercedes-benz/a-35-amg', 'mercedes-benz/a-45-amg', 'mercedes-benz/actros', 'mercedes-benz/amg-gt', 'mercedes-benz/amg-one', 'mercedes-benz/atego', 'mercedes-benz/b-series-(all)', 'mercedes-benz/b-150', 'mercedes-benz/b-160', 'mercedes-benz/b-170', 'mercedes-benz/b-180', 'mercedes-benz/b-200', 'mercedes-benz/b-220', 'mercedes-benz/b-250', 'mercedes-benz/b-electric-drive', 'mercedes-benz/c-series-(all)', 'mercedes-benz/c-160', 'mercedes-benz/c-180', 'mercedes-benz/c-200', 'mercedes-benz/c-220', 'mercedes-benz/c-230', 'mercedes-benz/c-240', 'mercedes-benz/c-250', 'mercedes-benz/c-270', 'mercedes-benz/c-280', 'mercedes-benz/c-30-amg', 'mercedes-benz/c-300', 'mercedes-benz/c-32-amg', 'mercedes-benz/c-320', 'mercedes-benz/c-350', 'mercedes-benz/c-36-amg', 'mercedes-benz/c-400', 'mercedes-benz/c-43-amg', 'mercedes-benz/c-450', 'mercedes-benz/c-55-amg', 'mercedes-benz/c-63-amg', 'mercedes-benz/ce-(all)', 'mercedes-benz/ce-200', 'mercedes-benz/ce-220', 'mercedes-benz/ce-230', 'mercedes-benz/ce-280', 'mercedes-benz/ce-300', 'mercedes-benz/citan', 'mercedes-benz/cl-(all)', 'mercedes-benz/cl', 'mercedes-benz/cl-160', 'mercedes-benz/cl-180', 'mercedes-benz/cl-200', 'mercedes-benz/cl-220', 'mercedes-benz/cl-230', 'mercedes-benz/cl-320', 'mercedes-benz/cl-420', 'mercedes-benz/cl-500', 'mercedes-benz/cl-55-amg', 'mercedes-benz/cl-600', 'mercedes-benz/cl-63-amg', 'mercedes-benz/cl-65-amg', 'mercedes-benz/cla-(all)', 'mercedes-benz/cla-180', 'mercedes-benz/cla-200', 'mercedes-benz/cla-220', 'mercedes-benz/cla-250', 'mercedes-benz/cla-35-amg', 'mercedes-benz/cla-45-amg', 'mercedes-benz/clc', 'mercedes-benz/cle', 'mercedes-benz/cle-180', 'mercedes-benz/cle-200', 'mercedes-benz/cle-220', 'mercedes-benz/cle-300', 'mercedes-benz/cle-450', 'mercedes-benz/cle-53-amg', 'mercedes-benz/cle-63-amg', 'mercedes-benz/clk-(all)', 'mercedes-benz/clk', 'mercedes-benz/clk-200', 'mercedes-benz/clk-220', 'mercedes-benz/clk-230', 'mercedes-benz/clk-240', 'mercedes-benz/clk-270', 'mercedes-benz/clk-280', 'mercedes-benz/clk-320', 'mercedes-benz/clk-350', 'mercedes-benz/clk-430', 'mercedes-benz/clk-500', 'mercedes-benz/clk-55-amg', 'mercedes-benz/clk-63-amg', 'mercedes-benz/cls-(all)', 'mercedes-benz/cls', 'mercedes-benz/cls-220', 'mercedes-benz/cls-250', 'mercedes-benz/cls-280', 'mercedes-benz/cls-300', 'mercedes-benz/cls-320', 'mercedes-benz/cls-350', 'mercedes-benz/cls-400', 'mercedes-benz/cls-450', 'mercedes-benz/cls-500', 'mercedes-benz/cls-53-amg', 'mercedes-benz/cls-55-amg', 'mercedes-benz/cls-63-amg', 'mercedes-benz/e-series-(all)', 'mercedes-benz/e-200', 'mercedes-benz/e-220', 'mercedes-benz/e-230', 'mercedes-benz/e-240', 'mercedes-benz/e-250', 'mercedes-benz/e-260', 'mercedes-benz/e-270', 'mercedes-benz/e-280', 'mercedes-benz/e-290', 'mercedes-benz/e-300', 'mercedes-benz/e-320', 'mercedes-benz/e-350', 'mercedes-benz/e-36-amg', 'mercedes-benz/e-400', 'mercedes-benz/e-420', 'mercedes-benz/e-43-amg', 'mercedes-benz/e-430', 'mercedes-benz/e-450', 'mercedes-benz/e-50-amg', 'mercedes-benz/e-500', 'mercedes-benz/e-53-amg', 'mercedes-benz/e-55-amg', 'mercedes-benz/e-550', 'mercedes-benz/e-60-amg', 'mercedes-benz/e-63-amg', 'mercedes-benz/eq-series-(all)', 'mercedes-benz/eqa', 'mercedes-benz/eqa-250', 'mercedes-benz/eqa-300', 'mercedes-benz/eqa-350', 'mercedes-benz/eqb-250', 'mercedes-benz/eqb-300', 'mercedes-benz/eqb-350', 'mercedes-benz/eqc-400', 'mercedes-benz/eqe-300', 'mercedes-benz/eqe-350', 'mercedes-benz/eqe-43', 'mercedes-benz/eqe-500', 'mercedes-benz/eqe-53', 'mercedes-benz/eqe-suv', 'mercedes-benz/eqs', 'mercedes-benz/eqs-suv', 'mercedes-benz/eqt', 'mercedes-benz/eqv-250', 'mercedes-benz/eqv-300', 'mercedes-benz/g-series-(all)', 'mercedes-benz/g', 'mercedes-benz/g-230', 'mercedes-benz/g-240', 'mercedes-benz/g-250', 'mercedes-benz/g-270', 'mercedes-benz/g-280', 'mercedes-benz/g-290', 'mercedes-benz/g-300', 'mercedes-benz/g-320', 'mercedes-benz/g-350', 'mercedes-benz/g-400', 'mercedes-benz/g-450', 'mercedes-benz/g-500', 'mercedes-benz/g-55-amg', 'mercedes-benz/g-580', 'mercedes-benz/g-63-amg', 'mercedes-benz/g-65-amg', 'mercedes-benz/g-650', 'mercedes-benz/gl-(all)', 'mercedes-benz/gl-320', 'mercedes-benz/gl-350', 'mercedes-benz/gl-400', 'mercedes-benz/gl-420', 'mercedes-benz/gl-450', 'mercedes-benz/gl-500', 'mercedes-benz/gl-55-amg', 'mercedes-benz/gl-63-amg', 'mercedes-benz/gla-(all)', 'mercedes-benz/gla-180', 'mercedes-benz/gla-200', 'mercedes-benz/gla-220', 'mercedes-benz/gla-250', 'mercedes-benz/gla-35-amg', 'mercedes-benz/gla-45-amg', 'mercedes-benz/glb-(all)', 'mercedes-benz/glb-180', 'mercedes-benz/glb-200', 'mercedes-benz/glb-220', 'mercedes-benz/glb-250', 'mercedes-benz/glb-35-amg', 'mercedes-benz/glc-(all)', 'mercedes-benz/glc-200', 'mercedes-benz/glc-220', 'mercedes-benz/glc-250', 'mercedes-benz/glc-300', 'mercedes-benz/glc-350', 'mercedes-benz/glc-400', 'mercedes-benz/glc-43-amg', 'mercedes-benz/glc-450', 'mercedes-benz/glc-63-amg', 'mercedes-benz/gle-(all)', 'mercedes-benz/gle-250', 'mercedes-benz/gle-300', 'mercedes-benz/gle-350', 'mercedes-benz/gle-400', 'mercedes-benz/gle-43-amg', 'mercedes-benz/gle-450', 'mercedes-benz/gle-500', 'mercedes-benz/gle-53-amg', 'mercedes-benz/gle-580', 'mercedes-benz/gle-63-amg', 'mercedes-benz/glk-(all)', 'mercedes-benz/glk-200', 'mercedes-benz/glk-220', 'mercedes-benz/glk-250', 'mercedes-benz/glk-280', 'mercedes-benz/glk-300', 'mercedes-benz/glk-320', 'mercedes-benz/glk-350', 'mercedes-benz/gls-(all)', 'mercedes-benz/gls-350', 'mercedes-benz/gls-400', 'mercedes-benz/gls-450', 'mercedes-benz/gls-500', 'mercedes-benz/gls-580', 'mercedes-benz/gls-600', 'mercedes-benz/gls-63-amg', 'mercedes-benz/m-series-(all)', 'mercedes-benz/ml-230', 'mercedes-benz/ml-250', 'mercedes-benz/ml-270', 'mercedes-benz/ml-280', 'mercedes-benz/ml-300', 'mercedes-benz/ml-320', 'mercedes-benz/ml-350', 'mercedes-benz/ml-400', 'mercedes-benz/ml-420', 'mercedes-benz/ml-430', 'mercedes-benz/ml-450', 'mercedes-benz/ml-500', 'mercedes-benz/ml-55-amg', 'mercedes-benz/ml-63-amg', 'mercedes-benz/marco-polo', 'mercedes-benz/maybach-gls', 'mercedes-benz/maybach-s-klasse', 'mercedes-benz/mb-100', 'mercedes-benz/r-series-(all)', 'mercedes-benz/r-280', 'mercedes-benz/r-300', 'mercedes-benz/r-320', 'mercedes-benz/r-350', 'mercedes-benz/r-500', 'mercedes-benz/r-63-amg', 'mercedes-benz/s-series-(all)', 'mercedes-benz/s-250', 'mercedes-benz/s-260', 'mercedes-benz/s-280', 'mercedes-benz/s-300', 'mercedes-benz/s-320', 'mercedes-benz/s-350', 'mercedes-benz/s-380', 'mercedes-benz/s-400', 'mercedes-benz/s-420', 'mercedes-benz/s-430', 'mercedes-benz/s-450', 'mercedes-benz/s-500', 'mercedes-benz/s-55-amg', 'mercedes-benz/s-550', 'mercedes-benz/s-560', 'mercedes-benz/s-560-e', 'mercedes-benz/s-580', 'mercedes-benz/s-600', 'mercedes-benz/s-63-amg', 'mercedes-benz/s-65-amg', 'mercedes-benz/s-650', 'mercedes-benz/s-680', 'mercedes-benz/sl-(all)', 'mercedes-benz/sl-230', 'mercedes-benz/sl-250', 'mercedes-benz/sl-280', 'mercedes-benz/sl-300', 'mercedes-benz/sl-320', 'mercedes-benz/sl-350', 'mercedes-benz/sl-380', 'mercedes-benz/sl-400', 'mercedes-benz/sl-420', 'mercedes-benz/sl-43-amg', 'mercedes-benz/sl-450', 'mercedes-benz/sl-500', 'mercedes-benz/sl-55-amg', 'mercedes-benz/sl-560', 'mercedes-benz/sl-60-amg', 'mercedes-benz/sl-600', 'mercedes-benz/sl-63-amg', 'mercedes-benz/sl-65-amg', 'mercedes-benz/sl-70-amg', 'mercedes-benz/sl-73-amg', 'mercedes-benz/slc-(all)', 'mercedes-benz/slc-180', 'mercedes-benz/slc-200', 'mercedes-benz/slc-250', 'mercedes-benz/slc-280', 'mercedes-benz/slc-300', 'mercedes-benz/slc-350', 'mercedes-benz/slc-380', 'mercedes-benz/slc-43-amg', 'mercedes-benz/slc-450', 'mercedes-benz/slc-500', 'mercedes-benz/slk-(all)', 'mercedes-benz/slk', 'mercedes-benz/slk-200', 'mercedes-benz/slk-230', 'mercedes-benz/slk-250', 'mercedes-benz/slk-280', 'mercedes-benz/slk-300', 'mercedes-benz/slk-32-amg', 'mercedes-benz/slk-320', 'mercedes-benz/slk-350', 'mercedes-benz/slk-55-amg', 'mercedes-benz/slr', 'mercedes-benz/sls', 'mercedes-benz/sprinter', 'mercedes-benz/t-class', 'mercedes-benz/t1', 'mercedes-benz/t2', 'mercedes-benz/v-series-(all)', 'mercedes-benz/v', 'mercedes-benz/v-200', 'mercedes-benz/v-220', 'mercedes-benz/v-230', 'mercedes-benz/v-250', 'mercedes-benz/v-280', 'mercedes-benz/v-300', 'mercedes-benz/vaneo', 'mercedes-benz/vario', 'mercedes-benz/viano', 'mercedes-benz/vito', 'mercedes-benz/w-114/115-strich-acht', 'mercedes-benz/x-series-(all)', 'mercedes-benz/x-220', 'mercedes-benz/x-250', 'mercedes-benz/x-350', 'mercedes-benz/others', 'opel/adam', 'opel/agila', 'opel/ampera', 'opel/ampera-e', 'opel/antara', 'opel/arena', 'opel/ascona', 'opel/astra', 'opel/calibra', 'opel/campo', 'opel/cascada', 'opel/combo', 'opel/combo-life', 'opel/combo-e', 'opel/combo-e-life', 'opel/commodore', 'opel/corsa', 'opel/corsa-e', 'opel/crossland', 'opel/crossland-x', 'opel/diplomat', 'opel/frontera', 'opel/grandland', 'opel/grandland-x', 'opel/gt', 'opel/insignia', 'opel/kadett', 'opel/karl', 'opel/manta', 'opel/meriva', 'opel/mokka', 'opel/mokka-x', 'opel/mokka-e', 'opel/monterey', 'opel/monza', 'opel/movano', 'opel/movano-e', 'opel/omega', 'opel/pick-up-sportscap', 'opel/rekord', 'opel/rocks-e', 'opel/senator', 'opel/signum', 'opel/sintra', 'opel/speedster', 'opel/tigra', 'opel/vectra', 'opel/vivaro', 'opel/vivaro-e', 'opel/zafira', 'opel/zafira-life', 'opel/zafira-tourer', 'opel/others', 'volkswagen/181', 'volkswagen/amarok', 'volkswagen/anfibio', 'volkswagen/arteon', 'volkswagen/atlas', 'volkswagen/beetle', 'volkswagen/bora', 'volkswagen/buggy', 'volkswagen/bus', 'volkswagen/caddy', 'volkswagen/cc', 'volkswagen/coccinelle', 'volkswagen/corrado', 'volkswagen/crafter', 'volkswagen/cross-touran', 'volkswagen/derby', 'volkswagen/e-up!', 'volkswagen/eos', 'volkswagen/escarabajo', 'volkswagen/fox', 'volkswagen/golf-(all)', 'volkswagen/cross-golf', 'volkswagen/golf', 'volkswagen/golf-cabriolet', 'volkswagen/golf-gtd', 'volkswagen/golf-gte', 'volkswagen/golf-gti', 'volkswagen/golf-plus', 'volkswagen/golf-r', 'volkswagen/golf-sportsvan', 'volkswagen/golf-variant', 'volkswagen/e-golf', 'volkswagen/grand-california', 'volkswagen/id.-buzz-(all)', 'volkswagen/id.-buzz', 'volkswagen/id.-buzz-cargo', 'volkswagen/id.3', 'volkswagen/id.4', 'volkswagen/id.5', 'volkswagen/id.6', 'volkswagen/id.7', 'volkswagen/iltis', 'volkswagen/jetta', 'volkswagen/käfer', 'volkswagen/karmann-ghia', 'volkswagen/kever', 'volkswagen/l80', 'volkswagen/lt', 'volkswagen/lupo', 'volkswagen/maggiolino', 'volkswagen/new-beetle', 'volkswagen/passat-(all)', 'volkswagen/passat', 'volkswagen/passat-alltrack', 'volkswagen/passat-cc', 'volkswagen/passat-variant', 'volkswagen/phaeton', 'volkswagen/pointer', 'volkswagen/polo-(all)', 'volkswagen/polo', 'volkswagen/polo-cross', 'volkswagen/polo-gti', 'volkswagen/polo-plus', 'volkswagen/polo-r-wrc', 'volkswagen/polo-sedan', 'volkswagen/polo-variant', 'volkswagen/routan', 'volkswagen/santana', 'volkswagen/scirocco', 'volkswagen/sharan', 'volkswagen/t-cross', 'volkswagen/t-roc', 'volkswagen/t1', 'volkswagen/t2', 'volkswagen/t3-series-(all)', 'volkswagen/t3', 'volkswagen/t3-blue-star', 'volkswagen/t3-california', 'volkswagen/t3-caravelle', 'volkswagen/t3-kombi', 'volkswagen/t3-multivan', 'volkswagen/t3-white-star', 'volkswagen/t4-series-(all)', 'volkswagen/t4', 'volkswagen/t4-allstar', 'volkswagen/t4-california', 'volkswagen/t4-caravelle', 'volkswagen/t4-kombi', 'volkswagen/t4-multivan', 'volkswagen/t5-series-(all)', 'volkswagen/t5', 'volkswagen/t5-california', 'volkswagen/t5-caravelle', 'volkswagen/t5-kombi', 'volkswagen/t5-multivan', 'volkswagen/t5-shuttle', 'volkswagen/t5-transporter', 'volkswagen/t6-series-(all)', 'volkswagen/t6-california', 'volkswagen/t6-caravelle', 'volkswagen/t6-kombi', 'volkswagen/t6-multivan', 'volkswagen/t6-transporter', 'volkswagen/t6.1', 'volkswagen/t6.1-california', 'volkswagen/t6.1-caravelle', 'volkswagen/t6.1-kombi', 'volkswagen/t6.1-multivan', 'volkswagen/t6.1-transporter', 'volkswagen/t7', 'volkswagen/t7-california', 'volkswagen/t7-caravelle', 'volkswagen/t7-kastenwagen', 'volkswagen/t7-kombi', 'volkswagen/t7-multivan', 'volkswagen/taigo', 'volkswagen/taro', 'volkswagen/tiguan-(all)', 'volkswagen/tiguan', 'volkswagen/tiguan-allspace', 'volkswagen/touareg', 'volkswagen/touran', 'volkswagen/transporter', 'volkswagen/up!', 'volkswagen/vento', 'volkswagen/viloran', 'volkswagen/xl1', 'volkswagen/others', 'renault/alaskan', 'renault/alpine-a110', 'renault/alpine-a310', 'renault/alpine-a610', 'renault/alpine-v6', 'renault/arkana', 'renault/austral', 'renault/avantime', 'renault/captur', 'renault/clio', 'renault/coupe', 'renault/duster', 'renault/espace', 'renault/express', 'renault/fluence', 'renault/fluence-z.e.', 'renault/fuego', 'renault/grand-espace', 'renault/grand-modus', 'renault/grand-scenic', 'renault/kadjar', 'renault/kangoo', 'renault/kangoo-e-tech', 'renault/kangoo-z.e.', 'renault/koleos', 'renault/laguna', 'renault/latitude', 'renault/logan', 'renault/mascott', 'renault/master', 'renault/megane', 'renault/megane-e-tech', 'renault/messenger', 'renault/modus', 'renault/p-1400', 'renault/r-11', 'renault/r-14', 'renault/r-18', 'renault/r-19', 'renault/r-20', 'renault/r-21', 'renault/r-25', 'renault/r-30', 'renault/r-4', 'renault/r-5', 'renault/r-6', 'renault/r-9', 'renault/rafale', 'renault/rapid', 'renault/safrane', 'renault/sandero', 'renault/sandero-stepway', 'renault/scenic', 'renault/spider', 'renault/super-5', 'renault/symbioz', 'renault/symbol', 'renault/talisman', 'renault/trafic', 'renault/twingo', 'renault/twizy', 'renault/vel-satis', 'renault/wind', 'renault/zoe', 'renault/others', '9ff/f70-etronic', '9ff/f97-a-max', '9ff/gt9', '9ff/gtronic', '9ff/gturbo', '9ff/speed9', '9ff/others', 'abarth/124-gt', 'abarth/124-rally-tribute', 'abarth/124-spider', 'abarth/500', 'abarth/500c', 'abarth/500e', 'abarth/595', 'abarth/595-competizione', 'abarth/595-pista', 'abarth/595-turismo', 'abarth/595c', 'abarth/695', 'abarth/695c', 'abarth/grande-punto', 'abarth/punto-evo', 'abarth/punto-supersport', 'abarth/others', 'ac/ace', 'ac/cobra', 'ac/others', 'acm/4-wd', 'acm/biagini-passo', 'acm/others', 'acura/ilx', 'acura/mdx', 'acura/nsx', 'acura/rdx', 'acura/rl', 'acura/rlx', 'acura/rsx', 'acura/tl', 'acura/tlx', 'acura/tsx', 'acura/zdx', 'acura/others', 'aiways/u5', 'aiways/u6-ion', 'aiways/others', 'aixam/400', 'aixam/500', 'aixam/a.', 'aixam/city', 'aixam/coupe', 'aixam/crossline', 'aixam/crossover', 'aixam/d-truck', 'aixam/e-truck', 'aixam/gti', 'aixam/gto', 'aixam/mac', 'aixam/mega', 'aixam/roadline', 'aixam/scouty-r', 'aixam/others', 'alba-mobility/cargo', 'alba-mobility/golf-cart', 'alba-mobility/le-22-limited-edition', 'alba-mobility/street-cart', 'alba-mobility/tour-cart', 'alba-mobility/others', 'alfa-romeo/145', 'alfa-romeo/146', 'alfa-romeo/147', 'alfa-romeo/155', 'alfa-romeo/156', 'alfa-romeo/159', 'alfa-romeo/164', 'alfa-romeo/166', 'alfa-romeo/1750', 'alfa-romeo/2000', 'alfa-romeo/33', 'alfa-romeo/4c', 'alfa-romeo/75', 'alfa-romeo/8c', 'alfa-romeo/90', 'alfa-romeo/alfa-6', 'alfa-romeo/alfasud', 'alfa-romeo/alfetta', 'alfa-romeo/brera', 'alfa-romeo/crosswagon', 'alfa-romeo/giulia', 'alfa-romeo/giulietta', 'alfa-romeo/gt', 'alfa-romeo/gtv', 'alfa-romeo/junior', 'alfa-romeo/mito', 'alfa-romeo/montreal', 'alfa-romeo/quadrifoglio', 'alfa-romeo/rz', 'alfa-romeo/spider', 'alfa-romeo/sportwagon', 'alfa-romeo/sprint', 'alfa-romeo/stelvio', 'alfa-romeo/sz', 'alfa-romeo/tonale', 'alfa-romeo/others', 'alpina/b10', 'alpina/b11', 'alpina/b12', 'alpina/b3', 'alpina/b4', 'alpina/b5', 'alpina/b6', 'alpina/b7', 'alpina/b8', 'alpina/b9', 'alpina/c1', 'alpina/c2', 'alpina/d10', 'alpina/d3', 'alpina/d4', 'alpina/d5', 'alpina/roadster-limited-edition', 'alpina/roadster-s', 'alpina/roadster-v8', 'alpina/xb7', 'alpina/xd3', 'alpina/xd4', 'alpina/others', 'alpine/a110', 'alpine/a290', 'alpine/others', 'amphicar/770', 'amphicar/others', 'angelelli-automobili/d-1-s-hypercar', 'angelelli-automobili/d-2-gt-granturismo-v12', 'angelelli-automobili/d-3-hypersuv', 'angelelli-automobili/effequaranta', 'angelelli-automobili/hintegrale', 'angelelli-automobili/others', 'ariel-motor/atom', 'ariel-motor/nomad', 'ariel-motor/others', 'artega/gt', 'artega/karo', 'artega/scalo', 'artega/others', 'aspark/owl', 'aspark/others', 'aspid/gt-21', 'aspid/ss', 'aspid/others', 'aston-martin/ar1', 'aston-martin/cygnet', 'aston-martin/db', 'aston-martin/db11', 'aston-martin/db12', 'aston-martin/db7', 'aston-martin/db9', 'aston-martin/dbs', 'aston-martin/dbx', 'aston-martin/lagonda', 'aston-martin/rapide', 'aston-martin/v8', 'aston-martin/valkyrie', 'aston-martin/vanquish', 'aston-martin/vantage', 'aston-martin/virage', 'aston-martin/volante', 'aston-martin/others', 'aurus/komendant', 'aurus/others', 'austin/estate', 'austin/healey', 'austin/maestro', 'austin/metro', 'austin/mini', 'austin/mini-moke', 'austin/mk', 'austin/montego', 'austin/others', 'austin-healey/100', 'austin-healey/3000', 'austin-healey/sprite', 'austin-healey/others', 'autobianchi/a-1000', 'autobianchi/a-112', 'autobianchi/y10', 'autobianchi/others', 'baic/b40', 'baic/beijing-x35', 'baic/beijing-x55', 'baic/beijing-x75', 'baic/bj20', 'baic/bj40', 'baic/bj80', 'baic/d20', 'baic/senova-d50', 'baic/senova-x25', 'baic/senova-x35', 'baic/senova-x55', 'baic/senova-x65', 'baic/senova-zhixing', 'baic/others', 'bedford/astramax', 'bedford/astravan', 'bedford/beagle', 'bedford/blitz', 'bedford/brava', 'bedford/ca', 'bedford/cf2', 'bedford/chevanne', 'bedford/dormobile', 'bedford/ha', 'bedford/kb', 'bedford/midi', 'bedford/mw', 'bedford/rascal', 'bedford/tj', 'bedford/others', 'bellier/asso', 'bellier/b8', 'bellier/divane', 'bellier/docker', 'bellier/jade', 'bellier/opale', 'bellier/sturdy', 'bellier/vx', 'bellier/others', 'bentley/arnage', 'bentley/azure', 'bentley/bacalar', 'bentley/bentayga', 'bentley/brooklands', 'bentley/continental', 'bentley/continental-gt', 'bentley/continental-gtc', 'bentley/eight', 'bentley/flying-spur', 'bentley/mulsanne', 'bentley/s1', 'bentley/s2', 'bentley/s3', 'bentley/turbo-r', 'bentley/turbo-rt', 'bentley/turbo-s', 'bentley/others', 'boldmen/cr-4', 'boldmen/others', 'bolloré/bluecar', 'bolloré/bluesummer', 'bolloré/blueutility', 'bolloré/others', 'borgward/arabella', 'borgward/bx5', 'borgward/bx7', 'borgward/hansa-1100', 'borgward/hansa-1500', 'borgward/hansa-1700', 'borgward/hansa-1800', 'borgward/hansa-2000', 'borgward/hansa-2300', 'borgward/hansa-2400', 'borgward/hansa-3500', 'borgward/hansa-400/500', 'borgward/isabella', 'borgward/p100', 'borgward/others', 'brilliance/bc3', 'brilliance/bs2', 'brilliance/bs4', 'brilliance/bs6', 'brilliance/granse', 'brilliance/jinbei', 'brilliance/zhonghua', 'brilliance/zunchi', 'brilliance/others', 'bristol/405', 'bristol/408', 'bristol/others', 'brute/custom', 'brute/others', 'bugatti/centodieci', 'bugatti/chiron', 'bugatti/divo', 'bugatti/eb-110', 'bugatti/eb-112', 'bugatti/veyron', 'bugatti/others', 'buick/cascada', 'buick/century', 'buick/electra', 'buick/enclave', 'buick/encore', 'buick/envision', 'buick/lacrosse', 'buick/le-sabre', 'buick/park-avenue', 'buick/regal', 'buick/riviera', 'buick/roadmaster', 'buick/skylark', 'buick/special', 'buick/verano', 'buick/others', 'byd/atto-3', 'byd/dolphin', 'byd/e6', 'byd/f1', 'byd/f3', 'byd/f3r', 'byd/f6', 'byd/f8', 'byd/han', 'byd/seal', 'byd/seal-u', 'byd/tang', 'byd/others', 'cadillac/allante', 'cadillac/ats', 'cadillac/bls', 'cadillac/brougham', 'cadillac/ct4', 'cadillac/ct5', 'cadillac/ct6', 'cadillac/cts', 'cadillac/deville', 'cadillac/dts', 'cadillac/eldorado', 'cadillac/escalade', 'cadillac/fleetwood', 'cadillac/lasalle', 'cadillac/lyriq', 'cadillac/series-62', 'cadillac/series-6200', 'cadillac/seville', 'cadillac/srx', 'cadillac/sts', 'cadillac/xlr', 'cadillac/xt4', 'cadillac/xt5', 'cadillac/xt6', 'cadillac/xts', 'cadillac/others', 'caravans-wohnm/adria', 'caravans-wohnm/ahorn', 'caravans-wohnm/airstream', 'caravans-wohnm/alpha', 'caravans-wohnm/arca', 'caravans-wohnm/autoroller', 'caravans-wohnm/autostar', 'caravans-wohnm/bavaria', 'caravans-wohnm/bawemo', 'caravans-wohnm/beisl', 'caravans-wohnm/benimar', 'caravans-wohnm/bimobil', 'caravans-wohnm/biod', 'caravans-wohnm/burow', 'caravans-wohnm/burow-mobil', 'caravans-wohnm/bürstner', 'caravans-wohnm/ca-mo-car', 'caravans-wohnm/carado', 'caravans-wohnm/caravelair', 'caravans-wohnm/caro', 'caravans-wohnm/carthago', 'caravans-wohnm/challenger', 'caravans-wohnm/chausson', 'caravans-wohnm/chrysler', 'caravans-wohnm/ci-international', 'caravans-wohnm/coachmen', 'caravans-wohnm/concorde', 'caravans-wohnm/cristall', 'caravans-wohnm/cs-reisemobile', 'caravans-wohnm/damon', 'caravans-wohnm/dehler', 'caravans-wohnm/delta', 'caravans-wohnm/dethleffs', 'caravans-wohnm/dream', 'caravans-wohnm/due-erre', 'caravans-wohnm/eifelland', 'caravans-wohnm/elnagh', 'caravans-wohnm/eriba', 'caravans-wohnm/euramobil', 'caravans-wohnm/euro-liner', 'caravans-wohnm/evm', 'caravans-wohnm/fendt', 'caravans-wohnm/ffb-/-tabbert', 'caravans-wohnm/fiat', 'caravans-wohnm/fleetwood', 'caravans-wohnm/florence', 'caravans-wohnm/ford', 'caravans-wohnm/ford-/-reimo', 'caravans-wohnm/frankia', 'caravans-wohnm/general-motors', 'caravans-wohnm/gigant', 'caravans-wohnm/giottiline', 'caravans-wohnm/globecar', 'caravans-wohnm/granduca', 'caravans-wohnm/hehn', 'caravans-wohnm/heku', 'caravans-wohnm/hobby', 'caravans-wohnm/holiday-rambler', 'caravans-wohnm/home-car', 'caravans-wohnm/hymer', 'caravans-wohnm/icf', 'caravans-wohnm/iveco', 'caravans-wohnm/karmann', 'caravans-wohnm/kentucky', 'caravans-wohnm/kip', 'caravans-wohnm/knaus', 'caravans-wohnm/la-strada', 'caravans-wohnm/laika', 'caravans-wohnm/linne-liner', 'caravans-wohnm/lmc', 'caravans-wohnm/m+m-mobile', 'caravans-wohnm/ma-bu', 'caravans-wohnm/maesss', 'caravans-wohnm/man', 'caravans-wohnm/mazda', 'caravans-wohnm/mclouis', 'caravans-wohnm/megamobil', 'caravans-wohnm/mercedes-benz', 'caravans-wohnm/miller', 'caravans-wohnm/mirage', 'caravans-wohnm/mitsubishi', 'caravans-wohnm/mizar', 'caravans-wohnm/mobilvetta', 'caravans-wohnm/monaco', 'caravans-wohnm/moncayo', 'caravans-wohnm/morelo', 'caravans-wohnm/neotec', 'caravans-wohnm/niesmann+bischoff', 'caravans-wohnm/niewiadow', 'caravans-wohnm/nordstar', 'caravans-wohnm/ormocar', 'caravans-wohnm/peugeot', 'caravans-wohnm/phoenix', 'caravans-wohnm/pilote', 'caravans-wohnm/pössl', 'caravans-wohnm/procab', 'caravans-wohnm/rapido', 'caravans-wohnm/reimo', 'caravans-wohnm/reisemobile-beier', 'caravans-wohnm/renault', 'caravans-wohnm/rimor', 'caravans-wohnm/riva', 'caravans-wohnm/riviera', 'caravans-wohnm/rmb', 'caravans-wohnm/roadtrek', 'caravans-wohnm/robel-mobil', 'caravans-wohnm/rockwood', 'caravans-wohnm/selbstbau', 'caravans-wohnm/sterckeman', 'caravans-wohnm/sunlight', 'caravans-wohnm/swift', 'caravans-wohnm/tabbert', 'caravans-wohnm/tec', 'caravans-wohnm/tischer', 'caravans-wohnm/trigano', 'caravans-wohnm/triple-e', 'caravans-wohnm/ultra', 'caravans-wohnm/vario', 'caravans-wohnm/vw', 'caravans-wohnm/weinsberg', 'caravans-wohnm/weippert', 'caravans-wohnm/westfalia', 'caravans-wohnm/wilk', 'caravans-wohnm/winnebago', 'caravans-wohnm/others', 'carver/base', 'carver/cargo', 'carver/others', 'casalini/kerry', 'casalini/m10', 'casalini/m110', 'casalini/m12', 'casalini/m14', 'casalini/m20', 'casalini/pick-up12', 'casalini/sulky', 'casalini/sulkycar', 'casalini/sulkydea/ydea', 'casalini/others', 'caterham/21', 'caterham/aeroseven', 'caterham/classic-7', 'caterham/classic-line', 'caterham/classic-s7', 'caterham/cosworth-csr-200', 'caterham/csr-175', 'caterham/csr-260', 'caterham/r-400', 'caterham/r300-superlight', 'caterham/roadsport-seven', 'caterham/seven-270', 'caterham/seven-310', 'caterham/seven-360', 'caterham/seven-420', 'caterham/seven-485', 'caterham/seven-620', 'caterham/sp/300.r', 'caterham/super-7', 'caterham/superlight', 'caterham/vxi', 'caterham/others', 'cenntro/avantier-c', 'cenntro/logistar-100', 'cenntro/logistar-200', 'cenntro/logistar-260', 'cenntro/metro', 'cenntro/neibor-150', 'cenntro/neibor-200', 'cenntro/others', 'changhe/a6', 'changhe/coolcar', 'changhe/freedom', 'changhe/ideal', 'changhe/mini-truck', 'changhe/q25', 'changhe/q35', 'changhe/q7', 'changhe/x5', 'changhe/others', 'chatenet/barooder', 'chatenet/ch-26', 'chatenet/ch-28', 'chatenet/ch-30', 'chatenet/ch-32', 'chatenet/ch-40', 'chatenet/ch-46', 'chatenet/media', 'chatenet/pick-up', 'chatenet/speedino', 'chatenet/sporteevo', 'chatenet/stella', 'chatenet/others', 'chery/à13', 'chery/a18', 'chery/a21', 'chery/a3', 'chery/amulet', 'chery/arrizo', 'chery/b13', 'chery/b14', 'chery/crosseastar', 'chery/crossover', 'chery/eastar', 'chery/eq', 'chery/fengyun', 'chery/fora', 'chery/fulwin', 'chery/karry', 'chery/kimo', 'chery/m11', 'chery/m14', 'chery/mikado', 'chery/mpv', 'chery/qq', 'chery/s18', 'chery/sweet', 'chery/tiggo', 'chery/very', 'chery/wow', 'chery/others', 'chevrolet/2500', 'chevrolet/alero', 'chevrolet/astro', 'chevrolet/avalanche', 'chevrolet/aveo', 'chevrolet/bel-air', 'chevrolet/beretta', 'chevrolet/blazer', 'chevrolet/bolt', 'chevrolet/c1500', 'chevrolet/camaro', 'chevrolet/caprice', 'chevrolet/captiva', 'chevrolet/cavalier', 'chevrolet/celebrity', 'chevrolet/chevelle', 'chevrolet/chevy-van', 'chevrolet/citation', 'chevrolet/colorado', 'chevrolet/corsica', 'chevrolet/corvair', 'chevrolet/monza', 'chevrolet/monza-convertible', 'chevrolet/monza-coupé', 'chevrolet/monza-sport-sedan', 'chevrolet/corvette', 'chevrolet/crew-cab', 'chevrolet/cruze', 'chevrolet/dixie-van', 'chevrolet/el-camino', 'chevrolet/epica', 'chevrolet/equinox', 'chevrolet/evanda', 'chevrolet/express', 'chevrolet/g', 'chevrolet/hhr', 'chevrolet/impala', 'chevrolet/k1500', 'chevrolet/k30', 'chevrolet/kalos', 'chevrolet/lacetti', 'chevrolet/lanos', 'chevrolet/lumina', 'chevrolet/malibu', 'chevrolet/matiz', 'chevrolet/monte-carlo', 'chevrolet/niva', 'chevrolet/nubira', 'chevrolet/orlando', 'chevrolet/rezzo', 'chevrolet/s-10', 'chevrolet/silverado', 'chevrolet/spark', 'chevrolet/ssr', 'chevrolet/suburban', 'chevrolet/tacuma', 'chevrolet/tahoe', 'chevrolet/tracker', 'chevrolet/trailblazer', 'chevrolet/trans-sport', 'chevrolet/traverse', 'chevrolet/trax', 'chevrolet/uplander', 'chevrolet/viva', 'chevrolet/volt', 'chevrolet/others', 'chrysler/200', 'chrysler/300-m', 'chrysler/300-srt', 'chrysler/300c', 'chrysler/aspen', 'chrysler/crossfire', 'chrysler/daytona', 'chrysler/es', 'chrysler/grand-voyager', 'chrysler/gs', 'chrysler/gts', 'chrysler/imperial', 'chrysler/le-baron', 'chrysler/neon', 'chrysler/new-yorker', 'chrysler/pacifica', 'chrysler/prowler', 'chrysler/pt-cruiser', 'chrysler/ram-van', 'chrysler/saratoga', 'chrysler/sebring', 'chrysler/stratus', 'chrysler/town-&-country', 'chrysler/valiant', 'chrysler/viper', 'chrysler/vision', 'chrysler/voyager', 'chrysler/others', 'cirelli/cirelli-2', 'cirelli/cirelli-3', 'cirelli/cirelli-4', 'cirelli/cirelli-5', 'cirelli/cirelli-7', 'cirelli/cirelli-8', 'cirelli/others', 'citroen/2cv', 'citroen/acadiane', 'citroen/ami', 'citroen/ax', 'citroen/axel', 'citroen/berlingo', 'citroen/bx', 'citroen/c-crosser', 'citroen/c-elysée', 'citroen/c-zero', 'citroen/c1', 'citroen/c15', 'citroen/c2', 'citroen/c25', 'citroen/c3-(all)', 'citroen/c3', 'citroen/c3-aircross', 'citroen/c3-picasso', 'citroen/c35', 'citroen/c4-(all)', 'citroen/c4', 'citroen/c4-aircross', 'citroen/c4-cactus', 'citroen/c4-picasso', 'citroen/c4-spacetourer', 'citroen/c4-x', 'citroen/e-c4-electric', 'citroen/e-c4-x', 'citroen/grand-c4-picasso', 'citroen/grand-c4-spacetourer', 'citroen/c5-(all)', 'citroen/c5', 'citroen/c5-aircross', 'citroen/c5-x', 'citroen/c6', 'citroen/c8', 'citroen/cx', 'citroen/ds', 'citroen/ds3', 'citroen/ds4', 'citroen/ds5', 'citroen/dyane', 'citroen/e-méhari', 'citroen/evasion', 'citroen/gsa', 'citroen/holidays', 'citroen/jumper', 'citroen/jumpy', 'citroen/lna', 'citroen/méhari', 'citroen/nemo', 'citroen/saxo', 'citroen/sm', 'citroen/spacetourer', 'citroen/traction', 'citroen/visa', 'citroen/xantia', 'citroen/xm', 'citroen/xsara', 'citroen/xsara-picasso', 'citroen/zx', 'citroen/others', 'cityel/cityel', 'cityel/cityel-fact-four', 'cityel/miniel', 'cityel/others', 'corvette/c1', 'corvette/c2', 'corvette/c3', 'corvette/c4', 'corvette/c5', 'corvette/c6-convertible', 'corvette/c6-coupe', 'corvette/c7', 'corvette/c8', 'corvette/cz6', 'corvette/grand-sport', 'corvette/stingray', 'corvette/z06', 'corvette/zr1', 'corvette/others', 'cupra/arona', 'cupra/ateca', 'cupra/born', 'cupra/formentor', 'cupra/formentor-vz5', 'cupra/ibiza', 'cupra/leon', 'cupra/tavascan', 'cupra/terramar', 'cupra/others', 'dacia/1310', 'dacia/berlina', 'dacia/break', 'dacia/dokker', 'dacia/double-cab', 'dacia/drop-side', 'dacia/duster', 'dacia/jogger', 'dacia/lodgy', 'dacia/logan', 'dacia/nova', 'dacia/pick-up', 'dacia/sandero', 'dacia/solenza', 'dacia/spring', 'dacia/others', 'daewoo/aranos', 'daewoo/damas', 'daewoo/espero', 'daewoo/evanda', 'daewoo/kalos', 'daewoo/korando', 'daewoo/lacetti', 'daewoo/lanos', 'daewoo/leganza', 'daewoo/lublin', 'daewoo/matiz', 'daewoo/musso', 'daewoo/nexia', 'daewoo/nubira', 'daewoo/rexton', 'daewoo/rezzo', 'daewoo/tacuma', 'daewoo/tico', 'daewoo/truck-plus', 'daewoo/others', 'daf/400', 'daf/428', 'daf/435', 'daf/others', 'daihatsu/applause', 'daihatsu/charade', 'daihatsu/charmant', 'daihatsu/copen', 'daihatsu/cuore', 'daihatsu/domino', 'daihatsu/extol', 'daihatsu/f-modelle', 'daihatsu/feroza', 'daihatsu/freeclimber', 'daihatsu/gran-move', 'daihatsu/hijet', 'daihatsu/materia', 'daihatsu/move', 'daihatsu/pionier', 'daihatsu/rocky', 'daihatsu/sirion', 'daihatsu/taft', 'daihatsu/terios', 'daihatsu/trevis', 'daihatsu/valera', 'daihatsu/yrv', 'daihatsu/others', 'daimler/double-six', 'daimler/six', 'daimler/sovereign', 'daimler/super-eight', 'daimler/super-v8', 'daimler/others', 'dallara/stradale', 'dallara/others', 'dangel/504', 'dangel/505', 'dangel/berlingo', 'dangel/boxer', 'dangel/c15', 'dangel/c25', 'dangel/ducato', 'dangel/expert', 'dangel/j5', 'dangel/jumper', 'dangel/jumpy', 'dangel/partner', 'dangel/scudo', 'dangel/others', 'de-la-chapelle/atalante-57s', 'de-la-chapelle/grand-prix', 'de-la-chapelle/roadster', 'de-la-chapelle/type-55-roadster', 'de-la-chapelle/type-55-tourer', 'de-la-chapelle/others', 'de-tomaso/biguà', 'de-tomaso/deauville', 'de-tomaso/guarà', 'de-tomaso/longchamp', 'de-tomaso/mangusta', 'de-tomaso/pantera', 'de-tomaso/vallelunga', 'de-tomaso/others', 'delorean/dmc-12', 'delorean/others', 'devinci-cars/db-721', 'devinci-cars/others', 'dfsk/c31', 'dfsk/c32', 'dfsk/c35', 'dfsk/c37', 'dfsk/city-pickup', 'dfsk/ec-35', 'dfsk/f5', 'dfsk/fengon', 'dfsk/fengon-5', 'dfsk/fengon-500', 'dfsk/fengon-580', 'dfsk/fengon-7', 'dfsk/glory-580', 'dfsk/glory-ev-3', 'dfsk/k01', 'dfsk/k02', 'dfsk/k05', 'dfsk/k07', 'dfsk/seres-3', 'dfsk/seres-5', 'dfsk/v21', 'dfsk/v22', 'dfsk/v25', 'dfsk/v27', 'dfsk/others', 'dodge/avenger', 'dodge/caliber', 'dodge/caravan', 'dodge/challenger', 'dodge/charger', 'dodge/coronet', 'dodge/dakota', 'dodge/dart', 'dodge/demon', 'dodge/durango', 'dodge/grand-caravan', 'dodge/intrepid', 'dodge/journey', 'dodge/magnum', 'dodge/neon', 'dodge/nitro', 'dodge/ram', 'dodge/stealth', 'dodge/stratus', 'dodge/van', 'dodge/viper', 'dodge/others', 'donkervoort/d8', 'donkervoort/f22', 'donkervoort/s8', 'donkervoort/others', 'dr-automobiles/city-cross', 'dr-automobiles/dr-3.0', 'dr-automobiles/dr-evo5', 'dr-automobiles/dr-f35', 'dr-automobiles/dr-zero', 'dr-automobiles/dr1', 'dr-automobiles/dr1.0', 'dr-automobiles/dr2', 'dr-automobiles/dr3', 'dr-automobiles/dr4', 'dr-automobiles/dr4.0', 'dr-automobiles/dr5', 'dr-automobiles/dr5.0', 'dr-automobiles/dr6', 'dr-automobiles/dr6.0', 'dr-automobiles/dr7.0', 'dr-automobiles/katay', 'dr-automobiles/pk8', 'dr-automobiles/others', 'ds-automobiles/ds-3', 'ds-automobiles/ds-3-crossback', 'ds-automobiles/ds-4', 'ds-automobiles/ds-4-crossback', 'ds-automobiles/ds-5', 'ds-automobiles/ds-7', 'ds-automobiles/ds-7-crossback', 'ds-automobiles/ds-9', 'ds-automobiles/others', 'dutton/b-plus', 'dutton/b-plus-series-2', 'dutton/b-type', 'dutton/beneto', 'dutton/cantera', 'dutton/legerra', 'dutton/malaga', 'dutton/malaga-b+', 'dutton/melos', 'dutton/p1', 'dutton/phaeton-series-1', 'dutton/phaeton-series-2', 'dutton/phaeton-series-3', 'dutton/phaeton-series-4', 'dutton/rico', 'dutton/rico-shuttle', 'dutton/sierra-drop-head', 'dutton/sierra-series-1', 'dutton/sierra-series-2', 'dutton/sierra-series-3', 'dutton/others', 'e.go/e.wave-x', 'e.go/life-20', 'e.go/life-40', 'e.go/life-60', 'e.go/life-first-edition', 'e.go/mover', 'e.go/others', 'econelo/m1', 'econelo/s1', 'econelo/others', 'edran/mk1', 'edran/others', 'elaris/beo', 'elaris/caro', 'elaris/caro-s', 'elaris/dyo', 'elaris/finn', 'elaris/jaco', 'elaris/lenn', 'elaris/pio', 'elaris/others', 'embuggy/ev-angel', 'embuggy/eva', 'embuggy/vintage', 'embuggy/others', 'emc/wave-2', 'emc/wave-3', 'emc/yudo', 'emc/others', 'emc/wave-2', 'emc/wave-3', 'emc/yudo', 'emc/others', 'estrima/birò', 'estrima/others', 'evetta/openair', 'evetta/prima', 'evetta/others', 'evo/cross4', 'evo/evo-electric', 'evo/evo3', 'evo/evo4', 'evo/evo5', 'evo/evo6', 'evo/evo7', 'evo/others', 'ferrari/12-cilindri', 'ferrari/195', 'ferrari/206', 'ferrari/208', 'ferrari/246', 'ferrari/250', 'ferrari/275', 'ferrari/288', 'ferrari/296', 'ferrari/296-gtb', 'ferrari/308', 'ferrari/328', 'ferrari/330', 'ferrari/348', 'ferrari/360', 'ferrari/365', 'ferrari/400', 'ferrari/412', 'ferrari/430-scuderia', 'ferrari/456', 'ferrari/458', 'ferrari/488', 'ferrari/512', 'ferrari/550', 'ferrari/575', 'ferrari/599', 'ferrari/612', 'ferrari/750', 'ferrari/812', 'ferrari/california', 'ferrari/daytona', 'ferrari/dino-gt4', 'ferrari/enzo-ferrari', 'ferrari/f12', 'ferrari/f355', 'ferrari/f40', 'ferrari/f430', 'ferrari/f50', 'ferrari/f512', 'ferrari/f8-spider', 'ferrari/f8-tributo', 'ferrari/ff', 'ferrari/fxx', 'ferrari/gtc4-lusso', 'ferrari/laferrari', 'ferrari/mondial', 'ferrari/monza', 'ferrari/portofino', 'ferrari/purosangue', 'ferrari/roma', 'ferrari/scuderia-spider-16m', 'ferrari/sf90-spider', 'ferrari/sf90-stradale', 'ferrari/superamerica', 'ferrari/testarossa', 'ferrari/others', 'fiat/124-coupè', 'fiat/124-spider', 'fiat/126', 'fiat/127', 'fiat/128', 'fiat/130', 'fiat/131', 'fiat/132', 'fiat/133', 'fiat/2300', 'fiat/242', 'fiat/500', 'fiat/500-abarth', 'fiat/500c', 'fiat/500c-abarth', 'fiat/500e', 'fiat/500l', 'fiat/500x', 'fiat/595-abarth', 'fiat/600', 'fiat/850', 'fiat/900', 'fiat/albea', 'fiat/argenta', 'fiat/barchetta', 'fiat/brava', 'fiat/bravo', 'fiat/campagnola', 'fiat/cinquecento', 'fiat/coupe', 'fiat/croma', 'fiat/dino', 'fiat/doblo', 'fiat/doblo', 'fiat/e-doblo', 'fiat/ducato', 'fiat/duna', 'fiat/e-ulysse', 'fiat/fiorino', 'fiat/freemont', 'fiat/fullback', 'fiat/grande-punto', 'fiat/idea', 'fiat/linea', 'fiat/marea', 'fiat/marengo', 'fiat/maxi', 'fiat/multipla', 'fiat/new-panda', 'fiat/palio', 'fiat/panda', 'fiat/penny', 'fiat/pininfarina', 'fiat/punto', 'fiat/punto-evo', 'fiat/qubo', 'fiat/regata', 'fiat/ritmo', 'fiat/scudo', 'fiat/sedici', 'fiat/seicento', 'fiat/spider-europa', 'fiat/stilo', 'fiat/strada', 'fiat/talento', 'fiat/tempra', 'fiat/tipo', 'fiat/topolino', 'fiat/ulysse', 'fiat/uno', 'fiat/x-1/9', 'fiat/others', 'fisker/emotion', 'fisker/karma', 'fisker/latigo-cs', 'fisker/ocean', 'fisker/orbit', 'fisker/others', 'forthing/t5-evo', 'forthing/u-tour', 'forthing/others', 'foton/tunland-g7', 'foton/others', 'gac-gonow/ga200', 'gac-gonow/ga500', 'gac-gonow/gx6', 'gac-gonow/troy', 'gac-gonow/victor', 'gac-gonow/victory', 'gac-gonow/way', 'gac-gonow/others', 'galloper/exceed', 'galloper/galloper', 'galloper/santamo', 'galloper/super-exceed', 'galloper/others', 'gappy/triple-dutch', 'gappy/others', 'gaz/22171', 'gaz/22177', 'gaz/2310', 'gaz/24', 'gaz/2401', 'gaz/2402', 'gaz/2404', 'gaz/2410', 'gaz/2411', 'gaz/2412', 'gaz/2434', 'gaz/2705', 'gaz/2752', 'gaz/31', 'gaz/3102', 'gaz/31022', 'gaz/310221', 'gaz/31026', 'gaz/31029', 'gaz/3105', 'gaz/3110', 'gaz/31105', 'gaz/3111', 'gaz/3221', 'gaz/3302', 'gaz/33023', 'gaz/38407', 'gaz/38649', 'gaz/38710', 'gaz/gazelle', 'gaz/next', 'gaz/siber', 'gaz/sobol', 'gaz/others', 'gem/e2', 'gem/e4', 'gem/e6', 'gem/el', 'gem/em', 'gem/es', 'gem/four', 'gem/two', 'gem/others', 'gemballa/aero', 'gemballa/avalanche', 'gemballa/gt', 'gemballa/gtp', 'gemballa/mig', 'gemballa/mirage', 'gemballa/mistrale', 'gemballa/tornado', 'gemballa/others', 'genesis/electrified-g80', 'genesis/g70', 'genesis/g70-shooting-brake', 'genesis/g80', 'genesis/g90', 'genesis/gv60', 'genesis/gv70', 'genesis/gv80', 'genesis/others', 'giana/smart-3500', 'giana/others', 'gillet/donkervoort', 'gillet/vertigo', 'gillet/others', 'giotti-victoria/gladiator', 'giotti-victoria/gyppo', 'giotti-victoria/others', 'gmc/acadia', 'gmc/canyon', 'gmc/envoy', 'gmc/safari', 'gmc/savana', 'gmc/sierra', 'gmc/sonoma', 'gmc/syclone', 'gmc/terrain', 'gmc/typhoon', 'gmc/vandura', 'gmc/yukon', 'gmc/others', 'goupil/g1', 'goupil/g4', 'goupil/g5', 'goupil/gem', 'goupil/others', 'great-wall/c20', 'great-wall/c30', 'great-wall/c50', 'great-wall/coolbear', 'great-wall/cowry', 'great-wall/deer', 'great-wall/florid', 'great-wall/gwperi', 'great-wall/h5e', 'great-wall/h6', 'great-wall/hover', 'great-wall/m4', 'great-wall/pegasus', 'great-wall/safe', 'great-wall/sailor', 'great-wall/sing', 'great-wall/socool', 'great-wall/steed', 'great-wall/voleex', 'great-wall/wingle', 'great-wall/others', 'grecav/amica', 'grecav/eke', 'grecav/sonique', 'grecav/others', 'gta/spano', 'gta/others', 'gwm/ora-03', 'gwm/ora-07', 'gwm/wey-03', 'gwm/wey-05', 'gwm/others', 'haima/2', 'haima/3', 'haima/3-hb', 'haima/6', 'haima/family', 'haima/freema', 'haima/fstar', 'haima/m3', 'haima/m5', 'haima/s5', 'haima/s7', 'haima/v70', 'haima/others', 'hamann/others', 'haval/h2', 'haval/h6', 'haval/h9', 'haval/others', 'hiphi/a', 'hiphi/x', 'hiphi/y', 'hiphi/z', 'hiphi/others', 'holden/coupe-60', 'holden/gtr-x', 'holden/hurricane', 'holden/monaro-convertible', 'holden/monaro-coupe', 'holden/monaro-hrt-427', 'holden/sandman', 'holden/ssx', 'holden/torana-tt36', 'holden/utester', 'holden/others', 'honda/accord', 'honda/ascot', 'honda/avancier', 'honda/beat', 'honda/capa', 'honda/city', 'honda/civic', 'honda/clarity', 'honda/concerto', 'honda/cr-v', 'honda/cr-z', 'honda/crosstour', 'honda/crx', 'honda/e', 'honda/e:ny1', 'honda/element', 'honda/fit', 'honda/fr-v', 'honda/hr-v', 'honda/insight', 'honda/inspire', 'honda/integra', 'honda/jazz', 'honda/legend', 'honda/life', 'honda/logo', 'honda/mobilio', 'honda/nsx', 'honda/odyssey', 'honda/orthia', 'honda/partner', 'honda/pilot', 'honda/prelude', 'honda/quintet', 'honda/ridgeline', 'honda/s-2000', 'honda/saber', 'honda/sabre', 'honda/shuttle', 'honda/sm-x', 'honda/stepwgn', 'honda/stream', 'honda/torneo', 'honda/zr-v', 'honda/others', 'hongqi/e-hs9', 'hongqi/others', 'hongqi/e-hs9', 'hongqi/others', 'hummer/h1', 'hummer/h2', 'hummer/h3', 'hummer/hx', 'hummer/others', 'hurtan/albaycín', 'hurtan/author', 'hurtan/grand-albaycín', 'hurtan/route-44', 'hurtan/t2', 'hurtan/vintage', 'hurtan/others', 'hyundai/accent', 'hyundai/atos', 'hyundai/avente', 'hyundai/azera', 'hyundai/bayon', 'hyundai/coupe', 'hyundai/creta', 'hyundai/elantra', 'hyundai/equus', 'hyundai/excel', 'hyundai/galloper', 'hyundai/genesis', 'hyundai/genesis-coupe', 'hyundai/getz', 'hyundai/grace', 'hyundai/grand-santa-fe', 'hyundai/grandeur', 'hyundai/h-100', 'hyundai/h-200', 'hyundai/h-300', 'hyundai/h-350', 'hyundai/h-1', 'hyundai/highway', 'hyundai/i10', 'hyundai/i20', 'hyundai/i30', 'hyundai/i40', 'hyundai/i50', 'hyundai/i800', 'hyundai/ioniq', 'hyundai/ioniq-5', 'hyundai/ioniq-6', 'hyundai/ix20', 'hyundai/ix35', 'hyundai/ix55', 'hyundai/kona', 'hyundai/lantra', 'hyundai/matrix', 'hyundai/nexo', 'hyundai/nf', 'hyundai/palisade', 'hyundai/pony', 'hyundai/porter', 'hyundai/s-coupe', 'hyundai/santa-fe', 'hyundai/santamo', 'hyundai/satellite', 'hyundai/solaris', 'hyundai/sonata', 'hyundai/sonica', 'hyundai/starex', 'hyundai/staria', 'hyundai/stellar', 'hyundai/terracan', 'hyundai/tiburon', 'hyundai/trajet', 'hyundai/tucson', 'hyundai/veloster', 'hyundai/veracruz', 'hyundai/verna', 'hyundai/xg-250', 'hyundai/xg-30', 'hyundai/xg-350', 'hyundai/others', 'ich-x/k2', 'ich-x/others', 'ineos/grenadier', 'ineos/others', 'infiniti/ex25', 'infiniti/ex30', 'infiniti/ex35', 'infiniti/ex37', 'infiniti/fx', 'infiniti/g25', 'infiniti/g35', 'infiniti/g37', 'infiniti/i35', 'infiniti/jx35', 'infiniti/m30', 'infiniti/m35', 'infiniti/m37', 'infiniti/m45', 'infiniti/q30', 'infiniti/q45', 'infiniti/q50', 'infiniti/q60', 'infiniti/q70', 'infiniti/q80', 'infiniti/qx30', 'infiniti/qx50', 'infiniti/qx56', 'infiniti/qx60', 'infiniti/qx70', 'infiniti/qx80', 'infiniti/others', 'innocenti/clip', 'innocenti/elba', 'innocenti/mille', 'innocenti/mini', 'innocenti/minitre', 'innocenti/small', 'innocenti/others', 'iso-rivolta/300', 'iso-rivolta/fidia', 'iso-rivolta/grifo', 'iso-rivolta/lele', 'iso-rivolta/vision-gt', 'iso-rivolta/others', 'isuzu/axiom', 'isuzu/bighorn', 'isuzu/campo', 'isuzu/d-max', 'isuzu/dlx', 'isuzu/gemini', 'isuzu/midi', 'isuzu/nkr', 'isuzu/nnr', 'isuzu/npr', 'isuzu/pick-up', 'isuzu/rodeo', 'isuzu/trooper', 'isuzu/wfr', 'isuzu/others', 'iveco/campagnola', 'iveco/daily', 'iveco/massif', 'iveco/others', 'izh/2106', 'izh/2125', 'izh/21251', 'izh/2126', 'izh/21261', 'izh/2715', 'izh/27156', 'izh/2717', 'izh/27171', 'izh/412', 'izh/nika', 'izh/others', 'jac/e-s2', 'jac/e-s4', 'jac/j7', 'jac/js3', 'jac/js4', 'jac/js7', 'jac/t8', 'jac/others', 'jaecoo/j6', 'jaecoo/j7', 'jaecoo/others', 'jaguar/420', 'jaguar/d-type', 'jaguar/daimler', 'jaguar/e-pace', 'jaguar/e-type', 'jaguar/f-pace', 'jaguar/f-type', 'jaguar/i-pace', 'jaguar/mk-ii', 'jaguar/s-type', 'jaguar/sovereign', 'jaguar/x-type', 'jaguar/x300', 'jaguar/xe', 'jaguar/xf', 'jaguar/xj', 'jaguar/xj12', 'jaguar/xj40', 'jaguar/xj6', 'jaguar/xj8', 'jaguar/xjr', 'jaguar/xjs', 'jaguar/xjsc', 'jaguar/xk', 'jaguar/xk8', 'jaguar/xkr', 'jaguar/others', 'jeep/avenger', 'jeep/cherokee', 'jeep/cj-5', 'jeep/cj-7', 'jeep/cj-8', 'jeep/comanche', 'jeep/commander', 'jeep/compass', 'jeep/gladiator', 'jeep/grand-cherokee', 'jeep/liberty', 'jeep/patriot', 'jeep/renegade', 'jeep/wagoneer', 'jeep/willys', 'jeep/wrangler', 'jeep/others', 'jensen/541', 'jensen/c-v8', 'jensen/convertible', 'jensen/coupé', 'jensen/ff', 'jensen/gt', 'jensen/healey-mk.1', 'jensen/healey-mk.2', 'jensen/interceptor', 'jensen/mk-ii', 'jensen/mk-iii', 'jensen/mk-iv', 'jensen/s-v8', 'jensen/sp', 'jensen/others', 'karma/gs-6', 'karma/gse-6', 'karma/pininfarina-gt', 'karma/revero', 'karma/revero-gt', 'karma/others', 'kg-mobility/actyon', 'kg-mobility/family', 'kg-mobility/kallista', 'kg-mobility/korando', 'kg-mobility/kyron', 'kg-mobility/musso', 'kg-mobility/rexton', 'kg-mobility/rodius', 'kg-mobility/tivoli', 'kg-mobility/torres', 'kg-mobility/xlv', 'kg-mobility/others', 'kia/besta', 'kia/carens', 'kia/carnival', "kia/ceed-/-cee'd", "kia/ceed-sw-/-cee'd-sw", 'kia/cerato', 'kia/clarus', 'kia/e-niro', 'kia/elan', 'kia/ev6', 'kia/ev9', 'kia/joice', 'kia/k2500', 'kia/k2700', 'kia/k2900', 'kia/leo', 'kia/magentis', 'kia/mentor', 'kia/mohave/borrego', 'kia/niro', 'kia/opirus', 'kia/optima', 'kia/picanto', 'kia/pregio', 'kia/pride', "kia/proceed-/-pro_cee'd", 'kia/retona', 'kia/rio', 'kia/roadster', 'kia/rocsta', 'kia/sephia', 'kia/shuma', 'kia/sorento', 'kia/soul', 'kia/spectra', 'kia/sportage', 'kia/stinger', 'kia/stonic', 'kia/venga', 'kia/xceed', 'kia/others', 'koenigsegg/agera', 'koenigsegg/cc', 'koenigsegg/jesko', 'koenigsegg/one:1', 'koenigsegg/regera', 'koenigsegg/others', 'ktm/x-bow-gt', 'ktm/x-bow-gt4', 'ktm/x-bow-r', 'ktm/x-bow-rr', 'ktm/x-bow-street', 'ktm/others', 'lada/110', 'lada/111', 'lada/112', 'lada/1200', 'lada/1300/1500/1600', 'lada/2106', 'lada/4x4', 'lada/aleko', 'lada/c-cross', 'lada/carlota', 'lada/forma', 'lada/granta', 'lada/kalina', 'lada/largus', 'lada/natacha', 'lada/niva', 'lada/nova', 'lada/priora', 'lada/sagona', 'lada/samara', 'lada/sprint', 'lada/taiga', 'lada/universal', 'lada/urban', 'lada/vaz-215', 'lada/vesta', 'lada/x-ray', 'lada/others', 'lamborghini/asterion', 'lamborghini/aventador', 'lamborghini/centenario', 'lamborghini/countach', 'lamborghini/diablo', 'lamborghini/espada', 'lamborghini/estoque', 'lamborghini/gallardo', 'lamborghini/huracán', 'lamborghini/jalpa', 'lamborghini/lm', 'lamborghini/miura', 'lamborghini/murciélago', 'lamborghini/reventon', 'lamborghini/revuelto', 'lamborghini/sian-fkp-37', 'lamborghini/terzo-millennio', 'lamborghini/urraco-p250', 'lamborghini/urus', 'lamborghini/veneno', 'lamborghini/others', 'lancia/a-112', 'lancia/appia', 'lancia/beta', 'lancia/dedra', 'lancia/delta', 'lancia/flaminia', 'lancia/flavia', 'lancia/fulvia', 'lancia/gamma', 'lancia/hpe', 'lancia/k', 'lancia/kappa', 'lancia/lybra', 'lancia/musa', 'lancia/phedra', 'lancia/prisma', 'lancia/stratos', 'lancia/thema', 'lancia/thesis', 'lancia/trevi', 'lancia/voyager', 'lancia/y', 'lancia/ypsilon', 'lancia/z', 'lancia/zeta', 'lancia/others', 'land-rover/defender', 'land-rover/discovery', 'land-rover/discovery-sport', 'land-rover/freelander', 'land-rover/lrx', 'land-rover/range-rover', 'land-rover/range-rover-evoque', 'land-rover/range-rover-sport', 'land-rover/range-rover-velar', 'land-rover/series', 'land-rover/others', 'ldv/convoy', 'ldv/maxus', 'ldv/others', 'leapmotor/c10', 'leapmotor/t03', 'leapmotor/others', 'levc/tx', 'levc/vn5', 'levc/others', 'lexus/ct-200h', 'lexus/es-series-(all)', 'lexus/es-300', 'lexus/es-330', 'lexus/es-350', 'lexus/gs-series-(all)', 'lexus/gs-200t', 'lexus/gs-250', 'lexus/gs-300', 'lexus/gs-350', 'lexus/gs-430', 'lexus/gs-450h', 'lexus/gs-460', 'lexus/gs-f', 'lexus/gx-series-(all)', 'lexus/gx-460', 'lexus/gx-470', 'lexus/is-series-(all)', 'lexus/is-200', 'lexus/is-220d', 'lexus/is-250', 'lexus/is-300', 'lexus/is-350', 'lexus/is-f', 'lexus/lbx', 'lexus/lc-series-(all)', 'lexus/lc-500', 'lexus/lc-500h', 'lexus/lc-f', 'lexus/lfa', 'lexus/lm', 'lexus/ls-series-(all)', 'lexus/ls-400', 'lexus/ls-430', 'lexus/ls-460', 'lexus/ls-500', 'lexus/ls-600', 'lexus/lx-series-(all)', 'lexus/lx-450d', 'lexus/lx-470', 'lexus/lx-500d', 'lexus/lx-570', 'lexus/lx-600', 'lexus/nx-series-(all)', 'lexus/nx-200t', 'lexus/nx-300', 'lexus/nx-300h', 'lexus/nx-350h', 'lexus/nx-450h+', 'lexus/rc-series-(all)', 'lexus/rc-200t', 'lexus/rc-300h', 'lexus/rc-350', 'lexus/rc-f', 'lexus/rx-series-(all)', 'lexus/rx-200t', 'lexus/rx-300', 'lexus/rx-330', 'lexus/rx-350', 'lexus/rx-350h', 'lexus/rx-400', 'lexus/rx-450h', 'lexus/rx-500h', 'lexus/rz', 'lexus/sc-series-(all)', 'lexus/sc-400', 'lexus/sc-430', 'lexus/ux-series-(all)', 'lexus/ux-200', 'lexus/ux-250h', 'lexus/ux-300e', 'lexus/ux-300h', 'lexus/others', 'lifan/1022', 'lifan/1025', 'lifan/330ev', 'lifan/650', 'lifan/650ev', 'lifan/820', 'lifan/breez-(520)', 'lifan/c30e', 'lifan/c32e', 'lifan/foison', 'lifan/m7', 'lifan/seasion', 'lifan/smily', 'lifan/solano-(620)', 'lifan/x50', 'lifan/x7', 'lifan/x70', 'lifan/x80', 'lifan/others', 'ligier/162', 'ligier/ambra', 'ligier/be-sun', 'ligier/be-two', 'ligier/be-up', 'ligier/due', 'ligier/ixo', 'ligier/js-50', 'ligier/js-60', 'ligier/myli', 'ligier/nova', 'ligier/optima', 'ligier/optimax', 'ligier/prima', 'ligier/x-pro', 'ligier/x-too', 'ligier/others', 'lincoln/aviator', 'lincoln/continental', 'lincoln/corsair', 'lincoln/cosmopolitan', 'lincoln/ls', 'lincoln/mark', 'lincoln/mkc', 'lincoln/mkt', 'lincoln/mkx', 'lincoln/mkz', 'lincoln/nautilus', 'lincoln/navigator', 'lincoln/town-car', 'lincoln/zephyr', 'lincoln/others', 'linzda/m3', 'linzda/others', 'lorinser/a-klasse', 'lorinser/b-klasse', 'lorinser/c-klasse', 'lorinser/e-klasse', 'lorinser/g-klasse', 'lorinser/gla', 'lorinser/glb', 'lorinser/glc', 'lorinser/gle', 'lorinser/puch', 'lorinser/s-klasse', 'lorinser/sl', 'lorinser/smart', 'lorinser/others', 'lotus/2-eleven', 'lotus/3-eleven', 'lotus/340-r', 'lotus/cortina', 'lotus/elan', 'lotus/eletre', 'lotus/elise', 'lotus/elite', 'lotus/emeya', 'lotus/emira', 'lotus/esprit', 'lotus/europa', 'lotus/evija', 'lotus/evora', 'lotus/excel', 'lotus/exige', 'lotus/omega', 'lotus/super-seven', 'lotus/type-130', 'lotus/v8', 'lotus/venturi', 'lotus/others', 'lucid/air', 'lucid/others', 'lynk-&-co/01', 'lynk-&-co/others', 'm-ero/microlino', 'm-ero/others', 'mahindra/alturas-g4', 'mahindra/bolero', 'mahindra/cj', 'mahindra/genio', 'mahindra/goa', 'mahindra/jeep', 'mahindra/kuv100', 'mahindra/marazzo', 'mahindra/nuvosport', 'mahindra/quanto', 'mahindra/reva', 'mahindra/scorpio', 'mahindra/thar', 'mahindra/tuv300', 'mahindra/verito', 'mahindra/xuv300', 'mahindra/xuv500', 'mahindra/xylo', 'mahindra/others', 'man/tge', 'man/others', 'mansory/aston-martin-(all)', 'mansory/aston-martin---cyrus', 'mansory/aston-martin---db9', 'mansory/aston-martin---vanquish', 'mansory/aston-martin---vantage', 'mansory/audi---r8', 'mansory/bentley-(all)', 'mansory/bentley---continental-gt', 'mansory/bentley---flying-spur', 'mansory/bentley---le-mansory', 'mansory/bentley---vitesse-rosé', 'mansory/bmw-(all)', 'mansory/bmw---7', 'mansory/bmw---x5', 'mansory/bmw---x6', 'mansory/bugatti---veyron', 'mansory/ferrari-(all)', 'mansory/ferrari---458', 'mansory/ferrari---599-gtb', 'mansory/ferrari---f12', 'mansory/ferrari---la-revoluzione', 'mansory/ferrari---siracusa', 'mansory/land-rover---range-rover', 'mansory/lotus-(all)', 'mansory/lotus---elise', 'mansory/lotus---evora', 'mansory/maserati-(all)', 'mansory/maserati---ghibli', 'mansory/maserati---gran-turismo', 'mansory/mclaren---12c', 'mansory/mercedes-benz-(all)', 'mansory/mercedes-benz---c', 'mansory/mercedes-benz---cls', 'mansory/mercedes-benz---e', 'mansory/mercedes-benz---g', 'mansory/mercedes-benz---gl', 'mansory/mercedes-benz---m', 'mansory/mercedes-benz---ml', 'mansory/mercedes-benz---s', 'mansory/mercedes-benz---sl', 'mansory/mercedes-benz---slk', 'mansory/mercedes-benz---slr', 'mansory/mercedes-benz---sls', 'mansory/mercedes-benz---v', 'mansory/mercedes-benz---viano', 'mansory/porsche-(all)', 'mansory/porsche---918', 'mansory/porsche---991', 'mansory/porsche---997', 'mansory/porsche---cayenne', 'mansory/porsche---macan', 'mansory/porsche---panamera', 'mansory/rolls-royce-(all)', 'mansory/rolls-royce---ghost', 'mansory/rolls-royce---phantom', 'mansory/rolls-royce---wraith', 'mansory/tesla---model-s', 'mansory/others', 'martin/cobra', 'martin/roadster', 'martin/others', 'martin-motors/bubble', 'martin-motors/ceo', 'martin-motors/coolcar', 'martin-motors/mm520', 'martin-motors/mm620', 'martin-motors/others', 'maserati/222', 'maserati/224', 'maserati/228', 'maserati/3200', 'maserati/418', 'maserati/420', 'maserati/4200', 'maserati/422', 'maserati/424', 'maserati/430', 'maserati/alfieri', 'maserati/biturbo', 'maserati/bora', 'maserati/coupe', 'maserati/ghibli', 'maserati/grancabrio', 'maserati/gransport', 'maserati/granturismo', 'maserati/grecale', 'maserati/indy', 'maserati/karif', 'maserati/levante', 'maserati/mc12', 'maserati/mc20', 'maserati/merak', 'maserati/quattroporte', 'maserati/racing', 'maserati/shamal', 'maserati/spyder', 'maserati/tc', 'maserati/others', 'matra/530', 'matra/others', 'maxus/deliver-9', 'maxus/edeliver-3', 'maxus/edeliver-7', 'maxus/edeliver-9', 'maxus/eg10', 'maxus/euniq-5', 'maxus/euniq-6', 'maxus/ev80', 'maxus/g10', 'maxus/mifa-9', 'maxus/rv80', 'maxus/t60', 'maxus/t90', 'maxus/v80', 'maxus/others', 'maybach/57', 'maybach/62', 'maybach/pullman', 'maybach/others', 'mazda/121', 'mazda/2', 'mazda/3', 'mazda/323', 'mazda/5', 'mazda/6', 'mazda/626', 'mazda/929', 'mazda/atenza', 'mazda/axela', 'mazda/b-series', 'mazda/bongo', 'mazda/bt-50', 'mazda/capella', 'mazda/cx-3', 'mazda/cx-30', 'mazda/cx-5', 'mazda/cx-60', 'mazda/cx-7', 'mazda/cx-80', 'mazda/cx-9', 'mazda/demio', 'mazda/e-series', 'mazda/familia', 'mazda/millenia', 'mazda/mpv', 'mazda/mx-3', 'mazda/mx-30', 'mazda/mx-5', 'mazda/mx-6', 'mazda/pick-up', 'mazda/premacy', 'mazda/protege', 'mazda/rx-7', 'mazda/rx-8', 'mazda/rx-9', 'mazda/tribute', 'mazda/xedos', 'mazda/others', 'mclaren/12-c', 'mclaren/540c', 'mclaren/570gt', 'mclaren/570s', 'mclaren/600lt', 'mclaren/620r', 'mclaren/650s-coupe', 'mclaren/650s-spider', 'mclaren/675lt', 'mclaren/720s', 'mclaren/750s', 'mclaren/765lt-coupe', 'mclaren/765lt-spider', 'mclaren/artura', 'mclaren/elva', 'mclaren/f1', 'mclaren/gt', 'mclaren/mp4-12c', 'mclaren/p1', 'mclaren/senna', 'mclaren/speedtail', 'mclaren/others', 'mega/break', 'mega/cabriolet', 'mega/club', 'mega/fourgon-vitre', 'mega/maxi-concept', 'mega/others', 'melex/148', 'melex/329', 'melex/341', 'melex/343', 'melex/345', 'melex/363', 'melex/364', 'melex/366', 'melex/374', 'melex/378', 'melex/379', 'melex/381', 'melex/385', 'melex/391', 'melex/392', 'melex/395', 'melex/423', 'melex/427', 'melex/433', 'melex/435', 'melex/443', 'melex/445', 'melex/447', 'melex/463', 'melex/464', 'melex/465', 'melex/466', 'melex/469', 'melex/563', 'melex/565', 'melex/627', 'melex/833', 'melex/835', 'melex/843', 'melex/845', 'melex/848', 'melex/860', 'melex/861', 'melex/864', 'melex/865', 'melex/943', 'melex/945', 'melex/947', 'melex/960', 'melex/961', 'melex/962', 'melex/963', 'melex/964', 'melex/965', 'melex/966', 'melex/967', 'melex/968', 'melex/969', 'melex/986', 'melex/others', 'mercury/marquis', 'mercury/sable', 'mercury/villager', 'mercury/others', 'mg/ehs', 'mg/hs', 'mg/marvel-r', 'mg/metro', 'mg/mg3', 'mg/mg4', 'mg/mg5', 'mg/mga', 'mg/mgb', 'mg/mgc', 'mg/mgf', 'mg/midget', 'mg/rv8', 'mg/td', 'mg/tf', 'mg/zr', 'mg/zs', 'mg/zt', 'mg/others', 'micro/microlino', 'micro/others', 'microcar/cargo', 'microcar/due', 'microcar/ecology/lyra', 'microcar/flex', 'microcar/m.cross', 'microcar/m.go', 'microcar/m8', 'microcar/mc1', 'microcar/mc2', 'microcar/sherpa', 'microcar/virgo', 'microcar/others', 'militem/ferox', 'militem/ferox-adventure', 'militem/ferox-t', 'militem/hero', 'militem/magnum', 'militem/others', 'minari/berlinetta', 'minari/rs-mk2', 'minari/others', 'minauto/access', 'minauto/cross', 'minauto/gt', 'minauto/minauto', 'minauto/others', 'mini/1000', 'mini/1300', 'mini/3/5-doors', 'mini/cooper', 'mini/cooper-d', 'mini/cooper-s', 'mini/cooper-sd', 'mini/cooper-se', 'mini/john-cooper-works', 'mini/one', 'mini/one-d', 'mini/aceman', 'mini/cabrio-series-(all)', 'mini/cooper-cabrio', 'mini/cooper-d-cabrio', 'mini/cooper-s-cabrio', 'mini/cooper-sd-cabrio', 'mini/john-cooper-works-cabrio', 'mini/one-cabrio', 'mini/clubman-series-(all)', 'mini/cooper-clubman', 'mini/cooper-d-clubman', 'mini/cooper-s-clubman', 'mini/cooper-sd-clubman', 'mini/john-cooper-works-clubman', 'mini/one-clubman', 'mini/one-d-clubman', 'mini/clubvan', 'mini/countryman-series-(all)', 'mini/cooper-countryman', 'mini/cooper-d-countryman', 'mini/cooper-s-countryman', 'mini/cooper-sd-countryman', 'mini/cooper-se-countryman', 'mini/countryman-c', 'mini/countryman-d', 'mini/countryman-s-all4', 'mini/jcw-countryman-all4', 'mini/john-cooper-works-countryman', 'mini/one-countryman', 'mini/one-d-countryman', 'mini/coupé-series-(all)', 'mini/cooper-coupe', 'mini/cooper-d-coupe', 'mini/cooper-s-coupe', 'mini/cooper-sd-coupe', 'mini/john-cooper-works-coupe', 'mini/paceman-series-(all)', 'mini/cooper-d-paceman', 'mini/cooper-paceman', 'mini/cooper-s-paceman', 'mini/cooper-sd-paceman', 'mini/john-cooper-works-paceman', 'mini/roadster-series-(all)', 'mini/cooper-roadster', 'mini/cooper-s-roadster', 'mini/cooper-sd-roadster', 'mini/john-cooper-works-roadster', 'mini/others', 'mitsubishi/3000-gt', 'mitsubishi/400', 'mitsubishi/airtrek', 'mitsubishi/asx', 'mitsubishi/attrage', 'mitsubishi/canter', 'mitsubishi/carisma', 'mitsubishi/chariot', 'mitsubishi/colt', 'mitsubishi/cordia', 'mitsubishi/cosmos', 'mitsubishi/delica', 'mitsubishi/diamante', 'mitsubishi/dingo', 'mitsubishi/dion', 'mitsubishi/eclipse', 'mitsubishi/eclipse-cross', 'mitsubishi/fto', 'mitsubishi/galant', 'mitsubishi/galloper', 'mitsubishi/grandis', 'mitsubishi/i-miev', 'mitsubishi/l200', 'mitsubishi/l300', 'mitsubishi/l400', 'mitsubishi/lancer', 'mitsubishi/legnum', 'mitsubishi/libero', 'mitsubishi/mirage', 'mitsubishi/montero', 'mitsubishi/outlander', 'mitsubishi/pajero', 'mitsubishi/pajero-pinin', 'mitsubishi/pajero-sport', 'mitsubishi/pick-up', 'mitsubishi/rvr', 'mitsubishi/santamo', 'mitsubishi/sapporo', 'mitsubishi/shogun', 'mitsubishi/sigma', 'mitsubishi/space-gear', 'mitsubishi/space-runner', 'mitsubishi/space-star', 'mitsubishi/space-wagon', 'mitsubishi/starion', 'mitsubishi/tredia', 'mitsubishi/others', 'mitsuoka/galue', 'mitsuoka/himiko', 'mitsuoka/like-t3', 'mitsuoka/rock-star', 'mitsuoka/ryugi', 'mitsuoka/viewt', 'mitsuoka/others', 'morgan/100-years-special', 'morgan/3-wheeler', 'morgan/4-sitzer', 'morgan/4/4', 'morgan/aero-8', 'morgan/aero-coupe', 'morgan/aero-max', 'morgan/aero-supersports', 'morgan/ev3', 'morgan/eva-gt', 'morgan/lifecar', 'morgan/plus-4', 'morgan/plus-8', 'morgan/plus-e', 'morgan/plus-six', 'morgan/roadster', 'morgan/supersport-pedal', 'morgan/others', 'moskvich/21215', 'moskvich/2137', 'moskvich/2138', 'moskvich/2140', 'moskvich/21406', 'moskvich/2141', 'moskvich/21412', 'moskvich/214145', 'moskvich/2142', 'moskvich/2335', 'moskvich/2901', 'moskvich/408', 'moskvich/412', 'moskvich/426', 'moskvich/427', 'moskvich/434', 'moskvich/duet', 'moskvich/ivan-kalita', 'moskvich/jurij-dolgorukij', 'moskvich/knjaz-vladimir', 'moskvich/svjatogor', 'moskvich/others', 'mp-lafer/lafer', 'mp-lafer/others', 'mpm-motors/erelis', 'mpm-motors/ps160', 'mpm-motors/others', 'nio/el6', 'nio/el7', 'nio/el8', 'nio/et5', 'nio/et7', 'nio/others', 'nissan/100-nx', 'nissan/200-sx', 'nissan/280-zx', 'nissan/300-zx', 'nissan/350z', 'nissan/370z', 'nissan/ad', 'nissan/almera', 'nissan/almera-tino', 'nissan/altima', 'nissan/ariya', 'nissan/armada', 'nissan/avenir', 'nissan/bassara', 'nissan/bluebird', 'nissan/cabstar', 'nissan/cargo', 'nissan/cedric', 'nissan/cefiro', 'nissan/cherry', 'nissan/cube', 'nissan/datsun', 'nissan/e-nv200', 'nissan/elgrand', 'nissan/evalia', 'nissan/expert', 'nissan/figaro', 'nissan/frontier', 'nissan/gloria', 'nissan/gt-r', 'nissan/interstar', 'nissan/juke', 'nissan/king-cab', 'nissan/kubistar', 'nissan/laurel', 'nissan/leaf', 'nissan/liberty', 'nissan/march', 'nissan/maxima', 'nissan/micra', 'nissan/murano', 'nissan/navara', 'nissan/note', 'nissan/np300', 'nissan/nv200', 'nissan/nv250', 'nissan/nv300', 'nissan/nv400', 'nissan/pathfinder', 'nissan/patrol', 'nissan/pick-up', 'nissan/pixo', 'nissan/prairie', 'nissan/presage', 'nissan/presea', 'nissan/primastar', 'nissan/primera', 'nissan/pulsar', 'nissan/qashqai', 'nissan/qashqai+2', 'nissan/quest', 'nissan/r-nessa', 'nissan/rogue', 'nissan/safari', 'nissan/sentra', 'nissan/serena', 'nissan/silvia', 'nissan/skyline', 'nissan/stagea', 'nissan/stanza', 'nissan/sunny', 'nissan/teana', 'nissan/terrano', 'nissan/tiida', 'nissan/titan', 'nissan/townstar', 'nissan/townstar', 'nissan/townstar-ev', 'nissan/trade', 'nissan/urvan', 'nissan/vanette', 'nissan/wingroad', 'nissan/x-trail', 'nissan/others', 'nsu/1000', 'nsu/prinz', 'nsu/prinz-1000', 'nsu/prinz-1000-tt', 'nsu/ro80', 'nsu/sport-prinz', 'nsu/tt', 'nsu/tts', 'nsu/wankel-spider', 'nsu/others', 'oldsmobile/442', 'oldsmobile/bravada', 'oldsmobile/custom-cruiser', 'oldsmobile/cutlass', 'oldsmobile/delta-88', 'oldsmobile/dynamic-88', 'oldsmobile/silhouette', 'oldsmobile/supreme', 'oldsmobile/toronado', 'oldsmobile/others', 'oldtimer/abarth', 'oldtimer/ac', 'oldtimer/adler', 'oldtimer/alfa-romeo', 'oldtimer/allard', 'oldtimer/alvis', 'oldtimer/amc', 'oldtimer/american', 'oldtimer/amphicar', 'oldtimer/ariel', 'oldtimer/aries', 'oldtimer/armstrong-siddeley', 'oldtimer/arnolt', 'oldtimer/asa', 'oldtimer/asc', 'oldtimer/aston-martin', 'oldtimer/auburn', 'oldtimer/audi', 'oldtimer/aurora', 'oldtimer/austin', 'oldtimer/auto-union', 'oldtimer/autobianchi', 'oldtimer/avanti', 'oldtimer/barkas', 'oldtimer/beast', 'oldtimer/bedford', 'oldtimer/belsize', 'oldtimer/benjamin', 'oldtimer/bentley', 'oldtimer/berkeley', 'oldtimer/bitter', 'oldtimer/bizzarrini', 'oldtimer/bmw', 'oldtimer/borgward', 'oldtimer/brennabor', 'oldtimer/bricklin', 'oldtimer/bugatti', 'oldtimer/buick', 'oldtimer/cadillac', 'oldtimer/chaika', 'oldtimer/champion', 'oldtimer/charron', 'oldtimer/checker', 'oldtimer/chenard-&-walker', 'oldtimer/chevrolet', 'oldtimer/chrysler', 'oldtimer/cisitalia', 'oldtimer/citroen', 'oldtimer/cj-rayburn', 'oldtimer/clan', 'oldtimer/clenet', 'oldtimer/commer', 'oldtimer/continental', 'oldtimer/cord', 'oldtimer/corvette', 'oldtimer/cunningham', 'oldtimer/d.f.p', 'oldtimer/daf', 'oldtimer/daimler', 'oldtimer/dante', 'oldtimer/datsun', 'oldtimer/day-elder', 'oldtimer/de-dion-bouton', 'oldtimer/de-lorean', 'oldtimer/de-soto', 'oldtimer/de-tomaso', 'oldtimer/delage', 'oldtimer/delahaye', 'oldtimer/denzel', 'oldtimer/desoto', 'oldtimer/deutz', 'oldtimer/dkw', 'oldtimer/dodge', 'oldtimer/dort', 'oldtimer/duesenberg', 'oldtimer/durant', 'oldtimer/dutton', 'oldtimer/edsel', 'oldtimer/elva', 'oldtimer/emw', 'oldtimer/england', 'oldtimer/enzmann', 'oldtimer/essex', 'oldtimer/excalibur', 'oldtimer/facel-vega', 'oldtimer/fairthorpe', 'oldtimer/falcon', 'oldtimer/fenton-riley', 'oldtimer/ferrari', 'oldtimer/fiat', 'oldtimer/fire-vehicle', 'oldtimer/fleur-de-lys', 'oldtimer/fn', 'oldtimer/ford', 'oldtimer/fordson', 'oldtimer/formula-car', 'oldtimer/franklin', 'oldtimer/frazer-nash', 'oldtimer/fuldamobil', 'oldtimer/gaz', 'oldtimer/ghia', 'oldtimer/gilbern', 'oldtimer/ginatta', 'oldtimer/ginetta', 'oldtimer/glas', 'oldtimer/gmc', 'oldtimer/goggomobil', 'oldtimer/goliath', 'oldtimer/gordon-keeble', 'oldtimer/graham-paige', 'oldtimer/gsm', 'oldtimer/gutbrod', 'oldtimer/hanomag', 'oldtimer/harley-davidson', 'oldtimer/healey', 'oldtimer/heinkel', 'oldtimer/heritage', 'oldtimer/hillman', 'oldtimer/hino', 'oldtimer/hispano-suiza', 'oldtimer/holden', 'oldtimer/honda', 'oldtimer/horch', 'oldtimer/hotchkiss', 'oldtimer/hrg', 'oldtimer/hudson', 'oldtimer/humber', 'oldtimer/hupmobile', 'oldtimer/ifa', 'oldtimer/ihc', 'oldtimer/innocenti', 'oldtimer/international', 'oldtimer/iso-rivolta', 'oldtimer/isuzu', 'oldtimer/jaguar', 'oldtimer/jeep', 'oldtimer/jensen', 'oldtimer/kaiser', 'oldtimer/kaiser---frazer', 'oldtimer/karmann', 'oldtimer/karmann-ghia', 'oldtimer/kelly', 'oldtimer/kleinschnittger', 'oldtimer/la-licorne', 'oldtimer/lagonda', 'oldtimer/lamborghini', 'oldtimer/lanchester', 'oldtimer/lancia', 'oldtimer/land-rover', 'oldtimer/lanz', 'oldtimer/lasalle', 'oldtimer/lea-francis', 'oldtimer/ligier', 'oldtimer/lincoln', 'oldtimer/lloyd', 'oldtimer/lmx', 'oldtimer/lombardi', 'oldtimer/lorraine-dietrich', 'oldtimer/lotus', 'oldtimer/mack', 'oldtimer/magirus', 'oldtimer/man', 'oldtimer/marauder', 'oldtimer/march', 'oldtimer/marcos', 'oldtimer/marendaz', 'oldtimer/marmon', 'oldtimer/maserati', 'oldtimer/mathis', 'oldtimer/matra', 'oldtimer/maybach', 'oldtimer/mazda', 'oldtimer/mercedes-benz', 'oldtimer/mercury', 'oldtimer/merlin', 'oldtimer/messerschmitt', 'oldtimer/metz', 'oldtimer/mg', 'oldtimer/military-vehicle', 'oldtimer/minerva', 'oldtimer/mitsubishi', 'oldtimer/monica', 'oldtimer/monteverdi', 'oldtimer/moretti', 'oldtimer/morgan', 'oldtimer/morgan-darmont', 'oldtimer/morris-leon-bolle', 'oldtimer/morris-minor', 'oldtimer/moskvitch', 'oldtimer/motorräder-bike', 'oldtimer/munga', 'oldtimer/muntz', 'oldtimer/nash', 'oldtimer/nissan', 'oldtimer/nsu', 'oldtimer/ogle', 'oldtimer/oldsmobile', 'oldtimer/om', 'oldtimer/opel', 'oldtimer/osca', 'oldtimer/overland', 'oldtimer/packard', 'oldtimer/panhard', 'oldtimer/panther', 'oldtimer/paterson', 'oldtimer/peerless', 'oldtimer/pegaso', 'oldtimer/peugeot', 'oldtimer/pierce-arrow', 'oldtimer/pontiac', 'oldtimer/porsche', 'oldtimer/puch', 'oldtimer/puma', 'oldtimer/rambler', 'oldtimer/reliant', 'oldtimer/renault', 'oldtimer/rent-bonnet', 'oldtimer/republic', 'oldtimer/riley', 'oldtimer/rolls-royce', 'oldtimer/rosengart', 'oldtimer/rotus', 'oldtimer/roush', 'oldtimer/rover', 'oldtimer/rovin', 'oldtimer/saab', 'oldtimer/salmson', 'oldtimer/saurer', 'oldtimer/seat', 'oldtimer/sebring', 'oldtimer/setra', 'oldtimer/shelby', 'oldtimer/shores', 'oldtimer/siata', 'oldtimer/simca', 'oldtimer/skoda', 'oldtimer/spartan', 'oldtimer/spitzer', 'oldtimer/standard', 'oldtimer/stephens', 'oldtimer/steyr', 'oldtimer/studebaker', 'oldtimer/stutz', 'oldtimer/subaru', 'oldtimer/sunbeam', 'oldtimer/talbot', 'oldtimer/tatra', 'oldtimer/tempo', 'oldtimer/toyota', 'oldtimer/trabant', 'oldtimer/tractor', 'oldtimer/trident', 'oldtimer/triumph', 'oldtimer/tucker', 'oldtimer/turner', 'oldtimer/tvr', 'oldtimer/uaz', 'oldtimer/unic', 'oldtimer/unimog', 'oldtimer/vanden-plas', 'oldtimer/veritas', 'oldtimer/vignale', 'oldtimer/vixen', 'oldtimer/voisin', 'oldtimer/volkswagen', 'oldtimer/volvo', 'oldtimer/wanderer', 'oldtimer/wartburg', 'oldtimer/westfalia', 'oldtimer/westfield', 'oldtimer/wetsch', 'oldtimer/willys', 'oldtimer/wolseley', 'oldtimer/yugo', 'oldtimer/zimmer', 'oldtimer/zündapp', 'oldtimer/others', 'omoda/5', 'omoda/others', 'ora/funky-cat', 'ora/others', 'pagani/huayra', 'pagani/zonda', 'pagani/others', 'panther-westwinds/lazer', 'panther-westwinds/de-ville', 'panther-westwinds/kallista', 'panther-westwinds/lima', 'panther-westwinds/rio', 'panther-westwinds/solo', 'panther-westwinds/others', 'peugeot/1007', 'peugeot/104', 'peugeot/106', 'peugeot/107', 'peugeot/108', 'peugeot/2008', 'peugeot/204', 'peugeot/205', 'peugeot/206', 'peugeot/207', 'peugeot/208', 'peugeot/3008', 'peugeot/301', 'peugeot/304', 'peugeot/305', 'peugeot/306', 'peugeot/307', 'peugeot/308', 'peugeot/309', 'peugeot/4007', 'peugeot/4008', 'peugeot/404', 'peugeot/405', 'peugeot/406', 'peugeot/407', 'peugeot/408', 'peugeot/5008', 'peugeot/504', 'peugeot/505', 'peugeot/508', 'peugeot/604', 'peugeot/605', 'peugeot/607', 'peugeot/806', 'peugeot/807', 'peugeot/bipper', 'peugeot/boxer', 'peugeot/camper', 'peugeot/e-2008', 'peugeot/e-208', 'peugeot/e-expert', 'peugeot/e-rifter', 'peugeot/expert', 'peugeot/ion', 'peugeot/j5', 'peugeot/j9', 'peugeot/partner', 'peugeot/ranch', 'peugeot/rcz', 'peugeot/rifter', 'peugeot/traveller', 'peugeot/others', 'pgo/cévennes', 'pgo/cobra', 'pgo/hemera', 'pgo/speedster', 'pgo/speedster-ii', 'pgo/others', 'piaggio/al500', 'piaggio/ape', 'piaggio/m500', 'piaggio/pk500', 'piaggio/porter', 'piaggio/quargo', 'piaggio/others', 'plymouth/acclaim', 'plymouth/arrow', 'plymouth/barracuda', 'plymouth/belvedere', 'plymouth/breeze', 'plymouth/caravelle', 'plymouth/colt', 'plymouth/conquest', 'plymouth/cricket', 'plymouth/cuda', 'plymouth/duster', 'plymouth/fury', 'plymouth/gran-fury', 'plymouth/gtx', 'plymouth/horizon', 'plymouth/laser', 'plymouth/neon', 'plymouth/prowler', 'plymouth/reliant', 'plymouth/road-runner', 'plymouth/sapporo', 'plymouth/satellite', 'plymouth/savoy', 'plymouth/scamp', 'plymouth/sundance', 'plymouth/superbird', 'plymouth/trailduster', 'plymouth/turismo', 'plymouth/valiant', 'plymouth/volaré', 'plymouth/voyager', 'plymouth/others', 'polestar/1', 'polestar/2', 'polestar/3', 'polestar/4', 'polestar/others', 'pontiac/6000', 'pontiac/aztek', 'pontiac/bonneville', 'pontiac/catalina-safari', 'pontiac/fiero', 'pontiac/firebird', 'pontiac/g6', 'pontiac/grand-am', 'pontiac/grand-prix', 'pontiac/gto', 'pontiac/montana', 'pontiac/solstice', 'pontiac/sunbird', 'pontiac/sunfire', 'pontiac/targa', 'pontiac/trans-am', 'pontiac/trans-sport', 'pontiac/vibe', 'pontiac/others', 'porsche/356', 'porsche/550', 'porsche/718-(all)', 'porsche/718', 'porsche/718-spyder', 'porsche/911-series-(all)', 'porsche/911', 'porsche/930', 'porsche/964', 'porsche/991', 'porsche/992', 'porsche/993', 'porsche/996', 'porsche/997', 'porsche/912', 'porsche/914', 'porsche/918', 'porsche/924', 'porsche/928', 'porsche/944', 'porsche/959', 'porsche/962', 'porsche/968', 'porsche/boxster', 'porsche/carrera-gt', 'porsche/cayenne', 'porsche/cayman', 'porsche/macan', 'porsche/panamera', 'porsche/targa', 'porsche/taycan', 'porsche/others', 'proton/313', 'proton/315', 'proton/316', 'proton/318', 'proton/413', 'proton/415', 'proton/416', 'proton/418', 'proton/420', 'proton/gen2', 'proton/persona', 'proton/satria', 'proton/others', 'puch/g', 'puch/haflinger', 'puch/pinzgauer', 'puch/others', 'ram/1500', 'ram/2500', 'ram/3500', 'ram/chassis-cab', 'ram/promaster', 'ram/others', 'regis/epic0', 'regis/others', 'reliant/ant', 'reliant/fox', 'reliant/kitten', 'reliant/rebel', 'reliant/regal', 'reliant/regent', 'reliant/rialto', 'reliant/robin', 'reliant/sabre-four', 'reliant/scimitar', 'reliant/others', 'rolls-royce/arnage-green-label', 'rolls-royce/arnage-red-label', 'rolls-royce/azure', 'rolls-royce/azure-mulliner', 'rolls-royce/camargue', 'rolls-royce/cloud', 'rolls-royce/continental-r-mulliner', 'rolls-royce/continental-r', 'rolls-royce/continental-sc', 'rolls-royce/corniche', 'rolls-royce/cullinan', 'rolls-royce/dawn', 'rolls-royce/flying-spur', 'rolls-royce/ghost', 'rolls-royce/le-mains-series', 'rolls-royce/park-ward', 'rolls-royce/phantom', 'rolls-royce/phantom-drophead', 'rolls-royce/silver-dawn', 'rolls-royce/silver-seraph', 'rolls-royce/silver-shadow', 'rolls-royce/silver-spirit', 'rolls-royce/silver-spur', 'rolls-royce/silver-wraith', 'rolls-royce/silver-wraith-ii', 'rolls-royce/spectre', 'rolls-royce/t', 'rolls-royce/touring', 'rolls-royce/wraith', 'rolls-royce/others', 'rover/100', 'rover/111', 'rover/114', 'rover/115', 'rover/200', 'rover/213', 'rover/214', 'rover/216', 'rover/218', 'rover/220', 'rover/25', 'rover/400', 'rover/414', 'rover/416', 'rover/418', 'rover/420', 'rover/45', 'rover/600', 'rover/618', 'rover/620', 'rover/623', 'rover/75', 'rover/800', 'rover/820', 'rover/825', 'rover/827', 'rover/city-rover', 'rover/estate', 'rover/metro', 'rover/mini', 'rover/montego', 'rover/rover', 'rover/sd', 'rover/streetwise', 'rover/tourer', 'rover/others', 'ruf/3400s', 'ruf/3600s', 'ruf/btr', 'ruf/ctr', 'ruf/ctr2', 'ruf/ctr3', 'ruf/dakara', 'ruf/gt', 'ruf/r-kompressor', 'ruf/r-turbo', 'ruf/rgt', 'ruf/rgt-8', 'ruf/rk-coupe/spyder', 'ruf/rt-12', 'ruf/rt-12r', 'ruf/rt-12s', 'ruf/scr', 'ruf/turbo-florio', 'ruf/turbo-r', 'ruf/others', 'saab/9-2x', 'saab/9-3', 'saab/9-4x', 'saab/9-5', 'saab/9-7x', 'saab/90', 'saab/900', 'saab/9000', 'saab/92', 'saab/93', 'saab/95', 'saab/96', 'saab/99', 'saab/gt-750', 'saab/sonett', 'saab/sport-/-gt-850', 'saab/others', 'santana/2500', 'santana/300', 'santana/350', 'santana/410', 'santana/anibal', 'santana/ps-10', 'santana/s300', 'santana/s350', 'santana/samurai', 'santana/vitara', 'santana/vitara-cabriolet', 'santana/others', 'seat/alhambra', 'seat/altea', 'seat/altea-xl', 'seat/arona', 'seat/arosa', 'seat/ateca', 'seat/cordoba', 'seat/exeo', 'seat/fura', 'seat/ibiza', 'seat/inca', 'seat/leon', 'seat/leon-e-hybrid', 'seat/malaga', 'seat/marbella', 'seat/mii', 'seat/panda', 'seat/ronda', 'seat/tarraco', 'seat/terra', 'seat/toledo', 'seat/others', 'segway/fugleman-1000', 'segway/fugleman-570', 'segway/fugleman-ut-10', 'segway/fugleman-ut6-h', 'segway/villain-1000-sh', 'segway/villain-sx10', 'segway/villain-sx10-h', 'segway/others', 'selvo/2p45', 'selvo/lt-cargo', 'selvo/others', 'seres/seres-3', 'seres/seres-5', 'seres/seres-7', 'seres/others', 'sevic/500', 'sevic/others', 'sgs/biarritz', 'sgs/gullwing', 'sgs/marbella-cabrio', 'sgs/monte-carlo-cabrio', 'sgs/pulman-limousine', 'sgs/st.-tropez-cabrio-limousine', 'sgs/others', 'shelby/f-150', 'shelby/f-150-super-snake', 'shelby/mustang-gt-h', 'shelby/mustang-super-snake', 'shelby/series-1', 'shelby/others', 'shuanghuan/ceo', 'shuanghuan/others', 'silence/s04', 'singer/others', 'skoda/105', 'skoda/120', 'skoda/130', 'skoda/135', 'skoda/citigo', 'skoda/enyaq', 'skoda/fabia', 'skoda/favorit', 'skoda/felicia', 'skoda/forman', 'skoda/kamiq', 'skoda/karoq', 'skoda/kodiaq', 'skoda/octavia', 'skoda/pick-up', 'skoda/praktik', 'skoda/rapid/spaceback', 'skoda/roomster', 'skoda/scala', 'skoda/snowman', 'skoda/superb', 'skoda/yeti', 'skoda/others', 'skywell/et5', 'skywell/others', 'smart/#1', 'smart/#3', 'smart/brabus', 'smart/city-coupé/city-cabrio', 'smart/crossblade', 'smart/forfour', 'smart/fortwo', 'smart/roadster', 'smart/others', 'speedart/others', 'sportequipe/sportequipe-5', 'sportequipe/sportequipe-6', 'sportequipe/sportequipe-7', 'sportequipe/others', 'spyker/c12', 'spyker/c8', 'spyker/d12', 'spyker/others', 'ssangyong/actyon', 'ssangyong/family', 'ssangyong/kallista', 'ssangyong/korando', 'ssangyong/kyron', 'ssangyong/musso', 'ssangyong/rexton', 'ssangyong/rodius', 'ssangyong/tivoli', 'ssangyong/torres', 'ssangyong/xlv', 'ssangyong/others', 'stormborn/city-pony---baw-pony', 'stormborn/others', 'streetscooter/work', 'streetscooter/work-l', 'streetscooter/others', 'studebaker/champion', 'studebaker/others', 'subaru/1200', 'subaru/1800', 'subaru/ascent', 'subaru/baja', 'subaru/brz', 'subaru/crosstrek', 'subaru/e10', 'subaru/e12', 'subaru/forester', 'subaru/impreza', 'subaru/justy', 'subaru/legacy', 'subaru/leone', 'subaru/levorg', 'subaru/libero', 'subaru/m60', 'subaru/m70', 'subaru/m80', 'subaru/mini', 'subaru/outback', 'subaru/solterra', 'subaru/svx', 'subaru/trezia', 'subaru/tribeca', 'subaru/vanille', 'subaru/vivio', 'subaru/wrx', 'subaru/xt', 'subaru/xv', 'subaru/others', 'suzuki/across', 'suzuki/alto', 'suzuki/baleno', 'suzuki/cappuccino', 'suzuki/carry', 'suzuki/celerio', 'suzuki/escudo', 'suzuki/grand-vitara', 'suzuki/ignis', 'suzuki/ik-2', 'suzuki/jimny', 'suzuki/kizashi', 'suzuki/liana', 'suzuki/lj-80', 'suzuki/maruti', 'suzuki/s-cross', 'suzuki/sa-310', 'suzuki/samurai', 'suzuki/santana', 'suzuki/sj-410', 'suzuki/sj-413', 'suzuki/sj-samurai', 'suzuki/splash', 'suzuki/super-carry', 'suzuki/swace', 'suzuki/swift', 'suzuki/sx4', 'suzuki/sx4-s-cross', 'suzuki/vitara', 'suzuki/wagon-r+', 'suzuki/x-90', 'suzuki/xl-7', 'suzuki/others', 'swm/g01', 'swm/g01f', 'swm/g03f', 'swm/g05', 'swm/others', 'talbot/alpine', 'talbot/horizon', 'talbot/matra-murena', 'talbot/matra-rancho', 'talbot/samba', 'talbot/simca-1100', 'talbot/simca-1510', 'talbot/solar-gl', 'talbot/solar-ls', 'talbot/solar-ralley', 'talbot/solara', 'talbot/sunbeam', 'talbot/tagora', 'talbot/others', 'tasso/bingo', 'tasso/c1db', 'tasso/c1dm', 'tasso/domino', 'tasso/hola', 'tasso/king', 'tasso/t2', 'tasso/t3', 'tasso/td', 'tasso/others', 'tata/aria', 'tata/bolt', 'tata/estate', 'tata/harrier', 'tata/hexa', 'tata/indica', 'tata/indigo', 'tata/nano', 'tata/nexon', 'tata/pick-up', 'tata/safari', 'tata/sport', 'tata/sumo', 'tata/telcoline', 'tata/telcosport', 'tata/tiago', 'tata/tigor', 'tata/xenon', 'tata/zest', 'tata/others', 'tazzari-ev/em1-anniversary', 'tazzari-ev/em1-citysport', 'tazzari-ev/zero-city', 'tazzari-ev/zero-classic', 'tazzari-ev/zero-em1', 'tazzari-ev/zero-em2', 'tazzari-ev/zero-evo', 'tazzari-ev/zero-junior', 'tazzari-ev/zero-se', 'tazzari-ev/zero-special-edition', 'tazzari-ev/zero-speedster', 'tazzari-ev/others', 'techart/others', 'tesla/cybertruck', 'tesla/model-3', 'tesla/model-s', 'tesla/model-x', 'tesla/model-y', 'tesla/roadster', 'tesla/others', 'togg/t10x', 'togg/others', 'town-life/ginevra', 'town-life/helektra', 'town-life/others', 'toyota/4-runner', 'toyota/allion', 'toyota/alphard', 'toyota/altezza', 'toyota/aristo', 'toyota/auris', 'toyota/avalon', 'toyota/avensis', 'toyota/avensis-verso', 'toyota/aygo', 'toyota/aygo-x', 'toyota/bb', 'toyota/belta', 'toyota/bz4x', 'toyota/c-hr', 'toyota/caldina', 'toyota/cami', 'toyota/camry', 'toyota/carina', 'toyota/celica', 'toyota/chaser', 'toyota/coaster', 'toyota/corolla', 'toyota/corolla-cross', 'toyota/corolla-verso', 'toyota/corona', 'toyota/corsa', 'toyota/cressida', 'toyota/cresta', 'toyota/crown', 'toyota/duet', 'toyota/dyna', 'toyota/estima', 'toyota/fj-cruiser', 'toyota/fj40', 'toyota/fortuner', 'toyota/fun-cruiser', 'toyota/funcargo', 'toyota/gaia', 'toyota/gr86', 'toyota/gt86', 'toyota/harrier', 'toyota/hdj', 'toyota/hiace', 'toyota/highlander', 'toyota/hilux', 'toyota/ipsum', 'toyota/iq', 'toyota/ist', 'toyota/kj', 'toyota/land-cruiser', 'toyota/land-cruiser-prado', 'toyota/lite-ace', 'toyota/mark-ii', 'toyota/mark-x', 'toyota/matrix', 'toyota/mirai', 'toyota/model-f', 'toyota/mr-2', 'toyota/nadia', 'toyota/noah', 'toyota/opa', 'toyota/paseo', 'toyota/passo', 'toyota/pick-up', 'toyota/picnic', 'toyota/platz', 'toyota/premio', 'toyota/previa', 'toyota/prius', 'toyota/prius+', 'toyota/proace', 'toyota/proace-city', 'toyota/ractis', 'toyota/raum', 'toyota/rav-4', 'toyota/sequoia', 'toyota/sienna', 'toyota/solara', 'toyota/sprinter', 'toyota/starlet', 'toyota/supra', 'toyota/tacoma', 'toyota/tercel', 'toyota/town-ace', 'toyota/tundra', 'toyota/urban-cruiser', 'toyota/venza', 'toyota/verossa', 'toyota/verso', 'toyota/verso-s', 'toyota/vista', 'toyota/vitz', 'toyota/voxy', 'toyota/will', 'toyota/windom', 'toyota/wish', 'toyota/yaris', 'toyota/yaris-cross', 'toyota/others', 'trabant/1.1', 'trabant/p50', 'trabant/p60', 'trabant/p601', 'trabant/rallye', 'trabant/trabant', 'trabant/others', 'trailer-anhänger/others', 'triumph/dolomite', 'triumph/gt6', 'triumph/herald', 'triumph/moss', 'triumph/spitfire', 'triumph/stag', 'triumph/tr1', 'triumph/tr2', 'triumph/tr3', 'triumph/tr4', 'triumph/tr5', 'triumph/tr6', 'triumph/tr7', 'triumph/tr8', 'triumph/others', 'trucks-lkw/atlas', 'trucks-lkw/cat', 'trucks-lkw/citroen', 'trucks-lkw/daewoo', 'trucks-lkw/daf', 'trucks-lkw/deutz-fahr', 'trucks-lkw/fiat', 'trucks-lkw/ford', 'trucks-lkw/fuchs', 'trucks-lkw/hanomag', 'trucks-lkw/hitachi', 'trucks-lkw/iveco', 'trucks-lkw/iveco-magirus', 'trucks-lkw/iveco-fiat', 'trucks-lkw/jungheinrich', 'trucks-lkw/koegel', 'trucks-lkw/komatsu', 'trucks-lkw/ldv', 'trucks-lkw/liebherr', 'trucks-lkw/linde', 'trucks-lkw/man', 'trucks-lkw/mercedes-benz', 'trucks-lkw/mitsubishi', 'trucks-lkw/multicar', 'trucks-lkw/neoplan', 'trucks-lkw/nissan', 'trucks-lkw/o-&-k', 'trucks-lkw/peugeot', 'trucks-lkw/renault', 'trucks-lkw/scania', 'trucks-lkw/schaeff', 'trucks-lkw/setra', 'trucks-lkw/volvo', 'trucks-lkw/vw', 'trucks-lkw/zeppelin', 'trucks-lkw/zettelmeyer', 'trucks-lkw/others', 'tvr/cerbera', 'tvr/chimaera', 'tvr/grantura', 'tvr/griffith', 'tvr/s-2,8', 'tvr/s2', 'tvr/s3', 'tvr/s4', 'tvr/sagaris', 'tvr/t350', 'tvr/tamora', 'tvr/tuscan', 'tvr/v8s', 'tvr/others', 'uaz/2206', 'uaz/2315', 'uaz/3151', 'uaz/3153', 'uaz/3159', 'uaz/3160', 'uaz/3162', 'uaz/3303', 'uaz/3692', 'uaz/3909', 'uaz/3962', 'uaz/469', 'uaz/buchanka', 'uaz/classic', 'uaz/dakar', 'uaz/farmer', 'uaz/hunter', 'uaz/patriot', 'uaz/pickup', 'uaz/profi', 'uaz/tigr', 'uaz/trofi', 'uaz/others', 'vanden-plas/armstrong', 'vanden-plas/princess', 'vanden-plas/others', 'vanderhall/carmel', 'vanderhall/edison-2', 'vanderhall/edison-4', 'vanderhall/venice', 'vanderhall/venice-r', 'vanderhall/venice-speedster', 'vanderhall/venice-speedster-r', 'vanderhall/others', 'vaz/1111', 'vaz/11113', 'vaz/11118', 'vaz/1113', 'vaz/1117', 'vaz/1118', 'vaz/1119', 'vaz/1706', 'vaz/1922', 'vaz/2016', 'vaz/2101', 'vaz/21011', 'vaz/21013', 'vaz/2102', 'vaz/2103', 'vaz/21033', 'vaz/2104', 'vaz/21043', 'vaz/21045', 'vaz/21046', 'vaz/21047', 'vaz/2105', 'vaz/21051', 'vaz/21053', 'vaz/2106', 'vaz/21060', 'vaz/21061', 'vaz/21063', 'vaz/21065', 'vaz/2107', 'vaz/21073', 'vaz/21074', 'vaz/2108', 'vaz/21081', 'vaz/21083', 'vaz/21086', 'vaz/2109', 'vaz/21091', 'vaz/21093', 'vaz/21096', 'vaz/21099', 'vaz/2110', 'vaz/21101', 'vaz/21102', 'vaz/21103', 'vaz/21104', 'vaz/21106', 'vaz/21108', 'vaz/2111', 'vaz/21111', 'vaz/21112', 'vaz/21113', 'vaz/21114', 'vaz/2112', 'vaz/21120', 'vaz/21121', 'vaz/21122', 'vaz/21123', 'vaz/21124', 'vaz/2113', 'vaz/21130', 'vaz/2114', 'vaz/21140', 'vaz/2115', 'vaz/21150', 'vaz/21150i', 'vaz/2120', 'vaz/2121', 'vaz/21213', 'vaz/21214', 'vaz/21218', 'vaz/212180', 'vaz/2123', 'vaz/2129', 'vaz/2131', 'vaz/21312', 'vaz/2170', 'vaz/2199', 'vaz/2328', 'vaz/2329', 'vaz/2364', 'vaz/roadster', 'vaz/others', 'vem/cargo', 'vem/cover', 'vem/double', 'vem/multi', 'vem/open', 'vem/people', 'vem/ribaltabile', 'vem/others', 'vinfast/vf-6', 'vinfast/vf-7', 'vinfast/vf-8', 'vinfast/vf-9', 'vinfast/others', 'volvo/240', 'volvo/244', 'volvo/245', 'volvo/262', 'volvo/264', 'volvo/265', 'volvo/340', 'volvo/360', 'volvo/440', 'volvo/460', 'volvo/480', 'volvo/740', 'volvo/744', 'volvo/745', 'volvo/760', 'volvo/764', 'volvo/780', 'volvo/850', 'volvo/855', 'volvo/940', 'volvo/944', 'volvo/945', 'volvo/960', 'volvo/965', 'volvo/amazon', 'volvo/c30', 'volvo/c40', 'volvo/c70', 'volvo/ec40', 'volvo/ex30', 'volvo/ex40', 'volvo/ex90', 'volvo/p1800', 'volvo/polar', 'volvo/pv544', 'volvo/s40', 'volvo/s60', 'volvo/s60-cross-country', 'volvo/s70', 'volvo/s80', 'volvo/s90', 'volvo/v40', 'volvo/v40-cross-country', 'volvo/v50', 'volvo/v60', 'volvo/v60-cross-country', 'volvo/v70', 'volvo/v90', 'volvo/v90-cross-country', 'volvo/xc40', 'volvo/xc60', 'volvo/xc70', 'volvo/xc90', 'volvo/others', 'voyah/dream', 'voyah/free', 'voyah/passion', 'voyah/others', 'wartburg/1.3', 'wartburg/1.6', 'wartburg/1000', 'wartburg/311', 'wartburg/312', 'wartburg/313', 'wartburg/353', 'wartburg/barkas', 'wartburg/framo', 'wartburg/ifa-f9', 'wartburg/wartburg', 'wartburg/others', 'weltmeister/ex5-z', 'weltmeister/ex6-plus', 'weltmeister/w6', 'weltmeister/others', 'wenckstern/full-custom', 'wenckstern/standard', 'wenckstern/standard-custom', 'wenckstern/others', 'westfield/7se', 'westfield/fw400', 'westfield/megablade', 'westfield/megabusa', 'westfield/megas2000', 'westfield/sdv', 'westfield/se', 'westfield/sei', 'westfield/seight', 'westfield/sport', 'westfield/sport-turbo', 'westfield/xi', 'westfield/xtr2', 'westfield/xtr4', 'westfield/others', 'wey/coffee-01', 'wey/coffee-02', 'wey/others', 'wiesmann/gecko', 'wiesmann/mf-28', 'wiesmann/mf-3', 'wiesmann/mf-30', 'wiesmann/mf-4', 'wiesmann/mf-5', 'wiesmann/others', 'xbus/bus', 'xbus/others', 'xev/kitty', 'xev/yoyo', 'xev/others', 'xpeng/g3i', 'xpeng/g9', 'xpeng/p5', 'xpeng/p7', 'xpeng/others', 'zastava/10', 'zastava/101', 'zastava/1100-tf', 'zastava/125-pz', 'zastava/128', 'zastava/1300', 'zastava/600', 'zastava/750', 'zastava/850', 'zastava/850-ak', 'zastava/900-ak', 'zastava/koral', 'zastava/skala', 'zastava/yugo', 'zastava/others', 'zaz/1102', 'zaz/1103', 'zaz/1105', 'zaz/chance', 'zaz/forza', 'zaz/lanos', 'zaz/sens', 'zaz/vida', 'zaz/others', 'zeekr/001', 'zeekr/x', 'zeekr/others', 'zhidou/d1', 'zhidou/d2', 'zhidou/d3', 'zhidou/kwb', 'zhidou/others', 'zotye/e200', 'zotye/t300', 'zotye/t600', 'zotye/t700', 'zotye/traum-meet-3', 'zotye/traum-s70', 'zotye/traum-seek-5', 'zotye/z100', 'zotye/z360', 'zotye/z700', 'zotye/others', 'others/aiways', 'others/amc', 'others/apal', 'others/aro', 'others/asia', 'others/auverland', 'others/barkas', 'others/bertone', 'others/bilenkin-classic-cars', 'others/binz', 'others/bitter', 'others/bm-grupa', 'others/british-leyland', 'others/burton', 'others/can-am', 'others/canta', 'others/carver', 'others/china-automobile', 'others/cmc', 'others/continental', 'others/cord', 'others/courb', 'others/datsun-go', 'others/de-lorean', 'others/derways', 'others/edrive', 'others/effedi-maranello', 'others/excalibur', 'others/fso', 'others/fun-tech', 'others/geely', 'others/genesis', 'others/ginetta', 'others/grandin-dallas', 'others/gumpert', 'others/hartge', 'others/hdpic', 'others/hobbycar', 'others/holden', 'others/ihc', 'others/indimo', 'others/iseki', 'others/italcar', 'others/jac', 'others/jdm', 'others/jiayuan', 'others/karabag', 'others/keinath', 'others/kit-cars', 'others/la-forza', 'others/landwind', 'others/loremo', 'others/marcos', 'others/melkus', 'others/mercury', 'others/mia', 'others/monteverdi', 'others/morris', 'others/mosler', 'others/nio', 'others/noble', 'others/polaris', 'others/qoros', 'others/quadix', 'others/qvale', 'others/radical', 'others/reva', 'others/rimac', 'others/romeo-ferraris', 'others/saleen', 'others/sam', 'others/savel', 'others/scheelen', 'others/scion', 'others/sdg', 'others/shandong', 'others/tagaz', 'others/teener', 'others/think-city', 'others/tiger', 'others/tramontana', 'others/trax', 'others/turner', 'others/van-diemen', 'others/vauxhall', 'others/venturi', 'others/vm', 'others/vortex', 'others/wallys', 'others/weineck', 'others/wenckstern', 'others/xev', 'others/yes!', 'others/zenvo', 'others/others']
print(f'All brand model array: {all_brand_model_array}')
all_price_array = all_price_array_to_url(find_all_price())
#all_price_array = ['priceto=500', 'pricefrom=500&priceto=1000', 'pricefrom=1000&priceto=1500', 'pricefrom=1500&priceto=2000', 'pricefrom=2000&priceto=2500', 'pricefrom=2500&priceto=3000', 'pricefrom=3000&priceto=4000', 'pricefrom=4000&priceto=5000', 'pricefrom=5000&priceto=6000', 'pricefrom=6000&priceto=7000', 'pricefrom=7000&priceto=8000', 'pricefrom=8000&priceto=9000', 'pricefrom=9000&priceto=10000', 'pricefrom=10000&priceto=12500', 'pricefrom=12500&priceto=15000', 'pricefrom=15000&priceto=17500', 'pricefrom=17500&priceto=20000', 'pricefrom=20000&priceto=25000', 'pricefrom=25000&priceto=30000', 'pricefrom=30000&priceto=40000', 'pricefrom=40000&priceto=50000', 'pricefrom=50000&priceto=75000', 'pricefrom=75000&priceto=100000']
print(f'All price array: {all_price_array}')
all_mileage_array = url_type_form_to_mileage(find_all_mileage())
#all_mileage_array = ['kmto=2500', 'kmfrom=2500&kmto=5000', 'kmfrom=5000&kmto=10000', 'kmfrom=10000&kmto=20000', 'kmfrom=20000&kmto=30000', 'kmfrom=30000&kmto=40000', 'kmfrom=40000&kmto=50000', 'kmfrom=50000&kmto=60000', 'kmfrom=60000&kmto=70000', 'kmfrom=70000&kmto=80000', 'kmfrom=80000&kmto=90000', 'kmfrom=90000&kmto=100000', 'kmfrom=100000&kmto=125000', 'kmfrom=125000&kmto=150000', 'kmfrom=150000&kmto=175000', 'kmfrom=175000&kmto=200000']
print(f'All mileage url type: {all_mileage_array}')
all_country_array = ['D', 'A', 'B', 'E', 'F', 'I', 'L', 'NL']
"""

#TODO COMPETED
#TODO Find descend element from urls
def split_url_to_desc(url, desc_index,mode):
    all_split_item = url.split(f'desc=')
    second_split_item = all_split_item[1]
    new_second_split = ''
    for fix_second_letter in second_split_item:
        if fix_second_letter == second_split_item[0]:
            fix_second_letter = ''
        new_second_split = new_second_split + fix_second_letter

    fixed_desc_url = f'{all_split_item[0]}desc={desc_index}{new_second_split}'
    all_fixed_desc_url = fixed_desc_url.split('sort=')

    second_split_desc_url = all_fixed_desc_url[1]
    all_second_split_desc_url = second_split_desc_url.split('&')
    all_second_split_desc_url.pop(0)

    new_second_split = ''
    for second_split_index in all_second_split_desc_url:
        new_second_split = new_second_split + '&' + second_split_index

    return f'{all_fixed_desc_url[0]}sort={mode}{new_second_split}'


#TODO COMPETED
def pure_number(text):
    pure_text = ''
    for letter in text:
        if letter==',':
            letter = ''
        pure_text = letter + pure_text
    return pure_text

#TODO COMPETED
def generate_url_based_on_brand_model_country(brand_model_array, country_array):
    all_brand_model_country_array = []
    brand_model = brand_model_array[0]
    brand_model_split = brand_model.split('/')
    brand = brand_model_split[0]

    brand_url = f'https://www.autoscout24.com/lst/{brand}?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&powertype=kw&search_id=72faoj4adc&sort=standard&source=homepage_search-mask&ustate=N%2CU'

    driver.get(brand_url)
    brand_car_info = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h1[@data-testid = "list-header-title"]'))
    )
    brand_car_info_text = brand_car_info.text
    brand_car_amount_text = brand_car_info_text.split(' ')[0]
    brand_car_amount = pure_number(brand_car_amount_text)
    #print(f'Brand car amount is : {brand_car_amount}')
    index = 0
    if int(brand_car_amount) > 400:

        for each_brand_model in brand_model_array:
            brand_model_url = f'https://www.autoscout24.com/lst/{each_brand_model}?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&powertype=kw&search_id=72faoj4adc&sort=standard&source=homepage_search-mask&ustate=N%2CU'
            driver.get(brand_model_url)
            car_info = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//h1[@data-testid = "list-header-title"]'))
            )
            car_info_text = car_info.text
            car_amount_text = car_info_text.split(' ')[0]
            car_amount = pure_number(car_amount_text)
            if int(car_amount) > 400:
                for country in country_array:
                    country_url = f'https://www.autoscout24.com/lst/{each_brand_model}?atype=C&cy={country}&damaged_listing=exclude&desc=0&powertype=kw&search_id=72faoj4adc&sort=standard&source=homepage_search-mask&ustate=N%2CU'
                    print(f'Index: {index} ')
                    all_brand_model_country_array.append(country_url)
                    index += 1
            else:
                all_brand_model_country_array.append(brand_model_url)
                print(f'Index: {index}')
                index += 1
    else:
        print(f'Index: {index} ')
        all_brand_model_country_array.append(brand_url)
        index += 1

    return all_brand_model_country_array

#TODO COMPETED
def brand_model_splitter(all_brand_model_array,brand_array):
    all_splitted_by_brands = []
    for each_brand in brand_array:
        local_brand_array = []
        for each_brand_model in all_brand_model_array:
            each_brand_model_text = each_brand_model.split('/')
            brand_text = each_brand_model_text[0]
            if each_brand == brand_text:
                local_brand_array.append(each_brand_model)
        all_splitted_by_brands.append(local_brand_array)
    return all_splitted_by_brands

#TODO COMPETED
def scrap_page_by_page(all_brand_model_array,all_country_array,file_name,counter):
    all_url = generate_url_based_on_brand_model_country(all_brand_model_array, all_country_array)
    url_index = 0
    all_df = []
    for url in all_url:
        print(f'Current url index = {url_index} Length of all url: {len(all_url)} ---->Current Url : {url}')
        driver.get(url)
        last_page_num = find_last_page_num()
        split_elements = split_url_until_find_page_add_powertype(url)


        for page_index in range(1, last_page_num+1):

            webpage_url = f'{split_elements[0]}&page={page_index}&powertype{split_elements[1]}'

            try:
                all_car_array = all_car_links(webpage_url)

                for each_link in all_car_array:
                    df = scrap_the_page_to_df(each_link)
                    print(f'Df is: {df}')
                    all_df.append(df)
                    counter += 1
                    print(f'Current Page Number-----> {page_index} Last page number:{last_page_num} //// Car ----> {counter}')
            except:
                pass
        url_index += 1
    concat_all_urls_and_print_to_csv(all_df,file_name)

#TODO COMPETED
def split_by_brand(brand_model_array):
    all_brands = []
    for element in brand_model_array:
        brand_model_text = element.split('/')
        brand_text = brand_model_text[0]
        if brand_text not in all_brands:
            all_brands.append(brand_text)
    return all_brands
#TODO COMPETED
#TODO Start the process
def automated_func(all_brand_model_array,start_index,brand_model_amount):

    all_brand_model_by_brand_array = brand_model_splitter(all_brand_model_array, split_by_brand(all_brand_model_array))
    brand = split_by_brand(all_brand_model_array)
    counter = 0
    for loop_size in range(start_index, start_index + brand_model_amount):
        file_name = f'{brand[loop_size]}_index_s_{loop_size}'
        scrap_page_by_page(all_brand_model_by_brand_array[loop_size], all_country_array,file_name,counter)


all_brand_model_array ,all_price_array, all_mileage_array, all_country_array = all_website_filtrations_for_url()
automated_func(all_brand_model_array,11, 2)

