import ast
import operator
from memory import remember, recall
import time
import pathlib

def slow_tool() -> str:
    time.sleep(10)
    return "finished"

def word_count(text: str) -> str:
    return str(len(text.split()))

def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

def calculator(expression: str) -> str:
    try:
        tree = ast.parse(expression, mode="eval")

        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.Mod: operator.mod,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

        def evaluate(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value

            if isinstance(node, ast.BinOp) and type(node.op) in operators:
                left = evaluate(node.left)
                right = evaluate(node.right)
                return operators[type(node.op)](left, right)

            if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
                operand = evaluate(node.operand)
                return operators[type(node.op)](operand)

            raise ValueError("Unsupported expression")

        return str(evaluate(tree.body))

    except Exception as e:
        return f"Error: {e}"


def write_file(path: str, content: str) -> str:
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File written successfully: {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def list_files(folder: str) -> str:
    try:
        path = pathlib.Path(folder)

        if not path.exists():
            return f"Folder not found: {folder}"

        files = [
            str(file)
            for file in path.iterdir()
            if file.is_file()
        ]

        return "\n".join(files)

    except Exception as e:
        return f"Error listing files: {e}"


TOOLS = {
    "read_file": {
        "fn": read_file,
        "args": ["path"],
        "desc": "Read a UTF-8 text file inside the workspace.",
    },
    "word_count": {
        "fn": word_count,
        "args": ["text"],
        "desc": "Count whitespace-separated words.",
    },
    "calculator": {
        "fn": calculator,
        "args": ["expression"],
        "desc": "Evaluate an arithmetic expression safely.",
    },
    "remember": {
    "fn": remember,
    "args": ["key", "value"],
    "desc": "Store a durable fact in long-term memory."
    },
    "recall": {
        "fn": recall,
        "args": ["key"],
        "desc": "Retrieve a durable fact from long-term memory."
    },
    "slow_tool": {
    "fn": slow_tool,
    "args": [],
    "desc": "Test tool that intentionally takes too long."
    },
        "write_file": {
        "fn": write_file,
        "args": ["path", "content"],
        "desc": "Write text content to a file inside the workspace.",
    },
    "list_files": {
    "fn": list_files,
    "args": ["folder"],
    "desc": "List all files inside a folder.",
},
}


def describe_tools() -> str:
    return "\n".join(
        f"- {name}({', '.join(tool['args'])}): {tool['desc']}"
        for name, tool in TOOLS.items()
    )

if __name__ == "__main__":
    print(describe_tools())
    print("Calculator test 1:", calculator("2**10"))
    print(
        "Calculator test 2:",
        calculator("__import__('os')")
    )
