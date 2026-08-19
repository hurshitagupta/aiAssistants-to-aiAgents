import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, describe_tools

import uuid
from memory import snapshot
from guards import with_retry, call_with_timeout

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

MAX_STEPS = 15

SYSTEM = f"""
You are an agent that solves the user's goal by using available tools.

Available tools:
{describe_tools()}

Rules:
1. Return exactly ONE valid JSON object on every turn.Do not include explanations, markdown, code fences, or multiple JSON objects.
2. Use a tool when a tool can perform the required operation.
3. Do not perform a tool's job yourself.
4. After receiving a tool result, decide whether another tool is needed.
5. Use action="final" only when the user's goal has been completed.
6. When calling a tool, action must be the tool name and args must contain its required arguments.
7. When finished, action must be "final", args must be {{}}, and answer must contain the final answer.
8. You MUST use the calculator tool for every arithmetic calculation. Never calculate totals, sums, or arithmetic yourself.

Required JSON format:
{{
    "thought": "brief reason for the next action",
    "action": "tool_name or final",
    "args": {{}},
    "answer": "final answer, or empty string if not finished"
}}
"""


@with_retry(attempts=3)
def ask_model(messages):
    response = client.chat.completions.create(
    model=os.environ["OPENROUTER_MODEL"],
    messages=messages,
    temperature=0,
    response_format={"type": "json_object"},
)

    content = response.choices[0].message.content

    if not content:
        print("Model returned no content.")
        print(response)
        return ""

    return content


def parse_decision(raw: str) -> dict:
    if not raw:
        return {
            "action": "invalid",
            "args": {},
            "answer": "",
        }

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "action": "invalid",
            "args": {},
            "answer": "",
        }


def execute_tool(decision: dict) -> str:
    action = decision.get("action")
    args = decision.get("args", {})

    if action not in TOOLS:
        return f"Unknown tool: {action}"

    tool = TOOLS[action]

    # Schema check: verify all required arguments are present
    missing = [
        arg for arg in tool["args"]
        if arg not in args
    ]

    if missing:
        return f"Missing required arguments: {missing}"

    try:

        if action in ["remember", "write_file"]:
            print(f"Confirmation required: allow the agent to perform {action} with {args}?")
            approval = input("Approve? (yes/no): ").strip().lower()

            if approval != "yes":
                return "Action denied: user did not approve the write."
            
        return call_with_timeout(
            tool["fn"],
            args,
            seconds=5.0
        )
    except Exception as e:
        return f"Tool error: {type(e).__name__}: {e}"


def run(goal: str) -> dict:
    history = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": goal},
    ]

    run_id = uuid.uuid4().hex[:8]

    trace = []

    for step in range(1, MAX_STEPS + 1):
        raw = ask_model(history)
        decision = parse_decision(raw)

        trace.append({
            "step": step,
            **decision,
        })

        action = decision.get("action")

        # Agent is finished
        if action == "final":
            snapshot(run_id, history)
            return {
                "answer": decision.get("answer", ""),
                "trace": trace,
            }

        # Model returned invalid JSON
        if action == "invalid":
            history.append({
                "role": "user",
                "content": (
                    "Your previous response was not valid JSON. "
                    "Return exactly one valid JSON object using the required format."
                ),
            })
            continue

        observation = execute_tool(decision)

        trace[-1]["observation"] = observation

        history.append({
            "role": "assistant",
            "content": raw,
        })

        history.append({
            "role": "user",
            "content": (
                f"TOOL RESULT\n"
                f"Tool: {action}\n"
                f"Result:\n{observation}\n\n"
                f"Decide the next action. Return ONLY valid JSON."
            ),
        })

    snapshot(run_id, history)

    return {
        "answer": "Maximum steps reached.",
        "trace": trace,
    }


# if __name__ == "__main__":
    # print(json.dumps(run(
    #     "Remember that my backup deadline is October 1, 2026."
    # ), indent=2))

    # print(json.dumps(run(
    #     "What is my project deadline?"
    # ), indent=2))

    # print(json.dumps(run(
    #     "Run the slow_tool."
    # ), indent=2))
    
    # print(json.dumps(run(
    #         "Use the calculator tool, but do not provide the expression argument."
    #     ), indent=2))
