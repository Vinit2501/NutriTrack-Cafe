from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# This uses the key you will set in Vercel
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class FoodPayload(BaseModel):
    food_query: str

@app.post("/api")
def analyze_nutrition(payload: FoodPayload):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # This is where your AI Studio prompt goes!
        prompt = f"""
        Act as a professional nutritionist for NutriTrack Cafe. 
        Analyze the following food item: {payload.food_query}
        1. List Fiber, Sugar, Sodium, Potassium, and Cholesterol.
        2. Provide a 2-sentence summary in English.
        3. Translate that summary into Hindi and Arabic.
        Keep the formatting clean and professional.
        """
        
        response = model.generate_content(prompt)
        return {"analysis": response.text}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
