from dotenv import load_dotenv

## load all the environment variables
load_dotenv()   

import streamlit as st
import os
import mysql.connector

import google.generativeai as genai

#config the API key
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#function and provide query as response

def get_gemini_response(question,prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0],question])
    return response.text


#function to retrieve sql query
def read_sql_query(sql,db):
    conn = mysql.connector.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.commit()
    cur.close()
    for row in rows:
        print(row)
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

## streamlit app

st.set_page_config(page_title="Retrieve any SQL query")
st.header("App to retrieve sql Data")

question = st.text_input("Input: ",key="input")

submit = st.button("Ask the Question")

if submit:
    response1 = get_gemini_response(question,prompt)
    print(response1)
    data = read_sql_query(response1,'student_marks.db')
    st.subheader("The  Response is")
    for row in data:
        print(row)
        st.header(row)