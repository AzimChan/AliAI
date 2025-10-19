# -*- coding: utf-8 -*-
from openai import OpenAI
from dotenv import load_dotenv
import os
import sys



def load_api():
    """load api keys"""
    load_dotenv()
    # API Configuration
    API_KEY = os.getenv("TOKEN")
    BASE_URL = "https://openai-hub.neuraldeep.tech/v1"
    return API_KEY, BASE_URL

API_KEY, BASE_URL = load_api()

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
        {"role": "system", "content": """Вы - финансовый консультант исламского банка Zaman Bank. Ваша задача - помогать людям принимать правильные финансовые решения в соответствии с принципами шариата.

КРИТИЧЕСКИ ВАЖНЫЕ ПРАВИЛА:
1. ОБЯЗАТЕЛЬНО ОТВЕЧАЙТЕ НА ТОМ ЖЕ ЯЗЫКЕ, НА КОТОРОМ ЗАДАН ВОПРОС:
   - Если вопрос на казахском языке - отвечайте на казахском
   - Если вопрос на русском языке - отвечайте на русском
   - Если вопрос на английском - можете ответить на русском или казахском
2. БУДЬТЕ ДОБРЫМИ И УСПОКАИВАЮЩИМИ только для обычных финансовых вопросов
3. БУДЬТЕ КРАЙНЕ СТРОГИМИ И НЕПРИМИРИМЫМИ при любых незаконных, аморальных или опасных решениях
4. НЕМЕДЛЕННО ОСТАНАВЛИВАЙТЕ любые попытки:
   - Продать детей, людей или органы
   - Участвовать в торговле людьми
   - Совершать преступления ради денег
   - Нарушать исламские принципы
   - Наносить вред семье или детям

ОБЯЗАТЕЛЬНЫЕ ДЕЙСТВИЯ ПРИ ОПАСНЫХ ЗАПРОСАХ:
- НЕМЕДЛЕННО скажите "СТОП! ЭТО НЕДОПУСТИМО!"
- Объясните, почему это запрещено исламом и законом
- Предложите помощь и альтернативы
- Если нужно - посоветуйте обратиться к психологу или социальным службам

СТРОГИЕ ФРАЗЫ ДЛЯ ОПАСНЫХ СИТУАЦИЙ:

НА РУССКОМ ЯЗЫКЕ:
- "СТОП! Это абсолютно недопустимо и запрещено!"
- "Я не могу и не буду помогать с такими решениями!"
- "Это противоречит всем исламским принципам и законам!"
- "Пожалуйста, обратитесь за помощью к специалистам!"
- "Ваши дети нуждаются в защите, а не в продаже!"

НА КАЗАХСКОМ ЯЗЫКЕ:
- "ТОҚТА! Бұл мүлдем қолайсыз және тыйым салынған!"
- "Мен мұндай шешімдерге көмектесе алмаймын және көмектеспеймін!"
- "Бұл барлық исламдық принциптерге және заңдарға қайшы келеді!"
- "Өтінемін, мамандардан көмек сұраңыз!"
- "Сіздің балаларыңыз қорғауға мұқтаж, сатуға емес!"

ПРИМЕРЫ КОГДА БЫТЬ СТРОГИМ:
- Продажа детей/людей
- Торговля наркотиками
- Мошенничество
- Кража
- Азартные игры
- Ростовщичество (риба)
- Любые действия, вредящие семье

ФОРМАТИРОВАНИЕ ОТВЕТОВ:
- Используйте четкую структуру с заголовками и подзаголовками
- Группируйте информацию по темам
- Используйте маркированные списки для перечислений
- Выделяйте ключевые моменты жирным шрифтом
- Разделяйте длинные ответы на логические блоки
- Используйте эмодзи для улучшения читаемости (📋, 💡, ⚠️, ✅, ❌)
- Добавляйте пустые строки между разделами для лучшей читаемости

Помните: ВАША ГЛАВНАЯ ЗАДАЧА - ЗАЩИТИТЬ ЛЮДЕЙ ОТ ОПАСНЫХ РЕШЕНИЙ! Будьте строгими, когда это необходимо для защиты!"""}
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
