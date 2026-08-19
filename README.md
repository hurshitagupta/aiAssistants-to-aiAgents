# From AI Assistants to AI Agents

## Project Overview

This project was completed as part of the **From AI Assistants to AI Agents — Hands-On Assessment**.

The project incrementally transforms a basic stateless AI assistant into an agent capable of using tools, reasoning through multi-step goals, maintaining memory, handling failures with guardrails, producing written artefacts, and recording structured traces.

Each task builds on the previous one and is stored in a separate task folder.

---

## Project Structure

```text
aiAssistants_to_aiAgents/
│
├── task1/
├── task2/
├── task3/
├── task4/
├── task5/
├── task6/
│   ├── receipts/
│   ├── agent.py
│   ├── tools.py
│   ├── scenario.py
│   └── report.md
│
├── traces/
├── memory.json
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone <https://github.com/hurshitagupta/aiAssistants-to-aiAgents.git>
cd aiAssistants_to_aiAgents
```

### 2. Install dependencies

Python 3.10+ is required.

```bash
pip install -r requirements.txt
```

Dependencies:

```text
openai==2.24.0
python-dotenv==1.2.2
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```text
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=your_model_name_here
```

API keys are loaded through environment variables and are not stored in the source code.

---

# Tasks

## Task 1 — The Stateless Baseline

Task 1 implements a basic prompt-completion assistant with no tools, memory, or agent loop.

The assistant was asked how many words were present in `notes.txt`. Since it had no ability to access the file, it could not reliably answer the question.

This establishes the baseline difference between a normal AI assistant and an AI agent.

### Run

```bash
python task1/assistant.py
```

---

## Task 2 — Tools with Real Schemas

Task 2 introduces tools that allow the system to perform operations instead of relying only on the model.

The tools include:

* `read_file` — reads a text file.
* `word_count` — counts whitespace-separated words.
* `calculator` — safely evaluates arithmetic expressions using Python AST.

The calculator accepts valid arithmetic such as `2**10` while rejecting unsafe expressions such as `__import__('os')`.

### Run

```bash
python task2/tools.py
```

---

## Task 3 — The Agent Loop

Task 3 converts the tool-enabled assistant into an agent using a:

**Reason → Act → Observe** loop.

The model selects a tool, the program executes it, and the result is returned to the model as an observation. The model then decides its next action.

The agent successfully solves the `notes.txt` goal using multiple tool calls.

A `MAX_STEPS` limit prevents the agent from looping indefinitely.

### Run

```bash
python task3/agent.py
```

---

## Task 4 — Memory and State

Task 4 introduces short-term and long-term memory.

Short-term memory is maintained through the message history during the current agent run.

Long-term memory is implemented using:

* `remember` — stores a durable fact.
* `recall` — retrieves a stored fact.

Durable information is stored in `memory.json`, allowing it to survive between separate Python processes.

Completed runs are also saved as structured JSON traces.

### Run

```bash
python task4/agent.py
```

---

## Task 5 — Robustness and Guardrails

Task 5 introduces controls that make the agent safer and more reliable.

The implemented guardrails include:

* **Step limit** — prevents infinite agent loops.
* **Timeout** — prevents a hanging tool from blocking the agent.
* **Retry** — retries failed model calls with exponential backoff.
* **Schema validation** — rejects missing required tool arguments.
* **Confirmation** — requires user approval before write operations.
* **Secret hygiene** — keeps API keys outside the source code.

Each guardrail was deliberately tested to demonstrate that it works.

### Run

```bash
python task5/agent.py
```

---

## Task 6 — Real-World Scenario: Expense Triage

Task 6 applies the agent architecture to a real-world expense-triage scenario.

The agent:

1. Discovers receipt files.
2. Reads each receipt.
3. Identifies categories and amounts.
4. Calculates category totals.
5. Flags receipts greater than $500.
6. Generates a written expense report.

The tools used include:

* `list_files`
* `read_file`
* `calculator`
* `write_file`

The generated artefact is:

```text
task6/report.md
```

The `write_file` action requires explicit user confirmation before the report is created.

### Run

```bash
python task6/scenario.py
```

### Failure Case and Fix

During testing, the model occasionally returned malformed structured output. Some responses contained explanatory text before the JSON or multiple JSON objects.

Because the agent uses `json.loads()` to parse model responses, these responses were marked as `invalid`, and the requested tool was not executed during that iteration.

To improve reliability, JSON response mode was enabled and the system prompt was strengthened to require exactly one JSON object without additional explanations or Markdown.

The invalid-response recovery mechanism was also retained. Therefore, if malformed output is still produced, the agent provides corrective feedback to the model and continues the loop instead of crashing.

---

## Traces

The `traces/` folder contains structured JSON snapshots of agent runs.

Each trace records information such as:

* Step
* Thought
* Action
* Arguments
* Observation

These traces make the agent's behaviour inspectable and replayable.

---

# Reflection

This assessment demonstrated the practical difference between a traditional AI assistant and an AI agent. At the beginning, the system could only receive a prompt and generate a response. Even a simple question about a local file could not be answered reliably because the model had no ability to interact with its environment.

Adding tools allowed the model to perform actions such as reading files, counting words, and calculating expressions. However, tools alone did not make the system fully agentic. The major transition happened when the Reason → Act → Observe loop was introduced. The model could choose an action, observe its result, and use that information to decide what to do next.

Memory added continuity to the system. Short-term message history preserved information during a run, while persistent JSON memory allowed facts to survive across separate processes.

The robustness task showed that autonomy also requires limits. Step limits, timeouts, retries, schema validation, confirmation, and secret hygiene made the agent safer and more reliable.

Task 6 brought these concepts together through an expense-triage workflow. The agent discovered files, read receipts, performed calculations through tools, identified high-value expenses, and generated a report. One important learning experience was handling malformed model output. Requesting JSON output improved reliability, but occasional invalid responses still occurred. Instead of assuming that model responses would always be perfect, the agent used recovery logic to detect invalid output, provide corrective feedback, and continue safely.

Overall, this assessment showed that an AI agent is not simply a more advanced prompt. It is a system that combines an LLM with tools, state, an execution loop, persistent memory, guardrails, and traceability. Building these capabilities incrementally made the evolution from a basic assistant to an autonomous agent clear and practical.


