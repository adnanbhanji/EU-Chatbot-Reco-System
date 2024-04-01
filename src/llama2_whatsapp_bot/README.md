# How to set up the Llama2 WhatsApp Chatbot
Remember to set `WHATSAPP_API_TOKEN`,your `WHATSAPP_CLOUD_NUMBER_ID`, your recipient's WhatsApp ID, and your `REPLICATE_API_TOKEN`.

`msgrcvd` is used to:
1. receive the user message forwarded by the webhook;
2. ask Llama 2 for the answer;
3. call the `WhatsAppClient`'s `send_text_message`` with a recipient's phone number.


For windows:
# Create a virtual environment
python3 -m venv whatsapp-llama
.\whatsapp-llama\Scripts\activate
pip install langchain replicate flask requests uvicorn gunicorn

Remember: when selecting the kernel, select your virtual environment.

## Running the Chatbot

Run the following command on the Terminal:

```
python app.py
```
Demo: https://drive.google.com/file/d/1cb83jhmdXKi2ctPJBOPmq6Hrvki41uSL/view?usp=sharing

## (Don´t do these steps since we are only going to use one Whatsapp business account)

If you were to use it, these would be the steps:
 
Start by visiting the WhatsApp Business Platform Cloud API guide. There, you'll need to complete a few initial steps to set up your WhatsApp Business integration:

Add WhatsApp to Your App: Integrate the WhatsApp service with your business's application through Meta's developer portal.
Register a Phone Number: Choose a phone number that will act as the sender for your messages. This number should not have been previously registered with WhatsApp.

Test Message Sending: Utilize the provided instructions to send a trial message, ensuring your setup is correct.

Set Up Webhooks: Follow guidelines to configure webhooks, allowing you to receive updates and notifications directly.
After these steps, proceed to set up your callback URL for webhooks by following the instructions in the Sample Callback URL for Webhooks Testing Guide. This involves creating a free account on Glitch.com, where you'll get a callback URL for your webhook.

Additionally, before beginning these steps, if you haven't already set up a WhatsApp Business account with a new phone number (one that hasn't been used with WhatsApp before), you'll need to do that. Here's how to add this step:

Set Up a New WhatsApp Business Account: Before initiating the API integration process, ensure you have a WhatsApp Business account. Choose a mobile phone number not previously registered with WhatsApp for this account. Follow WhatsApp's setup process to create your business profile.
Finally, navigate to the Meta for Developers Apps page. Choose your WhatsApp business app to access the necessary command in the App Dashboard (found under WhatsApp > API Setup > Step 2). 

## Modifying the Webhook

Create a glitch.com account. In the server.js file in glitch, paste the exact code in the server.js file in the whatsapp-llama folder, do the same for the app.py in glitch, paste the code in the app.py.

Then in the .env you will have to put this, with your token:
WEBHOOK_VERIFY_TOKEN="HAPPY"
GRAPH_API_TOKEN=""
FLASK_APP_URL=https://yourown.ngrok-free.app

Then, go to share and copy the live site webhook URL.


## Running the Chatbot

On your web server, if used run the following command on a Terminal:

```
python app.py
```
