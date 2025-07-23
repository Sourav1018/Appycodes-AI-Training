import json

from fastapi import APIRouter, HTTPException

from app.schemas.prompt import PromptRequest
from app.services.openai_chat import ask_openai
from app.tools.calculator import evaluate_expression
from app.tools.weather import get_weather_by_location

router = APIRouter()


@router.post("/chat")
async def chat(request: PromptRequest):
    follow_up_messages = []
    follow_up_messages.append({"role": "user", "content": request.message})
    try:
        resp = ask_openai(follow_up_messages)
        data = resp.model_dump() if hasattr(resp, "model_dump") else resp
        output = data.get("output", [])
        for msg in output:
            if msg.get("name") == "evaluate_expression":
                follow_up_messages.append(msg)
                args = json.loads(msg["arguments"])
                result = evaluate_expression(**args)
                follow_up_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": msg["call_id"],
                        "output": str(result),
                    }
                )

                print(f"follow_up_message call output: {follow_up_messages}")

                # Step 4: Get final response from LLM
                final_resp = ask_openai(follow_up_messages)
                final_data = (
                    final_resp.model_dump()
                    if hasattr(final_resp, "model_dump")
                    else final_resp
                )

                return {
                    "expression": args["expression"],
                    "result": result,
                    "final_llm_response": final_resp.output_text,
                    "raw_model_output": data,
                    "raw_followup_output": final_data,
                }
            elif msg.get("name") == "get_weather":
                follow_up_messages.append(msg)
                args = json.loads(msg["arguments"])
                result = get_weather_by_location(**args)
                follow_up_messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": msg["call_id"],
                        "output": json.dumps(result),
                    }
                )

                # Final LLM response
                final_resp = ask_openai(follow_up_messages)
                final_data = (
                    final_resp.model_dump()
                    if hasattr(final_resp, "model_dump")
                    else final_resp
                )

                return {
                    "location": args["location"],
                    "weather_data": result,
                    "final_llm_response": final_resp.output_text,
                    "raw_model_output": data,
                    "raw_followup_output": final_data,
                }

        # fallback if no function call was made
        return {"model_response": resp.output_text, "raw_model_output": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
