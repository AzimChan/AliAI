from openai import OpenAI
import os
api_key_value = "sk-roG3OusRr0TLCHAADks6lw"
BANK_BASE_URL = "https://openai-hub.neuraldeep.tech/v1"
# The client automatically uses the OPENAI_API_KEY environment variable
client = OpenAI(
    api_key=api_key_value,
    base_url=BANK_BASE_URL
    ) 

def generate_sharia_advice(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful, Sharia, Amir-Ai financial assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Example tailored to your Islamic bank project
advice = generate_sharia_advice("Explain the difference between Murabaha and Ijarah contracts.")
print(advice)