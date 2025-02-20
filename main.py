#using params key,value
# from fastapi import FastAPI
# from pydantic import BaseModel
# import google.generativeai as genai
# import psycopg2
# genai.configure(api_key="AIzaSyBAOoaNksSCkM_AquAMIJghmFPHHsiRl_k")
# app = FastAPI()
# # PostgreSQL Connection
# conn = psycopg2.connect(
#     dbname="chatbot_db", 
#     user="postgres", 
#     password="chet1212", 
#     host="localhost", 
#     port="5432"
# )
# cursor = conn.cursor()

# class UserInput(BaseModel):
#     message: str

# @app.post("/chat")
# def chat_with_gemini(prompt):
#     try:
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(prompt)

#         reply = response.text.strip()

#         # Store conversation in PostgreSQL
#         cursor.execute("INSERT INTO conversations (user_input, bot_reply) VALUES (%s, %s)", (prompt, reply))
#         conn.commit()

#         return {"Reply": reply}

#     except Exception as e:
#         raise e

# using body JSON
from fastapi import FastAPI # Creates an API server
from pydantic import BaseModel # Define data structure for requests
import google.generativeai as genai # Google Gemini AI for responses
import psycopg2 # PostgreSQL database connection

# Configure Google Gemini API
genai.configure(api_key="AIzaSyBAOoaNksSCkM_AquAMIJghmFPHHsiRl_k") #checks the key

app = FastAPI() #handle HTTP requests

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="chatbot_db", 
    user="postgres", 
    password="chet1212", 
    host="localhost", 
    port="5432"
)
cursor = conn.cursor()

# Define request model
class UserInput(BaseModel):
    message: str #Ensures requests have a JSON body with a "message" 

@app.post("/chat")
def chat_with_gemini(request: UserInput):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(request.message)  

        reply = response.text.replace("\n", " ")
        # reply = response.text
        cursor.execute(
            "INSERT INTO conversations (user_input, bot_reply) VALUES (%s, %s)", 
            (request.message, reply)
        )
        conn.commit()

        return {"Reply": reply}

    except Exception as e:
        return {"error": str(e)}