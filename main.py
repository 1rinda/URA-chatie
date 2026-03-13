from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Trade Assistant API", version="1.0.0")

# Enable CORS for the frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Models ---

class DutyCalculationRequest(BaseModel):
    hs_code: str
    origin_country: str
    destination_country: str
    item_value: float
    currency: str
    shipping_cost: float

class DutyCalculationResponse(BaseModel):
    import_duty: float
    vat: float
    other_taxes: float
    total_payable: float
    currency: str

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    suggestions: List[str]

# --- Mock Data ---

HS_CODES = {
    "8471.30.01": {"name": "Laptop computers", "duty_rate": 0.10, "vat_rate": 0.20},
    "6403.91.00": {"name": "Leather shoes", "duty_rate": 0.25, "vat_rate": 0.20},
}

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"status": "Trade Assistant API is online"}

@app.post("/calculate-duty", response_model=DutyCalculationResponse)
async def calculate_duty(request: DutyCalculationRequest):
    """
    Calculates import duty and VAT based on HS code and value.
    """
    # Look up rates based on HS code (simplified)
    code_data = HS_CODES.get(request.hs_code)
    if not code_data:
        raise HTTPException(status_code=404, detail="HS code not found")
    
    base_value = request.item_value + request.shipping_cost
    duty = base_value * code_data["duty_rate"]
    vat = (base_value + duty) * code_data["vat_rate"]
    
    return DutyCalculationResponse(
        import_duty=round(duty, 2),
        vat=round(vat, 2),
        other_taxes=0.0,
        total_payable=round(duty + vat, 2),
        currency=request.currency
    )

@app.get("/hs-code-search")
async def search_hs_codes(query: str):
    """
    Searches for HS codes by name or code.
    """
    results = [
        {"code": k, "name": v["name"]} 
        for k, v in HS_CODES.items() 
        if query.lower() in k.lower() or query.lower() in v["name"].lower()
    ]
    return {"results": results}

@app.post("/chat", response_model=ChatResponse)
async def chat_assistant(message: ChatMessage):
    """
    A simple echo chatbot (to be replaced with an LLM/RAG system).
    """
    user_msg = message.message.lower()
    
    if "duty" in user_msg or "calculate" in user_msg:
        reply = "I can help you calculate duties! Please provide the HS code and the value of your shipment."
        suggestions = ["Calculate Laptop Duty", "How is VAT calculated?"]
    elif "hello" in user_msg or "hi" in user_msg:
        reply = "Hello! I am your Trade Assistant. How can I help you today?"
        suggestions = ["Search HS Codes", "Latest Trade News"]
    else:
        reply = f"I've received your message about '{message.message}'. I'm currently in demo mode, but I'll soon be connected to the TradeLogic engine!"
        suggestions = ["Talk to an Agent", "Export Procedures"]
        
    return ChatResponse(reply=reply, suggestions=suggestions)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
