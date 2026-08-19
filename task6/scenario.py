import json
from agent import run

goal = """
Read all receipt files inside task6/receipts.

For each receipt:
- identify the category
- identify the amount

Calculate the total spending for each category.
You MUST use the calculator tool for all arithmetic.
Do not calculate totals yourself.

Flag any receipt with an amount greater than 500.

Then create task6/report.md containing:
- category totals
- flagged receipts
- a short summary

Use the available tools to complete the task.
"""

result = run(goal)

print(json.dumps(result, indent=2))