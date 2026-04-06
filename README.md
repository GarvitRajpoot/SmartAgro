# 🌱 SmartAgro — AI Powered Agriculture System

SmartAgro is an intelligent agriculture platform designed to assist farmers and agricultural enthusiasts using Machine Learning and Artificial Intelligence.

It provides smart recommendations, real-time disease detection, and an AI assistant to improve crop productivity and decision-making.

---

## 🚀 Features

### 🌾 Crop Recommendation

* Suggests the most suitable crop based on environmental conditions:

  * Temperature
  * Rainfall
  * Soil pH
  * Soil moisture
  * Humidity
  * Sunlight hours

---

### 📈 Yield Prediction

* Estimates expected crop yield (kg/hectare)
* Uses trained ML models specific to crops

---

### 🩺 Disease Detection (AI Vision)

* Upload an image of a plant/crop
* AI detects:

  * Disease name
  * Short description
  * Prevention steps
* Uses Google Gemini Vision API

---

### 🤖 Smart Chatbot Assistant

* Ask agriculture-related questions
* Get instant AI responses
* Supports both short and detailed explanations

---

## 🏗️ Project Structure

SmartAgro/
│
├── backend/
│   ├── main.py                  # FastAPI backend
│   ├── models/                 # ML models
│   │   ├── crop_recommender.pkl
│   │   └── yield_models/
│   ├── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── input.html
│   ├── result.html
│   ├── disease.html
│   ├── chatbot.html
│   ├── chatbot.js
│   └── assets/
│
├── .gitignore
├── README.md

---

## ⚙️ Tech Stack

### 🔹 Backend

* FastAPI
* Python
* Joblib

### 🔹 Frontend

* HTML
* CSS
* JavaScript

### 🔹 AI / ML

* Scikit-learn
* Google Gemini API (Vision + Chat)

---

## 🧠 System Workflow

### Crop Recommendation Flow

1. User enters farm data
2. Backend processes input
3. ML model predicts best crop
4. Yield model estimates production

---

### Disease Detection Flow

1. User uploads image
2. Image sent to AI model
3. AI analyzes plant condition
4. Returns disease + solution

---

### Chatbot Flow

1. User asks a question
2. Backend sends request to AI
3. AI generates response
4. Response displayed in UI

---

## 🛠️ Installation & Setup

### 1️⃣ Clone Repository

git clone https://github.com/your-username/SmartAgro.git
cd SmartAgro

---

### 2️⃣ Setup Backend

cd backend
pip install -r requirements.txt

---

### 3️⃣ Create Environment File

Create a `.env` file inside backend folder:

GEMINI_API_KEY=your_api_key_here

---

### 4️⃣ Run Backend Server

uvicorn main:app --reload

Server will start at:
http://127.0.0.1:8000

---

### 5️⃣ Run Frontend

Open the file:
frontend/index.html
in your browser

---

## 🔐 Security Notes

* API key is stored in `.env` file
* `.env` is ignored using `.gitignore`
* No sensitive data is exposed to frontend

---

## 📊 Future Enhancements

* 🌍 Multi-language support
* 📱 Mobile application
* ☁️ Cloud deployment
* 🌦️ Weather API integration
* 📊 Advanced analytics dashboard

---

## 📸 Screenshots (Optional)

Add screenshots in a folder:

screenshots/home.png
screenshots/result.png
screenshots/disease.png

---

## 👨‍💻 Author

Garvit Rajpoot

---

## 📜 License

This project is developed for educational and innovation purposes.
