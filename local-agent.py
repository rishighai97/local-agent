from agents import Agent, OpenAIChatCompletionsModel, OpenAIResponsesModel, Runner, function_tool
from openai import AsyncOpenAI
from datetime import datetime
import pytz
import openai
import json

openai.base_url = "http://localhost:8091"
openai.api_key = 'ollama'


def automatic_timezone_tool_calling(question: str):
    agent = Agent(
        name="Time aware local llm", 
        instructions="You are an assistant which can figure out timezone from function tool",
        model = OpenAIChatCompletionsModel( 
                model="Qwen3-4B",
                openai_client=AsyncOpenAI(api_key="ollama" , base_url="http://127.0.0.1:8091")
            ),
        tools=[get_current_time_function_tool]
        )
    result = Runner.run_sync(
        agent,
        input=question
    )
    
    print(result.final_output)

@function_tool
def get_current_time_function_tool(timezone: str):
    """
    Returns time in requested pytz timezone. 
    Pass the timezone in format that could be understood by pytz.timezone(). 
    For example, "Asia/Tokyo" for Japan time, "UTC" for Coordinated Universal Time, 
    "America/New_York" for Eastern Time (US & Canada), etc.
    """
    return get_current_time_manual_tool(timezone)

def get_current_time_manual_tool(timezone: str):
    tz = pytz.timezone(timezone)
    current_time = datetime.now(tz)
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

def manual_timezone_tool_calling(question: str):
    response = openai.chat.completions.create(
        model="Qwen3-4B",
        messages=[
            {
                'role': 'user', 
                'content': question
             }
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_current_time",
                    "description": "Returns time in requested timezone",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "timezone": {
                                "type": "string",
                                "description": """Timezone of the city. Default to UTC if not provided. 
                                Pass the timezone in format that could be understood by pytz.timezone()"""
                            }
                        },
                        "required": ["timezone"]
                    }
                }
            }
        ]
    )
    message = response.choices[0].message

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        print("Tool call arguments:", args)
        result = get_current_time_manual_tool(**args)
        print(f"""
                    Tool args: {tool_call.function.arguments}
                    Tool name: {tool_call.function.name}
                    Tool call result for timezone {args.get("timezone")}: {result}  
              """)
        print("Tool result:", result)
    else:
        print("No tool calls found in the response.")
        print("Model response:", message.content)

def run():
    #manual_timezone_tool_calling("What is the time in Mumbai?")
    automatic_timezone_tool_calling("What is the time in Mumbai?")
    

if __name__ == '__main__':
    run()