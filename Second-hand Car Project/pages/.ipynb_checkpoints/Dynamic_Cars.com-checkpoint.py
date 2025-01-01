from urllib.parse import unquote
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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

pd.set_option('display.max_columns',None)
pd.set_option('display.width',600)

# URL of the website
website = 'https://www.cars.com/shopping/'

# WebDriver options for Chrome
ch_options = Options()
ch_options.add_argument("--disable-notifications")
ch_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

# Initialize WebDriver in session state
if 'driver2' not in st.session_state:
    st.session_state.driver2 = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=ch_options
    )

# Access the driver from session state
driver = st.session_state.driver2
driver.get(website)

#st.title("Car Brand and Model Selection")
try:
    driver = st.session_state.driver2

    if "brand_model_dict" not in st.session_state:
        # Marka seçim alanını bul
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "makes"))
        )
        grup = dropdown.find_element(By.XPATH, '//*[@id="makes"]/optgroup[1]')
        options = grup.find_elements(By.TAG_NAME, "option")

        brand_names = []
        brand_model_dict = {}

        for brand in options:
            brand_value = brand.get_attribute("value")
            brand_name = brand.text

           # if brand_value == "All makes" or not brand_value:
            #    continue

            brand_names.append(brand_name)
            brand.click()  # Markayı seç

            # Modelleri bulma
            model_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "models"))
            )
            model_options = model_dropdown.find_elements(By.TAG_NAME, "option")

            models = [ model.text for model in model_options if model.get_attribute("value")]
            brand_model_dict[brand_name] = models

        # Verileri session_state'e kaydet
        st.session_state.brand_names = brand_names
        st.session_state.brand_model_dict = brand_model_dict


        # Fiyat ve mesafe değerlerini alma
        if "price_values" not in st.session_state:
            price_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "make-model-max-price"))
            )
            price_option = price_dropdown.find_elements(By.TAG_NAME, "option")
            st.session_state.price_values = [
                price.text for price in price_option if price.get_attribute("value")
            ]

        if "distance_values" not in st.session_state:
            distance_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "make-model-maximum-distance"))
            )
            distance_option = distance_dropdown.find_elements(By.TAG_NAME, "option")
            st.session_state.distance_values = [
                distance.text for distance in distance_option if distance.get_attribute("value")
            ]
except Exception as e:
    st.error(f"An error occurred: {e}")

# webteki click işlemleri gerçekleştime
def select_option(dropdown_id, option_text):
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, dropdown_id))
    )
    options = dropdown.find_elements(By.TAG_NAME, "option")
    for option in options:
        if option.text == option_text:
            option.click()
            option.get_attribute("value")
            break


if "brand_names" in st.session_state:
    selected_brand = st.sidebar.selectbox("Select a Brand", st.session_state.brand_names) 
    if selected_brand in st.session_state.brand_model_dict:
        selected_model = st.sidebar.selectbox("Select a Model", st.session_state.brand_model_dict[selected_brand]) 

if 'selected_brand' in locals() and 'selected_model' in locals():
    select_option("makes", selected_brand)
    select_option("models", selected_model)

if "price_values" in st.session_state:
    selected_price = st.sidebar.selectbox("Select a Max Price", st.session_state.price_values) 
    if selected_price:
        select_option("make-model-max-price", selected_price)

if "distance_values" in st.session_state:
    selected_distance = st.sidebar.selectbox("Select a Max Distance", st.session_state.distance_values) 
    if selected_distance:
        select_option("make-model-maximum-distance", selected_distance)


#find next page url
def next_page_url():
    web = 'https://www.cars.com'
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="next_paginate"]'))
        )
        raw_url = next_button.get_attribute("href")
        if raw_url:
            # If the URL is relative, prepend the base URL
            if not raw_url.startswith("http"):
                raw_url = web + raw_url
            decoded_url = unquote(raw_url)
            print(f"Decoded URL: {decoded_url}")  # Debugging: Check the decoded URL
            return decoded_url
        else:
            print("No href attribute found for the next button.")
            return None
    except Exception as e:
        print(f"Next page element not found: {e}")
        return None
    

features_fetched = False
car_urls = []
if 'car_data' not in st.session_state:
    st.session_state.car_data = []
if 'columns' not in st.session_state:
    st.session_state.columns = []


# Araç listesini çekme
def scrape_car_list():
    global car_urls
    car_list = driver.find_elements(By.CLASS_NAME, 'vehicle-card-link')
    for car in car_list:
        car_urls.append(car.get_attribute('href'))

# Araç detaylarını çekme
def scrape_car_details(car_url):
    global features_fetched
    try:
        driver.get(car_url)

        # Araç bilgilerini alma
        full_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'listing-title'))
        ).text
        price = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-content-inner-focus-ring"]/div[4]/section/header/div[3]/span'))
        ).text

        year = full_name.split(' ')[0]
        name = ' '.join(full_name.split(' ')[1:2])
        model = ' '.join(full_name.split(' ')[2:])

        all_features = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'fancy-description-list'))
        )
        features_text = all_features.text

        # Özellikleri DataFrame olarak işleme
        df = pd.DataFrame(features_text.split("\n"))
        df1 = df.iloc[0::2].reset_index(drop=True)  # Özellik başlıkları
        df2 = df.iloc[1::2].reset_index(drop=True)  # Özellik değerleri

        # Sütunları yalnızca bir kez çek
        if not st.session_state.get('features_fetched', False):
            st.session_state.features_fetched = True
            st.session_state.columns = ['year', 'name', 'model', 'price'] + df1[0].tolist()

        feature_dict = dict(zip(df1[0], df2[0]))
        car_details = [year, name, model, price] + [
            feature_dict.get(col, None) for col in st.session_state.columns[4:]
        ]
        st.session_state.car_data.append(car_details)
    except Exception as e:
        print(f"Error processing car at {car_url}: {e}")


if "scraping_active" not in st.session_state:
    st.session_state.scraping_active = False 

def stop_scraping():
    """Scraping işlemini durdurma."""
    st.session_state.scraping_active = False
    st.markdown(
        "<style>.spinner-container { display: none; }</style>",
        unsafe_allow_html=True
    )
    st.warning("Scraping işlemi durduruldu.")


# Card display function with improved HTML structure
def display_cards(filtered_data):

    st.markdown("""
            
    """, unsafe_allow_html=True)

    for i, (_, row) in enumerate(filtered_data.iterrows()):
        with st.container():
            # Basic information to be displayed on the card surface
            st.markdown(
                f"""                     
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Brand:</span> {row.get('name', 'Unknown')} 
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Model:</span> {row.get('model', 'Unknown')}   
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Year:</span>  {row.get('year', 'Unknown')}
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Price:</span> {row.get('price', 'Unknown')} TL
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Mileage:</span>   {row.get('Mileage', 'Unknown')} km
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Fuel Type:</span> {row.get('Fuel type', 'Unknown')} 
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Transmission Type:</span> {row.get('Transmission', 'Unknown')}
                """, 
                unsafe_allow_html=True
            )
            
            with st.expander(
                "View Details", expanded=False):

                st.markdown(f"""   
                    <div class="card">
                        <h3>{row.get('name', 'Unknown')} {row.get('model', 'Unknown')} ({row.get('year', 'Unknown')})</h3>
                        <p><strong>Price:</strong>   {row.get('price', 'Unknown')} </p>
                        <p><strong>Mileage:</strong>   {row.get('Mileage', 'Unknown')} km</p>
                        <p><strong>Fuel Type:</strong> {row.get('Fuel type', 'Unknown')}</p>
                        <p><strong>Transmission Type:</strong> {row.get('Transmission', 'Unknown')}</p>
                        <hr>
                        <!-- Detailed Informations -->                       
                        <p><strong>Engine:</strong> {row.get('Engine', 'Unknown')}</p>                                   
                        <p><strong>Exterior Color:</strong> {row.get('Exterior color', 'Unknown')}</p>
                        <p><strong>Interior Color:</strong> {row.get('Interior color', 'Unknown')}</p>
                        <p><strong>Drivetrain:</strong> {row.get('Drivetrain', 'Unknown')}</p>
                        <p><strong>MPG:</strong> {row.get('MPG', 'Unknown')}</p>
                        <p><strong>VIN:</strong> {row.get('VIN', 'Unknown')}</p>
                        <p><strong>Stock:</strong> {row.get('Stock #', 'Unknown')}</p>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<hr style='border: 1px solid black; margin: 20px 0;'>", unsafe_allow_html=True)


#CSS Animasyon ve Stil Kodu
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

# HTML Animasyon Kodu
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
st.title("Car Scraper")
total_cars = 0
if st.sidebar.button("Search Cars"):
    try:
        st.session_state.scraping_active = True 
        # CSS ve HTML ekleme (Animasyonu başlatma)
        st.markdown(spinner_css, unsafe_allow_html=True)
        st.markdown(spinner_html, unsafe_allow_html=True)

        if st.session_state.scraping_active:
            if st.button("Stop Scraping"):
                stop_scraping()
        # Arama butonuna tıklama
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "spark-button[data-linkname='search-all-make']"))
        )
        driver.execute_script("arguments[0].click();", search_button)
        # Alınan sayfa URL'lerini ve içindeli arabalrı  gezme
        while st.session_state.scraping_active: 
            next_page = next_page_url()
            try:
                scrape_car_list()
                for car_url in car_urls:
                    scrape_car_details(car_url)
                    total_cars += 1 
                car_urls.clear()

                if not next_page:
                    st.warning("No more pages to scrape.")
                    break
                driver.get(next_page)
                time.sleep(1)
            except Exception as e:
                print(f"Error visiting {next_page}: {e}")
                break

        if st.session_state.scraping_active:
            st.subheader(f"Total number of data obtained: {total_cars}")
        else:
            st.warning("Scraping operation stopped by user.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        # İşlem tamamlandığında animasyonu gizleme
        st.markdown(
            "<style>.spinner-container { display: none; }</style>",
            unsafe_allow_html=True
        )
        st.session_state.scraping_active = False 




if st.session_state.car_data:
    df_cars = pd.DataFrame(st.session_state.car_data, columns=st.session_state.columns)
    display_cards(df_cars)
    csv = df_cars.to_csv(index=False)
    st.download_button("Download Data as CSV", csv, f"{selected_model}_verileri.csv", "text/csv")
 


