from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tools import save_lead_and_notify 
import uvicorn

app = FastAPI()

@app.post("/save-lead")
async def save_lead(request: Request):
    body = await request.json()
    
    tool_call = body["message"]["toolCallList"][0]
    args = tool_call["function"]["arguments"]
    
    result = await save_lead_and_notify(
        name               = args.get("name", ""),
        email              = args.get("email", ""),
        phone              = args.get("phone", ""),
        care_need          = args.get("care_need", ""),
        location           = args.get("location", ""),
        notes              = args.get("notes", ""),
        age                = args.get("age", ""),
        gender             = args.get("gender", ""),
        living_arrangement = args.get("living_arrangement", ""),
        physician          = args.get("physician", ""),
        conditions         = args.get("conditions", ""),
        hospitalizations   = args.get("hospitalizations", ""),
        medications        = args.get("medications", ""),
        allergies          = args.get("allergies", ""),
        care_type          = args.get("care_type", ""),
        care_hours         = args.get("care_hours", ""),
        insurance          = args.get("insurance", ""),
        budget             = args.get("budget", ""),
        home_hazards       = args.get("home_hazards", ""),
        medical_equipment  = args.get("medical_equipment", ""),
        other_factors      = args.get("other_factors", ""),
        transportation     = args.get("transportation", ""),
    )
    
    return JSONResponse({
        "results": [{
            "toolCallId": tool_call["id"],
            "result": str(result)
        }]
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)