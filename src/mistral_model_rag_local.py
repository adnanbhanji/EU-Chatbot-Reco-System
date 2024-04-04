from fastapi import FastAPI, Request
from langchain_community.llms import CTransformers
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from urllib.parse import parse_qs
from twilio.rest import Client
import os

# Initialize FastAPI and Twilio client
app = FastAPI()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
MY_NUMBER = os.getenv("MY_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
twilio_number = TWILIO_NUMBER

# Load your documents and create the index
documents = SimpleDirectoryReader("./new").load_data()
llm = LlamaCPP(model_url='https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf', temperature=0.1, max_new_tokens=256, context_window=3900)
embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name="thenlper/gte-large"))
service_context = ServiceContext.from_defaults(chunk_size=256, llm=llm, embed_model=embed_model)
index = VectorStoreIndex.from_documents(documents, service_context=service_context)
query_engine = index.as_query_engine()
