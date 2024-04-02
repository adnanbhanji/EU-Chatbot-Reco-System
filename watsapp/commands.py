import requests, json
from   requests.auth import HTTPBasicAuth
from   config import *
import openai
import logging
from openai.error import RateLimitError
from config import vonage_sandbox_number, vonage_authorization_header, endpoint_vonage_message_send
from datetime import datetime
from toPDF import create_pdf_from_string


# Configuration and initial setup
from config import *
logging.basicConfig(format='%(message)s', level=logging.INFO)

user_info = {}
user_states = {}

# Define the questions for the report flow
questions = [
    ('farm_name', "What's the name of your farm?"),
    ('location', "Where is your farm located? Please provide the address or GPS coordinates."),
    ('farm_area', "How large is your farm? Please specify in hectares."),
    # Add more questions as needed
]

# Define the questions dictionary for easy lookup
questions_dict = {q[0]: q[1] for q in questions}

def help(req_data):
    msg = "Ask me anything..."
    logging.info(msg)
    return msg

def is_valid_name(name):
    return name.replace(' ', '').isalpha()

def is_valid_number(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def is_question(text):
    return text.strip().endswith('?')


def process_message(req_data):
    destination_number = req_data['from']
    message = req_data['text'].strip()

    # Check if the user is asking a question to ChatGPT
    if message.endswith('?'):
        response = chatbot(req_data, destination_number)  # Get response from ChatGPT
        send_whatsapp_msg(destination_number, response)
    elif message.lower() == 'solved':
        # Resume to the last question of the report if "solved" is input
        last_question_key = user_states.get(destination_number, None)
        if last_question_key:
            send_whatsapp_msg(destination_number, questions_dict[last_question_key])
        else:
            send_whatsapp_msg(destination_number, "You can start the report by typing 'start report'.")
    elif message.lower() == 'start report':
        user_info[destination_number] = {}
        user_states[destination_number] = questions[0][0]  # Start with the first question
        send_whatsapp_msg(destination_number, questions_dict[questions[0][0]])
    else:
        # Continue with the report filling process
        if destination_number in user_states:
            handle_response(destination_number, message)
        else:
            send_whatsapp_msg(destination_number, "Please start the report by typing 'start report'.")

def handle_response(destination_number, message):
    current_question_index = questions.index((user_states[destination_number], questions_dict[user_states[destination_number]]))
    
    if not is_valid_number(message) and user_states[destination_number] == 'farm_area':
        send_whatsapp_msg(destination_number, "Please enter a valid number for the farm area.")
    elif not is_valid_name(message) and user_states[destination_number] == 'farm_name':
        send_whatsapp_msg(destination_number, "Please enter a valid name for your farm.")
    else:
        user_info[destination_number][user_states[destination_number]] = message
        next_question_index = current_question_index + 1
        if next_question_index < len(questions):
            next_question_key = questions[next_question_index][0]
            user_states[destination_number] = next_question_key
            send_whatsapp_msg(destination_number, questions_dict[next_question_key])
        else:
            generate_and_send_report(destination_number)

            

def generate_and_send_report(destination_number):
    report_content = create_report_content(user_info[destination_number])
    pdf_filename = f"{destination_number}_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    create_pdf_from_string(report_content, pdf_filename)
    # Send the PDF report or provide a download link
    send_whatsapp_msg(destination_number, "Your report has been generated. Please download it from [link].")
    # Clean up after sending the report
    user_info.pop(destination_number, None)
    user_states.pop(destination_number, None)
    
def create_report_content(user_responses):
    content = "Farm Report\n\n"
    for key, answer in user_responses.items():
        content += f"{key.replace('_', ' ').capitalize()}: {answer}\n"
    return content



def hello_vonage_ai(req_data):
    recipient = req_data['from']['number']
    url = f"{endpoint_vonage_ai}/init"
    headers = {'X-Vgai-Key': vonage_ai_key}
    payload = '{"agent_id" : "' + vonage_ai_agent_id + '"}'
    response = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(response.text)
    session_data = {recipient: resp_data['session_id']}
    user_sessions.update(session_data)
    url = f"{endpoint_vonage_ai}/step"
    headers = {'X-Vgai-Key': vonage_ai_key}
    payload = '{"session_id" : "' + user_sessions[recipient] + '"}'
    response = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(response.text)
    msg = resp_data['flow_path'][1]['message']['text'] + "\n"
    msg = msg + resp_data['flow_path'][2]['message']['text']
    logging.info(f"recipient: {recipient} triggered Vonage AI Stock advisor")
    logging.info(f"{msg}")
    return msg




def get_advice_vonage_ai(req_data):
    recipient = req_data['from']['number']
    symbol = str(req_data['message']['content']['text']).upper().strip().split()[-1]
    url = f"{endpoint_vonage_ai}/step"
    headers = {'X-Vgai-Key': vonage_ai_key}
    payload = '{"session_id" : "' + user_sessions[recipient] + '",' \
                                                               '"user_input":"' + symbol + '"}'
    response = requests.request("POST", url, headers=headers, data=payload)
    resp_data = json.loads(response.text)
    msg = resp_data['flow_path'][1]['message']['text'] + "\n"
    msg = msg + json.loads(resp_data['flow_path'][2]['message']['text'])['advice']
    logging.info(f"{msg}")
    return msg


def send_msg(channel, recipient, msg):
    if channel == "whatsapp":
        send_whatsapp_msg(recipient, msg)




def send_whatsapp_img(destination_number, imgurl, caption="image"):
    payload = {
        "message_type": "image",
        "to": destination_number,
        "from": vonage_sandbox_number,
        "channel": "whatsapp",
        "image": {
            "url": imgurl,
            "caption": caption
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': vonage_authorization_header
    }
    response = requests.post(endpoint_vonage_message_send, headers=headers, data=json.dumps(payload))
    print(response.text)  # Adding print to debug API response
    return response.text




def send_whatsapp_msg(destination_number, msg):
    payload = json.dumps({
        "from": vonage_sandbox_number,
        "to": destination_number,
        "message_type": "text",
        "text": msg,
        "channel": "whatsapp"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': vonage_authorization_header
    }

    try:
        response = requests.post(endpoint_vonage_message_send, headers=headers, data=payload)
        print("Response from send_whatsapp_msg:", response.text)  # Print the response for debugging
    except Exception as e:
        logging.error(f"Error sending WhatsApp message: {str(e)}")



def chatbot(req_data):
    recipient = req_data['from']
    user_message = str(req_data['text']).strip()
    openai.api_key = openai_key

    # Script providing context for the Assistant's responses
    script = "You are a helpful assistant knowledgeable about farming practices, designed to collect detailed reports from farmers about their farm conditions. Please ensure you collect accurate information on the farm's name, location, size, and any issues they're facing."

    messages = [
        {"role": "system", "content": script},
        {"role": "user", "content": user_message}
    ]

    try:
        send_whatsapp_msg(recipient, "Please wait, communicating with ChatGPT...")
        chat_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        reply = chat_response.choices[0].message['content']
        logging.info(f"Answer received: {reply}")
        return reply
    except Exception as e:
        logging.error(f"Error communicating with ChatGPT: {str(e)}")
        return "Sorry, I encountered an error. Please try again later."





def imagebot(req_data):
    question = str(req_data['text']).upper().strip()
    recipient = req_data['from']
    openai.api_key = openai_key
    response = ""
    image_url = ""
    send_whatsapp_msg(recipient, "Please wait, communicating to chatgpt...")
    try:
        response = openai.Image.create(
            prompt=question,
            n=1,
            size="1024x1024"
            )
        logging.info(f"answer recieved: {response}")
        image_url = response['data'][0]['url']
    except:
        image_url = "http://khan2a.com:8080/get_image?name=meme.jpg"
    return image_url


def chatgpt_text(req_data):
    question = str(req_data['text']).upper().strip()
    destination_number = req_data['from']
    logging.info(f"Question received: {question}")
    
    # Use the updated chatbot function
    msg = chatbot(req_data)
    logging.info(f"Sending reply: {msg}")
    send_whatsapp_msg(destination_number, msg)



# Make sure to update or implement the chatbot, send_whatsapp_img, and imagebot functions accordingly.
    
    


command_set = {'CHATGPT_TEXT': chatgpt_text,
               'HELP': help,
               'HELLO': hello_vonage_ai,
               'SEND': get_advice_vonage_ai}