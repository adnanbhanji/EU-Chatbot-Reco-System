from fastapi import FastAPI, Request
from langchain_community.llms import CTransformers
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from urllib.parse import parse_qs
from twilio.rest import Client
import logging
from dotenv import load_dotenv
import os
from pdf_generation import generate_enhanced_pdf

load_dotenv()  # take environment variables from .env.


# Initialize FastAPI and Twilio client
app = FastAPI()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
MY_NUMBER = os.getenv("MY_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
twilio_number = TWILIO_NUMBER

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load your documents and create the index
documents = SimpleDirectoryReader("./src/dataset").load_data()
llm = LlamaCPP(model_url='https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q6_K.gguf?download=true', temperature=0.1, max_new_tokens=256, context_window=3900)
embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name="thenlper/gte-large"))
service_context = ServiceContext.from_defaults(chunk_size=256, llm=llm, embed_model=embed_model)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
query_engine = index.as_query_engine()

conversation_states = {}

@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}

@app.post("/")
async def reply(question: Request):
    body = parse_qs(await question.body())
    from_number = body[b'From'][0].decode()  # Extract sender number
    llm_question = body[b'Body'][0].decode()

    if from_number not in conversation_states:
        conversation_states[from_number] = {
            "history": [1],
            "ask_mode": False,
            "question_mode": False,
            "last_system_question": "",
            "data_collected": {}
        }

    current_history = conversation_states[from_number]["history"]
    current_state = current_history[-1]
    last_system_question = conversation_states[from_number]["last_system_question"]

    if llm_question.lower() == "solved":
        # Repeat the last system-driven question instead of the user's last question
        response = last_system_question if last_system_question else "Please start the report."
    elif llm_question.endswith("?"):
        conversation_states[from_number]["question_mode"] = True
        # Here, you might handle user-driven questions differently
        try:
            response = query_engine.query(llm_question)
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            response = "I'm sorry, I encountered an error processing your question. Please try again."
    else:
        # Normal conversation flow
        if not conversation_states[from_number]["ask_mode"]:
            current_state += 1
            current_history.append(current_state)
            # Handle the initial message separately
            if current_state == 1 and not last_system_question:
                response = "Welcome to the Farm Report Bot! Please provide your full name."
            else:
                response = determine_response(current_state, from_number, llm_question)
            conversation_states[from_number]["last_system_question"] = response  # Update only on state-driven questions
        else:
            # Handling inquiries here, assuming they don't affect the last_system_question directly
            try:
                response = query_engine.query(llm_question)
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                response = "I'm sorry, I encountered an error processing your question. Please try again."

    send_message(MY_NUMBER, response)
    return {"message": response}

  
def determine_response(current_state, from_number, llm_question):
    responses = {
        2: "What's your full name?",
        3: "Where is your farm located?",
        4: "How large is your farm?",
        5: "How many cows do you have in your farm?",
        6: "How much methane does your farm emit?",
        7: "Which calculation method have you chosen? (Method A, Method B, or Method C)",
        8: "How much electricity does your farm consume?",
        9: "How much fuel does your farm consume?",
        10: "What type of fuel?",
        11: "We have successfully finished the questions."
    }

    if current_state in responses:
        key = responses[current_state]  # Using current state as the key
        conversation_states[from_number]["data_collected"][key] = llm_question
        return responses.get(current_state, "Continue with the next question.")

    elif current_state >= 12:
        # All questions have been asked; generate the PDF
        generate_enhanced_pdf(conversation_states[from_number]["data_collected"], f"{from_number}_farm_report.pdf")
        print(f"this is how the format looks: {conversation_states[from_number]['data_collected']}")
        return "Thank you for providing all the information. Your PDF report has been generated."


def send_message(to_number, body_text):
    try:
        message = client.messages.create(
            from_=f"whatsapp:{twilio_number}",
            body=body_text,
            to=f"whatsapp:{to_number}"
        )
        logger.info(f"Message sent to {to_number}: {message.body}")
    except Exception as e:
        logger.error(f"Error sending message to {to_number}: {e}")

