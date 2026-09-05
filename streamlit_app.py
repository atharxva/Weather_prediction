import sys
from pathlib import Path
import streamlit as st

# Add project root directory to path
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

from src.predict import predict_by_city

# Page setup
st.set_page_config(
    page_title="Rain Prediction AI",
    page_icon="🌧️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .metric-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 10px;
    }
    .stButton button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🌧️ Rain Prediction AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0aec0;'>Predict whether it will rain tomorrow in any city using live weather metrics & ML.</p>", unsafe_allow_html=True)
st.divider()

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    city_input = st.text_input("Enter City Name", value="London", placeholder="e.g. Mumbai, Tokyo, New York")

with col2:
    st.write("") # Spacing
    st.write("") 
    predict_btn = st.button("Predict 🚀", type="primary")

st.markdown("##### 💡 Quick Suggestions")
quick_cities = ["Mumbai", "Tokyo", "London", "New York", "Sydney", "Paris"]
q_cols = st.columns(len(quick_cities))

selected_quick_city = None
for idx, q_city in enumerate(quick_cities):
    with q_cols[idx]:
        if st.button(q_city, key=f"quick_{q_city}"):
            selected_quick_city = q_city

city_to_predict = selected_quick_city if selected_quick_city else city_input

if predict_btn or selected_quick_city:
    if not city_to_predict.strip():
        st.error("Please enter a valid city name.")
    else:
        with st.spinner(f"Fetching live weather & running prediction for **{city_to_predict}**..."):
            try:
                res = predict_by_city(city_to_predict)
                
                st.success(f"Forecast loaded for **{res['city']}** ({res['date']})")
                
                m1, m2 = st.columns(2)
                
                with m1:
                    rain = res['rain_tomorrow']
                    icon = "🌧️ YES" if rain == "YES" else "☀️ NO"
                    st.metric(label="Will it Rain Tomorrow?", value=icon)
                    
                with m2:
                    st.metric(label="Rain Probability", value=res['rain_probability'])
                
                if res['rain_tomorrow'] == "YES":
                    st.warning("⚠️ **High chance of rain tomorrow.** Don't forget to carry an umbrella!")
                else:
                    st.info("☀️ **Low chance of rain tomorrow.** Enjoy the clear weather!")
                    
            except ValueError as ve:
                st.error(f"❌ {str(ve)}")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

st.divider()
st.caption("Powered by Open-Meteo API & Scikit-Learn ML Model")
