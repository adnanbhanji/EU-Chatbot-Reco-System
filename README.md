# EU-Chatbot-Reco-System

### 🌍 Project Description

Compliance with EU Commission environmental carbon emission reporting mandates can be a laborious process, prone to human error, and costly in terms of time and resources. This project aims to solve this with a WhatsApp-based chatbot designed to streamline and simplify carbon emission reporting, ensuring compliance with EU Commission reporting standards.

### 🔑 Key Features & Benefits

- **Dynamic Reporting**: Utilise Natural Language Processing (NLP) and AI to send and receive text messages via WhatsApp, which auto-populate the carbon emission report with real-time data.
- **Efficiency**: Eliminate manual data entry and reduce reporting time significantly.
- **User-Friendly**: No complex installations or training required; WhatsApp familiarity ensures ease of use.
- **Accuracy & Compliance**: Ensure precise reporting to meet EU Commission requirements, minimising the risk of penalties.
- **Real-Time Updates**: Receive notifications and alerts regarding reporting deadlines and regulatory changes.
- **Cost-Effective**: A cost-efficient alternative to hiring additional personnel or outsourcing reporting.
- **Environmental Impact**: Simplifying reporting contributes to a company's broader sustainability efforts.

### ChatBot DEMO
https://drive.google.com/file/d/1ZdZFKwC7FdsoWqDSDwNN1BUNR34xbHax/view?usp=sharing

We would like to express our gratitude to our mentors, collaborators, and data providers who contributed to the success of this project.

### Prerequisites

Before you begin, ensure you meet the following requirements:
- Python 3.6 - 3.9 installed on your system.
- Pip for installing Python packages.

###  Installation

Follow these steps to set up the project locally:

1. **Clone the repository**
   
   Clone the project repository to your local machine using Git:
   
   ```sh
   git clone https://github.com/adnanbhanji/EU-Chatbot-Reco-System.git
   cd EU-Chatbot-Reco-System
   ```

2. **Create a virtual environment**

   It's recommended to create a virtual environment for Python projects to manage dependencies effectively. You can do this by running:
   
   ```sh
   python3 -m venv venv
   ```

   Activate the virtual environment:
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```sh
     source venv/bin/activate
     ```

3. **Install dependencies**

   Install all the required dependencies using pip:
   
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory of the project to store your environment variables (e.g., API keys, database URLs). Refer to the `.env.example` file for the required variables.

5. **Run the setup script**

   Ensure `setup.py` is properly configured, then run it to install the package locally:
   
   ```sh
   python setup.py develop
   ```

### Configuration

- **Vonage and OpenAI Credentials**: Ensure you have valid credentials for Vonage and OpenAI. These should be set in the `config.py` file or stored as environment variables and read from there.

### Running the Application

To run the application, execute the following command in the root directory:

```sh
python src/app.py
```

This will start a Flask web server on the specified port (default is 8080). The server will handle incoming requests as defined in your application routes.

### Testing

The project includes unit and integration tests. To run these tests, follow these steps:

1. **Unit Tests**

   Run the unit tests to ensure the individual components function correctly:
   
   ```sh
   pytest tests/unit/
   ```

2. **Integration Tests**

   Run the integration tests to verify the application works as expected when components interact:
   
   ```sh
   pytest tests/integration/
   ```

Ensure your testing environment variables are set correctly.

### 👥 The Team

- Adnan Bhanji: Project Manager
- Beatrice Mossberg: Data Engineer
- Riyad Mazari: Data Scientist
- Sofia Morena Lasa: Data Scientist
- Khaled Akel: Machine Learning Engineer
- Hussein Soliman: MLOps Engineer

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or add new features.

## License

See the [MIT Licenese](https://github.com/adnanbhanji/EU-Chatbot-Reco-System/blob/729f6c44b4583e550ab68274eee0a8b37536ff1f/LICENSE).
