import streamlit as st 
import joblib
import pandas as pd
import base64
import time
import sqlite3
import hashlib

# Load model
model = joblib.load("best_lgbm_model.pkl")

# Database Functions
def create_usertable():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')
    conn.commit()
    conn.close()

def add_userdata(username, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    return hash_password(password) == hashed


# Sidebar Navigation
def sidebar():
    st.sidebar.title("More")
    page = st.sidebar.radio("Go to", ["Home", "About", "Contact", "Logout"])
    return page

# Set background
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

    background_style = f"""
    <style>
    .stApp {{
        background: url("data:image/jpg;base64,{encoded_string}") no-repeat center center fixed;
        background-size: cover;
    }}

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
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Main App Logic
def main():
    create_usertable()
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if not st.session_state.logged_in:
        if st.session_state.page == "login":
            login_page()
        elif st.session_state.page == "register":
            register_page()
    else:
        if st.session_state.page == "predict":
            prediction()
            st.markdown("""
    <style>
    label {
        color: white !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

          
        elif st.session_state.page == "result":
            result_page()
        else:
            page = sidebar()
            if page == "Home":
                home()
            elif page == "About":
                about()
            elif page == "Contact":
                contact()
            elif page == "Logout":
                st.session_state.logged_in = False
                st.session_state.page = "login"
                st.success("Logged out successfully!")
                st.rerun()


# Login Page
def login_page():
    st.sidebar.title("More")
    page = st.sidebar.radio("Go to", ["Home", "About", "Contact"])

    if page == "About":
        about()
        return
    elif page == "Contact":
        contact()
        return

    st.markdown("<h2 style='text-align:center;'>Login</h2>", unsafe_allow_html=True)
    with st.container():
        st.write("---")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            login_submit = st.form_submit_button("Login")
            if login_submit:
                hashed_pswd = hash_password(password)
                result = login_user(username, hashed_pswd)
                if result:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Incorrect Username/Password")
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("Don't have an account?")
        if st.button("Register Here"):
            st.session_state.page = "register"
            st.rerun()

# Register Page
def register_page():
    st.markdown("<h2 style='text-align:center;'>Register</h2>", unsafe_allow_html=True)
    with st.container():
        st.write("---")
        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type='password')
            confirm_password = st.text_input("Confirm Password", type='password')
            register_submit = st.form_submit_button("Register")

            if register_submit:
                if not new_username or not new_password or not confirm_password:
                    st.warning("Please fill out all fields!")
                elif new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    hashed_new_pswd = hash_password(new_password)
                    conn = sqlite3.connect('data.db')
                    c = conn.cursor()
                    c.execute('SELECT * FROM userstable WHERE username = ?', (new_username,))
                    existing_user = c.fetchone()
                    conn.close()
                    if existing_user:
                        st.error("Username already exists. Try another.")
                    else:
                        add_userdata(new_username, hashed_new_pswd)
                        st.success("User Registered Successfully! Please Login.")
                        time.sleep(1)
                        st.session_state.page = "login"
                        st.rerun()
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# Home Page
def home():
    set_background("inside_image_compressed.jpg") 
    st.markdown('<h1 style="font-size: 40px;font-weight: bold;font-family: Arial, sans-serif;text-align: center;color: white;margin-top: 10%;">CROP YIELD PREDICTION SYSTEM</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="font-size: 18px;font-family: Arial, sans-serif;text-align: center;color: white;margin-bottom: 20px;">Empowering farmers with data-driven insights for better harvests</h3>', unsafe_allow_html=True)
    st.markdown('<div class="continue-button">', unsafe_allow_html=True)
    if st.button("Continue", key="continue_button"):
        st.session_state.page = "predict"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Prediction Page
def prediction():
    set_background("inside_image_compressed.jpg")
    st.markdown('<h1 style="font-size: 40px; color:white; text-align: center;">CROP YIELD PREDICTION</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-size: 14px; color:white;">Enter the required details for an accurate yield prediction.</h2>',unsafe_allow_html=True)
    st.markdown('<h3 style="font-size: 20px; color:white;">Agronomic Factors</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        Rainfall_mm = st.number_input("Rainfall (mm)", min_value=0, max_value=1000)
        Temperature_Celsius = st.number_input("Temperature (°C)", min_value=10.0, max_value=40.0)
    with col2:
        Days_to_Harvest = st.number_input("Days to Harvest", min_value=30, max_value=150)

    st.markdown('<h4 style="font-size: 20px; color:white;">Other Details</h4>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        Fertilizer_Used = st.selectbox("Fertilizer Used", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        Irrigation_Used = st.selectbox("Irrigation Used", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    with col4:
        crop_options = {0: "Cotton", 1: "Rice", 2: "Barley", 3: "Soybean", 4: "Wheat", 5: "Maize"}
        soil_options = {0: "Sandy", 1: "Clay", 2: "Loam", 3: "Silt", 4: "Peaty", 5: "Chalky"}
        Crop = st.selectbox("Crop Type", options=crop_options.keys(), format_func=lambda x: crop_options[x])
        Soil_Type = st.selectbox("Soil Type", options=soil_options.keys(), format_func=lambda x: soil_options[x])

    user_input = pd.DataFrame([[Rainfall_mm, Fertilizer_Used, Irrigation_Used, Temperature_Celsius, Days_to_Harvest, Crop, Soil_Type]],
                              columns=["Rainfall_mm", "Fertilizer_Used", "Irrigation_Used", "Temperature_Celsius", "Days_to_Harvest", "Crop", "Soil_Type"])

    st.markdown('<h5 style="font-size: 20px; color:white;">User Input Details</h5>', unsafe_allow_html=True)
    user_input_display = user_input.copy()
    user_input_display["Crop"] = user_input_display["Crop"].map(crop_options)
    user_input_display["Soil_Type"] = user_input_display["Soil_Type"].map(soil_options)
    binary_mapping = {0: "No", 1: "Yes"}
    user_input_display["Irrigation_Used"] = user_input_display["Irrigation_Used"].map(binary_mapping)
    user_input_display["Fertilizer_Used"] = user_input_display["Fertilizer_Used"].map(binary_mapping)
    st.write(user_input_display)

    if st.button("Predict", key="predict_button"):
        prediction_val = model.predict(user_input)[0]
        st.session_state["prediction"] = prediction_val  
        st.session_state.page = "result"
        st.rerun()

    if st.button("Back to Home", key="back_home"):
        st.session_state.page = "Home"
        st.rerun()

def result_page():
    st.markdown('<h1 style="font-size: 25px; color:black; text-align: center;">PREDICTED CROP YIELD</h1>', unsafe_allow_html=True)

    if "prediction" not in st.session_state:
        st.error("No prediction available. Please go back and enter input values.")
        if st.button("Back to Prediction"):
            st.session_state.page = "predict"
            st.rerun()
        st.stop() 

    prediction_val = st.session_state["prediction"]
    st.metric(label="Predicted Yield", value=f"{prediction_val:.2f} tons/hectare")

    if prediction_val < 2:
        st.error("Low Yield")
        st.write("**Description:** Yield is significantly below average. Indicates poor crop performance.")
        st.write("**Possible Reasons:**")
        st.write("- Poor soil fertility\n- Inadequate irrigation\n- Improper fertilizer use\n- Pest or disease attacks\n- Lack of modern farming practices")
        st.write("**Recommendations to Improve:**")
        st.write("- **Soil Testing & Fertilization:** Conduct soil tests and apply balanced fertilizers.")
        st.write("- **Crop Rotation:** Implement crop rotation to restore soil nutrients.")
        st.write("- **Irrigation Optimization:** Use drip or sprinkler systems for better water management.")
        st.write("- **Pest & Disease Management:** Adopt Integrated Pest Management (IPM) techniques.")
        st.write("- **Modern Farming Techniques:** Use precision farming tools such as sensors and drones.")

    elif 2 <= prediction_val <= 4:
        st.warning("Moderate Yield")
        st.write("**Description:** Yield is around average but has room for improvement.")
        st.write("**Possible Reasons:**")
        st.write("- Sub-optimal soil conditions\n- Inconsistent irrigation practices\n- Improper use of fertilizers\n- Moderate pest/disease presence")
        st.write("**Recommendations to Improve:**")
        st.write("- **Soil Health Monitoring:** Regularly monitor pH, nutrients, and organic matter.")
        st.write("- **Efficient Fertilizer Usage:** Adopt split fertilizer application techniques.")
        st.write("- **Water Management:** Schedule irrigation based on crop growth stages.")
        st.write("- **Disease Prevention:** Use certified seeds and proper spacing.")
        st.write("- **Training & Awareness:** Attend local agricultural extension workshops.")

    else:
        st.success("High Yield")
        st.write("**Description:** Yield is above average. Indicates optimal crop performance.")
        st.write("**Suggestions to Maintain or Enhance:**")
        st.write("- **Continue Best Practices:** Maintain current fertilization, irrigation, and pest management methods.")
        st.write("- **Adopt Advanced Technologies:** Explore precision agriculture, satellite data, and IoT tools.")
        st.write("- **Sustainable Practices:** Incorporate more organic fertilizers, reduce chemical inputs.")
        st.write("- **Monitor & Document:** Keep records of farming activities to analyze successful patterns.")
        st.write("- **Stay Updated:** Keep learning about the latest agricultural advancements.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back to Prediction"):
            st.session_state.page = "predict"
            st.rerun()
    with col2:
        if st.button("Back to Home"):
            st.session_state.page = "Home"
            st.rerun()

# About Page
def about():
    st.markdown("<h2 style='text-align:center;'>About</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='max-width:650px; margin: 0 auto; border:1px solid #ccc; padding:20px; border-radius:10px; background-color: #f9f9f9;'>
        <p style='font-size:16px; text-align:justify;'>
            Welcome to the Crop Yield Prediction System!<br><br>
            At Crop Yield Prediction System, our mission is to empower farmers and agricultural professionals with data-driven insights to enhance crop productivity. 
            Using advanced machine learning models, we analyze key agronomic factors such as rainfall, temperature, soil type, and irrigation to predict crop yield with high accuracy. 
            Our platform helps farmers make informed decisions about resource allocation, optimizing their agricultural practices for better harvests.<br><br>
            By leveraging technology, we aim to contribute to a more sustainable and efficient farming ecosystem, ensuring food security and economic growth for the agricultural community.
        </p>
    </div>
    """, unsafe_allow_html=True)

#
def contact():
    st.markdown("<h2 style='text-align:center;'>Contact</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style='max-width:650px; margin: 0 auto; border:1px solid #ccc; padding:20px; border-radius:10px; background-color: #f9f9f9;'>
        <p style='font-size:16px; text-align:justify;'>
            Need assistance? If you need any help, guidance, or have any questions regarding our Crop Yield Prediction System, 
            feel free to reach out to us anytime. Our team is here to assist you and ensure you have the best possible experience. 
            Don’t hesitate to contact us — we're happy to help!
        </p>
        <hr style='margin: 10px 0;'>
        <p style='font-size:16px;'>
            <strong>Email:</strong> <a href='mailto:cropyieldprediction2025@gmail.com'>cropyieldprediction2025@gmail.com</a><br>
        </p>
    </div>
    """, unsafe_allow_html=True)



if __name__ == '__main__':
    main()