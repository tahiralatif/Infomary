from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tools import save_lead_and_notify 
from pyngrok import ngrok, conf
import uvicorn

app = FastAPI()

@app.post("/save-lead")
async def save_lead(request: Request):
    body = await request.json()
    
    tool_call = body["message"]["toolCallList"][0]
    args = tool_call["function"]["arguments"]
    
    result = await save_lead_and_notify(
        name      = args.get("name"),
        email     = args.get("email"),
        phone     = args.get("phone"),
        care_need = args.get("care_need"),
        location  = args.get("location"),
        notes     = args.get("notes", "")
    )
    
    return JSONResponse({
        "results": [{
            "toolCallId": tool_call["id"],
            "result": str(result)
        }]
    })

if __name__ == "__main__":
    ngrok.set_auth_token("3BelbQExlcTxrVJjYbRld78oJfy_7TmEV1CK9obk8dypVCwJr")
    
    public_url = ngrok.connect(8000)
    print("\n" + "="*50)
    print(f"  ✅ VAPI WEBHOOK URL:")
    print(f"  {public_url}/save-lead")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)