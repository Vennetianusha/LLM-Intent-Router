# LLM Intent Router

This project is a simple AI-based service that routes user prompts to the correct expert response based on the detected intent.

The system uses a language model to analyze the user message and determine what type of request it is, such as coding help, data analysis, writing assistance, or career guidance.

## How It Works

1. **Intent Detection**
   - The user's prompt is analyzed using an LLM.
   - The model returns the detected intent and a confidence score.

2. **Prompt Routing**
   - Based on the detected intent, the request is routed to a specific expert persona:
     - Code Expert
     - Data Expert
     - Writing Expert
     - Career Expert

3. **Clarification**
   - If the model is not confident enough, the system asks the user for clarification.

4. **Logging**
   - All requests and responses are stored in `route_log.jsonl` for tracking.

## Features

- Intent classification using LLM
- Prompt routing to expert personas
- Confidence-based clarification
- Error handling for invalid responses
- Interaction logging

## Installation

Install the required packages:


pip install openai python-dotenv


## Environment Setup

Create a `.env` file and add your API key:


OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o-mini
CONFIDENCE_THRESHOLD=0.7


## Running the Project

Start the interactive CLI:


python main.py


Run the test cases:


python main.py --test


## Project Structure


router.py -> Routing and intent detection logic
prompts.py -> Expert persona prompts
main.py -> CLI interface
app.py -> Service entry point
route_log.jsonl -> Request logs
Dockerfile -> Docker setup
docker-compose.yml -> Container configuration


## Technologies Used

- Python
- OpenAI API
- Docker

## Author

Anusha Pavani Venneti
