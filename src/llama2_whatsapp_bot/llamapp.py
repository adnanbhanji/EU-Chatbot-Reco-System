from langchain_community.llms import Replicate  
from flask import Flask, request
import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pdfdesign import generate_pdf
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

# Define the questions for the report flow
questions = [
    ('farm_name', "What's the name of your farm?"),
    ('owner_name', "What is your name?"),
    ('location', "Where is your farm located? Please provide the address or GPS coordinates."),
    ('farm_area', "How large is your farm? Please specify in hectares."),
    ('num_cows', "How many dairy cows are on your farm?"),
    ('methane_emissions', "What are the farm's total methane emissions in kg CO2-eq?"),
    ('methane_calculation', "How were these methane emissions calculated? Please specify the method."),
    ('electricity_consumption', "How much electricity does your farm consume in kWh?"),
    ('fuel_consumption', "How much fuel does your farm consume? Please specify in L/m3."),
    ('fuel_type', "What type of fuel does your farm use?"),
    ('declaration_date', "Please provide the date of this declaration."),
    ('finish', "Thank you for providing the information. You can continue with any doubt you have."),
]
# Define user_states to keep track of the current state of the conversation
user_states = {}

# Initialize user_interactions to track interruptions with questions
user_interactions = {}

# Define the questions dictionary for easy lookup
questions_dict = {q[0]: q[1] for q in questions}

user_responses = {}


# Define the state machine transitions
state_transitions = {
    'start': 'farm_name',
    'farm_name': 'owner_name',
    'owner_name': 'location',
    'location': 'farm_area',
    'farm_area': 'num_cows',
    'num_cows': 'methane_emissions',
    'methane_emissions': 'methane_calculation',
    'methane_calculation': 'electricity_consumption',
    'electricity_consumption': 'fuel_consumption',
    'fuel_consumption': 'fuel_type',
    'fuel_type': 'declaration_date',
    'declaration_date': 'finish',
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

    # Handle interruption with a direct question
    if message.endswith("?"):
        # Indicate that the user is asking an interruption question
        user_interactions[destination_number] = 'question'
        return handle_llama_interaction(message, destination_number)
    elif message.lower() == 'solved' and user_interactions.get(destination_number) == 'question':
        # Clear the interruption state
        user_interactions.pop(destination_number)
        # If 'solved' is received, repeat the current question instead of moving to the next
        if destination_number in user_states:
            current_state = user_states[destination_number]
            if current_state:
                # Repeat the same question
                question = questions_dict.get(current_state, "Could not find the previous question.")
                return ask_question((current_state, question), destination_number)
            else:
                return "There seems to be an error. Please start your report by typing 'start report'."

    # Check if the message starts with "start report" to initiate the report flow
    if message.lower() == 'start report':
        user_states[destination_number] = 'start'
        next_question_key = get_next_question(user_states[destination_number])
        return ask_question((next_question_key, questions_dict[next_question_key]), destination_number)

    # Check if the user is currently in the process of answering questions
    if destination_number in user_states:
        current_state = user_states[destination_number]
        next_state = get_next_question(current_state)
        if next_state:
            return process_answer(message, current_state, destination_number)
        else:
            user_states.pop(destination_number)  # Conversation complete
            return "Report completed."
    else:
        return "Please start your report by typing 'start report'."

def handle_llama_interaction(message, destination_number):
    try:
        # Directly use the response from the LLaMA model as the answer
        answer = llm.invoke(input=message)  # Assuming this directly returns the text response

        print("Question received:", message)
        print("LLaMA response:", answer)

        # Send the LLaMA response back to the user
        response_status = client.send_text_message(answer, destination_number)
        if response_status != 200:
            print(f"Failed to send WhatsApp message: HTTP {response_status}")
            return f"Failed to send WhatsApp message: HTTP {response_status}", 500
    except Exception as e:
        print(f"Error processing question: {str(e)}")
        return f"Error processing question: {str(e)}", 500

    return "Question answered: " + answer


def ask_question(question, destination_number):
    # Send the question
    response_status = client.send_text_message(question[1], destination_number)
    if response_status != 200:
        print(f"Failed to send WhatsApp message: HTTP {response_status}")
        return f"Failed to send WhatsApp message: HTTP {response_status}", 500

    # Update user_states to keep track of the current state
    user_states[destination_number] = question[0]
    return "Asking question: " + question[1]

# Adjustments in the prepare_summary function to ensure all variables are correctly included
def prepare_summary(destination_number):
    responses = user_responses.get(destination_number, {})

    # Format the responses to match the expected structure by generate_pdf
    # Assuming `generate_pdf` expects a flat dictionary with specific keys
    formatted_responses = {
        'farm_name': responses.get('farm_name', 'Not provided'),
        'owner_name': responses.get('owner_name', 'Not provided'),
        'location': responses.get('location', 'Not provided'),
        'farm_area': responses.get('farm_area', 'Not provided'),
        'num_cows': responses.get('num_cows', 'Not provided'),
        'methane_emissions': responses.get('methane_emissions', 'Not provided'),
        'methane_calculation': responses.get('methane_calculation', 'Not provided'),
        'electricity_consumption': responses.get('electricity_consumption', 'Not provided'),
        'fuel_consumption': responses.get('fuel_consumption', 'Not provided'),
        'fuel_type': responses.get('fuel_type', 'Not provided'),
        'declaration_date': responses.get('declaration_date', 'Not provided'),
    }

    fileName = f"Farm_Report_{destination_number}.pdf"
    documentTitle = "Farm Report Summary"

    # Ensure `generate_pdf` is correctly called with the formatted_responses
    generate_pdf(formatted_responses, fileName, documentTitle)

    notification_message = "Your farm report summary has been created. Please check your email or dashboard."
    client.send_text_message(notification_message, destination_number)

    return "Summary PDF generated."
    

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
        # Check if we've reached the 'finish' state to send the thank you message
        if next_question == 'finish':  # Before concluding the conversation
            final_message = questions_dict[next_question]  # Get the final thank you message
            client.send_text_message(final_message, destination_number)
            summary = prepare_summary(destination_number)  # Generate and send the report
            user_states.pop(destination_number, None)  # Cleanup
            user_responses.pop(destination_number, None)  # Cleanup
            return summary
        else:  # If not the final message, ask the next question
            return ask_question((next_question, questions_dict[next_question]), destination_number)
    else:
        # If there's no next question and we somehow missed 'finish', conclude
        user_states.pop(destination_number, None)  # Cleanup
        return "Unexpected end of conversation."


if __name__ == "__main__":
    app.run(debug=True)
