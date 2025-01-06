from selenium import webdriver
from selenium.webdriver.chrome.service import  Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.chrome.options import Options
import streamlit as st

options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--headless")
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=options)
driver.maximize_window()

st.markdown("""
<body>
    <section class="home" id="home">
        <div class="content">
            <h3></h3>
            <p></p>
        </div>
    </section>
</body>    
""", unsafe_allow_html=True)

with open("common.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

website = 'https://www.autoscout24.com/'
path = f'{website}lst?atype=C&desc=0&page=1&search_id=2554r0bdct&sort=standard&source=listpage_pagination&ustate=N%2CU'
driver.get(path)

def pop_up_accept():
    try:
        pop_up_accept = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class = "_consent-accept_1lphq_114"]'))
        )
        pop_up_accept.click()
    except:
        pass
pop_up_accept()

def pure_number(text):
    pure_text = ''
    for letter in text:
        if letter==',':
            letter = ''
        pure_text = letter + pure_text
    return pure_text

def find_last_page_num():

    try:
        pagination_bar = WebDriverWait(driver, 20).until(
            lambda driver: driver.find_elements(By.XPATH, '//nav[@class ="scr-pagination FilteredListPagination_pagination__3WXZT"]/ul/li')
        )


        last_page = pagination_bar[-3]
        last_page_number = int(last_page.text)
    except:
        last_page_number = 1
    return last_page_number


def all_car_links(webpage_url):
    driver.get(webpage_url)

    try:
        possible_all_car_links = WebDriverWait(driver, 20).until(
            lambda driver: driver.find_elements(By.XPATH,'//div[@class = "ListItem_header__J6xlG ListItem_header_new_design__Rvyv_"]/a'))
               
        all_links = []
        for link in possible_all_car_links:
            car_link = link.get_attribute('href')
            all_links.append(car_link)         
    except:
        all_links = []
    return all_links

def split_url_until_find_page_add_powertype(url):
    splitted_url = url.split('&powertype')
    splitted_elements = []
    for element in splitted_url:
        splitted_elements.append(element)
    return splitted_elements

def scrap_the_page_to_df(url):
    driver.get(url)
    all_headers = []
    all_features = []
    df_feature = {}
    try:
        # TODO Car Brand
        car_name = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//span[@class = "StageTitle_boldClassifiedInfo__sQb0l"]'))
        )

        df_feature['brand'] = car_name.text
    except:
        df_feature['brand'] = ''
    try:
        # TODO Car Model
        car_model = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//span[@class = "StageTitle_model__EbfjC StageTitle_boldClassifiedInfo__sQb0l"]'))
        )

        df_feature['model'] = car_model.text
    except:
        df_feature['model'] = ''

    try:
        # TODO Car Price
        car_price = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//span[@class = "PriceInfo_price__XU0aF"]'))
        )
        df_feature['price'] = car_price.text
    except:
        df_feature['price'] = ''

    try:
        # TODO General Feature
        first_feature_block = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class = "VehicleOverview_containerMoreThanFourItems__691k2"]'))
        )
        first_feature_block_each_row = WebDriverWait(first_feature_block,20).until(
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
        all_block = WebDriverWait(driver, 20).until(
            lambda driver: driver.find_elements(By.XPATH,
                                                '//dl[@class = "DataGrid_defaultDlStyle__xlLi_"]')
        )
        #all_block = driver.find_elements(By.XPATH, '//dl[@class = "DataGrid_defaultDlStyle__xlLi_"]')
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

#TODO Contstuct selection phase for fuel_type, power , mileage, gearbox: WORKING <<TESTED>>
def contruct_all_possibilities_for_FPMG(fuel,each_power_from,each_power_to,each_mileage_from,each_mileage_to,gearbox_array):

    all_FPMG = []
    for each_fuel in fuel:
        for each_gearbox in gearbox_array:
            fpmg = f'fuel={each_fuel}&gear={each_gearbox}&kmfrom={each_mileage_from}&kmto={each_mileage_to}&powerfrom={each_power_from}&powerto={each_power_to}&powertype=hp'
            all_FPMG.append(fpmg)
    return all_FPMG

#TODO select brand #TODO select model
def filtered_form(brand_model,fuel_array, power_from_array,power_to_array ,mileage_from_array,mileage_to_array, gearbox_array):
    all_urls = []
    all_FPMG = contruct_all_possibilities_for_FPMG(fuel_array,power_from_array,power_to_array,mileage_from_array,mileage_to_array,gearbox_array)
    for fpmg in all_FPMG:
        page_url = f'{website}/lst/{brand_model}/?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&{fpmg}&powertype=kw&search_id=ppuu00tm4c&sort=standard&source=homepage_search-mask&ustate=N%2CU'
        all_urls.append(page_url)
    return all_urls

#Working <<Tested>>
def generate_url_for_web(brand,selected_brand_models, country_array):
    all_brand_model_country_array = []

    brand_url = f'https://www.autoscout24.com/lst/{brand}?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&powertype=kw&search_id=72faoj4adc&sort=standard&source=homepage_search-mask&ustate=N%2CU'

    driver.get(brand_url)
    brand_car_info = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h1[@data-testid = "list-header-title"]'))
    )
    brand_car_info_text = brand_car_info.text
    brand_car_amount_text = brand_car_info_text.split(' ')[0]
    brand_car_amount = pure_number(brand_car_amount_text)
    #print(f'Brand car amount is : {brand_car_amount}')
    index = 0
    if int(brand_car_amount) > 400:

        for each_brand_model in selected_brand_models:
            brand_model_url = f'https://www.autoscout24.com/lst/{each_brand_model}?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&powertype=kw&search_id=72faoj4adc&sort=standard&source=homepage_search-mask&ustate=N%2CU'
            driver.get(brand_model_url)
            car_info = WebDriverWait(driver, 20).until(
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

#Completed <<WORKING>><<Tested>>
def brand_model_for_web(wanted_brand):
    page_url = f'{website}/lst/{wanted_brand}?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&powertype=kw&search_id=ppuu00tm4c&sort=standard&source=homepage_search-mask&ustate=N%2CU'
    driver.get(page_url)
    # TODO ALL Models
    all_brand_input_for_model = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_elements(By.XPATH, '//div[@class = "input-wrapper"]/input')
    )
    brand_model = all_brand_input_for_model[1]
    brand_model.click()
    try:
        all_models = driver.find_elements(By.XPATH, '//li[@role= "option"]')
        brand_model_array = []
        for model in all_models:
            model_text = model.text
            lower_text = model_text.lower()
            final_model_letter = ''
            for model_letter in lower_text:
                if model_letter == ' ':
                    model_letter = '-'
                final_model_letter = final_model_letter + model_letter
                brand_model_array.append(final_model_letter)
        return brand_model_array
    except:
        pass

#Completed <<Tested>>
def generate_specific_brand_model_country_url_for_web(brand,selected_models):
    print(f'Selected models:{selected_models}')
    country_array = ['D', 'A', 'B', 'E', 'F', 'I', 'L', 'NL']
    models = brand_model_for_web(brand)
    brand_model_array = []

    for model in selected_models:

        brand_model_text = f'{brand}/{model}'
        brand_model_array.append(brand_model_text)
    print(f'Brand model array: {brand_model_array}')

    brand_model_country_urls = generate_url_for_web(brand,brand_model_array, country_array)
    return brand_model_country_urls

def fix_car_amount(amount_text):
    try:
        splitted_car_amount = amount_text.split(',')
        return splitted_car_amount[0]+splitted_car_amount[1]
    except:
        return amount_text
    
def check_car_amount():
    car_info = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//h1[@data-testid = "list-header-title"]'))
    )
    car_info_text = car_info.text
    car_amount_text = car_info_text.split(' ')[0]
    return car_amount_text

spinner_css = """
<style>
.spinner-container {
    display: flex;
    align-items: center;
    justify-content: center;
    height: auto; 
}
.loader {
    position: fixed; 
    top: 50%; 
    left: 50%; 
    transform: translate(-50%, -50%); 
    display: flex;
    justify-content: center;
    -webkit-box-reflect: below -25px linear-gradient(transparent,#0005);
    margin-top: 20px;
    font-size: 3em;
    color: transparent;
    text-transform: uppercase;
    -webkit-text-stroke: 1px black;
    font-weight: 800;
}
.loader span {
    display: inline-block; 
    animation: wavy 1s ease-in-out infinite;
}
.loader span:nth-child(1) { animation-delay: 0.1s; }
.loader span:nth-child(2) { animation-delay: 0.2s; }
.loader span:nth-child(3) { animation-delay: 0.3s; }
.loader span:nth-child(4) { animation-delay: 0.4s; }
.loader span:nth-child(5) { animation-delay: 0.5s; }
.loader span:nth-child(6) { animation-delay: 0.6s; }
.loader span:nth-child(7) { animation-delay: 0.7s; }
.loader span:nth-child(8) { animation-delay: 0.8s; }
.loader span:nth-child(9) { animation-delay: 0.9s; }
.loader span:nth-child(10) { animation-delay: 1s; }

@keyframes wavy {
    0% {
        transform: translateY(0);
        color: transparent;
        text-shadow: none;
    }
    20% {
        transform: translateY(-15px); 
        color: #040d15;
        text-shadow: 0 0 5px #040d15,
                     0 0 25px #040d15,
                     0 0 50px #040d15;
    }
    40%, 100% {
        transform: translateY(0);
        color: transparent;
        text-shadow: none;
    }
}
.hidden {
    opacity: 0;
    visibility: hidden;
}
</style>
"""

spinner_html = """
<div class="spinner-container">
    <div class="loader">
        <span>L</span>
        <span>O</span>
        <span>A</span>
        <span>D</span>
        <span>I</span>
        <span>N</span>
        <span>G</span>
        <span>.</span>
        <span>.</span>
        <span>.</span>
    </div>
</div>
"""
if 'loading' not in st.session_state:
    st.session_state['loading'] = False

#Completed <<Tested>>
def scrap_page_by_page_web(selected_brands,selected_models,counter,fuel_array, power_from_array, power_to_array, mileage_from_array,mileage_to_array, gearbox_array,status): 
    brands_models = sorting_model_brand_selections(selected_brands,selected_models,all_model_for_each_brand,all_brands)
    if 'all_df' not in st.session_state:
        st.session_state.all_df = []
    all_url = []
    for brand_model in brands_models:
        all_url = all_url + filtered_form(brand_model,fuel_array, power_from_array,power_to_array ,mileage_from_array,mileage_to_array, gearbox_array)
       
    url_index = 0
    for url in all_url:
        if not status:  # Dış döngüyü de durdur
            break 
        print(f'Current url index = {url_index} Length of all url: {len(all_url)} -> Url : {url_index}')
        
        driver.get(url)
        
        car_amount = int(fix_car_amount(check_car_amount()))
        
        
        last_page_num = find_last_page_num()
        split_elements = split_url_until_find_page_add_powertype(url)
        
        for page_index in range(1, last_page_num + 1):    
            if not status:  
                break  

            webpage_url = f'{split_elements[0]}&page={page_index}&powertype{split_elements[1]}'
            
            all_car_array_with_0_pages = all_car_links(webpage_url)

            all_car_array = all_car_array_with_0_pages[:car_amount]

            for each_link in all_car_array:
                
                if not status:           
                    break
           
                df = scrap_the_page_to_df(each_link)
                
                try:
                    st.write(display_cards(df))
                    print(f'WEB=> Df is : {df}')
                    st.session_state.all_df.append(df)
                    counter += 1
                    print(f'Current Page Number -----> {page_index} //// Car ----> {counter}')
                except:
                    pass                  
           
        url_index += 1
                 
    if 'all_df' in st.session_state:
        all_df = st.session_state.all_df
        if isinstance(all_df, list) and len(all_df) > 0:
           
            combined_df = pd.concat(all_df, ignore_index=True)
            combined_df.to_csv('temp_data.csv', index=False)
            st.session_state.all_df = combined_df 
        
        elif isinstance(all_df, pd.DataFrame) and not all_df.empty:
            all_df.to_csv('temp_data.csv', index=False)
        else:
            st.session_state.loading = False
            st.markdown(
            "<style>.spinner-container { display: none; }</style>",
            unsafe_allow_html=True
            )  
            st.warning('No car found...')
    
    del st.session_state['all_df']

    driver.close()

def remove_temp_csv(csv_name):
    if os.path.exists(csv_name):
        os.remove(csv_name)

def display_cards(df):
    with st.container():
    # Basic information to be displayed on the card surface
        st.markdown(
            f"""                     
                <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Brand:</span>  {df['brand'].values[0]} 
                <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Model:</span> {df['model'].values[0]}  
                <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Price:</span> {df['price'].values[0]}            
    """, 
    unsafe_allow_html=True
        )
        with st.expander(          
            "View Details", expanded=False):           
            st.markdown(f"""   
                <div class="card">
                    <h3>{df['brand'].values[0]} {df['model'].values[0]}  </h3>
                        <!-- Detailed Informations -->          
                        <p><strong>Fuel type:</strong> {df['Fuel type'].values[0]}</p>     
                        <p><strong>Mileage:</strong> {df['Mileage'].values[0]}</p>     
                        <p><strong>Gearbox:</strong> {df['Gearbox'].values[0]}</p>     
                        <p><strong>Power:</strong> {df['Power'].values[0]}</p>  
                        <p><strong>Type:</strong> {df['Type'].values[0]}</p>                  
                        <p><strong>First Registration:</strong> {df['First registration'].values[0]}</p>                                                                                           
                        <p><strong>Seller:</strong> {df['Seller'].values[0]}</p>
                </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid black; margin: 20px 0;'>", unsafe_allow_html=True)
                
def find_all_brands_array():
    all_brands_array = []

    all_brand_input = driver.find_elements(By.XPATH,'//div[@class = "input-wrapper"]/input')
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
            print(f'Brand: {final_letter_brand}')
            all_brands_array.append(final_letter_brand)
    return all_brands_array

def find_all_brand_model_array():
    print('Starting to work!')
    all_brand_model_array = []
    
    all_brands_array = find_all_brands_array()
    for brand_key in all_brands_array:
        page_url = f'{website}/lst/{brand_key}?atype=C&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=0&powertype=kw&search_id=ppuu00tm4c&sort=standard&source=homepage_search-mask&ustate=N%2CU'
        driver.get(page_url)
        # TODO ALL Models
        
        all_brand_input_for_model = WebDriverWait(driver, 20).until(
            lambda driver: driver.find_elements(By.XPATH,
                                                '//div[@class = "input-wrapper"]/input')
        )
        
        brand_input_for_model = all_brand_input_for_model[1]
        brand_input_for_model.click()
        try:
            all_models = driver.find_elements(By.XPATH, '//li[@role= "option"]')
            all_models_array  = []
            for model in all_models:
                model_text = model.text
                lower_text = model_text.lower()
                final_model_letter = ''
                for model_letter in lower_text:
                    if model_letter == ' ':
                        model_letter = '-'
                    final_model_letter = final_model_letter + model_letter
                all_models_array.append(final_model_letter)
                print(f'Current  = {brand_key}/{final_model_letter}')
            all_brand_model_array.append(all_models_array)
        except Exception as e:
            print(f'Error : {e}')

    return all_brand_model_array

#all_brands = find_all_brands_array()
#Output of the find_all_brands_array
all_brands= ['audi', 'bmw', 'ford', 'mercedes-benz', 'opel', 'volkswagen', 'renault', 'other-makes', '9ff', 'abarth', 'ac', 'acm', 'acura', 'aiways', 'aixam', 'alba-mobility', 'alfa-romeo', 'alpina', 'alpine', 'amphicar', 'angelelli-automobili', 'ariel-motor', 'artega', 'aspark', 'aspid', 'aston-martin', 'aurus', 'austin', 'austin-healey', 'autobianchi', 'baic', 'bedford', 'bellier', 'bentley', 'boldmen', 'bolloré', 'borgward', 'brilliance', 'bristol', 'brute', 'bugatti', 'buick', 'byd', 'cadillac', 'caravans-wohnm', 'carver', 'casalini', 'caterham', 'cenntro', 'changhe', 'chatenet', 'chery', 'chevrolet', 'chrysler', 'cirelli', 'citroen', 'cityel', 'corvette', 'cupra', 'dacia', 'daewoo', 'daf', 'daihatsu', 'daimler', 'dallara', 'dangel', 'de-la-chapelle', 'de-tomaso', 'delorean', 'devinci-cars', 'dfsk', 'dodge', 'donkervoort', 'dr-automobiles', 'ds-automobiles', 'dutton', 'e.go', 'econelo', 'edran', 'elaris', 'embuggy', 'emc', 'estrima', 'evetta', 'evo', 'ferrari', 'fiat', 'fisker', 'forthing', 'foton', 'gac-gonow', 'galloper', 'gappy', 'gaz', 'gem', 'gemballa', 'genesis', 'giana', 'gillet', 'giotti-victoria', 'gmc', 'goupil', 'great-wall', 'grecav', 'gta', 'gwm', 'haima', 'hamann', 'haval', 'hiphi', 'holden', 'honda', 'hongqi', 'hummer', 'hurtan', 'hyundai', 'ich-x', 'ineos', 'infiniti', 'innocenti', 'iso-rivolta', 'isuzu', 'iveco', 'izh', 'jac', 'jaecoo', 'jaguar', 'jeep', 'jensen', 'karma', 'kg-mobility', 'kia', 'koenigsegg', 'ktm', 'lada', 'lamborghini', 'lancia', 'land-rover', 'ldv', 'leapmotor', 'levc', 'lexus', 'lifan', 'ligier', 'lincoln', 'linzda', 'lorinser', 'lotus', 'lucid', 'lynk-&-co', 'm-ero', 'mahindra', 'man', 'mansory', 'martin', 'martin-motors', 'maserati', 'matra', 'maxus', 'maybach', 'mazda', 'mclaren', 'mega', 'melex', 'mercury', 'mg', 'micro', 'microcar', 'militem', 'minari', 'minauto', 'mini', 'mitsubishi', 'mitsuoka', 'morgan', 'moskvich', 'mp-lafer', 'mpm-motors', 'nio', 'nissan', 'nsu', 'oldsmobile', 'oldtimer', 'omoda', 'ora', 'pagani', 'panther-westwinds', 'peugeot', 'pgo', 'piaggio', 'plymouth', 'polestar', 'pontiac', 'porsche', 'proton', 'puch', 'ram', 'regis', 'reliant', 'rolls-royce', 'rover', 'ruf', 'saab', 'santana', 'seat', 'segway', 'selvo', 'seres', 'sevic', 'sgs', 'shelby', 'shuanghuan', 'silence', 'singer', 'skoda', 'skywell', 'smart', 'speedart', 'sportequipe', 'spyker', 'ssangyong', 'stormborn', 'streetscooter', 'studebaker', 
'subaru', 'suzuki', 'swm', 'talbot', 'tasso', 'tata', 'tazzari-ev', 'techart', 'tesla', 'togg', 'town-life', 'toyota', 'trabant', 'trailer-anhänger', 'triumph', 'trucks-lkw', 'tvr', 'uaz', 'vanden-plas', 'vanderhall', 
'vaz', 'vem', 'vinfast', 'volvo', 'voyah', 'wartburg', 'weltmeister', 'wenckstern', 'westfield', 'wey', 'wiesmann', 'xbus', 'xev', 'xpeng', 'zastava', 'zaz', 'zeekr', 'zhidou', 'zotye', 'others']

#all_models_array = find_all_brand_model_array()
#Output of the find_all_brand_model_array
all_model_for_each_brand = [['100', '200', '50', '80', '90', 'a1', 'a2', 'a3', 'a4', 'a4-allroad', 'a5', 'a6', 'a6-allroad', 'a7', 'a8', 'allroad', 'cabriolet', 'coupe', 'e-tron', 'e-tron-gt', 'q1', 'q2', 'q3', 'q4-e-tron', 'q5', 'q6', 'q7', 'q8', 'q8-e-tron', 'quattro', 'r8', 'rs', 'rs-e-tron-gt', 'rs-q3', 'rs-q5', 'rs-q8', 'rs2', 'rs3', 'rs4', 'rs5', 'rs6', 'rs7', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 'sq2', 'sq3', 'sq5', 'sq6', 'sq7', 'sq8', 'sq8-e-tron', 'tt', 'tt-rs', 'tts', 'v8', 'others'], ['1-series-(all)', '114', '116', '118', '120', '123', '125', '128', '130', '135', '140', '2-series-(all)', '214', '216', '218', '220', '223', '225', '228', '230', '235', '240', '2002', '3-series-(all)', '315', '316', '318', '320', '323', '324', '325', '328', '330', '335', '340', 'active-hybrid-3', '4-series-(all)', '418', '420', '425', '428', '430', '435', '440', '5-series-(all)', '518', '520', '523', '524', '525', '528', '530', '535', '540', '545', '550', 'active-hybrid-5', '6-series-(all)', '620', '628', '630', '633', '635', '640', '645', '650', '7-series-(all)', '725', '728', '730', 
'732', '735', '740', '745', '750', '760', 'active-hybrid-7', '8-series-(all)', '830', '840', '850', 'i3', 'i4', 'i5', 'i7', 'i8', 'ix', 'ix1', 'ix2', 'ix3', 'm-series-(all)', '1er-m-coupé', 'm1', 'm2', 'm3', 'm4', 'm5', 'm550', 'm6', 'm8', 'm850', 'x-series-(all)', 'active-hybrid-x6', 'x1', 'x2', 'x2-m', 'x3', 'x3-m', 'x4', 'x4-m', 'x5', 'x5-m', 'x6', 'x6-m', 'x7', 'x7-m', 'xm', 'z-series-(all)', 'z1', 'z3', 'z3-m', 'z4', 'z4-m', 'z8', 'others'], ['aerostar', 'b-max', 'bronco', 'c-max', 'capri', 'connect-elekto', 'consul', 'cougar', 'courier', 'crown', 'customline', 'econoline', 'econovan', 'ecosport', 'edge', 'escape', 'escort', 'excursion', 'expedition', 'explorer', 'express', 'f-1', 'f-100', 'f-150', 'f-250', 'f-350', 'f-360', 'f-450', 'f-550', 'f-650', 'f-super-duty', 'fairlane', 'falcon', 'fiesta', 'flex', 'focus', 'focus-c-max', 'focus-cc', 'freestar', 'freestyle', 'fusion', 'galaxy', 'gran-torino', 'granada', 'grand-c-max', 'grand-tourneo', 'gt', 'ka/ka+', 'kuga', 'm', 'maverick', 'mercury', 'mondeo', 'mustang', 'mustang-mach-e', 'orion', 'probe', 'puma', 'ranger-(all)', 'ranger', 'ranger-raptor', 'rs-200', 's-max', 'scorpio', 'sierra', 'sportka', 'streetka', 'taunus', 'taurus', 'thunderbird', 'torino', 'tourneo-(all)', 'tourneo', 'tourneo-connect', 'tourneo-courier', 'tourneo-custom', 'transit-(all)', 'e-transit', 'transit', 'transit-bus', 'transit-connect', 'transit-courier', 'transit-custom', 'windstar', 'others'], ['170', '180', '190', '200', '208', '210/310', '220', '230', '240', '250', '260', '270', '280', '300', '308', '320', '350', '380', '400', '416', '420', '450', '500', '560', '600', 'a-series-(all)', 'a-140', 'a-150', 'a-160', 'a-170', 'a-180', 'a-190', 'a-200', 'a-210', 'a-220', 'a-250', 'a-35-amg', 'a-45-amg', 'actros', 'amg-gt', 'amg-one', 'atego', 'b-series-(all)', 'b-150', 'b-160', 'b-170', 'b-180', 'b-200', 'b-220', 'b-250', 'b-electric-drive', 'c-series-(all)', 'c-160', 'c-180', 'c-200', 'c-220', 'c-230', 'c-240', 'c-250', 'c-270', 'c-280', 'c-30-amg', 'c-300', 'c-32-amg', 'c-320', 'c-350', 'c-36-amg', 'c-400', 'c-43-amg', 'c-450', 'c-55-amg', 'c-63-amg', 'ce-(all)', 'ce-200', 'ce-220', 'ce-230', 'ce-280', 'ce-300', 
'citan', 'cl-(all)', 'cl', 'cl-160', 'cl-180', 'cl-200', 'cl-220', 'cl-230', 'cl-320', 'cl-420', 'cl-500', 'cl-55-amg', 'cl-600', 'cl-63-amg', 'cl-65-amg', 'cla-(all)', 'cla-180', 'cla-200', 'cla-220', 'cla-250', 'cla-35-amg', 'cla-45-amg', 'clc', 'cle', 'cle-180', 'cle-200', 'cle-220', 'cle-300', 'cle-450', 'cle-53-amg', 'cle-63-amg', 'clk-(all)', 'clk', 'clk-200', 'clk-220', 'clk-230', 'clk-240', 'clk-270', 'clk-280', 'clk-320', 'clk-350', 'clk-430', 'clk-500', 'clk-55-amg', 'clk-63-amg', 'cls-(all)', 'cls', 'cls-220', 'cls-250', 'cls-280', 'cls-300', 'cls-320', 'cls-350', 'cls-400', 'cls-450', 'cls-500', 'cls-53-amg', 'cls-55-amg', 'cls-63-amg', 'e-series-(all)', 'e-200', 'e-220', 'e-230', 'e-240', 'e-250', 'e-260', 'e-270', 'e-280', 'e-290', 'e-300', 'e-320', 'e-350', 'e-36-amg', 'e-400', 'e-420', 'e-43-amg', 'e-430', 'e-450', 'e-50-amg', 'e-500', 'e-53-amg', 'e-55-amg', 'e-550', 'e-60-amg', 'e-63-amg', 'eq-series-(all)', 'eqa', 'eqa-250', 'eqa-300', 'eqa-350', 'eqb-250', 'eqb-300', 'eqb-350', 'eqc-400', 'eqe-300', 'eqe-350', 'eqe-43', 'eqe-500', 'eqe-53', 'eqe-suv', 'eqs', 'eqs-suv', 'eqt', 'eqv-250', 'eqv-300', 'g-series-(all)', 'g', 'g-230', 'g-240', 'g-250', 'g-270', 'g-280', 'g-290', 'g-300', 'g-320', 'g-350', 'g-400', 'g-450', 'g-500', 'g-55-amg', 'g-580', 'g-63-amg', 'g-65-amg', 'g-650', 'gl-(all)', 'gl-320', 'gl-350', 'gl-400', 'gl-420', 'gl-450', 'gl-500', 'gl-55-amg', 'gl-63-amg', 'gla-(all)', 'gla-180', 'gla-200', 'gla-220', 'gla-250', 'gla-35-amg', 'gla-45-amg', 'glb-(all)', 'glb-180', 'glb-200', 'glb-220', 'glb-250', 'glb-35-amg', 'glc-(all)', 'glc-200', 'glc-220', 'glc-250', 'glc-300', 'glc-350', 'glc-400', 'glc-43-amg', 'glc-450', 'glc-63-amg', 'gle-(all)', 'gle-250', 'gle-300', 'gle-350', 'gle-400', 'gle-43-amg', 'gle-450', 'gle-500', 'gle-53-amg', 'gle-580', 'gle-63-amg', 'glk-(all)', 'glk-200', 'glk-220', 'glk-250', 'glk-280', 'glk-300', 'glk-320', 'glk-350', 'gls-(all)', 'gls-350', 'gls-400', 'gls-450', 'gls-500', 'gls-580', 'gls-600', 'gls-63-amg', 'm-series-(all)', 'ml-230', 'ml-250', 'ml-270', 'ml-280', 'ml-300', 'ml-320', 'ml-350', 'ml-400', 'ml-420', 'ml-430', 'ml-450', 'ml-500', 'ml-55-amg', 'ml-63-amg', 'marco-polo', 'maybach-gls', 'maybach-s-klasse', 'mb-100', 'r-series-(all)', 'r-280', 'r-300', 'r-320', 'r-350', 'r-500', 'r-63-amg', 's-series-(all)', 's-250', 's-260', 's-280', 's-300', 's-320', 's-350', 's-380', 's-400', 's-420', 's-430', 's-450', 's-500', 's-55-amg', 's-550', 's-560', 's-560-e', 's-580', 's-600', 's-63-amg', 's-65-amg', 's-650', 's-680', 'sl-(all)', 'sl-230', 'sl-250', 'sl-280', 'sl-300', 'sl-320', 'sl-350', 'sl-380', 'sl-400', 'sl-420', 'sl-43-amg', 'sl-450', 'sl-500', 'sl-55-amg', 'sl-560', 'sl-60-amg', 'sl-600', 'sl-63-amg', 'sl-65-amg', 'sl-70-amg', 'sl-73-amg', 'slc-(all)', 'slc-180', 'slc-200', 'slc-250', 'slc-280', 'slc-300', 'slc-350', 'slc-380', 'slc-43-amg', 'slc-450', 'slc-500', 'slk-(all)', 'slk', 'slk-200', 'slk-230', 'slk-250', 'slk-280', 'slk-300', 'slk-32-amg', 'slk-320', 'slk-350', 'slk-55-amg', 'slr', 'sls', 'sprinter', 't-class', 't1', 't2', 'v-series-(all)', 'v', 'v-200', 'v-220', 'v-230', 'v-250', 'v-280', 'v-300', 'vaneo', 'vario', 'viano', 'vito', 'w-114/115-strich-acht', 'x-series-(all)', 'x-220', 'x-250', 'x-350', 'others'], ['adam', 'agila', 'ampera', 'ampera-e', 'antara', 'arena', 'ascona', 'astra', 'calibra', 'campo', 'cascada', 'combo', 'combo-life', 'combo-e', 'combo-e-life', 'commodore', 'corsa', 'corsa-e', 'crossland', 'crossland-x', 'diplomat', 'frontera', 'grandland', 'grandland-x', 'gt', 'insignia', 'kadett', 'karl', 'manta', 'meriva', 'mokka', 'mokka-x', 'mokka-e', 'monterey', 'monza', 'movano', 'movano-e', 'omega', 'pick-up-sportscap', 'rekord', 'rocks-e', 'senator', 'signum', 'sintra', 'speedster', 'tigra', 'vectra', 'vivaro', 'vivaro-e', 'zafira', 'zafira-life', 'zafira-tourer', 'others'], ['181', 'amarok', 'anfibio', 'arteon', 'atlas', 'beetle', 'bora', 'buggy', 'bus', 'caddy', 'cc', 'coccinelle', 'corrado', 'crafter', 'cross-touran', 'derby', 'e-up!', 'eos', 'escarabajo', 'fox', 'golf-(all)', 'cross-golf', 'golf', 'golf-cabriolet', 'golf-gtd', 'golf-gte', 'golf-gti', 'golf-plus', 'golf-r', 'golf-sportsvan', 'golf-variant', 'e-golf', 'grand-california', 'id.-buzz-(all)', 'id.-buzz', 'id.-buzz-cargo', 'id.3', 'id.4', 'id.5', 'id.6', 'id.7', 'iltis', 'jetta', 'käfer', 'karmann-ghia', 'kever', 
'l80', 'lt', 'lupo', 'maggiolino', 'new-beetle', 'passat-(all)', 'passat', 'passat-alltrack', 'passat-cc', 'passat-variant', 'phaeton', 'pointer', 'polo-(all)', 'polo', 'polo-cross', 'polo-gti', 'polo-plus', 'polo-r-wrc', 'polo-sedan', 'polo-variant', 'routan', 'santana', 'scirocco', 'sharan', 't-cross', 't-roc', 't1', 't2', 't3-series-(all)', 't3', 't3-blue-star', 't3-california', 't3-caravelle', 't3-kombi', 't3-multivan', 't3-white-star', 't4-series-(all)', 't4', 't4-allstar', 't4-california', 't4-caravelle', 't4-kombi', 't4-multivan', 't5-series-(all)', 't5', 't5-california', 't5-caravelle', 't5-kombi', 't5-multivan', 't5-shuttle', 't5-transporter', 't6-series-(all)', 't6-california', 't6-caravelle', 't6-kombi', 't6-multivan', 't6-transporter', 't6.1', 't6.1-california', 't6.1-caravelle', 't6.1-kombi', 't6.1-multivan', 't6.1-transporter', 't7', 't7-california', 't7-caravelle', 't7-kastenwagen', 't7-kombi', 't7-multivan', 'taigo', 'taro', 'tayron', 'tiguan-(all)', 'tiguan', 'tiguan-allspace', 'touareg', 'touran', 'transporter', 'up!', 'vento', 'viloran', 'xl1', 'others'], ['alaskan', 'alpine-a110', 'alpine-a310', 'alpine-a610', 'alpine-v6', 'arkana', 'austral', 'avantime', 'captur', 'clio', 'coupe', 'duster', 'espace', 'express', 'fluence', 'fluence-z.e.', 'fuego', 'grand-espace', 'grand-modus', 'grand-scenic', 'kadjar', 'kangoo', 'kangoo-e-tech', 'kangoo-z.e.', 'koleos', 'laguna', 'latitude', 'logan', 'mascott', 'master', 'megane', 'megane-e-tech', 'messenger', 'modus', 'p-1400', 'r-11', 'r-14', 'r-18', 'r-19', 'r-20', 'r-21', 'r-25', 'r-30', 'r-4', 'r-5', 'r-6', 'r-9', 'rafale', 'rapid', 'safrane', 'sandero', 'sandero-stepway', 'scenic', 'spider', 'super-5', 'symbioz', 'symbol', 'talisman', 'trafic', 'twingo', 
'twizy', 'vel-satis', 'wind', 'zoe', 'others'], [], ['f70-etronic', 'f97-a-max', 'gt9', 'gtronic', 'gturbo', 'speed9', 'others'], ['124-gt', '124-rally-tribute', '124-spider', '500', '500c', '500e', '595', '595-competizione', '595-pista', '595-turismo', '595c', '695', '695c', 'grande-punto', 'punto-evo', 'punto-supersport', 'others'], ['ace', 'cobra', 'others'], ['4-wd', 'biagini-passo', 'others'], ['ilx', 'mdx', 'nsx', 'rdx', 'rl', 'rlx', 'rsx', 'tl', 'tlx', 'tsx', 'zdx', 'others'], ['u5', 'u6-ion', 'others'], ['400', '500', 'a.', 'city', 'coupe', 'crossline', 'crossover', 'd-truck', 'e-truck', 'gti', 'gto', 'mac', 'mega', 'roadline', 'scouty-r', 'others'], ['cargo', 'golf-cart', 'le-22-limited-edition', 'street-cart', 'tour-cart', 'others'], ['145', '146', '147', '155', '156', '159', '164', '166', '1750', '2000', '33', '4c', '75', '8c', '90', 'alfa-6', 'alfasud', 'alfetta', 'brera', 'crosswagon', 'giulia', 'giulietta', 'gt', 'gtv', 'junior', 'mito', 'montreal', 'quadrifoglio', 'rz', 'spider', 'sportwagon', 'sprint', 'stelvio', 'sz', 'tonale', 'others'], ['b10', 'b11', 'b12', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'c1', 'c2', 'd10', 'd3', 'd4', 'd5', 'roadster-limited-edition', 'roadster-s', 'roadster-v8', 'xb7', 'xd3', 'xd4', 'others'], ['a110', 'a290', 'others'], ['770', 'others'], ['d-1-s-hypercar', 'd-2-gt-granturismo-v12', 'd-3-hypersuv', 'effequaranta', 'hintegrale', 'others'], ['atom', 'nomad', 'others'], ['gt', 'karo', 'scalo', 'others'], ['owl', 'others'], ['gt-21', 'ss', 'others'], ['ar1', 'cygnet', 'db', 'db11', 'db12', 'db7', 'db9', 'dbs', 'dbx', 'lagonda', 'rapide', 'v8', 'valkyrie', 'vanquish', 'vantage', 'virage', 'volante', 'others'], ['komendant', 'others'], ['estate', 'healey', 'maestro', 'metro', 'mini', 'mini-moke', 'mk', 'montego', 'others'], ['100', '3000', 'sprite', 'others'], ['a-1000', 'a-112', 'y10', 'others'], ['b40', 'beijing-x35', 'beijing-x55', 'beijing-x75', 'bj20', 'bj40', 'bj80', 'd20', 'senova-d50', 'senova-x25', 'senova-x35', 'senova-x55', 'senova-x65', 'senova-zhixing', 'others'], ['astramax', 'astravan', 'beagle', 'blitz', 'brava', 'ca', 'cf2', 'chevanne', 'dormobile', 'ha', 'kb', 'midi', 'mw', 'rascal', 'tj', 'others'], ['asso', 'b8', 'divane', 'docker', 'jade', 'opale', 'sturdy', 'vx', 'others'], ['arnage', 'azure', 'bacalar', 'bentayga', 'brooklands', 'continental', 'continental-gt', 'continental-gtc', 'eight', 'flying-spur', 'mulsanne', 's1', 's2', 's3', 'turbo-r', 'turbo-rt', 'turbo-s', 'others'], ['cr-4', 'others'], ['bluecar', 'bluesummer', 'blueutility', 'others'], ['arabella', 'bx5', 'bx7', 'hansa-1100', 'hansa-1500', 'hansa-1700', 'hansa-1800', 'hansa-2000', 'hansa-2300', 'hansa-2400', 'hansa-3500', 'hansa-400/500', 'isabella', 'p100', 'others'], ['bc3', 'bs2', 'bs4', 'bs6', 'granse', 'jinbei', 'zhonghua', 'zunchi', 'others'], ['405', '408', 'others'], ['custom', 'others'], ['centodieci', 'chiron', 'divo', 'eb-110', 'eb-112', 'veyron', 'others'], ['cascada', 'century', 'electra', 'enclave', 'encore', 'envision', 'lacrosse', 'le-sabre', 'park-avenue', 'regal', 'riviera', 'roadmaster', 'skylark', 'special', 'verano', 'others'], ['atto-3', 'dolphin', 'e6', 'f1', 'f3', 'f3r', 'f6', 'f8', 'han', 'seal', 'seal-u', 'tang', 'others'], ['allante', 'ats', 'bls', 'brougham', 'ct4', 'ct5', 'ct6', 'cts', 'deville', 'dts', 'eldorado', 'escalade', 'fleetwood', 'lasalle', 'lyriq', 'series-62', 'series-6200', 'seville', 'srx', 'sts', 'xlr', 'xt4', 'xt5', 'xt6', 'xts', 'others'], ['adria', 'ahorn', 'airstream', 'alpha', 'arca', 'autoroller', 'autostar', 'bavaria', 'bawemo', 'beisl', 'benimar', 'bimobil', 'biod', 'burow', 'burow-mobil', 'bürstner', 'ca-mo-car', 'carado', 'caravelair', 'caro', 'carthago', 'challenger', 'chausson', 'chrysler', 'ci-international', 'coachmen', 'concorde', 'cristall', 'cs-reisemobile', 'damon', 'dehler', 'delta', 'dethleffs', 'dream', 'due-erre', 'eifelland', 'elnagh', 'eriba', 'euramobil', 'euro-liner', 'evm', 'fendt', 'ffb-/-tabbert', 'fiat', 'fleetwood', 'florence', 'ford', 'ford-/-reimo', 'frankia', 'general-motors', 'gigant', 'giottiline', 'globecar', 'granduca', 'hehn', 'heku', 'hobby', 'holiday-rambler', 'home-car', 'hymer', 'icf', 'iveco', 'karmann', 'kentucky', 'kip', 'knaus', 'la-strada', 'laika', 'linne-liner', 'lmc', 'm+m-mobile', 'ma-bu', 'maesss', 'man', 'mazda', 'mclouis', 'megamobil', 'mercedes-benz', 'miller', 'mirage', 'mitsubishi', 'mizar', 'mobilvetta', 'monaco', 'moncayo', 'morelo', 'neotec', 'niesmann+bischoff', 'niewiadow', 'nordstar', 'ormocar', 'peugeot', 'phoenix', 'pilote', 'pössl', 'procab', 'rapido', 'reimo', 'reisemobile-beier', 'renault', 'rimor', 'riva', 'riviera', 'rmb', 'roadtrek', 'robel-mobil', 'rockwood', 'selbstbau', 'sterckeman', 'sunlight', 'swift', 'tabbert', 'tec', 'tischer', 'trigano', 'triple-e', 'ultra', 'vario', 'vw', 'weinsberg', 'weippert', 'westfalia', 'wilk', 'winnebago', 'others'], ['base', 'cargo', 'others'], ['kerry', 'm10', 'm110', 'm12', 'm14', 'm20', 'pick-up12', 'sulky', 'sulkycar', 'sulkydea/ydea', 'others'], ['21', 'aeroseven', 'classic-7', 'classic-line', 'classic-s7', 'cosworth-csr-200', 'csr-175', 'csr-260', 'r-400', 'r300-superlight', 'roadsport-seven', 'seven-270', 'seven-310', 'seven-360', 'seven-420', 'seven-485', 'seven-620', 'sp/300.r', 'super-7', 'superlight', 'vxi', 'others'], ['avantier-c', 'logistar-100', 'logistar-200', 'logistar-260', 'metro', 'neibor-150', 'neibor-200', 'others'], ['a6', 'coolcar', 'freedom', 'ideal', 'mini-truck', 'q25', 'q35', 'q7', 'x5', 'others'], ['barooder', 'ch-26', 'ch-28', 'ch-30', 'ch-32', 'ch-40', 'ch-46', 'media', 'pick-up', 'speedino', 'sporteevo', 'stella', 'others'], ['à13', 'a18', 'a21', 'a3', 'amulet', 'arrizo', 'b13', 'b14', 'crosseastar', 'crossover', 'eastar', 'eq', 'fengyun', 'fora', 'fulwin', 'karry', 'kimo', 'm11', 'm14', 'mikado', 'mpv', 'qq', 's18', 'sweet', 'tiggo', 'very', 'wow', 'others'], ['2500', 'alero', 'astro', 'avalanche', 'aveo', 'bel-air', 'beretta', 'blazer', 'bolt', 'c1500', 'camaro', 'caprice', 'captiva', 'cavalier', 'celebrity', 'chevelle', 'chevy-van', 'citation', 'colorado', 'corsica', 'corvair', 'monza', 'monza-convertible', 'monza-coupé', 'monza-sport-sedan', 'corvette', 'crew-cab', 'cruze', 'dixie-van', 'el-camino', 'epica', 'equinox', 'evanda', 'express', 'g', 'hhr', 'impala', 'k1500', 'k30', 'kalos', 'lacetti', 'lanos', 'lumina', 'malibu', 'matiz', 'monte-carlo', 'niva', 'nubira', 'orlando', 'rezzo', 's-10', 'silverado', 'spark', 'ssr', 'suburban', 'tacuma', 'tahoe', 'tracker', 'trailblazer', 'trans-sport', 'traverse', 'trax', 'uplander', 'viva', 'volt', 'others'], ['200', '300-m', '300-srt', '300c', 'aspen', 'crossfire', 'daytona', 'es', 'grand-voyager', 'gs', 'gts', 'imperial', 'le-baron', 'neon', 'new-yorker', 'pacifica', 'prowler', 'pt-cruiser', 'ram-van', 'saratoga', 'sebring', 'stratus', 'town-&-country', 'valiant', 'viper', 'vision', 'voyager', 'others'], ['cirelli-2', 'cirelli-3', 'cirelli-4', 'cirelli-5', 'cirelli-7', 'cirelli-8', 'others'], ['2cv', 'acadiane', 'ami', 'ax', 'axel', 'berlingo', 'bx', 'c-crosser', 'c-elysée', 'c-zero', 'c1', 'c15', 'c2', 'c25', 'c3-(all)', 'c3', 'c3-aircross', 'c3-picasso', 'c35', 'c4-(all)', 'c4', 'c4-aircross', 'c4-cactus', 'c4-picasso', 'c4-spacetourer', 'c4-x', 'e-c4-electric', 'e-c4-x', 'grand-c4-picasso', 'grand-c4-spacetourer', 'c5-(all)', 'c5', 'c5-aircross', 'c5-x', 'c6', 'c8', 'cx', 'ds', 'ds3', 'ds4', 'ds5', 'dyane', 'e-méhari', 'evasion', 'gsa', 'holidays', 'jumper', 'jumpy', 'lna', 'méhari', 'nemo', 'saxo', 'sm', 'spacetourer', 'traction', 'visa', 'xantia', 'xm', 'xsara', 'xsara-picasso', 'zx', 'others'], ['cityel', 'cityel-fact-four', 
'miniel', 'others'], ['c1', 'c2', 'c3', 'c4', 'c5', 'c6-convertible', 'c6-coupe', 'c7', 'c8', 'cz6', 'grand-sport', 'stingray', 'z06', 'zr1', 'others'], ['arona', 'ateca', 'born', 'formentor', 'formentor-vz5', 'ibiza', 'leon', 'tavascan', 'terramar', 'others'], ['1310', 'berlina', 'bigster', 'break', 'dokker', 'double-cab', 'drop-side', 'duster', 'jogger', 'lodgy', 'logan', 'nova', 'pick-up', 'sandero', 'solenza', 'spring', 'others'], ['aranos', 'damas', 'espero', 'evanda', 'kalos', 'korando', 'lacetti', 'lanos', 'leganza', 'lublin', 'matiz', 'musso', 'nexia', 'nubira', 'rexton', 'rezzo', 'tacuma', 'tico', 'truck-plus', 'others'], ['400', '428', 
'435', 'others'], ['applause', 'charade', 'charmant', 'copen', 'cuore', 'domino', 'extol', 'f-modelle', 'feroza', 'freeclimber', 'gran-move', 'hijet', 'materia', 'move', 'pionier', 'rocky', 'sirion', 'taft', 'terios', 
'trevis', 'valera', 'yrv', 'others'], ['double-six', 'six', 'sovereign', 'super-eight', 'super-v8', 'others'], ['stradale', 'others'], ['504', '505', 'berlingo', 'boxer', 'c15', 'c25', 'ducato', 'expert', 'j5', 'jumper', 'jumpy', 'partner', 'scudo', 'others'], ['atalante-57s', 'grand-prix', 'roadster', 'type-55-roadster', 'type-55-tourer', 'others'], ['biguà', 'deauville', 'guarà', 'longchamp', 'mangusta', 'pantera', 'vallelunga', 'others'], ['dmc-12', 'others'], ['db-721', 'others'], ['c31', 'c32', 'c35', 'c37', 'city-pickup', 'ec-35', 'f5', 'fengon', 'fengon-5', 'fengon-500', 'fengon-580', 'fengon-7', 'forthing-4', 'forthing-5', 'glory-580', 'glory-ev-3', 'k01', 'k02', 'k05', 'k07', 'rich-3', 'seres-3', 'seres-5', 'v21', 'v22', 'v25', 'v27', 'others'], ['avenger', 'caliber', 'caravan', 'challenger', 'charger', 'coronet', 'dakota', 'dart', 'demon', 'durango', 'grand-caravan', 'intrepid', 'journey', 'magnum', 'neon', 'nitro', 'ram', 'stealth', 'stratus', 'van', 'viper', 'others'], ['d8', 'f22', 's8', 'others'], ['city-cross', 'dr-3.0', 'dr-evo5', 'dr-f35', 'dr-zero', 'dr1', 'dr1.0', 'dr2', 'dr3', 'dr4', 'dr4.0', 'dr5', 'dr5.0', 'dr6', 'dr6.0', 'dr7.0', 'katay', 'pk8', 'others'], ['ds-3', 'ds-3-crossback', 'ds-4', 'ds-4-crossback', 'ds-5', 'ds-7', 'ds-7-crossback', 'ds-9', 'others'], ['b-plus', 'b-plus-series-2', 'b-type', 'beneto', 'cantera', 'legerra', 'malaga', 'malaga-b+', 'melos', 'p1', 'phaeton-series-1', 'phaeton-series-2', 'phaeton-series-3', 'phaeton-series-4', 'rico', 'rico-shuttle', 'sierra-drop-head', 'sierra-series-1', 'sierra-series-2', 'sierra-series-3', 'others'], ['e.wave-x', 'life-20', 'life-40', 'life-60', 'life-first-edition', 'mover', 'others'], ['m1', 's1', 'others'], ['mk1', 'others'], ['beo', 'caro', 'caro-s', 'dyo', 'finn', 'jaco', 'lenn', 'pio', 'others'], ['ev-angel', 'eva', 'vintage', 'others'], ['wave-2', 'wave-3', 'yudo', 'others'], ['birò', 'others'], ['openair', 'prima', 'others'], ['cross4', 'evo-electric', 'evo3', 'evo4', 'evo5', 'evo6', 'evo7', 'others'], ['12-cilindri', '195', '206', '208', '246', '250', '275', '288', '296', '296-gtb', '308', '328', '330', '348', '360', '365', '400', '412', '430-scuderia', '456', '458', '488', '512', '550', '575', '599', '612', '750', '812', 'california', 'daytona', 'dino-gt4', 'enzo-ferrari', 'f12', 'f355', 'f40', 'f430', 'f50', 'f512', 'f8-spider', 'f8-tributo', 'ff', 'fxx', 'gtc4-lusso', 'laferrari', 'mondial', 'monza', 'portofino', 'purosangue', 'roma', 'scuderia-spider-16m', 'sf90-spider', 'sf90-stradale', 'superamerica', 'testarossa', 'others'], ['124-coupè', '124-spider', '126', '127', '128', '130', '131', '132', '133', '2300', '242', '500', '500-abarth', '500c', '500c-abarth', '500e', '500l', '500x', '595-abarth', '600', '850', '900', 'albea', 'argenta', 'barchetta', 'brava', 'bravo', 'campagnola', 'cinquecento', 'coupe', 'croma', 'dino', 'doblo', 'doblo', 'e-doblo', 'ducato', 'duna', 'e-ulysse', 'fiorino', 'freemont', 'fullback', 'grande-punto', 'idea', 'linea', 'marea', 'marengo', 'maxi', 'multipla', 'new-panda', 'palio', 'panda', 'penny', 'pininfarina', 'punto', 'punto-evo', 'qubo', 'regata', 'ritmo', 'scudo', 'sedici', 'seicento', 'spider-europa', 'stilo', 'strada', 'talento', 'tempra', 'tipo', 'topolino', 'ulysse', 'uno', 'x-1/9', 'others'], ['emotion', 'karma', 'latigo-cs', 'ocean', 'orbit', 'others'], ['t5-evo', 'u-tour', 'others'], ['tunland-g7', 'others'], ['ga200', 'ga500', 'gx6', 'troy', 'victor', 'victory', 'way', 'others'], ['exceed', 'galloper', 'santamo', 'super-exceed', 'others'], ['triple-dutch', 'others'], ['22171', '22177', '2310', '24', '2401', '2402', '2404', '2410', '2411', '2412', '2434', '2705', '2752', '31', '3102', '31022', '310221', '31026', '31029', '3105', '3110', '31105', '3111', '3221', '3302', '33023', '38407', '38649', '38710', 'gazelle', 'next', 'siber', 'sobol', 'others'], ['e2', 'e4', 'e6', 'el', 'em', 'es', 'four', 'two', 'others'], ['aero', 'avalanche', 'gt', 'gtp', 'mig', 'mirage', 'mistrale', 'tornado', 'others'], ['electrified-g80', 'g70', 'g70-shooting-brake', 'g80', 'g90', 'gv60', 'gv70', 'gv80', 'others'], ['smart-3500', 'others'], ['donkervoort', 'vertigo', 'others'], ['gladiator', 'gyppo', 'others'], ['acadia', 'canyon', 'envoy', 'safari', 'savana', 'sierra', 'sonoma', 'syclone', 'terrain', 'typhoon', 'vandura', 'yukon', 'others'], ['g1', 'g4', 'g5', 'gem', 'others'], ['c20', 'c30', 'c50', 'coolbear', 'cowry', 'deer', 'florid', 'gwperi', 'h5e', 'h6', 'hover', 'm4', 'pegasus', 'safe', 'sailor', 'sing', 'socool', 'steed', 'voleex', 'wingle', 'others'], ['amica', 'eke', 'sonique', 'others'], ['spano', 'others'], ['ora-03', 'ora-07', 'wey-03', 'wey-05', 'others'], ['2', '3', '3-hb', '6', 'family', 'freema', 'fstar', 'm3', 'm5', 's5', 's7', 'v70', 'others'], ['others'], ['h2', 'h6', 'h9', 'others'], ['a', 'x', 'y', 'z', 'others'], ['coupe-60', 'gtr-x', 'hurricane', 'monaro-convertible', 'monaro-coupe', 'monaro-hrt-427', 'sandman', 'ssx', 'torana-tt36', 'utester', 'others'], ['accord', 'ascot', 'avancier', 'beat', 'capa', 'city', 'civic', 'clarity', 'concerto', 'cr-v', 'cr-z', 'crosstour', 'crx', 'e', 'e:ny1', 'element', 'fit', 'fr-v', 'hr-v', 'insight', 'inspire', 'integra', 'jazz', 'legend', 'life', 'logo', 'mobilio', 'nsx', 'odyssey', 'orthia', 'partner', 'pilot', 'prelude', 'quintet', 'ridgeline', 's-2000', 'saber', 'sabre', 'shuttle', 'sm-x', 'stepwgn', 'stream', 'torneo', 'zr-v', 'others'], ['e-hs9', 'others'], ['h1', 'h2', 'h3', 'hx', 'others'], ['albaycín', 'author', 'grand-albaycín', 'route-44', 't2', 'vintage', 'others'], ['accent', 'atos', 'avente', 'azera', 'bayon', 'coupe', 'creta', 'elantra', 'equus', 'excel', 'galloper', 'genesis', 
'genesis-coupe', 'getz', 'grace', 'grand-santa-fe', 'grandeur', 'h-100', 'h-200', 'h-300', 'h-350', 'h-1', 'highway', 'i10', 'i20', 'i30', 'i40', 'i50', 'i800', 'ioniq', 'ioniq-5', 'ioniq-6', 'ix20', 'ix35', 'ix55', 'kona', 'lantra', 'matrix', 'nexo', 'nf', 'palisade', 'pony', 'porter', 's-coupe', 'santa-fe', 'santamo', 'satellite', 'solaris', 'sonata', 'sonica', 'starex', 'staria', 'stellar', 'terracan', 'tiburon', 'trajet', 'tucson', 'veloster', 'veracruz', 'verna', 'xg-250', 'xg-30', 'xg-350', 'others'], ['k2', 'others'], ['grenadier', 'others'], ['ex25', 'ex30', 'ex35', 'ex37', 'fx', 'g25', 'g35', 'g37', 'i35', 'jx35', 'm30', 'm35', 'm37', 'm45', 'q30', 'q45', 'q50', 'q60', 'q70', 'q80', 'qx30', 'qx50', 'qx56', 'qx60', 'qx70', 'qx80', 'others'], ['clip', 'elba', 'mille', 'mini', 'minitre', 'small', 'others'], ['300', 'fidia', 'grifo', 'lele', 'vision-gt', 
'others'], ['axiom', 'bighorn', 'campo', 'd-max', 'dlx', 'gemini', 'midi', 'nkr', 'nnr', 'npr', 'pick-up', 'rodeo', 'trooper', 'wfr', 'others'], ['campagnola', 'daily', 'massif', 'others'], ['2106', '2125', '21251', '2126', '21261', '2715', '27156', '2717', '27171', '412', 'nika', 'others'], ['e-s2', 'e-s4', 'j7', 'js3', 'js4', 'js7', 't8', 'others'], ['j6', 'j7', 'others'], ['420', 'd-type', 'daimler', 'e-pace', 'e-type', 'f-pace', 'f-type', 'i-pace', 'mk-ii', 's-type', 'sovereign', 'x-type', 'x300', 'xe', 'xf', 'xj', 'xj12', 'xj40', 'xj6', 'xj8', 'xjr', 'xjs', 'xjsc', 'xk', 'xk8', 'xkr', 'others'], ['avenger', 'cherokee', 'cj-5', 'cj-7', 'cj-8', 'comanche', 'commander', 'compass', 'gladiator', 'grand-cherokee', 'liberty', 'patriot', 'renegade', 'wagoneer', 'willys', 'wrangler', 'others'], ['541', 'c-v8', 'convertible', 'coupé', 'ff', 'gt', 'healey-mk.1', 'healey-mk.2', 'interceptor', 'mk-ii', 'mk-iii', 'mk-iv', 's-v8', 'sp', 'others'], ['gs-6', 'gse-6', 'pininfarina-gt', 'revero', 'revero-gt', 'others'], ['actyon', 'family', 'kallista', 'korando', 'kyron', 'musso', 'rexton', 'rodius', 'tivoli', 'torres', 'xlv', 'others'], ['besta', 'carens', 'carnival', "ceed-/-cee'd", "ceed-sw-/-cee'd-sw", 'cerato', 'clarus', 'e-niro', 'elan', 'ev3', 'ev6', 'ev9', 'joice', 'k2500', 'k2700', 'k2900', 'leo', 'magentis', 'mentor', 'mohave/borrego', 'niro', 'opirus', 'optima', 'picanto', 'pregio', 'pride', "proceed-/-pro_cee'd", 'retona', 'rio', 'roadster', 'rocsta', 'sephia', 'shuma', 'sorento', 'soul', 'spectra', 'sportage', 'stinger', 'stonic', 'venga', 'xceed', 'others'], ['agera', 'cc', 'jesko', 'one:1', 'regera', 'others'], ['x-bow-gt', 'x-bow-gt4', 'x-bow-r', 'x-bow-rr', 'x-bow-street', 'others'], ['110', '111', '112', '1200', '1300/1500/1600', '2106', '4x4', 'aleko', 'c-cross', 'carlota', 'forma', 'granta', 'kalina', 'largus', 'natacha', 'niva', 'nova', 'priora', 'sagona', 'samara', 'sprint', 'taiga', 'universal', 'urban', 'vaz-215', 'vesta', 'x-ray', 'others'], ['asterion', 'aventador', 'centenario', 'countach', 'diablo', 'espada', 'estoque', 'gallardo', 'huracán', 'jalpa', 'lm', 'miura', 'murciélago', 'reventon', 'revuelto', 'sian-fkp-37', 'terzo-millennio', 'urraco-p250', 'urus', 'veneno', 'others'], ['a-112', 'appia', 'beta', 'dedra', 'delta', 'flaminia', 'flavia', 'fulvia', 'gamma', 'hpe', 'k', 'kappa', 'lybra', 'musa', 'phedra', 'prisma', 'stratos', 'thema', 'thesis', 'trevi', 'voyager', 'y', 'ypsilon', 'z', 'zeta', 'others'], ['defender', 'discovery', 'discovery-sport', 'freelander', 'lrx', 'range-rover', 'range-rover-evoque', 'range-rover-sport', 'range-rover-velar', 'series', 'others'], ['convoy', 'maxus', 'others'], ['c10', 't03', 'others'], ['tx', 'vn5', 'others'], ['ct-200h', 'es-series-(all)', 'es-300', 'es-330', 'es-350', 'gs-series-(all)', 'gs-200t', 'gs-250', 'gs-300', 'gs-350', 'gs-430', 'gs-450h', 'gs-460', 'gs-f', 'gx-series-(all)', 'gx-460', 'gx-470', 'is-series-(all)', 'is-200', 'is-220d', 'is-250', 'is-300', 'is-350', 'is-f', 'lbx', 'lc-series-(all)', 'lc-500', 'lc-500h', 'lc-f', 'lfa', 'lm', 'ls-series-(all)', 'ls-400', 'ls-430', 'ls-460', 'ls-500', 'ls-600', 'lx-series-(all)', 'lx-450d', 'lx-470', 'lx-500d', 'lx-570', 'lx-600', 'nx-series-(all)', 'nx-200t', 'nx-300', 'nx-300h', 'nx-350h', 'nx-450h+', 'rc-series-(all)', 'rc-200t', 'rc-300h', 'rc-350', 'rc-f', 'rx-series-(all)', 'rx-200t', 'rx-300', 'rx-330', 'rx-350', 'rx-350h', 'rx-400', 'rx-450h', 'rx-500h', 'rz', 'sc-series-(all)', 'sc-400', 'sc-430', 'ux-series-(all)', 'ux-200', 'ux-250h', 'ux-300e', 'ux-300h', 'others'], ['1022', '1025', '330ev', '650', '650ev', '820', 'breez-(520)', 'c30e', 'c32e', 'foison', 'm7', 'seasion', 'smily', 'solano-(620)', 'x50', 'x7', 'x70', 
'x80', 'others'], ['162', 'ambra', 'be-sun', 'be-two', 'be-up', 'due', 'ixo', 'js-50', 'js-60', 'myli', 'nova', 'optima', 'optimax', 'prima', 'x-pro', 'x-too', 'others'], ['aviator', 'continental', 'corsair', 'cosmopolitan', 'ls', 'mark', 'mkc', 'mkt', 'mkx', 'mkz', 'nautilus', 'navigator', 'town-car', 'zephyr', 'others'], ['m3', 'others'], ['a-klasse', 'b-klasse', 'c-klasse', 'e-klasse', 'g-klasse', 'gla', 'glb', 'glc', 'gle', 'puch', 's-klasse', 'sl', 'smart', 'others'], ['2-eleven', '3-eleven', '340-r', 'cortina', 'elan', 'eletre', 'elise', 'elite', 'emeya', 'emira', 'esprit', 'europa', 'evija', 'evora', 'excel', 'exige', 'omega', 'super-seven', 'type-130', 'v8', 'venturi', 'others'], ['air', 'others'], ['01', 'others'], ['microlino', 'others'], ['alturas-g4', 'bolero', 'cj', 'genio', 'goa', 'jeep', 'kuv100', 'marazzo', 'nuvosport', 'quanto', 'reva', 'scorpio', 'thar', 'tuv300', 'verito', 'xuv300', 'xuv500', 'xylo', 'others'], ['tge', 'others'], ['aston-martin-(all)', 'aston-martin---cyrus', 'aston-martin---db9', 'aston-martin---vanquish', 'aston-martin---vantage', 'audi---r8', 'bentley-(all)', 'bentley---continental-gt', 'bentley---flying-spur', 'bentley---le-mansory', 'bentley---vitesse-rosé', 'bmw-(all)', 'bmw---7', 'bmw---x5', 'bmw---x6', 'bugatti---veyron', 'ferrari-(all)', 'ferrari---458', 'ferrari---599-gtb', 'ferrari---f12', 'ferrari---la-revoluzione', 'ferrari---siracusa', 'land-rover---range-rover', 'lotus-(all)', 'lotus---elise', 'lotus---evora', 'maserati-(all)', 'maserati---ghibli', 'maserati---gran-turismo', 'mclaren---12c', 'mercedes-benz-(all)', 'mercedes-benz---c', 'mercedes-benz---cls', 'mercedes-benz---e', 'mercedes-benz---g', 'mercedes-benz---gl', 'mercedes-benz---m', 'mercedes-benz---ml', 'mercedes-benz---s', 'mercedes-benz---sl', 'mercedes-benz---slk', 'mercedes-benz---slr', 'mercedes-benz---sls', 'mercedes-benz---v', 'mercedes-benz---viano', 'porsche-(all)', 'porsche---918', 'porsche---991', 'porsche---997', 'porsche---cayenne', 'porsche---macan', 'porsche---panamera', 'rolls-royce-(all)', 'rolls-royce---ghost', 'rolls-royce---phantom', 'rolls-royce---wraith', 'tesla---model-s', 'others'], ['cobra', 'roadster', 'others'], ['bubble', 'ceo', 'coolcar', 'mm520', 'mm620', 'others'], ['222', '224', '228', '3200', '418', '420', '4200', '422', '424', '430', 'alfieri', 'biturbo', 'bora', 'coupe', 'ghibli', 'grancabrio', 'gransport', 'granturismo', 'grecale', 'indy', 'karif', 'levante', 'mc12', 'mc20', 'merak', 'quattroporte', 'racing', 'shamal', 'spyder', 'tc', 'others'], ['530', 'others'], ['deliver-9', 'edeliver-3', 'edeliver-7', 'edeliver-9', 'eg10', 'euniq-5', 'euniq-6', 'ev80', 'g10', 'mifa-9', 'rv80', 't60', 't90', 'v80', 'others'], ['57', '62', 'pullman', 'others'], ['121', '2', '3', '323', '5', '6', '626', '929', 'atenza', 'axela', 'b-series', 'bongo', 'bt-50', 'capella', 'cx-3', 'cx-30', 'cx-5', 'cx-60', 'cx-7', 'cx-80', 'cx-9', 'demio', 'e-series', 'familia', 'millenia', 'mpv', 'mx-3', 'mx-30', 'mx-5', 'mx-6', 'pick-up', 'premacy', 'protege', 'rx-7', 'rx-8', 'rx-9', 'tribute', 'xedos', 'others'], ['12-c', '540c', '570gt', '570s', '600lt', '620r', '650s-coupe', '650s-spider', '675lt', '720s', '750s', '765lt-coupe', '765lt-spider', 'artura', 'elva', 'f1', 'gt', 'mp4-12c', 'p1', 'senna', 'speedtail', 'others'], ['break', 'cabriolet', 'club', 'fourgon-vitre', 'maxi-concept', 'others'], ['148', '329', '341', '343', '345', '363', '364', '366', '374', '378', '379', '381', '385', '391', '392', '395', '423', '427', '433', '435', '443', '445', '447', '463', '464', '465', '466', '469', '563', '565', '627', '833', '835', '843', '845', '848', '860', '861', '864', '865', '943', '945', '947', '960', '961', '962', '963', '964', '965', '966', '967', '968', '969', '986', 'others'], ['marquis', 'sable', 'villager', 'others'], ['ehs', 'hs', 'marvel-r', 'metro', 'mg3', 'mg4', 'mg5', 'mga', 'mgb', 'mgc', 'mgf', 'midget', 'rv8', 'td', 'tf', 'zr', 
'zs', 'zt', 'others'], ['microlino', 'others'], ['cargo', 'due', 'ecology/lyra', 'flex', 'm.cross', 'm.go', 'm8', 'mc1', 'mc2', 'sherpa', 'virgo', 'others'], ['ferox', 'ferox-adventure', 'ferox-t', 'hero', 'magnum', 'others'], ['berlinetta', 'rs-mk2', 'others'], ['access', 'cross', 'gt', 'minauto', 'others'], ['1000', '1300', '3/5-doors', 'cooper', 'cooper-d', 'cooper-s', 'cooper-sd', 'cooper-se', 'john-cooper-works', 'one', 'one-d', 'aceman', 'cabrio-series-(all)', 'cooper-cabrio', 'cooper-d-cabrio', 'cooper-s-cabrio', 'cooper-sd-cabrio', 'john-cooper-works-cabrio', 'one-cabrio', 'clubman-series-(all)', 'cooper-clubman', 'cooper-d-clubman', 'cooper-s-clubman', 'cooper-sd-clubman', 'john-cooper-works-clubman', 'one-clubman', 'one-d-clubman', 'clubvan', 'countryman-series-(all)', 'cooper-countryman', 'cooper-d-countryman', 'cooper-s-countryman', 'cooper-sd-countryman', 'cooper-se-countryman', 'countryman-c', 'countryman-d', 'countryman-s-all4', 'jcw-countryman-all4', 'john-cooper-works-countryman', 'one-countryman', 'one-d-countryman', 'coupé-series-(all)', 'cooper-coupe', 'cooper-d-coupe', 'cooper-s-coupe', 'cooper-sd-coupe', 'john-cooper-works-coupe', 'paceman-series-(all)', 'cooper-d-paceman', 'cooper-paceman', 'cooper-s-paceman', 'cooper-sd-paceman', 'john-cooper-works-paceman', 'roadster-series-(all)', 'cooper-roadster', 'cooper-s-roadster', 'cooper-sd-roadster', 'john-cooper-works-roadster', 'others'], ['3000-gt', '400', 'airtrek', 'asx', 'attrage', 'canter', 'carisma', 'chariot', 'colt', 'cordia', 'cosmos', 'delica', 'diamante', 'dingo', 'dion', 'eclipse', 'eclipse-cross', 'fto', 'galant', 'galloper', 'grandis', 'i-miev', 'l200', 'l300', 'l400', 'lancer', 'legnum', 'libero', 'mirage', 'montero', 'outlander', 
'pajero', 'pajero-pinin', 'pajero-sport', 'pick-up', 'rvr', 'santamo', 'sapporo', 'shogun', 'sigma', 'space-gear', 'space-runner', 'space-star', 'space-wagon', 'starion', 'tredia', 'others'], ['galue', 'himiko', 'like-t3', 'rock-star', 'ryugi', 'viewt', 'others'], ['100-years-special', '3-wheeler', '4-sitzer', '4/4', 'aero-8', 'aero-coupe', 'aero-max', 'aero-supersports', 'ev3', 'eva-gt', 'lifecar', 'plus-4', 'plus-8', 'plus-e', 'plus-six', 'roadster', 'supersport-pedal', 'others'], ['21215', '2137', '2138', '2140', '21406', '2141', '21412', '214145', '2142', '2335', '2901', '408', '412', '426', '427', '434', 'duet', 'ivan-kalita', 'jurij-dolgorukij', 'knjaz-vladimir', 'svjatogor', 'others'], ['lafer', 'others'], ['erelis', 'ps160', 'others'], ['el6', 'el7', 'el8', 'et5', 'et7', 'others'], ['100-nx', '200-sx', '280-zx', '300-zx', '350z', '370z', 'ad', 'almera', 'almera-tino', 'altima', 'ariya', 'armada', 'avenir', 'bassara', 'bluebird', 'cabstar', 'cargo', 'cedric', 'cefiro', 'cherry', 'cube', 'datsun', 'e-nv200', 'elgrand', 'evalia', 'expert', 'figaro', 'frontier', 'gloria', 'gt-r', 'interstar', 'juke', 'king-cab', 'kubistar', 'laurel', 'leaf', 'liberty', 'march', 'maxima', 'micra', 'murano', 'navara', 'note', 'np300', 'nv200', 'nv250', 'nv300', 'nv400', 'pathfinder', 'patrol', 'pick-up', 'pixo', 'prairie', 'presage', 'presea', 'primastar', 'primera', 'pulsar', 'qashqai', 'qashqai+2', 'quest', 'r-nessa', 'rogue', 'safari', 'sentra', 'serena', 'silvia', 'skyline', 'stagea', 'stanza', 'sunny', 'teana', 'terrano', 'tiida', 'titan', 'townstar', 'townstar', 'townstar-ev', 'trade', 'urvan', 'vanette', 'wingroad', 'x-trail', 'others'], ['1000', 'prinz', 'prinz-1000', 'prinz-1000-tt', 'ro80', 'sport-prinz', 'tt', 'tts', 'wankel-spider', 'others'], ['442', 'bravada', 'custom-cruiser', 'cutlass', 'delta-88', 'dynamic-88', 'silhouette', 'supreme', 'toronado', 'others'], ['abarth', 'ac', 'adler', 'alfa-romeo', 'allard', 'alvis', 'amc', 'american', 'amphicar', 'ariel', 'aries', 'armstrong-siddeley', 'arnolt', 'asa', 'asc', 'aston-martin', 'auburn', 'audi', 'aurora', 'austin', 'auto-union', 'autobianchi', 'avanti', 'barkas', 'beast', 'bedford', 'belsize', 'benjamin', 'bentley', 'berkeley', 'bitter', 'bizzarrini', 'bmw', 'borgward', 'brennabor', 'bricklin', 'bugatti', 'buick', 'cadillac', 'chaika', 'champion', 'charron', 'checker', 'chenard-&-walker', 'chevrolet', 'chrysler', 'cisitalia', 'citroen', 'cj-rayburn', 'clan', 'clenet', 'commer', 'continental', 'cord', 'corvette', 'cunningham', 'd.f.p', 'daf', 'daimler', 'dante', 'datsun', 'day-elder', 'de-dion-bouton', 'de-lorean', 'de-soto', 'de-tomaso', 'delage', 'delahaye', 'denzel', 'desoto', 'deutz', 'dkw', 'dodge', 'dort', 'duesenberg', 'durant', 'dutton', 'edsel', 'elva', 'emw', 'england', 'enzmann', 'essex', 'excalibur', 'facel-vega', 'fairthorpe', 'falcon', 'fenton-riley', 'ferrari', 'fiat', 'fire-vehicle', 'fleur-de-lys', 'fn', 'ford', 'fordson', 'formula-car', 'franklin', 'frazer-nash', 'fuldamobil', 'gaz', 'ghia', 'gilbern', 'ginatta', 'ginetta', 'glas', 'gmc', 'goggomobil', 'goliath', 'gordon-keeble', 'graham-paige', 'gsm', 'gutbrod', 'hanomag', 'harley-davidson', 'healey', 'heinkel', 'heritage', 'hillman', 'hino', 'hispano-suiza', 'holden', 'honda', 'horch', 'hotchkiss', 'hrg', 'hudson', 'humber', 'hupmobile', 'ifa', 'ihc', 'innocenti', 'international', 'iso-rivolta', 'isuzu', 'jaguar', 'jeep', 'jensen', 'kaiser', 'kaiser---frazer', 'karmann', 'karmann-ghia', 'kelly', 'kleinschnittger', 'la-licorne', 'lagonda', 'lamborghini', 'lanchester', 'lancia', 'land-rover', 'lanz', 'lasalle', 'lea-francis', 'ligier', 'lincoln', 'lloyd', 'lmx', 'lombardi', 'lorraine-dietrich', 'lotus', 'mack', 'magirus', 
'man', 'marauder', 'march', 'marcos', 'marendaz', 'marmon', 'maserati', 'mathis', 'matra', 'maybach', 'mazda', 'mercedes-benz', 'mercury', 'merlin', 'messerschmitt', 'metz', 'mg', 'military-vehicle', 'minerva', 'mitsubishi', 'monica', 'monteverdi', 'moretti', 'morgan', 'morgan-darmont', 'morris-leon-bolle', 'morris-minor', 'moskvitch', 'motorräder-bike', 'munga', 'muntz', 'nash', 'nissan', 'nsu', 'ogle', 'oldsmobile', 'om', 'opel', 
'osca', 'overland', 'packard', 'panhard', 'panther', 'paterson', 'peerless', 'pegaso', 'peugeot', 'pierce-arrow', 'pontiac', 'porsche', 'puch', 'puma', 'rambler', 'reliant', 'renault', 'rent-bonnet', 'republic', 'riley', 'rolls-royce', 'rosengart', 'rotus', 'roush', 'rover', 'rovin', 'saab', 'salmson', 'saurer', 'seat', 'sebring', 'setra', 'shelby', 'shores', 'siata', 'simca', 'skoda', 'spartan', 'spitzer', 'standard', 'stephens', 'steyr', 'studebaker', 'stutz', 'subaru', 'sunbeam', 'talbot', 'tatra', 'tempo', 'toyota', 'trabant', 'tractor', 'trident', 'triumph', 'tucker', 'turner', 'tvr', 'uaz', 'unic', 'unimog', 'vanden-plas', 'veritas', 'vignale', 'vixen', 'voisin', 'volkswagen', 'volvo', 'wanderer', 'wartburg', 'westfalia', 'westfield', 'wetsch', 'willys', 'wolseley', 'yugo', 'zimmer', 'zündapp', 'others'], ['5', 'others'], ['funky-cat', 'others'], ['huayra', 'zonda', 'others'], ['lazer', 'de-ville', 'kallista', 'lima', 'rio', 'solo', 'others'], ['1007', '104', '106', '107', '108', '2008', '204', '205', '206', '207', '208', '3008', '301', '304', '305', '306', '307', '308', '309', '4007', '4008', '404', '405', '406', '407', '408', '5008', '504', '505', '508', '604', '605', '607', '806', '807', 'bipper', 'boxer', 'camper', 'e-2008', 'e-208', 'e-expert', 'e-rifter', 'expert', 'ion', 'j5', 'j9', 'partner', 'ranch', 'rcz', 'rifter', 'traveller', 'others'], ['cévennes', 'cobra', 'hemera', 'speedster', 'speedster-ii', 'others'], ['al500', 'ape', 'm500', 'pk500', 'porter', 'quargo', 'others'], ['acclaim', 'arrow', 'barracuda', 'belvedere', 'breeze', 'caravelle', 'colt', 'conquest', 'cricket', 'cuda', 'duster', 'fury', 'gran-fury', 'gtx', 'horizon', 'laser', 'neon', 'prowler', 'reliant', 'road-runner', 'sapporo', 'satellite', 'savoy', 'scamp', 'sundance', 'superbird', 'trailduster', 'turismo', 'valiant', 'volaré', 'voyager', 'others'], ['1', '2', '3', '4', 'others'], ['6000', 'aztek', 'bonneville', 'catalina-safari', 'fiero', 'firebird', 'g6', 'grand-am', 'grand-prix', 'gto', 'montana', 'solstice', 'sunbird', 'sunfire', 'targa', 'trans-am', 'trans-sport', 'vibe', 'others'], ['356', '550', '718-(all)', '718', '718-spyder', '911-series-(all)', '911', '930', '964', '991', '992', '993', '996', '997', '912', '914', '918', '924', '928', '944', '959', '962', '968', 'boxster', 'carrera-gt', 'cayenne', 'cayman', 'macan', 'panamera', 'targa', 'taycan', 'others'], ['313', '315', '316', '318', '413', '415', '416', '418', '420', 'gen2', 'persona', 'satria', 'others'], ['g', 'haflinger', 'pinzgauer', 'others'], ['1500', '2500', '3500', 'chassis-cab', 'promaster', 'others'], ['epic0', 'others'], ['ant', 'fox', 'kitten', 'rebel', 'regal', 'regent', 'rialto', 'robin', 'sabre-four', 'scimitar', 'others'], ['arnage-green-label', 'arnage-red-label', 'azure', 'azure-mulliner', 'camargue', 'cloud', 'continental-r-mulliner', 'continental-r', 'continental-sc', 'corniche', 'cullinan', 'dawn', 'flying-spur', 'ghost', 'le-mains-series', 'park-ward', 'phantom', 'phantom-drophead', 'silver-dawn', 'silver-seraph', 'silver-shadow', 
'silver-spirit', 'silver-spur', 'silver-wraith', 'silver-wraith-ii', 'spectre', 't', 'touring', 'wraith', 'others'], ['100', '111', '114', '115', '200', '213', '214', '216', '218', '220', '25', '400', '414', '416', '418', '420', '45', '600', '618', '620', '623', '75', '800', '820', '825', '827', 'city-rover', 'estate', 'metro', 'mini', 'montego', 'rover', 'sd', 'streetwise', 'tourer', 'others'], ['3400s', '3600s', 'btr', 'ctr', 'ctr2', 'ctr3', 'dakara', 'gt', 'r-kompressor', 'r-turbo', 'rgt', 'rgt-8', 'rk-coupe/spyder', 'rt-12', 'rt-12r', 'rt-12s', 'scr', 'turbo-florio', 'turbo-r', 'others'], ['9-2x', '9-3', '9-4x', '9-5', '9-7x', '90', '900', '9000', '92', '93', '95', '96', '99', 'gt-750', 'sonett', 'sport-/-gt-850', 'others'], ['2500', '300', '350', '410', 'anibal', 'ps-10', 's300', 's350', 'samurai', 'vitara', 'vitara-cabriolet', 'others'], ['alhambra', 'altea', 'altea-xl', 'arona', 'arosa', 'ateca', 'cordoba', 'exeo', 'fura', 'ibiza', 'inca', 'leon', 'leon-e-hybrid', 'malaga', 'marbella', 'mii', 'panda', 'ronda', 'tarraco', 'terra', 'toledo', 'others'], ['fugleman-1000', 'fugleman-570', 'fugleman-ut-10', 'fugleman-ut6-h', 'villain-1000-sh', 'villain-sx10', 'villain-sx10-h', 'others'], ['2p45', 'lt-cargo', 'others'], ['seres-3', 'seres-5', 'seres-7', 'others'], ['500', 'others'], ['biarritz', 'gullwing', 'marbella-cabrio', 'monte-carlo-cabrio', 'pulman-limousine', 'st.-tropez-cabrio-limousine', 'others'], ['f-150', 'f-150-super-snake', 'mustang-gt-h', 'mustang-super-snake', 'series-1', 'others'], ['ceo', 'others'], ['s04'], ['others'], ['105', '120', '130', '135', 'citigo', 'enyaq', 'fabia', 'favorit', 'felicia', 'forman', 'kamiq', 'karoq', 'kodiaq', 'octavia', 'pick-up', 'praktik', 'rapid/spaceback', 'roomster', 'scala', 'snowman', 'superb', 'yeti', 'others'], ['et5', 'others'], ['#1', '#3', 'brabus', 'city-coupé/city-cabrio', 'crossblade', 'forfour', 'fortwo', 'roadster', 'others'], ['others'], ['sportequipe-5', 'sportequipe-6', 'sportequipe-7', 'others'], ['c12', 'c8', 'd12', 'others'], ['actyon', 'family', 'kallista', 'korando', 'kyron', 'musso', 'rexton', 'rodius', 'tivoli', 'torres', 'xlv', 'others'], ['city-pony---baw-pony', 'others'], ['work', 'work-l', 'others'], ['champion', 'others'], ['1200', '1800', 'ascent', 'baja', 'brz', 'crosstrek', 'e10', 'e12', 'forester', 'impreza', 'justy', 'legacy', 'leone', 'levorg', 'libero', 'm60', 'm70', 'm80', 'mini', 'outback', 'solterra', 'svx', 'trezia', 'tribeca', 'vanille', 'vivio', 'wrx', 'xt', 'xv', 'others'], ['across', 'alto', 'baleno', 'cappuccino', 'carry', 'celerio', 'escudo', 'grand-vitara', 'ignis', 'ik-2', 'jimny', 'kizashi', 'liana', 'lj-80', 'maruti', 's-cross', 'sa-310', 'samurai', 'santana', 'sj-410', 'sj-413', 'sj-samurai', 'splash', 'super-carry', 'swace', 'swift', 'sx4', 'sx4-s-cross', 'vitara', 'wagon-r+', 'x-90', 
'xl-7', 'others'], ['g01', 'g01f', 'g03f', 'g05', 'others'], ['alpine', 'horizon', 'matra-murena', 'matra-rancho', 'samba', 'simca-1100', 'simca-1510', 'solar-gl', 'solar-ls', 'solar-ralley', 'solara', 'sunbeam', 'tagora', 'others'], ['bingo', 'c1db', 'c1dm', 'domino', 'hola', 'king', 't2', 't3', 'td', 'others'], ['aria', 'bolt', 'estate', 'harrier', 'hexa', 'indica', 'indigo', 'nano', 'nexon', 'pick-up', 'safari', 'sport', 'sumo', 
'telcoline', 'telcosport', 'tiago', 'tigor', 'xenon', 'zest', 'others'], ['em1-anniversary', 'em1-citysport', 'zero-city', 'zero-classic', 'zero-em1', 'zero-em2', 'zero-evo', 'zero-junior', 'zero-se', 'zero-special-edition', 'zero-speedster', 'others'], ['others'], ['cybertruck', 'model-3', 'model-s', 'model-x', 'model-y', 'roadster', 'others'], ['t10x', 'others'], ['ginevra', 'helektra', 'others'], ['4-runner', 'allion', 'alphard', 'altezza', 'aristo', 'auris', 'avalon', 'avensis', 'avensis-verso', 'aygo', 'aygo-x', 'bb', 'belta', 'bz4x', 'c-hr', 'caldina', 'cami', 'camry', 'carina', 'celica', 'chaser', 'coaster', 'corolla', 'corolla-cross', 'corolla-verso', 'corona', 'corsa', 'cressida', 'cresta', 'crown', 'duet', 'dyna', 'estima', 'fj-cruiser', 'fj40', 'fortuner', 'fun-cruiser', 'funcargo', 'gaia', 'gr86', 'gt86', 'harrier', 'hdj', 'hiace', 'highlander', 'hilux', 'ipsum', 'iq', 'ist', 'kj', 'land-cruiser', 'land-cruiser-prado', 'lite-ace', 'mark-ii', 'mark-x', 'matrix', 'mirai', 'model-f', 'mr-2', 'nadia', 'noah', 'opa', 'paseo', 'passo', 'pick-up', 'picnic', 'platz', 'premio', 'previa', 'prius', 'prius+', 'proace', 'proace-city', 'ractis', 'raum', 'rav-4', 'sequoia', 'sienna', 'solara', 'sprinter', 'starlet', 'supra', 'tacoma', 'tercel', 'town-ace', 'tundra', 'urban-cruiser', 'venza', 'verossa', 'verso', 'verso-s', 'vista', 'vitz', 'voxy', 'will', 'windom', 'wish', 'yaris', 'yaris-cross', 'others'], ['1.1', 'p50', 'p60', 'p601', 'rallye', 'trabant', 'others'], ['others'], ['dolomite', 'gt6', 'herald', 'moss', 'spitfire', 'stag', 'tr1', 'tr2', 'tr3', 'tr4', 'tr5', 'tr6', 'tr7', 'tr8', 'others'], ['atlas', 'cat', 'citroen', 'daewoo', 'daf', 'deutz-fahr', 'fiat', 'ford', 'fuchs', 'hanomag', 'hitachi', 'iveco', 'iveco-magirus', 'iveco-fiat', 'jungheinrich', 'koegel', 'komatsu', 'ldv', 'liebherr', 'linde', 'man', 'mercedes-benz', 'mitsubishi', 'multicar', 'neoplan', 'nissan', 'o-&-k', 'peugeot', 'renault', 'scania', 'schaeff', 'setra', 'volvo', 'vw', 'zeppelin', 'zettelmeyer', 'others'], ['cerbera', 'chimaera', 'grantura', 'griffith', 's-2,8', 's2', 's3', 's4', 'sagaris', 't350', 'tamora', 'tuscan', 'v8s', 'others'], ['2206', '2315', '3151', '3153', '3159', '3160', '3162', '3303', '3692', '3909', '3962', '469', 'buchanka', 'classic', 'dakar', 'farmer', 'hunter', 'patriot', 'pickup', 'profi', 'tigr', 'trofi', 'others'], ['armstrong', 'princess', 'others'], ['carmel', 'edison-2', 'edison-4', 'venice', 'venice-r', 'venice-speedster', 'venice-speedster-r', 'others'], ['1111', '11113', '11118', '1113', '1117', '1118', '1119', '1706', '1922', '2016', '2101', '21011', '21013', 
'2102', '2103', '21033', '2104', '21043', '21045', '21046', '21047', '2105', '21051', '21053', '2106', '21060', '21061', '21063', '21065', '2107', '21073', '21074', '2108', '21081', '21083', '21086', '2109', '21091', '21093', '21096', '21099', '2110', '21101', '21102', '21103', '21104', '21106', '21108', '2111', '21111', '21112', '21113', '21114', '2112', '21120', '21121', '21122', '21123', '21124', '2113', '21130', '2114', '21140', '2115', '21150', '21150i', '2120', '2121', '21213', '21214', '21218', '212180', '2123', '2129', '2131', '21312', '2170', '2199', '2328', '2329', '2364', 'roadster', 'others'], ['cargo', 'cover', 'double', 'multi', 'open', 'people', 'ribaltabile', 'others'], ['vf-6', 'vf-7', 'vf-8', 'vf-9', 'others'], ['240', '244', '245', '262', '264', '265', '340', '360', '440', '460', '480', '740', '744', '745', '760', '764', '780', '850', '855', '940', '944', '945', '960', '965', 'amazon', 'c30', 'c40', 'c70', 'ec40', 'ex30', 'ex40', 'ex90', 'p1800', 'polar', 'pv544', 's40', 's60', 's60-cross-country', 's70', 's80', 's90', 'v40', 'v40-cross-country', 'v50', 'v60', 'v60-cross-country', 'v70', 'v90', 'v90-cross-country', 'xc40', 'xc60', 'xc70', 'xc90', 'others'], ['dream', 'free', 'passion', 'others'], ['1.3', '1.6', '1000', '311', '312', '313', '353', 'barkas', 'framo', 'ifa-f9', 'wartburg', 'others'], ['ex5-z', 'ex6-plus', 'w6', 'others'], ['full-custom', 'standard', 'standard-custom', 'others'], ['7se', 'fw400', 'megablade', 'megabusa', 'megas2000', 'sdv', 'se', 'sei', 'seight', 'sport', 'sport-turbo', 'xi', 'xtr2', 'xtr4', 'others'], ['coffee-01', 'coffee-02', 'others'], ['gecko', 'mf-28', 'mf-3', 'mf-30', 'mf-4', 'mf-5', 'others'], ['bus', 'others'], ['kitty', 'yoyo', 'others'], ['g3i', 'g9', 'p5', 'p7', 'others'], ['10', '101', '1100-tf', '125-pz', '128', '1300', '600', '750', '850', '850-ak', '900-ak', 'koral', 'skala', 'yugo', 'others'], ['1102', '1103', '1105', 'chance', 'forza', 'lanos', 'sens', 'vida', 'others'], ['001', 'x', 'others'], ['d1', 'd2', 'd3', 'kwb', 'others'], ['e200', 't300', 't600', 't700', 'traum-meet-3', 'traum-s70', 'traum-seek-5', 'z100', 'z360', 'z700', 'others'], ['aiways', 'amc', 'apal', 'aro', 'asia', 'auverland', 'barkas', 'bertone', 'bilenkin-classic-cars', 'binz', 'bitter', 'bm-grupa', 'british-leyland', 'burton', 'can-am', 'canta', 'carver', 'china-automobile', 'cmc', 'continental', 'cord', 'courb', 'datsun-go', 'de-lorean', 'derways', 'edrive', 'effedi-maranello', 'excalibur', 'fso', 'fun-tech', 'geely', 'genesis', 'ginetta', 'grandin-dallas', 'gumpert', 'hartge', 'hdpic', 'hobbycar', 'holden', 'ihc', 'indimo', 'iseki', 'italcar', 'jac', 'jdm', 'jiayuan', 'karabag', 'keinath', 'kit-cars', 'la-forza', 'landwind', 'loremo', 'marcos', 'melkus', 'mercury', 'mia', 'monteverdi', 'morris', 'mosler', 'nio', 'noble', 'polaris', 'qoros', 'quadix', 'qvale', 'radical', 'reva', 'rimac', 'romeo-ferraris', 'saleen', 'sam', 'savel', 'scheelen', 'scion', 'sdg', 'shandong', 'tagaz', 'teener', 'think-city', 'tiger', 'tramontana', 'trax', 'turner', 'van-diemen', 'vauxhall', 'venturi', 'vm', 'vortex', 'wallys', 'weineck', 'wenckstern', 'xev', 'yes!', 'zenvo', 'others']]

def brand_index_finder(selected_brand,all_brands):
    all_indices = []  
    for brand in selected_brand:
        index = 0
        for each_brand in all_brands:
            if brand == each_brand:
                all_indices.append(index)
                break
            index += 1
    return all_indices

def find_selected_brands_models(selected_brand,all_models):
    all_indices = brand_index_finder(selected_brand,all_brands)
    all_models_array = []
    for index in all_indices:
        all_models_array.append(all_models[index])
    return all_models_array

def find_selected_brands_models_for_selection(selected_brand,all_models):
    all_indices = brand_index_finder(selected_brand,all_brands)
    all_models_array = []
    for index in all_indices:
        for model in all_models[index]:
            all_models_array.append(model)
    return all_models_array

def sorting_model_brand_selections(selected_brand,selected_model,all_model_for_each_brand,all_brands):
    all_brand_indices = brand_index_finder(selected_brand,all_brands)
    all_brand_model_patterns = []
    for brand_index in all_brand_indices:
        for each_selected_model in selected_model: 
            if each_selected_model in all_model_for_each_brand[brand_index]:
                all_brand_model_patterns.append(f'{all_brands[brand_index]}/{each_selected_model}')
            
    return all_brand_model_patterns

all_fuel_options = ['Hybrid(Electric/Gasoline)','Hybrid(Electric/Diesel)','Gasoline','CNG','Diesel','Electric','Hydrogen','LPG','Ethanol','Others']

def update_selection_for_fuel(picked_types):
    all_url_versions = []
    all_fuel_type = {
        'Hybrid(Electric/Gasoline)': '2', 
        'Hybrid(Electric/Diesel)': '3',
        'Gasoline': 'B',
        'CNG' : 'C',
        'Diesel': 'D',
        'Electric' : 'E',
        'Hydrogen' : 'H',
        'LPG' :  'L',
        'Ethanol' : 'M',
        'Others' : 'O' 
    }   
    for each_picked in picked_types:       
        for fuel_type in all_fuel_type:
            if each_picked == fuel_type:
                all_url_versions.append(all_fuel_type[each_picked])
    return  all_url_versions         

all_gear_options = ['Automatic','Manuel' ,'Semi-automatic']

def update_selection_for_gearbox(picked_types):
    all_url_versions = []
    all_gear = {
        'Automatic' : 'A',
        'Manuel' : 'M',
        'Semi-automatic' : 'S',
    }
    for each_picked in picked_types:       
        for fuel_type in all_gear:
            if each_picked == fuel_type:
                all_url_versions.append(all_gear[each_picked])
    return  all_url_versions    

def find_mileage_and_power():
    all_mileage = []
    time.sleep(1)
    mileage_from_input = driver.find_element(By.XPATH, '//button[@id= "mileageFrom-input"]')
    mileage_from_input.click()

    all_miles = driver.find_elements(By.XPATH, '//ul[@id= "mileageFrom-input-suggestions"]/li')

    for mile in all_miles:
        if mile == all_miles[0]:
            all_mileage.append('')
        from_text = ''
        for each_text_from in mile.text:
            if each_text_from == ',':
                each_text_from = ""
            from_text = from_text + each_text_from
        all_mileage.append(from_text)

    return all_mileage

def add_to_all_df(all_filtrations,current_filtration):
    if check_empty_filtrations(current_filtration): 
        if current_filtration in all_filtrations:
            all_filtrations.remove(current_filtration)
        all_filtrations.append(current_filtration)

#Shows the previous filtrations
def find_prev_filtration(all_filtrations,current_filtration,system_index):
    if check_empty_filtrations(current_filtration): 
        if system_index != 0 and system_index != 1:
            return all_filtrations[system_index - 2]
        
def is_changed(prev_filtration,current_filtration,system_index):
   
    if system_index != 0 and system_index != 1 :
        if current_filtration == prev_filtration:
            return False
        else: 
            return True

#This functions controls the filtrations are they empyt or not.
def check_empty_filtrations(filtration):
    for index in range(len(filtration)):
        if filtration[index] == '' or filtration[index] == []: 
            return False
        elif index == len(filtration) - 1 and filtration[index] != []:       
            return True
   
mileage_and_power_options = ['', '2500', '5000', '10000', '20000', '30000', '40000', '50000', '60000', '70000', '80000', '90000', '100000', '125000', '150000', '175000', '200000']

def is_empty(selection_name):
    if not selection_name:
        return True

if 'all_filtrations' not in st.session_state:
    st.session_state.all_filtrations = []

selected_brands = st.sidebar.multiselect('Select brands' , all_brands)
selected_models = st.sidebar.multiselect('Select models', find_selected_brands_models_for_selection(selected_brands,all_model_for_each_brand))

selected_fuel_types = st.sidebar.multiselect('Select fuel type', all_fuel_options)
url_type_fuel = update_selection_for_fuel(selected_fuel_types)

selected_gearbox = st.sidebar.multiselect('Select gearbox', all_gear_options)
url_type_gear = update_selection_for_gearbox(selected_gearbox)

selected_mileage_from = st.sidebar.selectbox('Select mileage from', mileage_and_power_options)
selected_mileage_to = st.sidebar.selectbox('Select mileage to', mileage_and_power_options)

selected_power_from = st.sidebar.text_input('Select power from')
selected_power_to = st.sidebar.text_input('Select power to')

all_selected_filtrations = [selected_brands,selected_models,selected_fuel_types,selected_gearbox,selected_mileage_to,selected_power_from,selected_power_to]

if 'filtration_completed' not in st.session_state:
    st.session_state['filtration_completed'] = False

#This code block controls the counter of the page
st.session_state['filtration_completed'] = check_empty_filtrations(all_selected_filtrations)

if 'status' not in st.session_state:
    st.session_state['status'] = False

filtration_names = ['Brand', 'Model', 'Fuel Type', 'Gearbox', 'Mileage To', 'Power From', 'Power To']
selection_index = 0
for selections in all_selected_filtrations:
    if is_empty(selections) == True:
        st.session_state['filtration_completed'] = False
        st.warning(f'Please fill in the {filtration_names[selection_index]} field!')
        
    else:
        st.session_state['filtration_completed'] = True
    selection_index += 1

add_to_all_df(st.session_state.all_filtrations,all_selected_filtrations)

if is_changed(find_prev_filtration(st.session_state.all_filtrations,all_selected_filtrations,len(st.session_state.all_filtrations)),all_selected_filtrations,len(st.session_state.all_filtrations)) == True:
    
    #st.session_state['status'] = False
    if 'rerun_in_progress' not in st.session_state:
        st.session_state['rerun_in_progress'] = True  
        st.warning('Please wait...')
        st.session_state['status'] = False
        st.rerun()   
    else:
        st.session_state['rerun_in_progress'] = False  

if st.sidebar.button('Start Scraping'):
    if st.session_state['filtration_completed'] == False:
        st.warning('Please complete the filtration!')
    else:
        st.session_state['status'] = True
        st.session_state['loading'] = True  
        st.markdown(spinner_css, unsafe_allow_html=True)  
        st.markdown(spinner_html, unsafe_allow_html=True)  

if 'data_scraped' not in st.session_state:
    st.session_state['data_scraped'] = False

if st.session_state['status'] == True and st.session_state['filtration_completed'] == True:
    
    if st.sidebar.button('Stop / Finish'):
        st.session_state['status'] = False
        st.session_state['loading'] = False  
        st.markdown("<style>.spinner-container { display: none; }</style>", unsafe_allow_html=True)
        
    remove_temp_csv('temp_data.csv')
    
    if st.session_state['status'] == True:
        st.warning('Process Started...')

    scrap_page_by_page_web(selected_brands,selected_models,0,url_type_fuel, selected_power_from, selected_power_to, selected_mileage_from,selected_mileage_to, url_type_gear,st.session_state['status'])
    
    if st.session_state['status'] == False:
        st.session_state['loading'] = False  # Animasyonu durdur
        st.markdown("<style>.spinner-container { display: none; }</style>", unsafe_allow_html=True)
        try:          
            for index, row in pd.read_csv('temp_data.csv').iterrows():
                df = pd.DataFrame([row])
                st.write(display_cards(df))
                
        except:
            pass
           
    if os.path.isfile('temp_data.csv'):
        st.session_state['data_scraped'] = True
        st.warning('Scraping Completed!...')
    else:
        st.session_state['data_scraped'] = False

    if st.session_state['data_scraped'] == True:
        with open('temp_data.csv', "rb") as file:
            st.download_button(
                label="Download CSV",         
                data=file,                    
                file_name="Filtered_Data.csv",    
                mime="text/csv"               
            )
