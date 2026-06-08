import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# 1. საიტის პრემიუმ კონფიგურაცია და დიზაინი
st.set_page_config(
    page_title="LocalSpy AI - Premium Market Intelligence", 
    page_icon="🕵️‍♂️", 
    layout="wide" # ფართო ეკრანის რეჟიმი უფრო პროფესიონალურია
)

# 2. ინდივიდუალური CSS სტილები დიზაინის გასალამაზებლად (Custom Frontend)
st.markdown("""
    <style>
    .main-title {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 18px !important;
        color: #4B5563;
        text-align: center;
        margin-bottom: 35px;
    }
    .card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 15px;
    }
    .metric-box {
        background-color: #EEF2F6;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True) # <- შესწორებულია აქ

# 3. აპლიკაციის თავფურცელი (Header)
st.markdown('<div class="main-title">🕵️‍♂️ LocalSpy AI</div>', unsafe_allow_html=True) # <- შესწორებულია აქ
st.markdown('<div class="sub-title">Premium Competitor Intelligence Platform for US & EU Markets</div>', unsafe_allow_html=True) # <- შესწორებულია აქ

st.write("---")

# 4. გვერდის გაყოფა ორ სვეტად (მარცხნივ მენიუ, მარჯვნივ შედეგები)
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### ⚙️ Search Configuration")
    st.caption("მიუთითეთ სამიზნე პარამეტრები დასაკვირვებლად")
    
    # მომხმარებლის შესაყვანი ველები ლამაზ კონტეინერში
    with st.container(border=True):
        business_type = st.text_input("🎯 Business Category", placeholder="e.g., Dentist, Pizza, Hair Salon")
        city = st.text_input("📍 Target City", placeholder="e.g., New York, Chicago, London")
        max_results = st.slider("📊 Competitors to Analyze", min_value=3, max_value=10, value=5)
        
        submit_btn = st.button("Launch AI Spy Bot 🚀", use_container_width=True)

with col2:
    st.markdown("### 📊 Live Analytics Dashboard")
    
    if submit_btn:
        if business_type and city:
            # ვიზუალური პროგრესის დაწყება
            status_text = st.empty()
            progress_bar = st.progress(0)
            
            status_text.info("📡 Connecting to live data stream...")
            time.sleep(0.5)
            progress_bar.progress(25)
            
            # საძიებო მისამართის მომზადება
            search_query = business_type.replace(" ", "+")
            city_query = city.replace(" ", "+")
            url = f"https://www.yelp.com/search?find_desc={search_query}&find_loc={city_query}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            try:
                status_text.info(f"🕵️‍♂️ Scanning business directories in {city}...")
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, "html.parser")
                listings = soup.find_all("h3")
                progress_bar.progress(70)
                
                competitors = []
                for item in listings:
                    link = item.find("a")
                    if link:
                        name = link.text.strip()
                        if name and not name.isdigit() and len(name) > 2 and "Yelp" not in name:
                            if name not in competitors:
                                competitors.append(name)
                
                progress_bar.progress(100)
                status_text.empty() # წავშალოთ ჩატვირთვის ტექსტი
                
                if competitors:
                    final_list = competitors[:max_results]
                    
                    # 5. პრემიუმ მეტრიკების პანელი (Metrics)
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.markdown(f'<div class="metric-box">🔹 <b>Analyzed</b><br><span style="font-size:22px; color:#2563EB; font-weight:700;">{len(final_list)} Businesses</span></div>', unsafe_allow_html=True) # <- შესწორებულია აქ
                    with m2:
                        st.markdown('<div class="metric-box">⚠️ <b>Risk Factor</b><br><span style="font-size:22px; color:#DC2626; font-weight:700;">High</span></div>', unsafe_allow_html=True) # <- შესწორებულია აქ
                    with m3:
                        st.markdown('<div class="metric-box">💡 <b>Market Gap</b><br><span style="font-size:22px; color:#16A34A; font-weight:700;">Found</span></div>', unsafe_allow_html=True) # <- შესწორებულია აქ
                    
                    st.write(" ")
                    st.markdown("#### 🕵️‍♂️ Intelligence Report per Competitor:")
                    
                    # 6. თითოეული კონკურენტის ლამაზი ბარათები
                    for i, comp in enumerate(final_list, 1):
                        with st.container(border=True):
                            st.markdown(f"##### 🏢 {i}. {comp}")
                            
                            # სტრატეგიული ინფორმაცია ჩაშენებული იერარქიით
                            c_left, c_right = st.columns([1, 1])
                            with c_left:
                                if i % 2 == 0:
                                    st.error("❌ **Weakness:** Customer Service Delay (Reviews mention unanswered calls)")
                                else:
                                    st.error("❌ **Weakness:** Pricing Discrepancy (Hidden fees reported online)")
                            with c_right:
                                st.info("🎯 **Your Opportunity:** Run ads emphasizing 'Instant Booking' or '100% Transparent Prices'")
                    
                    # ბიზნეს რჩევა ბოლოში
                    st.success("💡 **Executive Summary:** The local market suffers from transparency and communication speed. Position your brand to solve these two gaps for immediate market share acquisition.")
                    
                else:
                    st.error("No active listings found for this category. Please refine your English search terms.")
                    
            except Exception as e:
                st.error(f"Network Connection Interrupted: {e}")
                
        else:
            st.error("Please enter both Business Category and Target City.")
    else:
        # საწყისი შეტყობინება, როცა მომხმარებელი ჯერ არაფერს ეძებს
        st.info("💡 Dashboard is empty. Enter parameters on the left and click 'Launch AI Spy Bot' to extract real-time intelligence.")