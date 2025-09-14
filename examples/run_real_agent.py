import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from src.mcp_file_explorer import MCPFileExplorer
from src.config import DEFAULT_PATH

# --- SETUP ---
load_dotenv()

github_token = os.getenv("GITHUB_API_KEY")

if not github_token :
    raise ValueError("GITHUB_API_KEY not found. Please set it in a .env file.")

client = OpenAI(
    api_key=github_token,
    base_url="https://models.github.ai/inference"
)
mcp = MCPFileExplorer(str(DEFAULT_PATH))

# --- DEFINE TOOLS FOR THE AI ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lists all files and directories in a given path.",
            "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "The directory path."}}, "required": ["path"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a specific file.",
            "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "The file path."}}, "required": ["path"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a specific file, overwriting it.",
            "parameters": {"type": "object", "properties": {"path": {"type": "string", "description": "The file path."}, "content": {"type": "string", "description": "The file content."}}, "required": ["path", "content"]},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Deletes a file at a given path inside the sandbox.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The file path."}
                },
                "required": ["path"],
            },
        },
    }
]

available_functions = {
    "list_files": mcp.list_files,
    "read_file": mcp.read_file,
    "write_file": mcp.write_file,
    "delete_file": mcp.delete_file, 
}

# --- AGENT'S MAIN LOOP ---
messages = [
    {"role": "system", "content": "You are a helpful AI assistant with access to a sandboxed file system. You fulfill user requests by calling the available tools. Default file type is text, unless specified by user. Be concise."}
]

print(f"🤖 MCP Agent Initialized. Sandboxed to: {DEFAULT_PATH}")
print("Type your commands below, or type 'exit' or 'quit' to end the session.")

# NEW: The main conversation loop with the user
while True:
    try:
        # Get input from the user in real-time
        user_input = input("\n> ")

        if user_input.lower() in ["exit", "quit"]:
            print("🤖 MCP Agent session terminated. Goodbye!")
            break
        
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        # NEW: Inner loop for the AI to use tools for a single user command
        while True:
            response = client.chat.completions.create(
                model="openai/gpt-4.1",
                messages=messages,
                temperature=1,
                tools=tools,
                tool_choice="auto",
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # If the AI has a final answer (no more tools), print it and break the inner loop
            if not tool_calls:
                final_answer = response_message.content
                print(f"\n🤖 MCP Agent: {final_answer}")
                messages.append({"role": "assistant", "content": final_answer})
                break

            # If the AI wants to use a tool, execute it
            print("--- Agent is using a tool ---")
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"Calling: {function_name}({', '.join(f'{k}={v}' for k, v in function_args.items())})")
                function_to_call = available_functions[function_name]
                function_response = function_to_call(**function_args)
                
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_response),
                    }
                )

    except KeyboardInterrupt:
        print("\n🤖 MCP Agent session terminated by user. Goodbye!")
        break
    except Exception as e:
        print(f"\nAn error occurred: {e}")