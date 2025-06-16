{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "16d7dce0-e197-4e87-9435-925383c8f311",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-06-16 09:25:27.733 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.734 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.737 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.738 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.738 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.739 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.740 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.741 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.742 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.749 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.750 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.751 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.752 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.755 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.756 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.765 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-06-16 09:25:27.769 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "False"
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import sqlite3\n",
    "\n",
    "def create_table():\n",
    "    conn = sqlite3.connect('mydatabase.db')\n",
    "    cursor = conn.cursor()\n",
    "    cursor.execute('''\n",
    "        CREATE TABLE IF NOT EXISTS info (\n",
    "            id INTEGER PRIMARY KEY AUTOINCREMENT,\n",
    "            Name TEXT NOT NULL,\n",
    "            Date TEXT NOT NULL\n",
    "        )\n",
    "    ''')\n",
    "    conn.commit()\n",
    "    conn.close()\n",
    "\n",
    "def insert_data(df):\n",
    "    conn = sqlite3.connect('mydatabase.db')\n",
    "    df.to_sql('info', conn, if_exists='append', index=False)\n",
    "    conn.commit()\n",
    "    conn.close()\n",
    "\n",
    "def fetch_data():\n",
    "    conn = sqlite3.connect('mydatabase.db')\n",
    "    df = pd.read_sql_query(\"SELECT * FROM info\", conn)\n",
    "    conn.close()\n",
    "    return df\n",
    "\n",
    "def convert_df_to_csv(df):\n",
    "    return df.to_csv(index=False).encode('utf-8')\n",
    "\n",
    "st.title(\"📋 Upload & View Info Table\")\n",
    "\n",
    "create_table()\n",
    "\n",
    "uploaded_file = st.file_uploader(\"Upload CSV or Excel File\", type=['csv', 'xlsx'])\n",
    "\n",
    "if uploaded_file:\n",
    "    try:\n",
    "        if uploaded_file.name.endswith('.csv'):\n",
    "            df = pd.read_csv(uploaded_file)\n",
    "        else:\n",
    "            df = pd.read_excel(uploaded_file)\n",
    "\n",
    "        if 'Name' in df.columns and 'Date' in df.columns:\n",
    "            insert_data(df[['Name', 'Date']])\n",
    "            st.success(\"Data uploaded and inserted into database.\")\n",
    "        else:\n",
    "            st.error(\"Uploaded file must have columns: 'Name' and 'Date'\")\n",
    "    except Exception as e:\n",
    "        st.error(f\"Error reading file: {e}\")\n",
    "\n",
    "st.subheader(\"📄 Current Data in 'info' Table\")\n",
    "data = fetch_data()\n",
    "st.dataframe(data)\n",
    "\n",
    "csv = convert_df_to_csv(data)\n",
    "st.download_button(\n",
    "    label=\"⬇️ Download Data as CSV\",\n",
    "    data=csv,\n",
    "    file_name='info_table.csv',\n",
    "    mime='text/csv'\n",
    ")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "7819e477-5478-4cfa-9e81-cac43f9c7923",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
