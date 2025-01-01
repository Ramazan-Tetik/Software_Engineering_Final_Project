import streamlit as st
import pandas as pd
import time
import re

 
with open("common.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.markdown("""
<body>
    <section class="home" id="home">
        <div class="content">
            <h3> </h3>
            <p></p>
        </div>
    </section>
</body>    
    """, unsafe_allow_html=True)
if "df" in st.session_state:
    del st.session_state["df"]

# Eski DataFrame'i temizle
if "df3" in st.session_state:
    del st.session_state["df3"]
    


df1 = pd.read_csv("car_info1.csv")
st.session_state["df1"] = df1

#in model dropdown menu,changes models appropriate form before sorting
def extract_number(model):
    
    match = re.search(r'\d+(\.\d+)?', model)
    if match:
        return float(match.group())  
    return 0 

# Card display function with improved HTML structure
def display_cards(filtered_data_arabam):

    for i, (_, row) in enumerate(filtered_data_arabam.iterrows()):
            with st.container():
            # Basic information to be displayed on the card surface
                st.markdown(
                    f"""                     
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Brand:</span> {row.get("Marka", "Bilinmiyor")} 
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Serie:</span> {row.get("Seri", "Bilinmiyor")} 
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Model:</span> {row.get("Model","Bilinmiyor")}   
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Year:</span>  {row.get("Yıl", "Bilinmiyor")}
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Price:</span> {row.get("Fiyat","Bilinmiyor")} TL
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Mileage:</span>   {row.get("Kilometre","Bilinmiyor")} km
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Fuel Type:</span> {row.get("Yakıt Tipi", "Bilinmiyor")} 
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Transmission Type:</span> {row.get("Vites Tipi", "Bilinmiyor")}
            """, 
            unsafe_allow_html=True
                )
                with st.expander(
                    
                    "View Details", expanded=False):
                    
                    st.markdown(f"""   
                        <div class="card">
                            <h3>{row['Marka']} {row['Seri']} {row['Model']} ({row['Yıl']})</h3>
                            <p><strong>Price:</strong>   {row['Fiyat']} TL</p>
                            <p><strong>Mileage:</strong>   {row['Kilometre']} km</p>
                            <p><strong>Fuel Type:</strong> {row['Yakıt Tipi']}</p>
                            <p><strong>Transmission Type:</strong> {row['Vites Tipi']}</p>
                            <hr>
                            <!-- Detailed Informations -->                       
                            <p><strong>Engine Capacity:</strong> {row['Motor Hacmi']}</p>
                            <p><strong>Engine Power:</strong> {row['Motor Gücü']} </p>
                            <p><strong>Class Type:</strong> {row['Sınıfı']}</p>
                            <p><strong>Drivetrain:</strong> {row['Çekiş']}</p>
                            <p><strong>Color:</strong> {row['Renk']}</p>
                            <p><strong>Body Type:</strong> {row['Kasa Tipi']}</p>
                            <p><strong>Maximum Speed:</strong> {row['Maksimum Hız']}</p>
                            <p><strong>0-100 km/h acceleration:</strong> {row['Hızlanma (0-100)']}</p>
                            <p><strong>Length - Width - Height:</strong> {row['Uzunluk']} - {row['Genişlik']} - {row['Yükseklik']}</p>
                            <p><strong>Weight - Curb Weight:</strong> {row['Ağırlık']} - {row['Boş Ağırlığı']}</p> 
                            <p><strong>Torque:</strong> {row['Tork']}</p> 
                            <p><strong>Maximum Power:</strong> {row['Maksimum Güç']}</p> 
                            <p><strong>Fuel Tank Capacity:</strong> {row['Yakıt Deposu']}</p>
                            <p><strong>Average Fuel Consumption:</strong> {row['Ortalama Yakıt Tüketimi']}</p>
                            <p><strong>City Fuel Consumption:</strong> {row['Şehir İçi Yakıt Tüketimi']}</p>
                            <p><strong>Highway Fuel Consumption:</strong> {row['Şehir Dışı Yakıt Tüketimi']}</p>
                            <p><strong>Number of Seats:</strong> {row['Koltuk Sayısı']}</p>
                            <p><strong>Trunk Capacity:</strong> {row['Bagaj Hacmi']}</p>
                            <p><strong>Production Year (First/Last):</strong> {row['Üretim Yılı (İlk/Son)']}</p>
                            <p><strong>Painted:</strong> {row['Boyalı']}</p>
                            <p><strong>Locally Painted:</strong> {row['Lokal Boyalı']}</p>
                            <p><strong>Replaced:</strong> {row['Değişmiş']}</p>
                            <p><strong>Wheelbase:</strong> {row['Aks Aralığı']}</p>
                            <p><strong>Front Tire:</strong> {row['Ön Lastik']}</p>               
                            <p><strong>From (Seller):</strong> {row['Kimden']}</p>
                            <p><strong>License Plate Nationality:</strong> {row['Plaka Uyruğu']}</p>  
                        </div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<hr style='border: 1px solid black; margin: 20px 0;'>", unsafe_allow_html=True)



@st.cache_data
def filter_data(selected_brands, selected_series, selected_models, selected_years, selected_price, selected_km, selected_fuel_types, selected_transmission_types):
    filtered_data_arabam = df1.copy()

    if selected_brands and "All Brands" not in selected_brands:
        filtered_data_arabam = filtered_data_arabam[filtered_data_arabam['Marka'].isin(selected_brands)]

    if selected_series and "All Series" not in selected_series:
        filtered_data_arabam = filtered_data_arabam[filtered_data_arabam['Seri'].isin(selected_series)]

    if selected_models and "All Models" not in selected_models:
        filtered_data_arabam = filtered_data_arabam[filtered_data_arabam['Model'].isin(selected_models)]

    if selected_years and "All Years" not in selected_years:
        filtered_data_arabam = filtered_data_arabam[filtered_data_arabam['Yıl'].isin(selected_years)]

    if selected_price:
        filtered_data_arabam = filtered_data_arabam[(filtered_data_arabam['Fiyat'] >= selected_price[0]) & (filtered_data_arabam['Fiyat'] <= selected_price[1])]

    if selected_km:
        filtered_data_arabam = filtered_data_arabam[(filtered_data_arabam['Kilometre'] >= selected_km[0]) & (filtered_data_arabam['Kilometre'] <= selected_km[1])]

    if selected_fuel_types:
        filtered_data_arabam = filtered_data_arabam[filtered_data_arabam['Yakıt Tipi'].isin(selected_fuel_types)]

    if selected_transmission_types:
        filtered_data_arabam = filtered_data_arabam[filtered_data_arabam['Vites Tipi'].isin(selected_transmission_types)]

    return filtered_data_arabam


# Step 1: Select Brand
brands = sorted(df1['Marka'].unique())
brands = ["All Brands"] + brands
selected_brands = st.sidebar.multiselect('Choose a car brand or brands:', options=brands, default=["All Brands"])

if "All Brands" in selected_brands and len(selected_brands) > 1:
    st.warning("The 'All Brands' option cannot be combined with other brands!")
    selected_brands = ["All Brands"]

# Step 2: Select Series (work dynamically even if "All Brands" is selected)
if "All Brands" in selected_brands:
    # If "All Brands" is selected, load all series
    series = df1['Seri'].unique()
    series = ["All Series"] + sorted(series)
    selected_series = st.sidebar.multiselect('Choose a car serie or series:', options=series, default=["All Series"])
else:
    # If specific brands are selected, filter series accordingly
    series = df1[df1['Marka'].isin(selected_brands)]['Seri'].unique()
    series = ["All Series"] + sorted(series)
    selected_series = st.sidebar.multiselect('Choose a car serie or series:', options=series, default=["All Series"])

if "All Series" in selected_series and len(selected_series) > 1:
    st.warning("The 'All Series' option cannot be combined with other series!")
    selected_series = ["All Series"]

# Step 3: Select Models (work dynamically even if "All Series" or "All Brands" is selected)
if "All Series" in selected_series or "All Brands" in selected_brands:
    # If "All Series" or "All Brands" is selected, load all models
    models = df1['Model'].unique()
    models = ["All Models"] + sorted(models)
    selected_models = st.sidebar.multiselect('Choose a car model or models:', options=models, default=["All Models"])
else:
    # If specific series are selected, filter models accordingly
    models = df1[
        (df1['Marka'].isin(selected_brands)) &
        (df1['Seri'].isin(selected_series) if "All Series" not in selected_series else True)
    ]['Model'].unique()
    models = ["All Models"] + sorted(models)
    selected_models = st.sidebar.multiselect('Choose a car model or models:', options=models, default=["All Models"])

if "All Models" in selected_models and len(selected_models) > 1:
    st.warning("The 'All Models' option cannot be combined with other models!")
    selected_models = ["All Models"]

# Step 4: Select Years (only if models are selected or "All Models" is selected)
if selected_models and ("All Models" in selected_models or len(selected_models) > 0):
    years = df1[
    (df1['Marka'].isin(selected_brands) if "All Brands" not in selected_brands else df1['Marka'].notna()) &
    (df1['Seri'].isin(selected_series) if "All Series" not in selected_series else df1['Seri'].notna()) &
    (df1['Model'].isin(selected_models) if "All Models" not in selected_models else df1['Model'].notna())
    ]['Yıl'].unique()

    years = sorted(years, reverse=True)
    selected_years = st.sidebar.multiselect('Choose a year or years:', options=["All Years"] + years,default=["All Years"])

    if "All Years" in selected_years and len(selected_years) > 1:
        st.warning("The 'All Years' option cannot be combined with other years!")
        selected_years = ["All Years"]
else:
    selected_years = ["All Years"]

# Step 5: Filter Data for Price and Mileage
filtered_data_arabam = df1[
    (df1['Marka'].isin(selected_brands) if "All Brands" not in selected_brands else df1['Marka'].notna()) &
    (df1['Seri'].isin(selected_series) if "All Series" not in selected_series else df1['Seri'].notna()) &
    (df1['Model'].isin(selected_models) if "All Models" not in selected_models else df1['Model'].notna()) &
    (df1['Yıl'].isin(selected_years) if "All Years" not in selected_years else df1['Yıl'].notna())
]

# Step 6: Dynamic Price and Mileage Sliders
if not filtered_data_arabam.empty:
    # Calculate dynamic min and max for price
    min_price, max_price = int(filtered_data_arabam['Fiyat'].min()), int(filtered_data_arabam['Fiyat'].max())
    if min_price == max_price:
        st.sidebar.write(f"Price Range: {min_price} (only one option available)")
        selected_price = (min_price, max_price)
    else:
        selected_price = st.sidebar.slider('Select Price Range:', min_value=min_price, max_value=max_price, value=(min_price, max_price), step=1000)

    # Calculate dynamic min and max for mileage
    min_km, max_km = int(filtered_data_arabam['Kilometre'].min()), int(filtered_data_arabam['Kilometre'].max())
    if min_km == max_km:
        st.sidebar.write(f"Mileage Range: {min_km} (only one option available)")
        selected_km = (min_km, max_km)
    else:
        selected_km = st.sidebar.slider('Select Mileage Range:', min_value=min_km, max_value=max_km, value=(min_km, max_km), step=1000)
else:
    selected_price = (0, 0)
    selected_km = (0, 0)

# Step 7: Fuel and Transmission Multiselect
fuel_types = filtered_data_arabam['Yakıt Tipi'].unique()
transmission_types = filtered_data_arabam['Vites Tipi'].unique()

selected_fuel_types = st.sidebar.multiselect('Select Fuel Type:', options=fuel_types, default=fuel_types)
selected_transmission_types = st.sidebar.multiselect('Select Transmission Type:', options=transmission_types, default=transmission_types)

# Apply final filters to the data
final_filtered_data_arabam = filtered_data_arabam[
    (filtered_data_arabam['Fiyat'] >= selected_price[0]) & (filtered_data_arabam['Fiyat'] <= selected_price[1]) &
    (filtered_data_arabam['Kilometre'] >= selected_km[0]) & (filtered_data_arabam['Kilometre'] <= selected_km[1]) &
    (filtered_data_arabam['Yakıt Tipi'].isin(selected_fuel_types)) &
    (filtered_data_arabam['Vites Tipi'].isin(selected_transmission_types))
]


if "filtered_data_arabam" not in st.session_state:
    st.session_state.filtered_data_arabam = None
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

spinner_css = """
<style>
.spinner-container {
    display: flex;
    align-items: center;
    justify-content: center;
    height: auto; /* Yüksekliği otomatik yaparak gereksiz boşluğu kaldırıyoruz */
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
    animation: fadeOut 2s 3s forwards; 
}
.loader span {
    display: inline-block; 
    animation: wavy 1s ease-in-out 3; 
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
        color:transparent;
        text-shadow:none;
    }
    20% {
        transform: translateY(-15px); 
        color:#040d15;
        text-shadow:0 0 5px #040d15,
        0 0 25px #040d15,
        0 0 50px #040d15;
    }
    40%,100% {
        transform: translateY(0);
        color: transparent;
        text-shadow: none;
    }
}
@keyframes fadeOut {
    0% { opacity: 1; }
    100% { opacity: 0; visibility: hidden; }
}
</style>
"""
st.markdown(spinner_css, unsafe_allow_html=True)

if st.sidebar.button("Search", key="search-btn"):

        spinner_html = """
    <div class="spinner-container">
        <div class="spinner"></div>
    </div>
    <div class="loader">
        <span >L</span>
        <span >O</span>
        <span >A</span>
        <span >D</span>
        <span >I</span>
        <span >N</span>
        <span >G</span>
        <span >.</span>
        <span >.</span>
        <span >.</span>
    </div>
    """
        # Simulate data loading while the spinner is visible.
        st.markdown(spinner_html, unsafe_allow_html=True)
        time.sleep(5) 
    
        filtered_data_arabam = filter_data(selected_brands, selected_series,selected_models, selected_years,selected_price, selected_km, selected_fuel_types,selected_transmission_types )    
        
    

        st.session_state.filtered_data_arabam = filtered_data_arabam
        st.session_state.current_page = 1

if st.session_state.filtered_data_arabam is None or st.session_state.filtered_data_arabam.empty:
    st.markdown(f"### Please Perform a Search to See Results")
else:
    
    filtered_data_arabam = st.session_state.filtered_data_arabam

    st.markdown("### Sort Options")
    col1, col2 = st.columns(2)
    sort_order = None
    
    with col1:
        if st.button("⬆️ Ascending"):
            sort_order = "Ascending"
            
    with col2:
        if st.button("⬇️ Descending"):
            sort_order = "Descending"
    if sort_order:
        if sort_order == "Ascending":
            filtered_data_arabam = filtered_data_arabam.sort_values(by="Fiyat", ascending=True)
        elif sort_order == "Descending":
            filtered_data_arabam = filtered_data_arabam.sort_values(by="Fiyat", ascending=False)

    # Pagination
    ITEMS_PER_PAGE = 20
    total_items = len(filtered_data_arabam)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # Slices the data of the current page
    start_idx = (st.session_state.current_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_data_arabam= filtered_data_arabam.iloc[start_idx:end_idx]

    st.markdown(f"### A total of {len(filtered_data_arabam)} car listings found:")
    st.markdown(f"### Showing page {st.session_state.current_page} of {total_pages}")

    display_cards(current_data_arabam)

    st.download_button("Download CSV File", filtered_data_arabam.to_csv(index=False),
                    file_name='car_price.csv', mime='text/csv')


    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous Page") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()

    with col3:
        if st.button("Next Page") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()

