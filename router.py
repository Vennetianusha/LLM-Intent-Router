import os
import json
import logging
from datetime import datetime
from typing import Dict, Tuple, Optional
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPTS, CLASSIFIER_PROMPT, check_manual_override

# Load environment variables
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.7))
LOG_FILE = "route_log.jsonl"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def log_interaction(intent: str, confidence: float, message: str, response: str):
    """
    Logs the interaction to a JSON Lines file.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "original_message": message,
        "classified_intent": intent,
        "confidence_score": confidence,
        "final_response": response
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def classify_intent(message: str) -> Dict:
    """
    Classifies the user's intent using a lightweight LLM call.
    Returns a dictionary with 'intent' and 'confidence'.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": CLASSIFIER_PROMPT},
                {"role": "user", "content": message}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        
        content = response.choices[0].message.content
        result = json.loads(content)
        
        # Validate keys
        if "intent" not in result or "confidence" not in result:
            raise ValueError("Invalid JSON structure from LLM")
            
        return result
        
    except Exception as e:
        print(f"Error in classification: {e}")
        return {"intent": "unclear", "confidence": 0.0}

def route_and_respond(message: str, classification: Dict) -> str:
    """
    Routes the message to the appropriate persona and returns the response.
    """
    intent = classification.get("intent", "unclear")
    confidence = classification.get("confidence", 0.0)
    
    # Apply confidence threshold
    if confidence < CONFIDENCE_THRESHOLD:
        intent = "unclear"
    
    if intent == "unclear" or intent not in SYSTEM_PROMPTS:
        # Generate a clarifying question
        system_prompt = "You are a helpful assistant. The user's request is unclear. Ask a polite clarifying question to understand if they need help with coding, data analysis, writing, or career advice."
    else:
        system_prompt = SYSTEM_PROMPTS[intent]
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {e}"

def process_message(message: str) -> Tuple[str, Dict]:
    """
    Full pipeline: Manual override -> Classify -> Route -> Respond -> Log
    """
    # 1. Check for manual override (@intent)
    manual_intent, cleaned_message = check_manual_override(message)
    
    if manual_intent:
        classification = {"intent": manual_intent, "confidence": 1.0}
    else:
        # 2. Classify intent
        classification = classify_intent(cleaned_message)
    
    # 3. Route and Respond
    response = route_and_respond(cleaned_message, classification)
    
    # 4. Log
    log_interaction(
        classification["intent"], 
        classification["confidence"], 
        message, 
        response
    )
    
    return response, classification

if __name__ == "__main__":
    # Quick test if run directly
    test_msg = "How do I sort a list in Python?"
    res, intent = process_message(test_msg)
    print(f"Intent: {intent}")
    print(f"Response: {res}")
