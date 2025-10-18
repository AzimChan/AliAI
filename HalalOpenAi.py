# -*- coding: utf-8 -*-
from openai import OpenAI
import os
import sys

# API Configuration
API_KEY = "sk-roG3OusRr0TLCHAADks6lw"
BASE_URL = "https://openai-hub.neuraldeep.tech/v1"

def create_client():
    """Create OpenAI client with current configuration"""
    return OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,
    )

def generate_sharia_advice(user_prompt: str, history: list, client) -> str:
    """Generate Sharia-compliant financial advice"""
    # Add user message to history
    history.append({"role": "user", "content": user_prompt})
    
    # Send request to API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )
    
    # Get response
    assistant_response = response.choices[0].message.content
    
    # Save response to history
    history.append({"role": "assistant", "content": assistant_response})
    
    return assistant_response

def test_api_connection(client):
    """Test API connection"""
    try:
        print("Testing API connection...")
        print(f"Using API key: {API_KEY[:10]}...")
        print(f"Using base URL: {BASE_URL}")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("API connection successful!")
        return True
    except Exception as e:
        print(f"API connection failed: {e}")
        return False

def main():
    print("Welcome to Zaman Bank - Islamic Bank!")
    print("I am your financial consultant. Ask questions about banking services.")
    print("To exit, type 'exit' or 'quit'")
    print("-" * 50)
    
    # Create client
    client = create_client()
    
    # Test connection
    if not test_api_connection(client):
        print("Please check your API key and network connection.")
        print("The API key might be invalid or expired.")
        
        # Ask for new API key
        new_key = input("\nEnter your API key (or press Enter to exit): ").strip()
        if new_key:
            global API_KEY
            API_KEY = new_key
            client = create_client()
            if not test_api_connection(client):
                print("Still failed. Exiting...")
                return
        else:
            print("Exiting...")
            return
    
    # Initialize conversation
    conversation_history = [
        {"role": "system", "content": "You are a financial consultant for Zaman Bank, an Islamic bank. Provide advice in accordance with Sharia principles and Islamic banking."}
    ]
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = input("\nYour question: ").strip()
            
            # Check exit commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! Thank you for using Zaman Bank.")
                break
            
            # Check if user entered something
            if not user_input:
                print("Please enter your question.")
                continue
            
            # Get AI response
            print("\nProcessing your request...")
            response = generate_sharia_advice(user_input, conversation_history, client)
            
            # Display response
            print(f"\nZaman Bank Consultant:\n{response}")
            
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print(f"Error type: {type(e).__name__}")
            print("Please try again.")

if __name__ == "__main__":
    main()