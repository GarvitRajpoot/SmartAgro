import os
import joblib
from datetime import datetime, timedelta
from dotenv import load_dotenv

from google import genai
from google.genai import types

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="SmartAgro API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_KEY:
    print("❌ GEMINI_API_KEY missing in .env")
    client = None
else:
    client = genai.Client(api_key=GEMINI_KEY)

CROP_MODEL_PATH = os.path.join('models', 'crop_recommender.pkl')

try:
    crop_model = joblib.load(CROP_MODEL_PATH)
    print("✅ Crop model loaded")
except Exception as e:
    print(f"❌ Crop model error: {e}")
    crop_model = None

YIELD_MODELS_DIR = 'models/yield_models'
yield_models = {}

if os.path.exists(YIELD_MODELS_DIR):
    for file in os.listdir(YIELD_MODELS_DIR):
        if file.endswith(".pkl"):
            crop_name = file.replace('yield_model_', '').replace('.pkl', '')
            try:
                yield_models[crop_name] = joblib.load(os.path.join(YIELD_MODELS_DIR, file))
            except:
                pass

class FarmData(BaseModel):
    temperature_c: float
    soil_ph: float
    soil_moisture_percent: float
    rainfall_mm: float
    humidity_percent: float
    sunlight_hours: float
    irrigation_type: str
    fertilizer_type: str
    pesticide_usage_ml: float
    total_days: int

class ChatRequest(BaseModel):
    message: str
    history: list = []

@app.get("/")
def home():
    return {"message": "SmartAgro API is running 🚀"}

@app.post("/api/recommend_crop")
async def recommend_crop(data: FarmData):
    if crop_model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        features = [[
            data.temperature_c,
            data.soil_ph,
            data.soil_moisture_percent,
            data.rainfall_mm,
            data.humidity_percent,
            data.sunlight_hours
        ]]

        crop = crop_model.predict(features)[0]
        confidence = crop_model.predict_proba(features).max()

        predicted_yield = 0
        if crop in yield_models:
            predicted_yield = yield_models[crop].predict(features)[0]

        return {
            "recommended_crop": crop,
            "confidence": float(confidence),
            "predicted_yield_kg_per_hectare": round(predicted_yield, 2),
            "sowing_date": (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
            "harvest_date": (datetime.now() + timedelta(days=100)).strftime('%Y-%m-%d')
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/detect_disease")
async def detect_disease(file: UploadFile = File(...)):
    if not client:
        raise HTTPException(status_code=500, detail="AI not initialized")

    try:
        image_bytes = await file.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=file.content_type
                ),
                """
You are a plant disease detection AI.

STRICT RULES:
- Keep output SHORT
- No bullet points, no symbols

FORMAT:
Disease: <max 3 words>
Description: <max 15 words>
Prevention: <max 15 words>

If healthy:
Disease: Healthy
Description: Plant is healthy
Prevention: Maintain watering and nutrients

If unsure:
Disease: Unknown
Description: Could not detect disease
Prevention: Try clearer image
"""
            ]
        )

        reply = ""

        if hasattr(response, "text") and response.text:
            reply = response.text.strip()
        elif response.candidates:
            reply = response.candidates[0].content.parts[0].text.strip()

        reply = reply.replace("\n", " ").strip()

        import re

        disease = re.search(r"Disease:(.*?)(Description:|$)", reply)
        desc = re.search(r"Description:(.*?)(Prevention:|$)", reply)
        prev = re.search(r"Prevention:(.*)", reply)

        return {
            "prediction": disease.group(1).strip() if disease else "Unknown",
            "description": desc.group(1).strip() if desc else "Not available",
            "prevention": prev.group(1).strip() if prev else "Try again"
        }

    except Exception as e:
        print("VISION ERROR:", e)
        return {
            "prediction": "Unknown",
            "description": "Could not analyze image",
            "prevention": "Try again"
        }

@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not client:
        raise HTTPException(status_code=500, detail="AI not initialized")

    try:
        # 🔥 Build conversation context
        history_text = ""

        for msg in req.history[-6:]:  # last 6 messages only
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['text']}\n"

        prompt = f"""
You are SmartAgro Assistant 🌱.

Rules:
- Continue conversation naturally
- If user says "explain in detail", expand previous answer
- Do not ask again unnecessarily
- Give practical agricultural advice

Conversation:
{history_text}

User: {req.message}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        reply = ""

        if hasattr(response, "text") and response.text:
            reply = response.text.strip()
        elif response.candidates:
            reply = response.candidates[0].content.parts[0].text.strip()

        return {"reply": reply}

    except Exception as e:
        print("CHAT ERROR:", e)
        return {"reply": "Error generating response"}