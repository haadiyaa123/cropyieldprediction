import streamlit as st
import joblib
import numpy as np
import pandas as pd
import base64
import time
import matplotlib.pyplot as plt

# Load the trained model
model = joblib.load("best_lgbm_model.pkl")

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# Function to set background image
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

    background_style = f"""
    <style>
    .stApp {{
        background: url("data:image/jpg;base64,{encoded_string}") no-repeat center center fixed;
        background-size: cover;
    
    .stButton>button {{
        display: block;
        margin: 0 auto;
        background-color: white !important;
        color: black !important;
        font-size: 18px !important;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }}
    .stButton>button:hover {{
        background-color: lightgray;
    }}

    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("More")
if st.sidebar.button("Home"):
    st.session_state.page = "home"
if st.sidebar.button("About"):
    st.session_state.page = "about"
if st.sidebar.button("Contact"):
    st.session_state.page = "contact"

# ========== Home Page ==========
if st.session_state.page == "home":
    set_background("background3.jpg") 

    # Add Title
    st.markdown('<h1 style="font-size: 40px;font-weight: bold;font-family: Arial, sans-serif;text-align: center;color: white;margin-top: 20%;">CROP YIELD PREDICTION SYSTEM</h1>', unsafe_allow_html=True)

    # Add Subtitle
    st.markdown('<h3 style="font-size: 18px;font-family: Arial, sans-serif;text-align: center;color: white;margin-bottom: 30px;">Empowering farmers with data-driven insights for better harvests</h3>', unsafe_allow_html=True)

    st.markdown('<div class="continue-button">', unsafe_allow_html=True)
    if st.button("Continue", key="continue_button"):
        st.session_state.page = "predict"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ========== Prediction Page ==========
elif st.session_state.page == "predict":
    set_background("inside image.jpg") 

    st.markdown('<h1 style="font-size: 40px; color:brown; text-align: center;">CROP YIELD PREDICTION</h1>', unsafe_allow_html=True)
    st.write("Enter the required details for an accurate yield prediction.")

    # Agronomic Factors Section
    st.markdown('<h2 style="font-size: 20px; color:brown;">Agronomic Factors</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        Rainfall_mm = st.number_input("Rainfall (mm)", min_value=0, max_value=1000)
        Temperature_Celsius = st.number_input("Temperature (°C)", min_value=10.0, max_value=50.0)
    with col2:
        Days_to_Harvest = st.number_input("Days to Harvest", min_value=30, max_value=150)

    # Other Details Section
    st.markdown('<h4 style="font-size: 20px; color:brown;">Other Details</h4>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        Fertilizer_Used = st.selectbox("Fertilizer Used", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        Irrigation_Used = st.selectbox("Irrigation Used", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    with col4:
        crop_options = {0: "Cotton", 1: "Rice", 2: "Barley", 3: "Soybean", 4: "Wheat", 5: "Maize"}
        soil_options = {0: "Sandy", 1: "Clay", 2: "Loam", 3: "Silt", 4: "Peaty", 5: "Chalky"}
        Crop = st.selectbox("Crop Type", options=crop_options.keys(), format_func=lambda x: crop_options[x])
        Soil_Type = st.selectbox("Soil Type", options=soil_options.keys(), format_func=lambda x: soil_options[x])

    # Convert inputs to DataFrame
    user_input = pd.DataFrame([[Rainfall_mm, Fertilizer_Used, Irrigation_Used, Temperature_Celsius, Days_to_Harvest, Crop, Soil_Type]],
                              columns=["Rainfall_mm", "Fertilizer_Used", "Irrigation_Used", "Temperature_Celsius", "Days_to_Harvest", "Crop", "Soil_Type"])

    st.markdown('<h4 style="font-size: 20px; color:brown;">User Input Details</h4>', unsafe_allow_html=True)
    user_input_display = user_input.copy()
    user_input_display["Crop"] = user_input_display["Crop"].map(crop_options)
    user_input_display["Soil_Type"] = user_input_display["Soil_Type"].map(soil_options)

    binary_mapping = {0: "No", 1: "Yes"}
    user_input_display["Irrigation_Used"] = user_input_display["Irrigation_Used"].map(binary_mapping)
    user_input_display["Fertilizer_Used"] = user_input_display["Fertilizer_Used"].map(binary_mapping)

    st.write(user_input_display)

    if st.button("Predict", key="predict_button"):
        with st.spinner('Analyzing your input...'):
            time.sleep(2) 
        prediction = model.predict(user_input)
        st.success("✅ Prediction Complete!")
        st.metric(label="Predicted Yield", value=f"{prediction[0]:.2f} tons/hectare")

        if prediction[0] < 2:
            st.warning("⚠️ Low Yield! Consider using better irrigation and fertilizers.")
        elif 2 <= prediction[0] <= 5:
            st.info("✅ Moderate Yield. Optimize fertilizer usage for better results.")
        else:
            st.success("🎉 High Yield! Your farming conditions are great!")

# ========== About Us Page ==========
elif st.session_state.page == "about":
    st.title("About")
    st.write("""Welcome to the Crop Yield Prediction System!  
        At Crop Yield Prediction System, our mission is to empower farmers and agricultural professionals with data-driven insights to enhance crop productivity. Using advanced machine learning models, we analyze key agronomic factors such as rainfall, temperature, soil type, and irrigation to predict crop yield with high accuracy. Our platform helps farmers make informed decisions about resource allocation, optimizing their agricultural practices for better harvests. By leveraging technology, we aim to contribute to a more sustainable and efficient farming ecosystem, ensuring food security and economic growth for the agricultural community.""")

# ========== Contact Page ==========
elif st.session_state.page == "contact":
    st.title("Contact")
    st.write("Email: support@cropyieldapp.com")
    st.write("Phone: +91 9876543210")        



