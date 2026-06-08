import streamlit as st
import pandas as pd
from google import genai
import json

# გვერდის სათაური და კონფიგურაცია
st.set_page_config(page_title="LocalSpy AI - ლოკალური მარკეტინგის დაზვერვა", page_icon="🕵️‍♂️", layout="wide")

# CSS სტილები პრემიუმ Frontend-ისთვის
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #4C6EF5; color: white; border-radius: 8px; width: 100%; }
    .report-card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.title("🕵️‍♂️ LocalSpy AI")
st.subheader("იპოვე მარკეტინგული ხარვეზები ადგილობრივ ბიზნესებში და შესთავაზე შენი მომსახურება")

# მომხმარებლის შეყვანილი მონაცემები
col1, col2 = st.columns(2)
with col1:
    business_type = st.text_input("ბიზნესის სფერო (მაგ: სტომატოლოგია, ფიტნეს კლუბი, სასტუმრო)", placeholder="სტომატოლოგია")
with col2:
    city = st.text_input("ქალაქი / ლოკაცია (მაგ: თბილისი, ბათუმი, ქუთაისი)", placeholder="თბილისი")

if st.button("მოძებნე და გააანალიზე ლოკაციები"):
    if not business_type or not city:
        st.warning("გთხოვთ შეავსოთ ორივე ველი!")
    else:
        # შემოწმება, დევს თუ არა Gemini-ს გასაღები საიტის პარამეტრებში
        if "GEMINI_API_KEY" not in st.secrets:
            st.error("შეცდომა: st.secrets-ში 'GEMINI_API_KEY' ვერ მოიძებნა. გთხოვთ ჩასვათ ის საიტის Settings -> Secrets-ში.")
        else:
            # აქ სწორად არის განსაზღვრული გასაღები
            my_api_key = st.secrets["GEMINI_API_KEY"]
            
            with st.spinner("🤖 LocalSpy AI უკავშირდება გუგლის სერვერებს და აანალიზებს ბიზნესებს..."):
                try:
                    # Google GenAI კლიენტის ინიციალიზაცია
                    client = genai.Client(api_key=my_api_key)
                    
                    # პრომპტი ხელოვნური ინტელექტისთვის
                    prompt = f"""
                    შენ ხარ ლოკალური მარკეტინგის ექსპერტი "LocalSpy AI". 
                    მოძებნე და მოიფიქრე 3 რეალური ან ძალიან ტიპური მაგალითი ბიზნესებისა სფეროდან: "{business_type}" ქალაქში: "{city}".
                    თითოეული ბიზნესისთვის დააგენერირე მარკეტინგული აუდიტი და შეადგინე JSON ფორმატი ზუსტად ამ სტრუქტურით (გამოიყენე ქართული ენა):
                    [
                      {{
                        "სახელი": "ბიზნესის დასახელება",
                        "ტელეფონი": "ტელეფონის ნომერი",
                        "ხარვეზი": "რა მარკეტინგული პრობლემა აქვს (მაგ: არ აქვს საიტი, ცუდი Facebook გვერდი, დაბალი რეიტინგი Google Maps-ზე)",
                        "პოტენციალი": "როგორ დაეხმატება ამ პრობლემის მოგვარება კლიენტების მოზიდვაში",
                        "შეთავაზება": "რა სერვისი უნდა შესთავაზოს ფრილანსერმა (მაგ: საიტის დამზადება 500 ლარად, რეკლამის ჩართვა)"
                      }}
                    ]
                    პასუხად დააბრუნე მხოლოდ და მხოლოდ სუფთა JSON ტექსტი, ყოველგვარი დამატებითი მისალმების ან '```json' ნიშნების გარეშე.
                    """
                    
                    # მოთხოვნა Gemini მოდელთან
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    
                    # პასუხის გაწმენდა და JSON-ად ქცევა
                    raw_text = response.text.strip()
                    if raw_text.startswith("```json"):
                        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                    elif raw_text.startswith("```"):
                        raw_text = raw_text.replace("```", "").strip()
                        
                    data = json.loads(raw_text)
                    
                    # შედეგების ჩვენება საიტზე
                    st.success(f"🕵️‍♂️ ნაპოვნია პოტენციური კლიენტები სფეროში: {business_type} ({city})")
                    
                    for biz in data:
                        st.markdown(f"""
                            <div class="report-card">
                                <h3>🏢 {biz['სახელი']}</h3>
                                <p>📞 <b>ტელეფონი:</b> {biz['ტელეფონი']}</p>
                                <p>❌ <b>მთავარი ხარვეზი:</b> <span style="color: #e03131;">{biz['ხარვეზი']}</span></p>
                                <p>📈 <b>ზრდის პოტენციალი:</b> {biz['პოტენციალი']}</p>
                                <div style="background-color: #edf2ff; padding: 10px; border-radius: 6px; margin-top: 10px;">
                                    💼 <b>საუკეთესო სტრატეგია შენთვის (რა მიჰყიდო):</b> {biz['შეთავაზება']}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"დაფიქსირდა შეცდომა Gemini API-სთან კავშირისას: {e}")
