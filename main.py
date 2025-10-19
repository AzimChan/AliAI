from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import random
import asyncio
import tempfile
import os
from HalalOpenAi import create_client, generate_sharia_advice
from whisper import transcribe_audio

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
2. ЗАДАВАЙТЕ УТОЧНЯЮЩИЕ ВОПРОСЫ: Если запрос клиента неясен или требует дополнительной информации, обязательно задайте уточняющие вопросы, прежде чем давать ответ.
3. БУДЬТЕ ДОБРЫМИ И УСПОКАИВАЮЩИМИ только для обычных финансовых вопросов
4. БУДЬТЕ КРАЙНЕ СТРОГИМИ И НЕПРИМИРИМЫМИ при любых незаконных, аморальных или опасных решениях
5. НЕМЕДЛЕННО ОСТАНАВЛИВАЙТЕ любые попытки:
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

# Whisper AI endpoint for voice transcription
@app.post("/transcribe")
async def transcribe_voice(audio: UploadFile = File(...)):
    try:
        # Check if file is audio
        if not audio.content_type or not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Transcribe audio
            text = transcribe_audio(temp_file_path, language="ru", filter_false=True)
            
            if text:
                return {"success": True, "text": text}
            else:
                return {"success": False, "text": "", "error": "No speech detected"}
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

# Real AI endpoint using HalalOpenAi
@app.get("/chat")
async def get_ai_response(message: str):
    try:
        # Check if message contains action keywords that should redirect to fake pages
        message_lower = message.lower()
        
        # Use LLM to detect user intent for feature usage
        intent_prompt = f"""
Проанализируй сообщение пользователя и определи, хочет ли он ИСПОЛЬЗОВАТЬ конкретные функции банка или просто спрашивает информацию.

Сообщение пользователя: "{message}"

Доступные функции для перенаправления:
1. QR-код сканер (/qr) - сканирование QR-кодов
2. Депозит калькулятор (/deposit) - открытие, создание, оформление депозитов/вкладов
3. Управление персональными данными (/personal-data) - просмотр, изменение личных данных
4. Авторизация (/auth) - вход в систему, регистрация

Ответь ТОЛЬКО одним словом:
- "qr" - если пользователь хочет сканировать QR-код
- "deposit" - если пользователь хочет открыть/создать депозит или вклад
- "personal" - если пользователь хочет посмотреть/изменить свои данные
- "auth" - если пользователь хочет войти/зарегистрироваться
- "none" - если пользователь просто спрашивает информацию или задает общие вопросы

Примеры:
"Хочу открыть депозит" → deposit
"Создай QR код" → qr
"Покажи мои данные" → personal
"Войти в систему" → auth
"Что такое депозит?" → none
"Расскажи про QR коды" → none
"Как работает авторизация?" → none
"""

        try:
            # Get intent from AI
            intent_response = ai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": intent_prompt}],
                max_tokens=10,
                temperature=0.1
            )
            
            intent = intent_response.choices[0].message.content.strip().lower()
            
            # Redirect based on detected intent
            if intent == "qr":
                return {"response": "Для работы с QR-кодами нажмите кнопку ниже:", "redirect": "/qr", "button": {"text": "Открыть QR-сканер", "url": "/qr", "class": "bg-gradient-to-r from-primary to-secondary hover:from-secondary hover:to-primary text-white px-6 py-3 rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"}}
            elif intent == "deposit":
                return {"response": "Для открытия депозита нажмите кнопку ниже:", "redirect": "/deposit", "button": {"text": "Калькулятор депозитов", "url": "/deposit", "class": "bg-gradient-to-r from-primary to-secondary hover:from-secondary hover:to-primary text-white px-6 py-3 rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"}}
            elif intent == "personal":
                return {"response": "Для управления персональными данными нажмите кнопку ниже:", "redirect": "/personal-data", "button": {"text": "Управление данными", "url": "/personal-data", "class": "bg-gradient-to-r from-primary to-secondary hover:from-secondary hover:to-primary text-white px-6 py-3 rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"}}
            elif intent == "auth":
                return {"response": "Для авторизации в системе нажмите кнопку ниже:", "redirect": "/auth", "button": {"text": "Вход в систему", "url": "/auth", "class": "bg-gradient-to-r from-primary to-secondary hover:from-secondary hover:to-primary text-white px-6 py-3 rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"}}
            
        except Exception as e:
            print(f"Intent detection failed: {e}")
            # Fall through to normal AI response if intent detection fails
        
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

