# FitTrack Pro — AI Fitness & Diet Planner

A fitness planning system that generates personalized diet and workout plans based on user metrics, with authentication and persistent tracking using MongoDB.

---

## 🚀 What This Actually Solves

Fitness planning is:
- Generic (same plans for everyone)  
- Hard to track consistently  
- Not personalized  

This system provides:
- BMI-based personalization  
- AI-generated diet and workout plans  
- Persistent tracking of user progress  

---

## ⚙️ Core Features

### User Management
- Login / Register system  
- User-specific data storage  

### Health Analysis
- BMI calculation with category classification  
- Input: age, height, weight  

### AI Recommendations
- Diet plan generation  
- Workout plan generation with duration  

### Tracking System
- Save meals  
- Log workouts  
- View history  

### Data Persistence
- MongoDB storage for user data  

---

## 🏗️ System Flow

User Input → BMI Calculation → AI API → Plan Generation → MongoDB Storage → UI Display

---

## 📁 Project Structure

FitTrack-Pro/  
├── app.py              # Streamlit app  
├── requirements.txt  
├── README.md  
├── .env                # API keys  
└── database/ (MongoDB)

---

## 🛠️ Tech Stack

Frontend / UI:
- Streamlit  

Backend Logic:
- Python  

Database:
- MongoDB  

AI Integration:
- Google Gemini API  

---

## 🚀 Setup

git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git  
cd YOUR_REPO  

pip install -r requirements.txt  

# Add API key  
Create .env:
GOOGLE_API_KEY=your_api_key  

# Start MongoDB  
mongod  

# Run app  
streamlit run app.py  

---

## 🧪 How to Use

1. Register / Login  
2. Enter health details  
3. Generate plans  
4. Save meals / workouts  
5. Track history  


## 💡 Future Improvements

- Add JWT authentication  
- Deploy with MongoDB Atlas  
- Add calorie tracking and goals  
- Improve UI and interaction  
- Add custom backend (Flask/Node)  

---

## 📌 Why This Project Matters

This project demonstrates:
- Integration of AI APIs into applications  
- User-specific data management  
- CRUD operations with MongoDB  
- Building interactive ML-powered apps  

---

## 👤 Author

Gonuguntala Jaikar Ramu  
https://github.com/viperxjaikar  

---

## ⭐ Star if useful
