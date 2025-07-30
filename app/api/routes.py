import json

from fastapi import APIRouter, HTTPException

from app.schemas.prompt import PromptRequest
from app.services.openai_chat import ask_openai
from app.tools.calculator import evaluate_expression
from app.tools.weather import get_weather_by_location

router = APIRouter()


@router.post("/chat")
async def chat(request: PromptRequest):
    follow_up_messages = [{"role": "user", "content": request.message}]
    try:
        resp = ask_openai(follow_up_messages)
        data = resp.model_dump() if hasattr(resp, "model_dump") else resp
        output = data.get("output", [])

        tool_results = []

        for msg in output:
            if msg.get("type") != "function_call":
                continue

            follow_up_messages.append(msg)
            args = json.loads(msg["arguments"])

            if msg["name"] == "evaluate_expression":
                result = evaluate_expression(**args)
                follow_up_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": msg["call_id"],
                        "output": str(result),
                    }
                )
                tool_results.append(
                    {
                        "tool": "evaluate_expression",
                        "expression": args["expression"],
                        "result": result,
                    }
                )

            elif msg["name"] == "get_weather":
                result = get_weather_by_location(**args)
                follow_up_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": msg["call_id"],
                        "output": json.dumps(result),
                    }
                )
                tool_results.append(
                    {
                        "tool": "get_weather",
                        "location": args["location"],
                        "result": result,
                    }
                )

        if tool_results:
            final_resp = ask_openai(follow_up_messages)
            final_data = (
                final_resp.model_dump()
                if hasattr(final_resp, "model_dump")
                else final_resp
            )
            return {
                "final_llm_response": final_resp.output_text,
                "tool_results": tool_results,
                "raw_model_output": data,
                "raw_followup_output": final_data,
            }
        else:
            return {
                "model_response": resp.output_text,
                "raw_model_output": data,
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
