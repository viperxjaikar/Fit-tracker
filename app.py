from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import plotly.express as px
from datetime import datetime

# 🔥 NEW IMPORTS
from pymongo import MongoClient
import bcrypt

load_dotenv()

# ================== API ==================
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("API Key not found")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# ================== MONGODB ==================
MONGO_URI = "mongodb://127.0.0.1:27017/" 
client = MongoClient(MONGO_URI)

db = client["fittrack"]
users_col = db["users"]
data_col = db["user_data"]

# ================== AUTH ==================
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def register_user(username, password):
    if users_col.find_one({"username": username}):
        return False
    users_col.insert_one({
        "username": username,
        "password": hash_password(password)
    })
    return True

def login_user(username, password):
    user = users_col.find_one({"username": username})
    if not user:
        return False
    return check_password(password, user["password"])

# ================== LOGIN UI ==================
if "user" not in st.session_state:

    st.title("🔐 Login / Register")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(u, p):
                st.session_state.user = u
                st.success("Logged in")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u2 = st.text_input("New Username")
        p2 = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register_user(u2, p2):
                st.success("User created. Login now.")
            else:
                st.error("Username exists")

    st.stop()

# ================== USER DATA ==================
user = st.session_state.user

def get_user_data(username):
    data = data_col.find_one({"username": username})
    if not data:
        return {"history": [], "meals": [], "workouts": []}
    return data

def save_user_data(username, data):
    data_col.update_one(
        {"username": username},
        {"$set": data},
        upsert=True
    )

user_data = get_user_data(user)

if "history" not in st.session_state:
    st.session_state.history = user_data.get("history", [])

if "saved_meals" not in st.session_state:
    st.session_state.saved_meals = user_data.get("meals", [])

if "workouts" not in st.session_state:
    st.session_state.workouts = user_data.get("workouts", [])

def save_all():
    save_user_data(user, {
        "history": st.session_state.history,
        "meals": st.session_state.saved_meals,
        "workouts": st.session_state.workouts
    })

# ================== FUNCTIONS ==================
def calculate_bmi(w,h):
    return w/((h/100)**2)

def categorize_bmi(b):
    if b<18.5:return "underweight","🔵 Underweight"
    elif b<24.9:return "normal","🟢 Normal"
    elif b<29.9:return "overweight","🟠 Overweight"
    else:return "obese","🔴 Obese"

def get_ai(p):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(p)

        # NEW: handle both formats
        if response.text:
            return response.text

        if hasattr(response, "candidates"):
            return response.candidates[0].content.parts[0].text

        return "No response generated"

    except Exception as e:
        return f"Error: {str(e)}"

def extract_meals(plan):
    return plan.split("Workout")[0]

def extract_workout_section(plan):
    if "Workout" not in plan:
        return "No workout section"
    return "Workout" + plan.split("Workout")[1]

# ================== UI ==================
st.set_page_config(layout="wide")
st.sidebar.title(f"👋 {user}")

page = st.sidebar.radio("Navigate",["BMI","Progress","Workouts","Meals","History"])

# ================== BMI ==================
if page=="BMI":

    name=st.text_input("Name")
    age=st.number_input("Age",1,120)
    height=st.number_input("Height",50,250)
    weight=st.number_input("Weight",10.0,300.0)

    if st.button("Calculate"):
        bmi=calculate_bmi(weight,height)
        code,cat=categorize_bmi(bmi)

        st.session_state.data={
            "name":name,
            "age":age,
            "height":height,
            "weight":weight,
            "bmi":bmi,
            "category":cat
        }

        prompt=f"""
        Based on BMI {bmi:.2f}, generate:
        1. Diet plan
        2. Workout plan (day-wise with duration)
        """

        with st.spinner("⚡ Generating your personalized plan..."):
            st.session_state.res=get_ai(prompt)

    if "data" in st.session_state:
        d=st.session_state.data
        st.metric("BMI",round(d["bmi"],2))
        st.write(d["category"])

        res=st.session_state.res
        st.markdown(res)

        c1,c2,c3=st.columns(3)

        if c1.button("Save Meal"):
            st.session_state.saved_meals.insert(0,{
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "meal_plan": extract_meals(res)
            })
            save_all()
            st.success("Saved")
            st.rerun()

        if c2.button("Save History"):
            st.session_state.history.insert(0,{
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **d,
                "recommendations": res
            })
            save_all()
            st.success("Saved")
            st.rerun()

        if c3.button("Log Workout"):
            st.session_state.workouts.insert(0,{
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "plan": extract_workout_section(res)
            })
            save_all()
            st.success("Workout saved")
            st.rerun()

# ================== MEALS ==================
elif page=="Meals":
    for i,m in enumerate(st.session_state.saved_meals):
        st.markdown(f"### 📅 {m['date']}")
        st.markdown(m["meal_plan"])

# ================== WORKOUT ==================
elif page=="Workouts":
    for i,w in enumerate(st.session_state.workouts):

        st.markdown(f"### 📅 {w['date']}")

        if "plan" in w:
            st.markdown(w["plan"])
        else:
            st.write(w)

        st.markdown("---")

# ================== PROGRESS ==================
elif page=="Progress":
    if st.session_state.history:
        df=pd.DataFrame(st.session_state.history)
        st.plotly_chart(px.line(df,x='date',y='bmi'))

# ================== HISTORY ==================
elif page=="History":
    for h in st.session_state.history:
        st.markdown(f"### 📅 {h['date']}")
        st.markdown(h["recommendations"])
        st.markdown("---")