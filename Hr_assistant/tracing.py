
"""Step 0b: LangSmith tracing.

LangSmith tracing is configured through environment variables.
LangChain automatically detects tracing configuration from the environment.

This module only checks whether tracing is enabled and logs the
agent ID and environment for visibility.
"""

from Hr_assistant import config
from Hr_assistant.logger import get_logger

logger = get_logger(__name__)


def check_langsmith_tracing() -> None:
    """Log whether LangSmith tracing is enabled for this run."""

    tracing_on = config.LANGSMITH_TRACING.lower() == "true"

    if tracing_on and config.LANGSMITH_API_KEY:
        logger.info(
            "LangSmith tracing ENABLED - agent '%s', environment '%s', traces at %s",
            config.LANGSMITH_AGENT_ID,
            config.LANGSMITH_AGENT_ENVIRONMENT,
            "https://smith.langchain.com",
        )
    else:
        logger.info(
            "LangSmith tracing is OFF "
            "(set LANGSMITH_TRACING=true and configure LANGSMITH_API_KEY in .env)"
        )
