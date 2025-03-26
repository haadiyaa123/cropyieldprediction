#  Crop Yield Prediction Web App

##  Overview

This web application predicts **crop yield per hectare** using machine learning techniques. Built with **Streamlit**, it allows users to input farming and environmental parameters to receive data-driven yield predictions. The app also provides **categorized yield insights** (Low, Moderate, High) along with actionable recommendations.

## Features

- ✅ **User Authentication**: Secure login & registration with **SQLite authentication**.
- ✅ **Machine Learning Model**: Uses a **LightGBM model** for accurate predictions.
- ✅ **Interactive UI**: Built with **Streamlit** for a user-friendly experience.
- ✅ **Categorized Results**: Provides detailed insights into Low, Moderate, and High yield predictions.
- ✅ **Background Styling**: Includes a semi-transparent overlay for better content visibility.
- ✅ **Navigation Flow**: Seamless transitions between Home, Prediction, and Result pages.

##  Project Structure

```
📦 crop-yield-prediction
│── 📂 app/               # Web application files
│── 📂 data/              # Raw and processed datasets
│── 📂 models/            # Trained ML models (LightGBM)
│── 📄 requirements.txt   # Python dependencies
│── 📄 README.md          # Project documentation
│── 📄 .gitignore         # Ignore unnecessary files
```

## Installation

To run the application locally, follow these steps:

### 1️⃣ **Clone the Repository**

```sh
git clone https://github.com/your-username/crop-yield-prediction.git
cd crop-yield-prediction
```

### 2️⃣ **Create a Virtual Environment (Optional, Recommended)**

```sh
python -m venv venv
# Activate venv (Windows)
venv\Scripts\activate
# Activate venv (Mac/Linux)
source venv/bin/activate
```

### 3️⃣ **Install Dependencies**

```sh
pip install -r requirements.txt
```

### 4️⃣ **Run the Application**

```sh
streamlit run app/app.py
```

## Machine Learning Model

- **Algorithm Used**: LightGBM
- **Target Variable**: `Yield_tons_per_hectare`
- **Feature Selection**: Uses relevant soil, crop, irrigation, and weather parameters.
- **Performance**: Achieves high accuracy in yield prediction.

## Yield Categories & Insights

- **Low Yield**: Factors affecting poor crop performance & improvement suggestions.
- **Moderate Yield**: Balanced growth insights & potential optimizations.
- **High Yield**: Key success factors & best practices for maximum yield.

## Contributing

Feel free to **fork** this repository, submit **pull requests**, or open **issues** for improvements!

## Contact

For any queries, reach out to **[your-email@example.com](mailto\:hadiyajaleel10@gmail.com)**.

---

🚜 **Empowering farmers with data-driven insights!** 
