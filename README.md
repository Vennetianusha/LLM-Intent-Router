# LLM-Powered Prompt Router for Intent Classification

This project implements a sophisticated two-step AI service that intelligently routes user requests to specialized expert personas based on detected intent.

## Architecture

1.  **Classify**: A lightweight LLM call (using `gpt-4o-mini`) analyzes the user's message and returns a structured JSON object with the detected intent (`code`, `data`, `writing`, `career`, or `unclear`) and a confidence score.
2.  **Route and Respond**: The system selects a specialized "Expert Persona" system prompt based on the intent. If the intent is below a confidence threshold (0.7) or is "unclear", it generates a clarifying question.
3.  **Log**: Every interaction is logged to `route_log.jsonl` for observability.

### Error Handling & Troubleshooting
- **Insufficient Quota (429)**: If you see this in the logs, it means your OpenAI account has an active key but no credits. You'll need to add a balance at [platform.openai.com](https://platform.openai.com/).
- **Invalid API Key (401)**: Double-check that your `.env` file contains the correct key without quotes or extra spaces.
- **JSON Parsing**: The system automatically defaults to an `"unclear"` intent if the LLM fails to provide a valid JSON structure.

## Features

- **Specialized Personas**: Focuses on Code, Data, Writing, and Careers.
- **Robust Error Handling**: Gracefully handles malformed JSON and API errors.
- **Manual Override**: Users can bypass classification using `@intent` (e.g., `@code fix my bug`).
- **Confidence Thresholding**: Ensures high-quality routing by asking for clarification when uncertain.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install openai python-dotenv
    ```
2.  **Configure Environment**:
    Create a `.env` file and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_actual_key_here
    MODEL_NAME=gpt-4o-mini
    CONFIDENCE_THRESHOLD=0.7
    ```

## Usage

### Interactive CLI
Run the service in interactive mode:
```bash
python main.py
```

### Batch Testing
Run the 15 mandatory test cases:
```bash
python main.py --test
```

### Docker Setup

1.  **Build and Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    *Note: Ensure your `.env` file is populated with a valid API key.*

## Project Structure

- `router.py`: Core routing logic and LLM orchestration.
- `prompts.py`: Definitions for expert personas and classifier prompts.
- `main.py`: CLI interface and batch test runner.
- `route_log.jsonl`: Interaction logs.
- `Dockerfile` & `docker-compose.yml`: Containerization files.
- `.env.example`: Template for environment variables.
