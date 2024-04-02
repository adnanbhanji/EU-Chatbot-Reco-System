# Getting Started

This guide outlines the steps required to set up and run the project, connecting it to WhatsApp via the Vonage API and leveraging Flask, ngrok, and OpenAI for functionality.

## Prerequisites

Before starting, ensure you have the following prerequisites installed and set up:
- Python
- Flask
- ngrok

Instructions on installing these prerequisites can be found at their respective official documentation pages.

## Installation

Follow this step-by-step guide to install the project:

1. **Sign Up for Vonage API**: Create a free account at [Vonage API](https://developer.vonage.com/en/home) to obtain your API keys.
2. **Install Python, Flask, and ngrok**: Make sure you have Python and Flask installed. For ngrok, follow the setup instructions specific to your operating system at [ngrok setup](https://dashboard.ngrok.com/get-started/setup).
3. **Set Up the WhatsApp API Sandbox**:
   - Navigate to the API Dashboard --> Developer Tools --> Message Sandbox.
   - Scan the QR code provided and send the given passphrase to the displayed number via WhatsApp.
   - Initialize ngrok in your command line interface (CLI) by typing `ngrok http 8080`. This command generates a forwarding URL.
   - In your Vonage account's Message Sandbox settings, paste the forwarding URL into the inbound webhook URL field and append `/wastatus` for the status webhook URL.

4. **Install Project Dependencies**:
   - Locate the `requirements.txt` file in your project directory.
   - Run `pip install -r requirements.txt` to install all necessary dependencies.

## Running the Project

To run the project and connect it to your WhatsApp, follow these detailed steps:

1. **Generate Authorization Header**:
   - Navigate to `watsapp` --> `generate_auth.py`.
   - Enter your Vonage `api_key` and `api_secret` found under API Settings in your Vonage account.
   - Execute `python generate_auth.py` to generate your authorization header.
   - Copy the generated authorization header into `config.py` as the value for `vonage_authorization_header`.

2. **Configure OpenAI API Key**:
   - Create an API Key at [OpenAI](https://platform.openai.com/api-keys). Ensure your key has credits to avoid errors.
   - In `config.py`, replace `openai_key` with your newly created OpenAI API Key.

3. **Update Configuration**:
   - In `config.py`, update `vonage_sandbox_number` with the number you used to send the passphrase to, excluding the `+` sign.

4. **Customize Command Trigger**:
   - In `commands.py`, find the line `elif question != "JOIN LINT MUSIC"` and replace `"JOIN LINT MUSIC"` with your passphrase in all caps.

5. **Environment Setup and Dependencies**:
   - Execute the following commands in your CLI to prepare your environment:
     ```bash
     Remove-Item -Recurse -Force .\env\
     python -m venv env
     .\env\Scripts\activate
     python -m pip install --upgrade pip setuptools wheel
     ```

6. **Run the Application**:
   - Start the application with `python app.py`.
   - Test the model by sending a message through WhatsApp. Use commands like "start registration" or "start report" to initiate specific processes, or directly interact with ChatGPT for other inquiries.

This setup guide should help you successfully configure and run the project, integrating it with WhatsApp for real-time messaging and data processing.
