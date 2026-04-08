from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from tools import save_lead_and_notify 
import uvicorn
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.post("/save-lead")
async def save_lead(request: Request):
    try:
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
    except Exception as e:
        print(f"Error in save_lead: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/google-search")
async def google_search_endpoint(request: Request):
    try:
        body = await request.json()

        tool_call = body["message"]["toolCallList"][0]
        args = tool_call["function"]["arguments"]

        query = args.get("query", "")
        if not query:
            return JSONResponse({
                "results": [{
                    "toolCallId": tool_call["id"],
                    "result": "No search query provided."
                }]
            })

        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            print("Error: SERPER_API_KEY not found in environment.")
            return JSONResponse({
                "results": [{
                    "toolCallId": tool_call["id"],
                    "result": "Error: Google Search API key is missing. Please set SERPER_API_KEY in .env."
                }]
            })

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": api_key,
                    "Content-Type": "application/json"
                },
                json={"q": query, "num": 5},
                timeout=10.0
            )

            if response.status_code != 200:
                print(f"Serper API Error: {response.status_code} - {response.text}")
                return JSONResponse({
                    "results": [{
                        "toolCallId": tool_call["id"],
                        "result": f"Error searching Google: {response.text}"
                    }]
                })

            results = response.json()
            organic = results.get("organic", [])

            output = ""
            for r in organic[:5]:
                output += f"• {r.get('title')}: {r.get('snippet')} ({r.get('link')})\n"

        return JSONResponse({
            "results": [{
                "toolCallId": tool_call["id"],
                "result": output or "No results found."
            }]
        })
    except Exception as e:
        print(f"Error in google_search_endpoint: {e}")
        return JSONResponse({
            "results": [{
                "toolCallId": (body.get("message", {}).get("toolCallList", [{}])[0].get("id") if 'body' in locals() else "unknown"),
                "result": f"Internal server error: {str(e)}"
            }]
        })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)