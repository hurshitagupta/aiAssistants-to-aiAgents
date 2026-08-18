import ast
import operator

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


TOOLS = [
    {
        "name": "read_file",
        "description": "Read and return the contents of a text file.",
        "required_arguments": ["path"],
    },
    {
        "name": "word_count",
        "description": "Count the number of words in the provided text.",
        "required_arguments": ["text"],
    },
    {
        "name": "calculator",
        "description": "Safely evaluate a basic arithmetic expression.",
        "required_arguments": ["expression"],
    },
]

def describe_tools():
    return TOOLS

if __name__ == "__main__":
    print(describe_tools())
    print("Calculator test 1:", calculator("2**10"))
    print(
        "Calculator test 2:",
        calculator("__import__('os')")
    )
