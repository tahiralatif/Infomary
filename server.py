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
    name               = args.get("name", "None"),
    email              = args.get("email", "None"),
    phone              = args.get("phone", "None"),
    care_need          = args.get("care_need", "None"),
    location           = args.get("location", "None"),
    notes              = args.get("notes", "None"),
    age                = args.get("age", "None"),
    gender             = args.get("gender", "None"),
    living_arrangement = args.get("living_arrangement", "None"),
    physician          = args.get("physician", "None"),
    conditions         = args.get("conditions", "None"),
    hospitalizations   = args.get("hospitalizations", "None"),
    medications        = args.get("medications", "None"),
    allergies          = args.get("allergies", "None"),
    care_type          = args.get("care_type", "None"),
    care_hours         = args.get("care_hours", "None"),
    insurance          = args.get("insurance", "None"),
    budget             = args.get("budget", "None"),
    home_hazards       = args.get("home_hazards", "None"),
    medical_equipment  = args.get("medical_equipment", "None"),
    other_factors      = args.get("other_factors", "None"),
    transportation     = args.get("transportation", "None"),
   )
    
    return JSONResponse({
        "results": [{
            "toolCallId": tool_call["id"],
            "result": str(result)
        }]
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)