# LangSmith Tracing

**Branch:** `langsmith-tracing` (built on top of `logging`)

## What is LangSmith?

LangSmith is LangChain's observability platform. Where our own `logger.py` (see [logger.md](logger.md)) writes plain-text logs to a file on your machine, LangSmith captures structured, visual **traces** of LLM and agent execution and displays them on a dashboard at smith.langchain.com.

A trace helps you understand:

- Every step the agent performed (LLM call → tool call → LLM call → final answer).
- The exact prompt sent to the LLM and the response received.
- Token usage and associated cost (when available).
- Execution time (latency) of individual steps.
- Errors that occurred during execution.

## Logging vs. Tracing — Why Do We Want Both?

| | `logger.py` (Our Own Logs) | LangSmith Tracing |
|---|---|---|
| Where it lives | `logs/` folder on your machine, plain text | smith.langchain.com, a web dashboard |
| What it shows | Events we explicitly log using `logger.info()` | Structured LLM and tool execution details |
| Best for | Quick debugging and tracking application events | Understanding LLM behavior, debugging agent execution, comparing runs, and analyzing latency and token usage |

They're complementary: our logs tell a short story of the application run, while LangSmith provides detailed visibility into LLM and agent execution.

## How It Works (No Manual Tracing Code Needed!)

LangChain supports automatic LangSmith tracing through environment variables.

For this configuration, add the following variables to your `.env` file:

```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=<your_api_key>

LANGSMITH_AGENT_ID=hrpolicy
LANGSMITH_AGENT_ENVIRONMENT=local
```

### Understanding the Environment Variables

- `LANGSMITH_TRACING=true` — Enables LangSmith tracing. Set it to `false` to disable tracing.
- `LANGSMITH_ENDPOINT` — Specifies the LangSmith API endpoint where traces are sent.
- `LANGSMITH_API_KEY` — Your LangSmith API key, available under Settings → API Keys. Never commit this key to GitHub.
- `LANGSMITH_AGENT_ID` — Identifies the agent associated with your tracing or agent integration.
- `LANGSMITH_AGENT_ENVIRONMENT` — Identifies the environment associated with the agent, such as `local`, `development`, or `production`.

**Important:** `LANGSMITH_AGENT_ID` and `LANGSMITH_AGENT_ENVIRONMENT` are agent-related configuration variables. They are not direct replacements for `LANGSMITH_PROJECT` in standard LangChain tracing.

For traditional LangChain project-based tracing, you can continue using:

```env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=<your_api_key>
LANGSMITH_PROJECT=hrrag
```

Use the configuration required by your particular LangSmith integration.

Because `config.py` already calls `load_dotenv()`, environment variables stored in `.env` are loaded into the application environment.

## What We Added on Top of Automatic Tracing

Setting the environment variables is sufficient to enable automatic tracing in supported LangChain integrations.

However, for this project, we also want to make tracing status visible in our application logs.

Therefore, we created a small `tracing.py` module that uses our existing logger to print one message at the beginning of every run.

Example when tracing is enabled:

```text
LangSmith tracing ENABLED - agent 'hrpolicy',
environment 'local', traces at https://smith.langchain.com
```

Example when tracing is disabled:

```text
LangSmith tracing is OFF
```

This module does not enable tracing itself. It only checks the environment configuration and logs the status.

## Files Changed

| File | What Changed |
|---|---|
| `.env` | Added LangSmith tracing and agent configuration variables. This file is gitignored. |
| `.env.example` | Added placeholder values so developers know which environment variables to configure. Safe to commit. |
| `hr_assistant/config.py` | Reads LangSmith environment variables using `os.getenv()`. |
| `hr_assistant/tracing.py` | Added `check_langsmith_tracing()` to log whether tracing is enabled. |
| `hr_assistant/pipeline.py` | Calls `check_langsmith_tracing()` at the beginning of `build_hr_assistant()`. |
| `requirements.txt` | Added `langsmith` explicitly under a new LangSmith tracing section. |

## Updated Configuration in config.py

```python
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

LANGSMITH_AGENT_ID = os.getenv("LANGSMITH_AGENT_ID")
LANGSMITH_AGENT_ENVIRONMENT = os.getenv("LANGSMITH_AGENT_ENVIRONMENT")
```

## Verified Working

The application logs confirm that the tracing configuration is detected:

```text
INFO | Hr_assistant.tracing |
LangSmith tracing ENABLED - agent 'hrpolicy',
environment 'local', traces at https://smith.langchain.com
```

This confirms that the application's tracing-status check recognizes the configured agent ID and environment.

To verify actual trace collection, open your LangSmith dashboard and check whether the corresponding execution appears there.

## Assignment for Students

1. Open your LangSmith dashboard and locate the traces generated by your application.
2. Open a trace and explore:
   - The prompt sent to the LLM.
   - The response generated by the LLM.
   - Token usage.
   - Execution time of individual steps.
   - Tool calls made by the agent.
3. Set `LANGSMITH_TRACING=false` in `.env`, restart the application, and verify that no new traces are generated while the application continues to work.
4. **Optional (Advanced):** LangSmith supports custom metadata and tags. Try tagging individual agent executions with their question topics.

Example:

```python
agent.invoke(
    {"question": "What is the leave policy?"},
    config={
        "tags": ["leave"],
        "metadata": {"topic": "leave"}
    }
)
```

Then open LangSmith and explore how these tags and metadata help you filter and organize traces.

---

**Key Takeaway:** Logging tells us what our application explicitly records. LangSmith tracing helps us understand what happens inside LLM and agent execution. Together, they make debugging and monitoring GenAI applications easier.