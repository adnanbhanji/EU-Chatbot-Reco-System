# API Reference for Flask-based WhatsApp Chatbot

## Overview

This Flask application implements a chatbot designed to interact with users via WhatsApp for collecting farm-related information and answering queries using llama2 model. The chatbot guides users through a predefined set of questions to gather data about their farms and allows for ad-hoc querying post-report submission.

## No Explicit Authentication

The current implementation does not include an authentication mechanism for API requests. If deployed publicly, consider adding authentication to secure the endpoints.

## Endpoints

The application provides a single endpoint to handle incoming messages from users and manage the conversation flow.

### Message Received (`/msgrcvd`)

- **Method**: GET
- **URL**: `/msgrcvd`
- **Description**: Processes incoming messages from users. It handles initiating and continuing the structured report flow, managing interruptions for ad-hoc questions, and resuming the flow post-interruption.
- **Query Parameters**:
  - `message`: The message received from the user, extracted from the query parameters.

## Core Functionalities

### Structured Conversation Flow

Through a series of predefined questions, the chatbot collects specific information about the user's farm, including the farm's name, location, and area.

### Ad-hoc Query Handling with OpenAI's GPT

Upon completing the structured flow or when receiving messages that end with a "?", the chatbot utilizes OpenAI's GPT models to generate responses, providing users with informative answers beyond the structured questions.

### Conversation State Management

The application maintains the state of each conversation, tracking which question a user is responding to and handling user interruptions for ad-hoc questions, ensuring a seamless conversation flow.

## Handling Interruptions

If a user's message ends with a "?", the chatbot temporarily exits the structured flow to process the query through GPT models. The flow resumes with the last unanswered question once the user types "solved".

## Post-Flow Interaction

After the structured conversation concludes with a "Thank you" message, users can continue to interact with the chatbot. They can ask additional questions, with the chatbot leveraging GPT models to respond.

## Implementation Notes

- The application uses the `Replicate` library for integrating with the llama2 model and the Facebook Graph API for sending messages via WhatsApp.
- State management is handled through in-memory dictionaries (`user_states`, `user_responses`, and `user_interactions`), tracking the progress and interactions of each user.

## Future Considerations

For production deployment, consider implementing the following:
- **Authentication**: Secure the endpoint to ensure that only authorized requests are processed.
- **Persistent State Management**: Use a database to persistently track conversation states and user data, enhancing reliability and scalability.
- **Error Handling and Logging**: Implement comprehensive error handling and logging mechanisms for better monitoring and troubleshooting.
- **API Rate Limiting**: Introduce rate limiting to protect against abuse and ensure service availability.
