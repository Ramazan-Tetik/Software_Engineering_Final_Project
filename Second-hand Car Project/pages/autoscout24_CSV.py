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


def find_all_countries_array():
    all_countries_array = []
    country_url_format = 'D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL'
    all_countries_text = country_url_format.split('%2C')
    for each_country in all_countries_text:
        all_countries_array.append(each_country)

    return all_countries_array





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


def split_url_until_find_page_add_powertype(url):
    splitted_url = url.split('&powertype')
    splitted_elements = []
    for element in splitted_url:
        splitted_elements.append(element)
    return splitted_elements



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



def pure_number(text):
    pure_text = ''
    for letter in text:
        if letter==',':
            letter = ''
        pure_text = letter + pure_text
    return pure_text


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


def split_by_brand(brand_model_array):
    all_brands = []
    for element in brand_model_array:
        brand_model_text = element.split('/')
        brand_text = brand_model_text[0]
        if brand_text not in all_brands:
            all_brands.append(brand_text)
    return all_brands


#TODO Start the process
def automated_func(all_brand_model_array,start_index,brand_model_amount):

    all_brand_model_by_brand_array = brand_model_splitter(all_brand_model_array, split_by_brand(all_brand_model_array))
    brand = split_by_brand(all_brand_model_array)
    counter = 0
    for loop_size in range(start_index, start_index + brand_model_amount):
        file_name = f'{brand[loop_size]}_index_s_{loop_size}'
        scrap_page_by_page(all_brand_model_by_brand_array[loop_size], all_country_array,file_name,counter)


all_brand_model_array ,all_price_array, all_mileage_array, all_country_array = all_website_filtrations_for_url()

#>>automated_func(all_brand_model_array,index_of_the_brand, size)

