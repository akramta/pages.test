# from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse, JSONResponse
# from fastapi.templating import Jinja2Templates
# from google import genai

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# # إعداد عميل GenAI
# client = genai.Client(api_key="AIzaSyCLuANVl6WdljIO8IPEdxPDW6xtsgWV_Ms")

# # حفظ كل المحادثة
# chat_history = []

# @app.get("/", response_class=HTMLResponse)
# async def get_chat(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/ask")
# async def ask(question: str = Form(...)):
#     # إضافة رسالة المستخدم للتاريخ
#     chat_history.append({"role": "user", "message": question})

#     # بناء محتوى الطلب للنموذج مع التاريخ كله
#     prompt = "أنت مساعد برمجي. اسمه أكرم فؤاد الصالحي. تذكر المحادثة السابقة:\n"
#     prompt += "أنا هنا لمساعدتك في حل مشاكلك البرمجية فقط. إذا كان السؤال خارج نطاق البرمجة، اعتذر.\n\n"
    
#     for msg in chat_history:
#         role = "مستخدم" if msg["role"] == "user" else "بوت"
#         prompt += f"{role}: {msg['message']}\n"

#     # إرسال الطلب لـ GenAI
#     response = client.models.generate_content(
#         model="gemini-1.5-flash",
#         contents=prompt
#     )

#     # إضافة رد البوت للتاريخ
#     chat_history.append({"role": "bot", "message": response.text})

#     return JSONResponse({"answer": response.text})

# @app.get("/history")
# async def get_history():
#     return JSONResponse(chat_history)
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from google import genai
import os

app = FastAPI()

# تعديل المسار ليكون المجلد الحالي حيث يوجد index.html
templates = Jinja2Templates(directory=os.path.dirname(__file__))

# إعداد عميل GenAI
client = genai.Client(api_key="AIzaSyCLuANVl6WdljIO8IPEdxPDW6xtsgWV_Ms")

# حفظ كل المحادثة
chat_history = []

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask(question: str = Form(...)):
    # إضافة رسالة المستخدم للتاريخ
    chat_history.append({"role": "user", "message": question})

    # بناء محتوى الطلب للنموذج مع التاريخ كله
    prompt = "أنت مساعد برمجي. اسمه أكرم فؤاد الصالحي. تذكر المحادثة السابقة:\n"
    prompt += "أنا هنا لمساعدتك في حل مشاكلك البرمجية فقط. إذا كان السؤال خارج نطاق البرمجة، اعتذر.\n\n"
    
    for msg in chat_history:
        role = "مستخدم" if msg["role"] == "user" else "بوت"
        prompt += f"{role}: {msg['message']}\n"

    # إرسال الطلب لـ GenAI
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    # إضافة رد البوت للتاريخ
    chat_history.append({"role": "bot", "message": response.text})

    return JSONResponse({"answer": response.text})

@app.get("/history")
async def get_history():
    return JSONResponse(chat_history)
