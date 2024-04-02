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
documents = SimpleDirectoryReader("/Users/adnanbhanji/Documents/GitHub/EU-Chatbot-Reco-System/src/new").load_data()
llm = LlamaCPP(model_url='https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf', temperature=0.1, max_new_tokens=256, context_window=3900)
embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name="thenlper/gte-large"))
service_context = ServiceContext.from_defaults(chunk_size=256, llm=llm, embed_model=embed_model)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
query_engine = index.as_query_engine()

conversation_states = {}

@app.post("/")
async def reply(question: Request):
    body = parse_qs(await question.body())
    from_number = body[b'From'][0].decode()  # Extract sender number
    llm_question = body[b'Body'][0].decode()

    if from_number not in conversation_states:
        conversation_states[from_number] = {"history": [1], "ask_mode": False, "question_mode": False, "last_system_question": ""}

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
            response = determine_response(current_state)
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

def determine_response(state):
    # Function to determine the response based on the current state
    if state == 1:
        return "X"
    elif state == 2:
        return "What's your full name?"
    elif state == 3:
        return "Where is your farm located?"
    elif state == 4:
        return "How large is your farm?"
    elif state >= 5:
        return "Thank you for the information! You can now ask me any question."
    else:
        return "I'm not sure what you're asking. Can you clarify?"

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
