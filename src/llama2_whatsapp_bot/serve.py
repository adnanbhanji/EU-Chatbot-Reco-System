from waitress import serve
from llama_chatbot import app

serve(app, host='0.0.0.0', port=5000)
