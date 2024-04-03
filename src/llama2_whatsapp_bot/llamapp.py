from langchain_community.llms import Replicate  
from flask import Flask, request
import os
import requests

class WhatsAppClient:
    API_URL = "https://graph.facebook.com/v18.0/"
    WHATSAPP_API_TOKEN = "EAAGSJRN7axMBOZCIIjoiR3OyhOZAt0MNodL4LatkBc0oULuq18hAdCIXKJB7NP5h6b34A7s4CoNPV7kOXebNJf0yGogFTLZCjcTuc34qZARdhCBMZA3TGo55ohRUqd2SvxgFdiOubPydZAMajfskDliHBZBEMlWDrUmqLejuazg98AiOnPIulzgUfbitRErw5RdGUScTp0NZBnqcrrrAT0ipnbvVdkwHmPCch9Lg"
    WHATSAPP_CLOUD_NUMBER_ID = "258052860729653"  # Remove /messages from here

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

os.environ["REPLICATE_API_TOKEN"] = "r8_0Ml6wLeCfwCSYLtFXEgRNfHp6L95sCD26WheA"    
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
# Define user_states to keep track of the current state of the conversation
user_states = {}



# Initialize user_interactions to track interruptions with questions
user_interactions = {}

# Define the questions dictionary for easy lookup
questions_dict = {q[0]: q[1] for q in questions}

# Define user_states to keep track of the current state of the conversation
user_states = {}

user_responses = {}


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

    destination_number = "34654431185"  # This should be dynamically determined based on the incoming request

    # Handle all interactions through LLaMA, using a script for context.
    return handle_llama_interaction(message, destination_number)


# This dictionary holds the conversation history for each user
conversation_history = {}

def handle_llama_interaction(user_message, destination_number):
    script = ("You are a helpful assistant knowledgeable about farming practices, "
              "designed to collect detailed reports from farmers about their farm conditions. "
              "Please ensure you collect accurate information on the farm's name, location, size, "
              "and any issues they're facing.")
    
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




def ask_question(question, destination_number):
    # Send the question
    response_status = client.send_text_message(question[1], destination_number)
    if response_status != 200:
        print(f"Failed to send WhatsApp message: HTTP {response_status}")
        return f"Failed to send WhatsApp message: HTTP {response_status}", 500

    # Update user_states to keep track of the current state
    user_states[destination_number] = question[0]
    return "Asking question: " + question[1]

def prepare_summary(destination_number):
    responses = user_responses.get(destination_number, {})
    summary_message = "Thank you for providing the information. Here's what you've shared:\n"
    summary_message += f"Farm Name: {responses.get('farm_name', 'Not provided')}\n"
    summary_message += f"Location: {responses.get('location', 'Not provided')}\n"
    summary_message += f"Farm Area: {responses.get('farm_area', 'Not provided')}\n"
    
    # Send the summary message
    client.send_text_message(summary_message, destination_number)
    return "Summary sent."


def process_answer(answer, current_state, destination_number):
    # Ensure we have a place to store this user's responses
    if destination_number not in user_responses:
        user_responses[destination_number] = {}
    # Store the current answer
    user_responses[destination_number][current_state] = answer

    # Move to the next state/question
    next_question = get_next_question(current_state)
    if next_question:
        user_states[destination_number] = next_question
        if next_question != 'finish':  # If there's a next question that is not the final message
            return ask_question((next_question, questions_dict[next_question]), destination_number)
    # If no more questions or reaching 'finish', prepare summary
    if current_state == 'farm_area' or next_question is None:  # Adjust this condition as needed
        summary = prepare_summary(destination_number)
        user_states.pop(destination_number, None)  # Cleanup
        user_responses.pop(destination_number, None)  # Cleanup
        return summary
    return "Unexpected end of conversation."



if __name__ == "__main__":
    app.run(debug=True)
