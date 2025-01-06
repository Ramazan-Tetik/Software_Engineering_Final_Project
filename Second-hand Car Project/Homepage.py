import streamlit as st

PAGES = {
    "CSV Arabam.com": "pages\CSV_Arabam.com.py",
    "CSV Autoscout24.com": "pages\CSV_Autoscout24.com.py",
    "CSV Cars.com": "pages\CSV_Cars.com.py",
    "Dynamic Arabam.com": "pages\Dynamic_Arabam.com.py",
    "Dynamic Autoscout24.com": "pages\Dynamic_Autoscout24.com.py",
    "Dynamic Cars.com": "pages\Dynamic_Cars.com.py"
}

st.markdown("""
   <body>
    <section class="home" id="home">
        <div class="content">
            <h3>Get Your Dream Car</h3>
            <p>Our collection offers a diverse selection of reliable, high-performance vehicles, from Compact to Luxury models to suit any driver's needs.</p>
        </div>
    </section>
</body>    
    """, unsafe_allow_html=True)

with open("common.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

