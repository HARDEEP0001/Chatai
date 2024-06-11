import os
from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import google.generativeai as genai

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://abc:har@cluster0.7rz7sik.mongodb.net/chatgpt"
mongo = PyMongo(app)

# Set and configure the Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyAVVFwOgc2FYdJY3VVIdAi0Yus5V48l7Jo"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def fetch_gemini_completion(question):
    response = model.generate_content(question)
    return response.text  # Ensure this returns the text content

@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    mychats = list(chats)
    return render_template("index.html", mychats=mychats)

@app.route("/api", methods=["POST"])
def qa():
    question = request.json.get("question")
    chat = mongo.db.chats.find_one({"question": question})
    if chat:
        data = {"result": chat['answer']}
    else:
        completion = fetch_gemini_completion(question)
        response = completion
        mongo.db.chats.insert_one({"question": question, "answer": response})
        data = {"result": response}

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
