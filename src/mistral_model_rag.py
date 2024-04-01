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
documents = SimpleDirectoryReader("/content/new/").load_data()
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
        conversation_states[from_number] = {"state": 1, "ask_mode": False}

    if llm_question.lower() == "start report":
        conversation_states[from_number] = {"state": 1, "ask_mode": False}

    if llm_question.endswith("?"):
        # Directly query the model if the message ends with a question mark
        try:
            response = query_engine.query(llm_question)
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            response = "Sorry, I couldn't process your request."
    else:
        if not conversation_states[from_number]["ask_mode"]:
            # Standard conversation logic
            state = conversation_states[from_number]["state"]
            if state == 1:
                response = "What's your full name?"
                conversation_states[from_number]["state"] = 2
            elif state == 2:
                response = "Where is your farm located?"
                conversation_states[from_number]["state"] = 3
            elif state == 3:
                response = "How large is your farm?"
                conversation_states[from_number]["state"] = 4
            elif state == 4:
                response = "Thank you for the information! You can now ask me any question."
                conversation_states[from_number]["ask_mode"] = True
            else:
                response = "Sorry, I couldn't process your request."
        else:
            # Query handling logic
            try:
                response = query_engine.query(llm_question)
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                response = "Sorry, I couldn't process your request."

    send_message(MY_NUMBER, response)
    return {"message": response}

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
