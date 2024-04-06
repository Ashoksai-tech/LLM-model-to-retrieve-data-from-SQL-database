from dotenv import load_dotenv
import streamlit as st
import os
import mysql.connector

import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to retrieve SQL query response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve SQL query
def read_sql_query(sql):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='aashoksai306@',
        database='student_marks'
    )
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return rows

prompt = ['''
 
 

```plaintext
You are an expert in converting English questions to SQL queries!

LO

The SQL database has the name STUDENT and has the following columns: NAME, CLASS, SECTION, and MARKS.

For example:

1. "How many entries of records are present?"
   (The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;)

2. "Tell me all the students studying in the Data Science class?"
   (The SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS="Data Science";)

Please provide English questions as prompts. Ensure that the SQL code generated does not include the word "SQL" and does not begin or end with any special characters.
```

This revised prompt provides clearer instructions and examples for the user and sets expectations for handling incomplete sentences.


''']



# Streamlit app
st.set_page_config(page_title="Retrieve any SQL query")
st.header("App to retrieve SQL Data")

question = st.text_input("Input:", key="input")
submit = st.button("Ask the Question")

if submit:
    response1 = get_gemini_response(question, prompt)
    print(response1)
    st.subheader("The Response is:")
    data = read_sql_query(response1)
    for row in data:
        
        st.write(row)
