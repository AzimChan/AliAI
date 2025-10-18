# -*- coding: utf-8 -*-
from openai import OpenAI
import os
import sys
api_key_value = "sk-roG3OusRr0TLCHAADks6lw"
BANK_BASE_URL = "https://openai-hub.neuraldeep.tech/v1"
# The client automatically uses the OPENAI_API_KEY environment variable
from openai import OpenAI

BANK_ROUTER_KEY = "sk-роутер_банка_ключ"
BANK_BASE_URL = "https://openai-hub.neuraldeep.tech/v1" 

client = OpenAI(
    api_key=BANK_ROUTER_KEY,
    base_url=BANK_BASE_URL,
) 

def generate_sharia_advice(user_prompt: str, history: list) -> str:
    # 1. Добавляем новый запрос пользователя в историю
    history.append(
        {"role": "user", "content": user_prompt}
    )
    
    # 2. Отправляем всю историю в API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history  # <--- Ключевой шаг для сохранения контекста!
    )
    
    # Получаем ответ
    assistant_response = response.choices[0].message.content
    
    # 3. Сохраняем ответ ИИ в историю
    history.append(
        {"role": "assistant", "content": assistant_response}
    )
    
    return assistant_response

conversation_history = [
    {"role": "system", "content": "Вы — финансовый консультант Zaman Bank, Исламского банка. Предоставляйте советы в соответствии с принципами шариата и исламского банкинга."}
]

def main():
    # Настройка кодировки для Windows
    if sys.platform.startswith('win'):
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    
    print("Добро пожаловать в Zaman Bank - Исламский банк!")
    print("Я ваш финансовый консультант. Задавайте вопросы о банковских услугах.")
    print("Для выхода введите 'выход' или 'exit'")
    print("-" * 50)
    
    while True:
        try:
            # Получаем ввод от пользователя
            user_input = input("\nВаш вопрос: ").strip()
            
            # Проверяем команды выхода
            if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                print("До свидания! Спасибо за обращение в Zaman Bank.")
                break
            
            # Проверяем, что пользователь ввел что-то
            if not user_input:
                print("Пожалуйста, введите ваш вопрос.")
                continue
            
            # Получаем ответ от ИИ
            print("\nОбрабатываю ваш запрос...")
            response = generate_sharia_advice(user_input, conversation_history)
            
            # Выводим ответ
            print(f"\nКонсультант Zaman Bank:\n{response}")
            
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            print("Попробуйте еще раз.")

if __name__ == "__main__":
    # Устанавливаем кодировку для Windows
    if sys.platform.startswith('win'):
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    main()