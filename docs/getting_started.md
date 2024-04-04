# Getting Started

This guide outlines the steps required to set up and run the project, connecting it to WhatsApp via the Twilio API and leveraging Flask, ngrok, and Mistral 7B for functionality.

## Prerequisites

Before starting, ensure you have the following prerequisites installed and set up:
- Python
- Flask
- ngrok

Instructions on installing these prerequisites can be found at their respective official documentation pages.

## Installation

Follow this step-by-step guide to install the project:

1. **Sign Up for Twilio API**: Create a free account to obtain your API keys.
2. **Install Python, Flask, and ngrok**: Make sure you have Python and Flask installed. For ngrok, follow the setup instructions specific to your operating system at [ngrok setup](https://dashboard.ngrok.com/get-started/setup).
3. **Set Up the WhatsApp API Sandbox**:
   - Navigate to the API Dashboard --> Developer Tools --> Message Sandbox.
   - Scan the QR code provided and send the given passphrase to the displayed number via WhatsApp.
   - Initialize ngrok in your command line interface (CLI) by typing `ngrok http 8080`. This command generates a forwarding URL.
   - In your Vonage account's Message Sandbox settings, paste the forwarding URL into the inbound webhook URL field and append `/wastatus` for the status webhook URL.

4. **Install Project Dependencies**:
   - Locate the `requirements.txt` file in your project directory.
   - Run `pip install -r requirements.txt` to install all necessary dependencies.