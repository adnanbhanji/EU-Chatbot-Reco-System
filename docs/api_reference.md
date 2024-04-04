# API Reference

## Overview

This API serves as the backend for a chatbot system designed to facilitate carbon emission reporting and user registration via WhatsApp. It integrates with Mistral 7B for natural language processing and leverages the Twilio API for WhatsApp communication. The primary purpose of this API is to manage the flow of data between the chatbot and the user, ensuring a seamless registration and reporting process.

## Authentication

To authenticate with the API, users must provide a valid API key with each request. The API key should be included in the request header as follows:


Replace `YOUR_API_KEY` with your actual API key. Contact the system administrator to obtain your API key if you do not already have one.

## Endpoints

### Endpoint 1: Start Registration Flow
- **Method**: POST
- **URL**: `/start-registration`
- **Description**: Initiates the user registration process by asking for the user's full name via WhatsApp.
- **Parameters**:
  - `destination_number`: The WhatsApp number to which the registration prompt will be sent.

### Endpoint 2: Continue Registration Flow
- **Method**: POST
- **URL**: `/continue-registration`
- **Description**: Continues the registration process based on user input, collecting additional details like farm location and size.
- **Parameters**:
  - `destination_number`: The user's WhatsApp number.
  - `message`: The message received from the user as part of the registration flow.

### Endpoint 3: Start Report Flow
- **Method**: POST
- **URL**: `/start-report`
- **Description**: Initiates the reporting process for users to report their farm's carbon emissions via WhatsApp.
- **Parameters**:
  - `destination_number`: The WhatsApp number to which the reporting prompt will be sent.

### Endpoint 4: Continue Report Flow
- **Method**: POST
- **URL**: `/continue-report`
- **Description**: Processes the user's responses for the emission reporting, including handling questions and collecting emission data.
- **Parameters**:
  - `destination_number`: The user's WhatsApp number.
  - `message`: The user's response or query related to the emission reporting.

## Additional Functionalities

Besides the main registration and reporting flows, the API offers integration with Mistral 7B to handle natural language queries and generate responses, providing an interactive chatbot experience. It also includes functionalities for image generation and the ability to send both text messages and images via WhatsApp, enhancing user engagement.

- **Text-Based Queries (Chatbot Function)**: Leverages Mistral 7B for answering user queries in natural language.
- **Image Generation (Imagebot Function)**: Utilizes Mistral 7B's capabilities to generate images based on text descriptions.
- **Message Sending Utilities**:
  - `send_whatsapp_msg`: Sends a text message to a specified WhatsApp number.
  - `send_whatsapp_img`: Sends an image to a specified WhatsApp number, enhancing the interactive experience.

This API is designed to be flexible and scalable, accommodating future expansions such as additional reporting categories, integration with other messaging platforms, and more advanced AI functionalities.