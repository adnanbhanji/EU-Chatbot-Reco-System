# Getting Started with Llama2 WhatsApp Chatbot Integration

This guide provides step-by-step instructions to set up a Llama2-powered chatbot for WhatsApp. Before proceeding, ensure you have the necessary tokens and IDs from WhatsApp and Replicate.

## Prerequisites

Before you start, you will need:
- **WhatsApp API Token**: For sending messages via WhatsApp.
- **WhatsApp Cloud Number ID**: The ID of your WhatsApp business number.
- **Recipient's WhatsApp ID**: The ID of the chatbot's recipient.
- **Replicate API Token**: For interacting with Llama2 AI(https://replicate.com/).
For getting the first 3, you can follow this guide: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started#set-up-developer-assets

## Setup

### Environment Setup

1. **Create a Virtual Environment** (Windows):
    ```cmd
    python3 -m venv whatsapp-llama
    .\whatsapp-llama\Scripts\activate
    pip install langchain replicate flask requests uvicorn gunicorn
    ```
After activating the virtual environment, install the necessary Python packages. Ensure your virtual environment is selected as the kernel if using an IDE. You can do this by opening the Command Palette (Ctrl+Shift+P or Cmd+Shift+P on macOS) and type Python: Select Interpreter.
Choose the Python interpreter that matches whatsapp-llama environment.

### Running the Chatbot

1. **Launch the Application**:
    Execute the chatbot application with the following command:
    ```cmd
    python app.py
    ```

## WhatsApp Business Platform Cloud API Integration

(Note: These steps are informative. For our project we will the same WhatsApp business account for this integration since it requires many steps.)

1. **Visit the WhatsApp Business Platform Cloud API guide** for initial setup instructions.
2. **Add WhatsApp to Your App**: Integrate WhatsApp with your business application through Meta's developer portal. Open this page: "https://developers.facebook.com/apps/" and create a business app
3. **Register a Phone Number**: Use a new number that's not been registered with WhatsApp before. You can not use the one given, since it will not work.
4. **Test Message Sending**: Follow the guide to send a test message.
5. **Set Up Webhooks**: Configure webhooks for real-time updates and notifications.

### Modifying the Webhook

1. **Glitch Account**: Create an account on glitch.com.
2. **Server Configuration**: Copy the `server.js` code provided in the llama2_whatsapp_bot to Glitch, adjusting the `.env` file with your tokens and Flask app URL you get from typing ngrok http 5000.

It should looks something like this:
   - WEBHOOK_VERIFY_TOKEN=HAPPY
   - GRAPH_API_TOKEN=
   - FLASK_APP_URL=https://9794-80-39-23-81.ngrok-free.app

4. **Webhook URL**: Share your live site webhook URL from Glitch into the WhatsApp configuration in the meta for developers portal.

### Running the Chatbot

- **Web Server Launch**: Use the command below on your terminal to run the Flask app.
    ```cmd
    python app.py
    ```

This guide aims to streamline the setup process for integrating Llama2 with WhatsApp, enhancing user engagement through AI-driven conversations. Ensure all tokens and IDs are securely stored and used appropriately throughout the setup.

