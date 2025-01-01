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

#df = pd.read_csv("new_up_data (3).csv")


# Eski DataFrame'i temizle
if "df" in st.session_state:
    del st.session_state["df"]

# Eski DataFrame'i temizle
if "df1" in st.session_state:
    del st.session_state["df1"]
    

if "df3" not in st.session_state:
    st.session_state['df3'] = pd.read_csv("autoscout24.csv")

df = st.session_state['df3']


# 'brand' sütunundaki tüm verileri string türüne dönüştür
df['brand'] = df['brand'].astype(str)
# 'models' sütunundaki tüm verileri string türüne dönüştür 
df['model'] = df['model'].astype(str)
# 'years' sütunundaki tüm verileri string türüne dönüştür
df['First registration'] = df['First registration'].astype(str)

# 'Mileage' sütunundaki tüm verileri float türüne dönüştür
df['Mileage'] = pd.to_numeric(df['Mileage'], errors='coerce') 
# Kilometre sütunundaki NaN değerleri doldur 
df['Mileage'].fillna(0, inplace=True)

#in model dropdown menu,changes models appropriate form before sorting
def extract_number(model):
    
    match = re.search(r'\d+(\.\d+)?', model)
    if match:
        return float(match.group())  
    return 0 


# Card display function with improved HTML structure
def display_cards(filtered_data_autoscout):

    for i, (_, row) in enumerate(filtered_data_autoscout.iterrows()):
            with st.container():
            # Basic information to be displayed on the card surface
                st.markdown(
                    f"""                     
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Brand:</span>  {row['brand']} 
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Model:</span> {row['model']}   
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Year:</span>  {row['First registration']}
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Price:</span> {row['price']} 
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Mileage:</span>   {row['Mileage']} 
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Fuel Type:</span> {row['Fuel type']} 
                        <span style="color:rgba(95, 15, 15, 0.779); font-weight: bold;">Transmission Type:</span> {row['Gearbox']}
            """, 
            unsafe_allow_html=True
                )
                with st.expander(
                    
                    "View Details", expanded=False):
                    
                    st.markdown(f"""   
                        <div class="card">
                            <h3>{row['brand']} {row['model']} ({row['First registration']})</h3>
                                <p><strong>Price:</strong>   {row['price']} $ </p>
                                <p><strong>Mileage:</strong>   {row['Mileage']} km</p>
                                <p><strong>Fuel Type:</strong> {row['Fuel type']}</p>
                                <p><strong>Transmission Type:</strong> {row['Gearbox']}</p>
                                <hr>
                                <!-- Detailed Informations -->                       
                                <p><strong>Power:</strong> {row['Power']}</p>                                   
                                <p><strong>Body Type:</strong> {row['Body type']}</p>
                                <p><strong>Type:</strong> {row['Type']}</p>
                                <p><strong>Engine Size :</strong> {row['Engine size']}</p>
                                <p><strong>Color:</strong> {row['Colour']}</p>
                                <p><strong>Seats:</strong> {row['Seats']}</p>
                                <p><strong>Doors:</strong> {row['Doors']}</p>
                                <p><strong>Seller:</strong> {row['Seller']}</p>
                        </div>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<hr style='border: 1px solid black; margin: 20px 0;'>", unsafe_allow_html=True)
                

@st.cache_data
def filter_data(selected_brands, selected_models, selected_years, selected_price, selected_km, selected_fuel_types, selected_transmission_types):
    filtered_data_autoscout = df.copy()

    if selected_brands and "All Brands" not in selected_brands:
        filtered_data_autoscout = filtered_data_autoscout[filtered_data_autoscout['brand'].isin(selected_brands)]

    if selected_models and "All Models" not in selected_models:
        filtered_data_autoscout = filtered_data_autoscout[filtered_data_autoscout['model'].isin(selected_models)]

    if selected_years and "All Years" not in selected_years:
        filtered_data_autoscout = filtered_data_autoscout[filtered_data_autoscout['First registration'].isin(selected_years)]

    if selected_price:
        filtered_data_autoscout = filtered_data_autoscout[(filtered_data_autoscout['price'] >= selected_price[0]) & (filtered_data_autoscout['price'] <= selected_price[1])]

    if selected_km:
        filtered_data_autoscout = filtered_data_autoscout[(filtered_data_autoscout['Mileage'] >= selected_km[0]) & (filtered_data_autoscout['Mileage'] <= selected_km[1])]

    if selected_fuel_types:
        filtered_data_autoscout = filtered_data_autoscout[filtered_data_autoscout['Fuel type'].isin(selected_fuel_types)]

    if selected_transmission_types:
        filtered_data_autoscout = filtered_data_autoscout[filtered_data_autoscout['Gearbox'].isin(selected_transmission_types)]

    return filtered_data_autoscout


# Step 1: Select Brand
brands = sorted(df['brand'].unique())
brands = ["All Brands"] + brands
selected_brands = st.sidebar.multiselect('Choose a car brand or brands:', options=brands, default=["All Brands"])

if "All Brands" in selected_brands and len(selected_brands) > 1:
    st.warning("The 'All Brands' option cannot be combined with other brands!")
    selected_brands = ["All Brands"]

# Step 2: Select Models (work dynamically even if "All Brands" is selected)
if "All Brands" in selected_brands:
    # If "All Brands" is selected, load all series
    models = df['model'].unique()
    models = ["All Models"] + sorted(models)
    selected_models = st.sidebar.multiselect('Choose a car model or models:', options=models, default=["All Models"])
else:
    # If specific brands are selected, filter models accordingly
    models = df[df['brand'].isin(selected_brands)]['model'].unique()
    models = ["All Models"] + sorted(models)
    selected_models = st.sidebar.multiselect('Choose a car model or models:', options=models, default=["All Models"])

if "All Models" in selected_models and len(selected_models) > 1:
    st.warning("The 'All Models' option cannot be combined with other models!")
    selected_models = ["All Models"]

# Step 4: Select Years (only if models are selected or "All Models" is selected)
if selected_models and ("All Models" in selected_models or len(selected_models) > 0):
    years = df[
    (df['brand'].isin(selected_brands) if "All Brands" not in selected_brands else df['brand'].notna()) &
    (df['model'].isin(selected_models) if "All Models" not in selected_models else df['model'].notna())
    ]['First registration'].unique()

    years = sorted(years, reverse=True)
    selected_years = st.sidebar.multiselect('Choose a year or years:', options=["All Years"] + years,default=["All Years"])

    if "All Years" in selected_years and len(selected_years) > 1:
        st.warning("The 'All Years' option cannot be combined with other years!")
        selected_years = ["All Years"]
else:
    selected_years = ["All Years"]

# Step 5: Filtered Data Based on Selections
filtered_data_autoscout = df[
    (df['brand'].isin(selected_brands) if "All Brands" not in selected_brands else df['brand'].notna()) &
    (df['model'].isin(selected_models) if "All Models" not in selected_models else df['model'].notna()) &
    (df['First registration'].isin(selected_years) if "All Years" not in selected_years else df['First registration'].notna())
]

# Step 6: Dynamic Price and Mileage Sliders
if not filtered_data_autoscout.empty:
    # Calculate dynamic min and max for price
    min_price, max_price = int(filtered_data_autoscout['price'].min()), int(filtered_data_autoscout['price'].max())
    if min_price == max_price:
        st.sidebar.write(f"Price Range: {min_price} (only one option available)")
        selected_price = (min_price, max_price)
    else:
        selected_price = st.sidebar.slider('Select Price Range:', min_value=min_price, max_value=max_price, value=(min_price, max_price), step=1000)

    # Calculate dynamic min and max for mileage
    min_km, max_km = int(filtered_data_autoscout['Mileage'].min()), int(filtered_data_autoscout['Mileage'].max())
    if min_km == max_km:
        st.sidebar.write(f"Mileage Range: {min_km} (only one option available)")
        selected_km = (min_km, max_km)
    else:
        selected_km = st.sidebar.slider('Select Mileage Range:', min_value=min_km, max_value=max_km, value=(min_km, max_km), step=1000)
else:
    selected_price = (0, 0)
    selected_km = (0, 0)

# Step 7: Fuel and Transmission Multiselect
fuel_types = filtered_data_autoscout['Fuel type'].unique()
transmission_types = filtered_data_autoscout['Gearbox'].unique()

selected_fuel_types = st.sidebar.multiselect('Select Fuel Type:', options=fuel_types, default=fuel_types)
selected_transmission_types = st.sidebar.multiselect('Select Transmission Type:', options=transmission_types, default=transmission_types)

# Apply final filters to the data
final_filtered_data_autoscout = filtered_data_autoscout[
    (filtered_data_autoscout['price'] >= selected_price[0]) & (filtered_data_autoscout['price'] <= selected_price[1]) &
    (filtered_data_autoscout['Mileage'] >= selected_km[0]) & (filtered_data_autoscout['Mileage'] <= selected_km[1]) &
    (filtered_data_autoscout['Fuel type'].isin(selected_fuel_types)) &
    (filtered_data_autoscout['Gearbox'].isin(selected_transmission_types))
]


if "filtered_data_autoscout" not in st.session_state:
    st.session_state.filtered_data_autoscout = None
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
    
        filtered_data_autoscout = filter_data(selected_brands, selected_models, selected_years,selected_price, selected_km, selected_fuel_types,selected_transmission_types )    
        
        st.session_state.filtered_data_autoscout = filtered_data_autoscout
        st.session_state.current_page = 1

if st.session_state.filtered_data_autoscout is None or st.session_state.filtered_data_autoscout.empty:
    st.markdown(f"### Please Perform a Search to See Results")
else:
    
    filtered_data_autoscout = st.session_state.filtered_data_autoscout

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
            filtered_data_autoscout = filtered_data_autoscout.sort_values(by="price", ascending=True)
        elif sort_order == "Descending":
            filtered_data_autoscout = filtered_data_autoscout.sort_values(by="price", ascending=False)

    # Pagination
    ITEMS_PER_PAGE = 20
    total_items = len(filtered_data_autoscout)
    total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE

    # Slices the data of the current page
    start_idx = (st.session_state.current_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_data_autoscout = filtered_data_autoscout.iloc[start_idx:end_idx]

    st.markdown(f"### A total of {len(filtered_data_autoscout)} car listings found:")
    st.markdown(f"### Showing page {st.session_state.current_page} of {total_pages}")
    
    
    
    display_cards(current_data_autoscout)

    st.download_button("Download CSV File", filtered_data_autoscout.to_csv(index=False),
                    file_name='new_up_data (3).csv', mime='text/csv')


    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous Page") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()

    with col3:
        if st.button("Next Page") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()
