import sys
import argparse
from router import process_message

# Mandatory test cases from the user request
TEST_MESSAGES = [
    "how do i sort a list of objects in python?",
    "explain this sql query for me",
    "This paragraph sounds awkward, can you help me fix it?",
    "I'm preparing for a job interview, any tips?",
    "what's the average of these numbers: 12 45 23 67 34",
    "Help me make this better.",
    "I need to write a function that takes a user id and returns their profile, but also i need help with my resume.",
    "hey",
    "Can you write me a poem about clouds?",
    "Rewrite this sentence to be more professional.",
    "I'm not sure what to do with my career.",
    "what is a pivot table",
    "fxi thsi bug pls: for i in range(10) print(i)",
    "How do I structure a cover letter?",
    "My boss says my writing is too verbose."
]

def run_tests():
    print("Starting Batch Test of 15 Messages...\n")
    print(f"{'#':<3} | {'Intent':<10} | {'Conf':<6} | {'Message'}")
    print("-" * 60)
    
    for i, msg in enumerate(TEST_MESSAGES, 1):
        try:
            response, classification = process_message(msg)
            print(f"{i:<3} | {classification['intent']:<10} | {classification['confidence']:<6.2f} | {msg[:50]}...")
        except Exception as e:
            print(f"{i:<3} | ERROR      | 0.00   | {msg[:50]}... (Error: {e})")
    
    print("\nBatch testing complete. Check `route_log.jsonl` for full details.")

def interactive_cli():
    print("--- LLM-Powered Prompt Router ---")
    print("Enter your message to get a specialized response.")
    print("Prefix with @intent to override (e.g., @code Fix this bug).")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                break
                
            if not user_input:
                continue
                
            response, classification = process_message(user_input)
            
            print(f"\n[Detected Intent: {classification['intent']} (Conf: {classification['confidence']:.2f})]")
            print(f"Assistant: {response}\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM Prompt Router CLI")
    parser.add_argument("--test", action="store_true", help="Run the 15 mandatory test cases")
    args = parser.parse_args()
    
    if args.test:
        run_tests()
    else:
        interactive_cli()
