import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime

RECORDS_FOLDER = "data/records"

def save_history(username, plant_type, disease_name, confidence, summary_text, location="unknown"):
    os.makedirs(RECORDS_FOLDER, exist_ok=True)

    record = {
        "user": username,
        "plant_type": plant_type,
        "disease": disease_name,
        "confidence": round(confidence * 100, 2),
        "summary": summary_text,
        "location": location,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    filename = f"{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(os.path.join(RECORDS_FOLDER, filename), "w") as f:
        json.dump(record, f, indent=4)

def load_records(folder=RECORDS_FOLDER):
    if not os.path.exists(folder):
        return pd.DataFrame()

    records = []
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file)) as f:
                try:
                    records.append(json.load(f))
                except Exception:
                    pass
    return pd.DataFrame(records)

def show_user_history(username):
    df = load_records()
    if df.empty or 'user' not in df.columns:
        st.info("No diagnoses yet.")
        return

    user_df = df[df['user'] == username]
    if user_df.empty:
        st.info("No diagnoses found for this user.")
    else:
        st.subheader("📜 Your Diagnosis History")
        st.dataframe(user_df[["timestamp", "plant_type", "disease", "confidence"]].sort_values("timestamp", ascending=False))

def show_area_statistics():
    df = load_records()
    if df.empty:
        st.info("No statistical data yet.")
        return

    st.subheader("📊 Statistics of Detected Plant Diseases")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔎 Most Common Diseases")
        st.bar_chart(df["disease"].value_counts())

    with col2:
        st.markdown("#### 🪴 Most Affected Plant Types")
        st.bar_chart(df["plant_type"].value_counts())

    if "location" in df.columns:
        st.markdown("#### 📍 Disease by Location")
        st.bar_chart(df["location"].value_counts())