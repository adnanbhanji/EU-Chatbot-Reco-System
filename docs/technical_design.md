# Technical Design

## Introduction

This document details the technical design of the emission reporting chatbot system, focusing on the integration of WhatsApp for user interaction, the utilization of Mistral 7B for natural language processing, and Azure for cloud services. The design emphasizes efficient data collection, processing, and storage, leveraging modern technologies to ensure reliability and scalability.

## System Design

The system is architecturally divided into four main components: the WhatsApp interface, the language processing engine, the backend server, and the cloud storage solution. This structure supports modular development, simplifying maintenance and enhancing system adaptability.

### User Interface

The user interface is provided through WhatsApp, utilizing the Twilio API for seamless interaction with users. This choice allows for broad accessibility and leverages the widespread use of WhatsApp for intuitive user engagement.

### Language Processing Engine

The core of the system's natural language processing capabilities is powered by Mistral 7B. This choice was made due to Mistral 7B's advanced understanding and generation of human-like text, enabling the system to accurately interpret user messages and generate appropriate responses.

### Backend Server

The backend, developed with Flask, acts as the intermediary between the WhatsApp interface, the Mistral 7B engine, and the data storage. Flask was chosen for its simplicity, flexibility, and the ability to rapidly develop and deploy web applications.

### Cloud Storage

Azure services are utilized for data storage and serverless functions, providing a scalable, secure, and reliable infrastructure. Azure's integration capabilities and extensive service offerings support the system's data processing and storage needs effectively.

### Diagrams and Models

(Insert system architecture diagram or model here)

## Design Decisions

### Decision 1: Integration of Twilio API with WhatsApp

- **Rationale**: The Twilio API was selected for its comprehensive support for WhatsApp messaging, including robust documentation and ease of use, which significantly simplifies the integration process.
- **Impact**: This integration enables the system to reliably send and receive messages on WhatsApp, providing a familiar platform for users to report emissions, thereby increasing user engagement and data collection efficiency.

### Decision 2: Use of Mistral 7B for Language Processing

- **Rationale**: Mistral 7B was chosen for its state-of-the-art natural language processing capabilities, enabling the system to understand and generate human-like responses. This facilitates accurate interpretation of user messages and automated responses, enhancing user interaction.
- **Impact**: Leveraging Mistral 7B significantly improves the system's ability to process and understand diverse user inputs, making the chatbot more intuitive and effective in collecting accurate emission data.

### Decision 3: Deployment on Azure Cloud Services

- **Rationale**: Azure was selected for its robust cloud services, offering scalability, reliability, and a wide range of tools and services that cater to the project's needs, including serverless functions and secure data storage options.
- **Impact**: Using Azure ensures that the system can scale to handle increasing loads, provides a high level of data security and reliability, and supports seamless integration of various components and services used in the project.

## Conclusion

The emission reporting chatbot system's technical design integrates key technologies—WhatsApp via Twilio API, Mistral 7B, Flask, and Azure services—to create a robust, scalable, and user-friendly platform for environmental data collection. This design ensures the project is well-positioned to adapt to future technology advancements and user needs, solidifying its value and impact in environmental conservation efforts.