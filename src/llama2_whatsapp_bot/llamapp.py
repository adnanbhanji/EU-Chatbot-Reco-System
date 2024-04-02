from langchain_community.llms import Replicate  
from flask import Flask
from flask import request
import os
import requests
import json

class WhatsAppClient:
    API_URL = "https://graph.facebook.com/v18.0/"
    WHATSAPP_API_TOKEN = ""
    WHATSAPP_CLOUD_NUMBER_ID = ""  # Remove /messages from here

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {self.WHATSAPP_API_TOKEN}",
            "Content-Type": "application/json",
        }
        # Correctly initialize the API URL
        self.API_URL = f"{self.API_URL}{self.WHATSAPP_CLOUD_NUMBER_ID}/messages"

    def send_text_message(self, message, phone_number):
        payload = {
            "messaging_product": 'whatsapp',
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        # Use self.API_URL directly since it already includes /messages
        response = requests.post(self.API_URL, json=payload, headers=self.headers)
        if response.status_code != 200:
            print("Failed to send message:", response.text)
            return response.status_code
        return response.status_code

os.environ["REPLICATE_API_TOKEN"] = ""    
llama2_13b_chat = "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d"

llm = Replicate(
    model=llama2_13b_chat,
    model_kwargs={"temperature": 0.01, "top_p": 1, "max_new_tokens":500}
)
client = WhatsAppClient()
app = Flask(__name__)

# Define the questions for the report flow
questions = [
    ('farm_name', "What's the name of your farm?"),
    ('location', "Where is your farm located? Please provide the address or GPS coordinates."),
    ('farm_area', "How large is your farm? Please specify in hectares."),
    # Add more questions as needed
]

# Define the questions dictionary for easy lookup
questions_dict = {q[0]: q[1] for q in questions}

@app.route("/")
def hello_llama():
    return "<p>Hello Llama 2</p>"

@app.route('/msgrcvd', methods=['POST', 'GET'])
def msgrcvd():
    message = request.args.get('message')
    if not message:
        return "Message is required.", 400

    if message.lower() == 'start report':
        return ask_questions()

    try:
        # Invoke LLaMA model to get a response
        answer = llm.invoke(message)
        print("Message received:", message)
        print("Response generated:", answer)

        # Use the obtained 'answer' to send the WhatsApp message
        response_status = client.send_text_message(answer, "34654431185")  # Ensure this is the recipient's WhatsApp ID
        if response_status != 200:
            print(f"Failed to send WhatsApp message: HTTP {response_status}")
            return f"Failed to send WhatsApp message: HTTP {response_status}", 500
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return f"Error processing message: {str(e)}", 500

    return message + "<p/>" + answer

def ask_questions():
    # Send the first question
    response_status = client.send_text_message(questions_dict[questions[0][0]], "34654431185")
    if response_status != 200:
        print(f"Failed to send WhatsApp message: HTTP {response_status}")
        return f"Failed to send WhatsApp message: HTTP {response_status}", 500

    return "Started report. Asking questions."

if __name__ == "__main__":
    app.run(debug=True)
