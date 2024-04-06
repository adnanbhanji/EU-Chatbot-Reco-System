from langchain_community.llms import Replicate  
from flask import Flask, request
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class WhatsAppClient:
    API_URL = "https://graph.facebook.com/v18.0/"
    WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")
    WHATSAPP_CLOUD_NUMBER_ID = os.getenv("WHATSAPP_CLOUD_NUMBER_ID")  
    
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

os.environ["REPLICATE_API_TOKEN"] = os.getenv("REPLICATE_API_TOKEN")
llama2_13b_chat = "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d"

llm = Replicate(
    model=llama2_13b_chat,
    model_kwargs={"temperature": 0.01, "top_p": 1, "max_new_tokens":500}
)
client = WhatsAppClient()
app = Flask(__name__)

@app.route("/")
def hello_llama():
    return "<p>Hello Llama 2</p>"

@app.route('/msgrcvd', methods=['POST', 'GET'])
def msgrcvd():
    message = request.args.get('message')
    if not message:
        return "Message is required.", 400

    destination_number = "34654431185"  # This should be dynamically determined based on the incoming request

    # Handle all interactions through LLaMA, using a script for context.
    return handle_llama_interaction(message, destination_number)


# This dictionary holds the conversation history for each user
conversation_history = {}

def handle_llama_interaction(user_message, destination_number):
    script = ("You are a helpful assistant knowledgeable about farming practices, "
              "designed to collect detailed reports from farmers about their farm conditions. "
              "Please ensure you collect accurate information on the farm's name, farm name, location, size, farm's total methane emissions in kg CO2-eq?,"
              "electricity consumption, date of declaration and any issues they're facing.")
    
    # Retrieve the existing conversation history
    history = conversation_history.get(destination_number, [])

    # Add the system message and the user's latest message to the history
    if not history:
        history.append({"role": "system", "content": script})
    history.append({"role": "user", "content": user_message})
    
    try:
        # Invoke the LLaMA model to get a response, passing 'input' as expected
        response = llm.invoke(input=[msg for msg in history])
        # Assuming 'response' contains the response text directly
        assistant_message = response if isinstance(response, str) else "Sorry, I couldn't generate a response."

        # Update the conversation history with the assistant's response
        conversation_history[destination_number] = history + [{"role": "assistant", "content": assistant_message}]

        # Send the LLaMA's reply back to the user
        response_status = client.send_text_message(assistant_message, destination_number)
        if response_status != 200:
            print(f"Failed to send WhatsApp message: HTTP {response_status}")
            return f"Failed to send WhatsApp message: HTTP {response_status}", 500
    except Exception as e:
        print(f"Error processing message with LLaMA: {str(e)}")
        return f"Error processing message with LLaMA: {str(e)}", 500

    return assistant_message


if __name__ == "__main__":
    app.run(debug=True)
