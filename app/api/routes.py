import json
from fastapi import APIRouter, HTTPException
from app.schemas.prompt import PromptRequest
from app.services.openai_chat import ask_openai
from app.tools.calculator import evaluate_expression

router = APIRouter()

@router.post("/chat")
async def chat(request: PromptRequest):
    try:
        resp = ask_openai(request.message)
        data = resp.model_dump() if hasattr(resp, "model_dump") else resp
        output = data.get("output", [])
        for msg in output:
            if msg.get("name") == "evaluate_expression":
                args = json.loads(msg["arguments"])
                result = evaluate_expression(**args)
                return {
                    "expression": args["expression"],
                    "result": result,
                    "raw_model_output": data
                }

        # fallback if no function call was made
        return {
            "model_response": resp.output_text,
            "raw_model_output": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
