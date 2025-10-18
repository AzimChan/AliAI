from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import random
import asyncio
from HalalOpenAi import create_client, generate_sharia_advice

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize AI client
ai_client = create_client()
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

Помните: ВАША ГЛАВНАЯ ЗАДАЧА - ЗАЩИТИТЬ ЛЮДЕЙ ОТ ОПАСНЫХ РЕШЕНИЙ! Будьте строгими, когда это необходимо для защиты!"""}
]

# Serve the static frontend (index.html, script.js, etc.)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def get_index():
    return FileResponse("frontend/index.html")

# Fake pages for redirection
@app.get("/qr")
async def get_qr_page():
    return FileResponse("frontend/qr.html")

@app.get("/deposit")
async def get_deposit_page():
    return FileResponse("frontend/deposit.html")

@app.get("/personal-data")
async def get_personal_data_page():
    return FileResponse("frontend/personal-data.html")

@app.get("/auth")
async def get_auth_page():
    return FileResponse("frontend/auth.html")

# Real AI endpoint using HalalOpenAi
@app.get("/chat")
async def get_ai_response(message: str):
    try:
        # Check if message contains keywords that should redirect to fake pages
        message_lower = message.lower()
        
        # Keywords for different fake pages
        qr_keywords = ['qr', 'кьюар', 'код', 'сканировать', 'сканирование', 'штрих', 'штрихкод']
        deposit_keywords = ['депозит', 'вклад', 'накопить', 'сбережения', 'процент', 'доходность', 'инвестиции']
        personal_data_keywords = ['данные', 'персональные', 'информация', 'профиль', 'личные', 'конфиденциальность']
        auth_keywords = ['войти', 'авторизация', 'логин', 'пароль', 'вход', 'регистрация', 'аккаунт']
        
        # Check for redirect keywords
        if any(keyword in message_lower for keyword in qr_keywords):
            return {"response": "Для работы с QR-кодами перейдите по ссылке: <a href='/qr' target='_blank' class='text-primary hover:underline'>Открыть QR-генератор</a>", "redirect": "/qr"}
        elif any(keyword in message_lower for keyword in deposit_keywords):
            return {"response": "Для открытия депозита перейдите по ссылке: <a href='/deposit' target='_blank' class='text-primary hover:underline'>Калькулятор депозитов</a>", "redirect": "/deposit"}
        elif any(keyword in message_lower for keyword in personal_data_keywords):
            return {"response": "Для управления персональными данными перейдите по ссылке: <a href='/personal-data' target='_blank' class='text-primary hover:underline'>Управление данными</a>", "redirect": "/personal-data"}
        elif any(keyword in message_lower for keyword in auth_keywords):
            return {"response": "Для авторизации в системе перейдите по ссылке: <a href='/auth' target='_blank' class='text-primary hover:underline'>Вход в систему</a>", "redirect": "/auth"}
        
        # Use the real AI to generate response
        response = generate_sharia_advice(message, conversation_history, ai_client)
        return {"response": response}
    except Exception as e:
        # Fallback to simulated response if AI fails
        fallback_responses = [
            "Извините, произошла ошибка при обработке вашего запроса.",
            "К сожалению, я не могу обработать ваш запрос в данный момент.",
            "Пожалуйста, попробуйте еще раз через несколько минут."
        ]
        return {"response": random.choice(fallback_responses)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

