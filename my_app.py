import streamlit as st
import pandas as pd
import sqlite3
import socket
import os
from io import BytesIO

# Function to get local IP
def get_ip_address():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unavailable"

# Database setup
conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    email TEXT,
    ip_address TEXT
)
""")
conn.commit()

st.title("📊 Data Uploader with Email & IP Logging")

# Email input
email = st.text_input("Enter your Email")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=['csv', 'xlsx'])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")
    st.write("Preview:")
    st.dataframe(df)

    # Button to insert into DB
    if st.button("Add to Database"):
        ip = get_ip_address()
        if 'Name' not in df.columns or 'Date' not in df.columns:
            st.error("File must contain 'Name' and 'Date' columns.")
        else:
            for _, row in df.iterrows():
                cursor.execute("INSERT INTO info (name, date, email, ip_address) VALUES (?, ?, ?, ?)",
                               (row['Name'], str(row['Date']), email, ip))
            conn.commit()
            st.success("Data added to database!")

# Show data in DB
st.subheader("📋 Current Database")
df_db = pd.read_sql("SELECT * FROM info", conn)
st.dataframe(df_db)

# Download button
csv = df_db.to_csv(index=False).encode('utf-8')
st.download_button("Download Data as CSV", data=csv, file_name='info_data.csv', mime='text/csv')
