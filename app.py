from flask import Flask, request, jsonify
import os
import time
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure the Google AI SDK
genai.configure(api_key="AIzaSyCNNnU7naa1X1Ko9ACbivyko3rVhU7f-gI")

def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file("C:\\Users\\user\\Desktop\\chatbot\\Flask\\MentAura.docx", mime_type=mime_type)
    return file

def wait_for_files_active(files):
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")

# Initialize the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route('/',methods=['GET'])
def good():
    return jsonify({"message":"Hello World"})


# Define a route for the chatbot
@app.route('/', methods=['POST'])
def chat():
    print('hello')
    data = request.json
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Simulate the chat session
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": "you are a mental health chatbot who use to give solutions to the problems users face Tone and Persona:\nMy tone is friendly, compassionate, and supportive, aimed at making users feel understood and empowered.\nI avoid medical jargon whenever possible and strive to provide clear, actionable advice.\nI’m designed to be a proactive companion, providing reminders and suggestions to help users stay on top of their health. and it must be a friend to the user and it named \"bristo\" an ai companion "}
        ]
    )

    # Send the user message to the model
    response = chat_session.send_message(user_input)

    print(jsonify({"response":response.text}))

    # Return the model's response
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(port=8000, debug=True)




