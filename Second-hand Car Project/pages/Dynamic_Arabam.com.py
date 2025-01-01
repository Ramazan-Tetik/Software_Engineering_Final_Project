import streamlit as st
import pandas as pd
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import math
import time


# Global driver setup
if "driver1" not in st.session_state:
    ch_options = webdriver.ChromeOptions()
    ch_options.add_argument("--disable-notifications")
    ch_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    )
    st.session_state.driver1 = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=ch_options
    )
    st.session_state.page_loaded = False

driver = st.session_state.driver1

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



def get_single_car_data(driver):
    car_data = {}
    
    try:
        car_data['Fiyat'] = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]").text
    except Exception:
        car_data['Fiyat'] = 'Belirtilmemiş'
        
    try:
        car_data['Marka'] = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[2]").text
    except Exception:
        car_data['Marka'] = 'Belirtilmemiş'
        
    try:                                                    
        car_data['Model'] = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[5]/div[2]").text
    except Exception:
        car_data['Model'] = 'Belirtilmemiş'

    try:
        car_data['Seri'] = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[4]/div[2]").text
    except Exception:
        car_data['Seri'] = 'Belirtilmemiş'


    # Araç ile ilgili diğer genel bilgileri çekmek için for döngüsü
    for div_num in range(1, 5):  # 1'den 4'e kadar div numaralarını geziyoruz
        li_num = 1  # her div'in içindeki li numaraları da sıralı
        while True:
            try:
                # XPath ile li elemanını çekiyoruz
                car_info_xpath = f'/html/body/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[4]/div/div[{div_num}]/ul/li[{li_num}]'
                
                # Başlık kısmını (span[1]) ve içerik kısmını (span[2]) ayrı ayrı çekiyoruz
                title_xpath = car_info_xpath + '/span[1]'
                content_xpath = car_info_xpath + '/span[2]'
                
                title_element = driver.find_element(By.XPATH, title_xpath)
                content_element = driver.find_element(By.XPATH, content_xpath)
                
                title = title_element.text
                content = content_element.text
                
                # Car data'ya başlık ve içerik olarak ekliyoruz
                car_data[title] = content if content else 'Belirtilmemiş'
                
                # Bir sonraki li elemanını kontrol etmek için sayıyı artırıyoruz
                li_num += 1
            except Exception:
                # Eğer belirli bir div içinde li elemanı kalmazsa döngüden çık
                break

    # Lokal Boyalı Parçaları çek
    try:
        lokal_boyali = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[2]/ul/li")
        car_data['Lokal Boyalı'] = [li.text for li in lokal_boyali] if lokal_boyali else ['Belirtilmemiş']
    except Exception as e:
        car_data['Lokal Boyalı'] = ['Belirtilmemiş']

    # Boyalı Parçaları çek
    try:
        boyali = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[3]/ul/li")
        car_data['Boyalı'] = [li.text for li in boyali] if boyali else ['Belirtilmemiş']
    except Exception as e:
        car_data['Boyalı'] = ['Belirtilmemiş']

    # Değişmiş Parçaları çek
    try:
        degismis = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[1]/div[4]/ul/li")
        car_data['Değişmiş'] = [li.text for li in degismis] if degismis else ['Belirtilmemiş']
    except Exception as e:
        car_data['Değişmiş'] = ['Belirtilmemiş']

    # Tramer tutarını çek
    try:
        tramer_xpath = "/html/body/div[2]/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[2]/div[2]/span"
        tramer = driver.find_element(By.XPATH, tramer_xpath).text
        car_data['Tramer Tutarı'] = tramer if tramer else 'Belirtilmemiş'
    except Exception as e:
        car_data['Tramer Tutarı'] = 'Belirtilmemiş'
    
    return car_data



def brand(driver):
    brand_list = []
    page_count_list = []
    car_count_list = []

    for i in range(1, 67):
        try:
            car_count_xpath = f"/html/body/div[2]/div[2]/div[3]/div/div[1]/div/div[2]/span/form/div[1]/div/div/div/div/ul/li/div/div[1]/div/div/ul[{i}]/li/a/span[2]"
            car_count = driver.find_element(By.XPATH, car_count_xpath).text
            car_count = int(car_count.replace(".", "").replace(",", ""))
            car_count_list.append(car_count)

            page_count = math.ceil(car_count / 50)
            page_count = min(page_count, 50)
            page_count_list.append(page_count)

            brand_xpath = f"/html/body/div[2]/div[2]/div[3]/div/div[1]/div/div[2]/span/form/div[1]/div/div/div/div/ul/li/div/div[1]/div/div/ul[{i}]/li/a"
            brand = driver.find_element(By.XPATH, brand_xpath).text
            brand = brand.rsplit(" ", 1)[0]
            brand_list.append(brand)
        except Exception as e:
            continue

    return brand_list, page_count_list, car_count_list


def model_info(driver, brand_name):
    model_counts_list = []
    model_name = []
    model_page_list = []

    # Belirtilen markanın URL'sine gidiyoruz
    url = f"https://www.arabam.com/ikinci-el/otomobil/{brand_name.lower().replace(' ', '-')}/?take=50"
    driver.get(url)
    #st.success(f"{brand_name} sitesine girildi.")

    j = 1  # İlk model öğesinden başlıyoruz
    while True:
        try:
            # XPATH ile model bilgilerini çekme
            xpath = f'/html/body/div[2]/div[2]/div[3]/div/div[1]/div/div[2]/span/form/div[1]/div/div/div[1]/div/ul/li/ul/li/div/div[1]/div/div/ul[{j}]/li/a'
            element = driver.find_element(By.XPATH, xpath)
            full_text = element.text

            # Model sayısı ve isimlerini ayıklama
            model_counts = full_text.rsplit(" ", 1)[-1]
            model_counts = int(model_counts.replace('.', '').replace(',', ''))
            model_counts_list.append(model_counts)

            model_name_x = full_text.rsplit(" ", 1)[0]
            model_name.append(model_name_x)

            # Sayfa sayısını hesaplama
            model_page_count = math.ceil(model_counts / 50)
            model_page_count = min(model_page_count, 50)  # Maksimum 50 sayfa sınırı
            model_page_list.append(model_page_count)

            j += 1  # Sonraki modele geç
        except Exception as e:
            break  # Tüm modeller alındıktan sonra döngüyü bitir

    # "Tüm Modeller" seçeneğini ekle
    model_name.insert(0, "All Models")
    model_counts_list.insert(0, sum(model_counts_list))
    model_page_list.insert(0, max(model_page_list) if model_page_list else 1)

    return model_name, model_counts_list, model_page_list


def calculate_dynamic_page_count(driver):
    xpath="/html/body/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]/div/div[1]/span/span"
    try:
        # XPath ile toplam araç sayısını alıyoruz
        total_cars_text = driver.find_element(By.XPATH, xpath).text
        total_cars = int(total_cars_text)  # Metni integer'a çeviriyoruz
        page_count = math.ceil(total_cars / 50)  # 50'ye bölerek sayfa sayısını hesaplıyoruz (tavan bölme)
        page_count = min(page_count, 50)
        return page_count
    except Exception as e:
        st.error(f"The number of pages could not be calculated dynamically: {e}")
        return 1  # Varsayılan olarak 1 sayfa döndürüyoruz


def fetch_car_data(driver, url, page_count):
    all_car_info = []
    for page_num in range(1, page_count + 1):
        page_url = f"{url}&page={page_num}"
        driver.get(page_url)
        st.info(f"{page_num}. page is processing...")
        time.sleep(5)  # Sayfanın yüklenmesi için bekliyoruz

        try:
            car_rows = driver.find_elements(By.CSS_SELECTOR, '.listing-table-wrapper tr')
            car_count_on_page = len(car_rows)

            for i in range(2, car_count_on_page):  # İlk 2 satır başlıklar için kullanılıyor
                try:
                    car_info_xpath = f'/html/body/div[2]/div[2]/div[3]/div/div[2]/div[2]/div[2]/table/tbody/tr[{i}]/td[2]/a'
                    driver.find_element(By.XPATH, car_info_xpath).click()

                    # Araç bilgilerini çek
                    single_car_data = get_single_car_data(driver)
                    all_car_info.append(single_car_data)
                    driver.back()
                except Exception as e:
                    #st.error(f"Araç bilgisi çekilemedi: {e}")
                    continue
        except Exception as e:
            #st.error(f"Sayfa verileri alınamadı: {e}")
            continue

    return all_car_info

# Card display function with improved HTML structure
def display_cards(filtered_data):

    for i, (_, row) in enumerate(filtered_data.iterrows()):
        with st.container():
            # Basic information to be displayed on the card surface
            st.markdown(
                f"""                     
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Brand:</span> {row.get("Marka", "Belirtilmedi")} 
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Serie:</span> {row.get("Seri", "Belirtilmedi")} 
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Model:</span> {row.get("Model", "Belirtilmedi")}   
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Year:</span>  {row.get("Yıl", "Belirtilmedi")}
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Price:</span> {row.get("Fiyat", "Belirtilmedi")} 
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Mileage:</span>   {row.get("Kilometre", "Belirtilmedi")} 
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Fuel Type:</span> {row.get("Yakıt Tipi", "Belirtilmedi")} 
                    <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Transmission Type:</span> {row.get("Vites Tipi", "Belirtilmedi")}
            """, 
            unsafe_allow_html=True
            )
            with st.expander(
                "View Details", expanded=False):
                st.markdown(f"""   
                    <div class="card">
                        <h3>{row.get('Marka', 'Belirtilmedi')} {row.get('Seri', 'Belirtilmedi')} {row.get('Model', 'Belirtilmedi')} ({row.get('Yıl', 'Belirtilmedi')})</h3>
                        <p><strong>Price:</strong>   {row.get('Fiyat', 'Belirtilmedi')} </p>
                        <p><strong>Mileage:</strong>   {row.get('Kilometre', 'Belirtilmedi')} </p>
                        <p><strong>Fuel Type:</strong> {row.get('Yakıt Tipi', 'Belirtilmedi')}</p>
                        <p><strong>Transmission Type:</strong> {row.get('Vites Tipi', 'Belirtilmedi')}</p>
                        <hr>
                        <!-- Detailed Informations -->                       
                        <p><strong>Engine Capacity:</strong> {row.get('Motor Hacmi', 'Belirtilmedi')}</p>
                        <p><strong>Engine Power:</strong> {row.get('Motor Gücü', 'Belirtilmedi')} </p>
                        <p><strong>Class Type:</strong> {row.get('Sınıfı', 'Belirtilmedi')}</p>
                        <p><strong>Color:</strong> {row.get('Renk', 'Belirtilmedi')}</p>
                        <p><strong>Body Type:</strong> {row.get('Kasa Tipi', 'Belirtilmedi')}</p>
                        <p><strong>Maximum Speed:</strong> {row.get('Maksimum Hız', 'Belirtilmedi')}</p>
                        <p><strong>0-100 km/h acceleration:</strong> {row.get('Hızlanma (0-100)', 'Belirtilmedi')}</p>
                        <p><strong>Length - Width - Height:</strong> {row.get('Uzunluk', 'Belirtilmedi')} - {row.get('Genişlik', 'Belirtilmedi')} - {row.get('Yükseklik', 'Belirtilmedi')}</p>
                        <p><strong>Weight - Curb Weight:</strong> {row.get('Ağırlık', 'Belirtilmedi')} - {row.get('Boş Ağırlığı', 'Belirtilmedi')}</p> 
                        <p><strong>Torque:</strong> {row.get('Tork', 'Belirtilmedi')}</p> 
                        <p><strong>Maximum Power:</strong> {row.get('Maksimum Gücü', 'Belirtilmedi')}</p> 
                        <p><strong>Fuel Tank Capacity:</strong> {row.get('Yakıt Deposu', 'Belirtilmedi')}</p>
                        <p><strong>Average Fuel Consumption:</strong> {row.get('Ortalama Yakıt Tüketimi', 'Belirtilmedi')}</p>
                        <p><strong>Number of Seats:</strong> {row.get('Koltuk Sayısı', 'Belirtilmedi')}</p>
                        <p><strong>Trunk Capacity:</strong> {row.get('Bagaj Hacmi', 'Belirtilmedi')}</p>
                        <p><strong>Production Year (First/Last):</strong> {row.get('Üretim Yılı (İlk/Son)', 'Belirtilmedi')}</p>
                        <p><strong>Drivetrain:</strong> {row.get('Çekiş', 'Belirtilmedi')}</p>
                        <p><strong>Tramer Amount:</strong> {row.get('Tramer Tutarı', 'Belirtilmedi')}</p> 
                        <p><strong>Painted:</strong> {row.get('Boyalı', 'Belirtilmedi')}</p>
                        <p><strong>Locally Painted:</strong> {row.get('Lokal Boyalı', 'Belirtilmedi')}</p>
                        <p><strong>Replaced:</strong> {row.get('Değişmiş', 'Belirtilmedi')}</p>
                        <p><strong>Wheelbase:</strong> {row.get('Aks Aralığı', 'Belirtilmedi')}</p>
                        <p><strong>City Fuel Consumption:</strong> {row.get('Şehir İçi Yakıt Tüketimi', 'Belirtilmedi')}</p>
                        <p><strong>Highway Fuel Consumption:</strong> {row.get('Şehir Dışı Yakıt Tüketimi', 'Belirtilmedi')}</p>
                        <p><strong>Front Tire:</strong> {row.get('Ön Lastik', 'Belirtilmedi')}</p>
                        <p><strong>From (Seller):</strong> {row.get('Kimden', 'Belirtilmedi')}</p>
                        <p><strong>License Plate Nationality:</strong> {row.get('Plaka Uyruğu', 'Belirtilmedi')}</p>

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

def sayfa_3():
    st.markdown("### Dynamic Data Collection and Processing")
    if not st.session_state.page_loaded:
        driver.get("https://www.arabam.com/ikinci-el/otomobil?take=50")
        st.session_state.page_loaded = True

        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
            st.success("Cookies accepted.")
        except:
            st.warning("The cookie consent button was not found or timed out.")

    # Markaları topluyoruz
    if "brand_list" not in st.session_state:
        st.session_state.brand_list, st.session_state.page_count_list, st.session_state.car_count_list = brand(driver)

    brand_list = st.session_state.brand_list
    if brand_list:
        selected_brand = st.sidebar.selectbox("Select a brand:", brand_list, key="selected_brand")

        if selected_brand:
            base_url = f"https://www.arabam.com/ikinci-el/otomobil/{selected_brand.lower().replace(' ', '-')}/?take=50"

            if st.sidebar.button(f"Collect models for {selected_brand}", key="fetch_models"):
                driver.get(base_url)
                st.success(f"Logged into the site for {selected_brand}")
                st.session_state.model_name, st.session_state.model_counts_list, st.session_state.model_page_list = model_info(driver, selected_brand)

            if "model_name" in st.session_state and st.session_state.model_name:
                selected_model = st.sidebar.selectbox("Select Model:", st.session_state.model_name, key="selected_model")

                if selected_model:
                    if selected_model == "All Models":
                        final_url = f"https://www.arabam.com/ikinci-el/otomobil/{selected_brand.lower().replace(' ', '-')}/?take=50"
                        page_count = st.session_state.page_count_list[brand_list.index(selected_brand)]
                    else:
                        final_url = f"https://www.arabam.com/ikinci-el/otomobil/{selected_brand.lower().replace(' ', '-')}-{selected_model.lower().replace(' ', '-')}/?take=50"
                        page_count = st.session_state.model_page_list[st.session_state.model_name.index(selected_model)]

                    # "Seçilen Modelin Sayfasına Git" butonu
                    if st.sidebar.button(f"Go to Selected Model ({selected_model}) Page"):
                        driver.get(final_url)
                        st.success(f"Navigated to the {selected_model} Page.")

                    # Fiyat ve kilometre filtreleme alanları
                    min_price = st.sidebar.number_input("Minimum Price (TL):", min_value=0, value=0, step=1000, key="min_price")
                    max_price = st.sidebar.number_input("Maximum Price (TL):", min_value=0, value=0, step=1000, key="max_price")
                    min_km = st.sidebar.number_input("Minimum KM:", min_value=0, value=0, step=1000, key="min_km")
                    max_km = st.sidebar.number_input("Maximum KM:", min_value=0, value=0, step=1000, key="max_km")

                    # Filtrelenmiş sayfaya git butonu
                    if st.sidebar.button("Go to Filtered Page"):
                        base_url_1 = f"https://www.arabam.com/ikinci-el/otomobil/{selected_brand.lower().replace(' ', '-')}"
                        if selected_model != "All Models":
                            base_url_1 += f"-{selected_model.lower().replace(' ', '-')}"
                            
                        params = ["currency=TL"]  # Sabit parametre olarak para birimi
                    
                        # Filtre parametrelerini kontrol edip listeye ekliyoruz
                        if min_price > 0:
                            params.append(f"minPrice={min_price}")
                        if max_price > 0:
                            params.append(f"maxPrice={max_price}")
                        if min_km > 0:
                            params.append(f"minkm={min_km}")
                        if max_km > 0:
                            params.append(f"maxkm={max_km}")
                    
                        # Parametreleri "&" ile birleştirerek final URL'yi oluşturuyoruz
                        if len(params) > 1:  # Filtre parametreleri varsa
                            query_string = "&".join(params)
                            final_url = f"{base_url_1}?{query_string}&take=50"
                        else:
                            final_url = f"{base_url_1}?take=50"  # Filtre yoksa sadece temel URL

                        # Filtrelenmiş URL'yi driver'a gönderiyoruz
                        driver.get(final_url)
                        st.session_state.final_url = final_url
                        #st.success(f"Filtrelenmiş sayfaya gidildi: {final_url}")
                    

                    # "Retrieve Data" butonu
                    if st.sidebar.button("Retrieve Data"):
                        if "final_url" in st.session_state:

                            st.markdown(spinner_css, unsafe_allow_html=True)
                            st.markdown(spinner_html, unsafe_allow_html=True)
                        
                            # Dinamik sayfa sayısını hesaplama
                            dynamic_page_count = calculate_dynamic_page_count(driver)
                            # Veri çekme işlemini başlat
                            car_data = fetch_car_data(driver, st.session_state.final_url, dynamic_page_count)
                            
                            # Veri çekme tamamlandığında animasyonu gizle
                            st.markdown(
                                "<style>.spinner-container { display: none; }</style>",
                                unsafe_allow_html=True
                            )
                
                            if car_data:
                                st.success("Fetching Completed.")
                                st.subheader(f"Total number of data obtained: {len(car_data)}")
                                df = pd.DataFrame(car_data)
                                display_cards(df)
                                csv = df.to_csv(index=False)
                                st.download_button("Download Data as CSV", csv, f"{selected_model}_verileri.csv", "text/csv")
                            else:
                                st.warning("Data not found.")
                          
                        else:
                            st.warning("Please go to the filtered page first.")
                else:
                    st.warning("Please select a model.")
            else:
                st.warning("Please click the 'Collect Models' button first to gather the models.")
    else:
        st.warning("Brand not found!")

sayfa_3()