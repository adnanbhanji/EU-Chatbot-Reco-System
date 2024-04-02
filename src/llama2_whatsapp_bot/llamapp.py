from langchain_community.llms import Replicate  
from flask import Flask, request
import os
import requests

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
    ('finish', "Thank you for providing the information, you can continue with any doubt you have.")
    # Add more questions as needed
]

# Define the questions dictionary for easy lookup
questions_dict = {q[0]: q[1] for q in questions}

# Define user_states to keep track of the current state of the conversation
user_states = {}

# Define the state machine transitions
state_transitions = {
    'start': 'farm_name',
    'farm_name': 'location',
    'location': 'farm_area',
    'farm_area': 'finish',
    'finish': None  # End of the conversation
}

def get_next_question(current_state):
    return state_transitions.get(current_state)

@app.route("/")
def hello_llama():
    return "<p>Hello Llama 2</p>"

@app.route('/msgrcvd', methods=['POST', 'GET'])
def msgrcvd():
    message = request.args.get('message')
    if not message:
        return "Message is required.", 400

    destination_number = "34654431185"  # Replace with the recipient's WhatsApp ID

    # Check if the message starts with "start report" to initiate the report flow
    if message.lower() == 'start report':
        # Start the conversation by asking the first question
        user_states[destination_number] = 'start'  # Initialize state
        next_question_key = get_next_question(user_states[destination_number])
        return ask_question((next_question_key, questions_dict[next_question_key]), destination_number)

    # Check if the user is currently in the process of answering questions
    if destination_number in user_states:
        current_state = user_states[destination_number]
        next_state = get_next_question(current_state)
        if next_state:
            # Process the answer and ask the next question
            return process_answer(message, current_state, destination_number)
        else:
            # If there's no next state, the conversation is assumed to be complete
            user_states.pop(destination_number)
            # You can also add a message to indicate the conversation/report is complete.
            return "Report completed."
    else:
        # If the user is not in the middle of answering questions, use LLaMA for the response
        try:
            # Invoke LLaMA model to get a response
            answer = llm.invoke(message)
            print("Message received:", message)
            print("Response generated:", answer)

            # Use the obtained 'answer' to send the WhatsApp message
            response_status = client.send_text_message(answer, destination_number)
            if response_status != 200:
                print(f"Failed to send WhatsApp message: HTTP {response_status}")
                return f"Failed to send WhatsApp message: HTTP {response_status}", 500
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return f"Error processing message: {str(e)}", 500

        return message + "<p/>" + answer


def ask_question(question, destination_number):
    # Send the question
    response_status = client.send_text_message(question[1], destination_number)
    if response_status != 200:
        print(f"Failed to send WhatsApp message: HTTP {response_status}")
        return f"Failed to send WhatsApp message: HTTP {response_status}", 500

    # Update user_states to keep track of the current state
    user_states[destination_number] = question[0]
    return "Asking question: " + question[1]

def process_answer(answer, current_state, destination_number):
    # Process the user's answer
    next_question = get_next_question(current_state)
    if next_question:
        user_states[destination_number] = next_question
        return ask_question((next_question, questions_dict[next_question]), destination_number)
    else:
        user_states.pop(destination_number)  # Remove the user state
        return "Report completed."

if __name__ == "__main__":
    app.run(debug=True)
