"""Streamlit interface for the HR Policy Assistant (dark theme).

Run with:
    streamlit run app.py
"""

from datetime import datetime

import streamlit as st

from Hr_assistant.guardrails import REFUSAL_MESSAGE, check_input, check_output
from Hr_assistant.logger import get_logger
from Hr_assistant.pipeline import build_hr_assistant


logger = get_logger(__name__)

st.set_page_config(
    page_title="People Policy | HR Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

TOPICS = [
    (
        "🌴",
        "Leave & holidays",
        "How many annual leave days do I have?",
    ),
    (
        "🏡",
        "Flexible work",
        "What are the work-from-home rules?",
    ),
    (
        "📝",
        "Probation & exit",
        "What is the probation notice period?",
    ),
]

SUGGESTIONS = [
    "How many annual leave days do I have?",
    "What is the probation notice period?",
    "What are the work-from-home rules?",
    "How do I apply for sick leave?",
]


# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------

def inject_css() -> None:
    """Dark theme with high-contrast text."""

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap');

        :root {
            --bg: #0E1420;
            --surface: #161E2E;
            --surface-2: #1D2739;
            --border: #2B3850;
            --text: #E8EDF5;
            --text-soft: #A9B6CB;
            --accent: #5EEAD4;
            --accent-strong: #2DD4BF;
            --accent-ink: #062B27;
            --user-bg: #1B3A44;
            --user-border: #2F6670;
        }

        html, body, [class*="css"], .stApp {
            font-family: 'DM Sans', system-ui, sans-serif;
        }

        /* ---------- Base ---------- */
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {
            background-color: var(--bg);
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background-color: transparent;
        }

        .block-container {
            max-width: 920px;
            padding-top: 2.2rem;
            padding-bottom: 7rem;
        }

        h1, h2, h3, h4 { color: var(--text) !important; }
        p, li, label, span { color: var(--text); }

        /* ---------- Hero ---------- */
        .hero-title {
            font-family: 'Fraunces', Georgia, serif;
            font-size: clamp(2.2rem, 5vw, 3.6rem);
            font-weight: 700;
            line-height: 1.1;
            letter-spacing: -0.01em;
            color: var(--text);
            margin: 0 0 0.9rem 0;
        }

        .hero-copy {
            max-width: 620px;
            color: var(--text-soft);
            font-size: 1.08rem;
            line-height: 1.7;
            margin-bottom: 1.6rem;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.3rem 0.8rem;
            border: 1px solid var(--border);
            background: var(--surface);
            border-radius: 999px;
            font-size: 0.85rem;
            color: var(--text-soft);
            margin-bottom: 1.2rem;
        }

        .pill .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 0 3px rgba(94, 234, 212, 0.18);
        }

        .section-label {
            color: var(--text-soft);
            font-size: 0.95rem;
            margin: 0.4rem 0 0.6rem 0;
        }

        /* ---------- Sidebar ---------- */
        [data-testid="stSidebar"] {
            background-color: var(--surface);
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * { color: var(--text); }

        [data-testid="stSidebar"] .stCaption,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: var(--text-soft) !important;
        }

        [data-testid="stSidebar"] hr { border-color: var(--border); }

        .brand {
            font-family: 'Fraunces', Georgia, serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.2rem;
        }

        .brand-sub {
            color: var(--text-soft);
            font-size: 0.9rem;
            margin-bottom: 0.4rem;
        }

        .stat-box {
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 0.7rem 0.9rem;
            margin-top: 0.4rem;
            color: var(--text-soft);
            font-size: 0.9rem;
        }

        .stat-box b { color: var(--accent); font-size: 1.1rem; }

        /* ---------- Buttons ---------- */
        .stButton button {
            background-color: var(--surface-2);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 12px;
            font-weight: 500;
            text-align: left;
            padding: 0.6rem 0.9rem;
            transition: border-color 0.15s ease, background-color 0.15s ease;
        }

        .stButton button:hover {
            background-color: #243149;
            border-color: var(--accent-strong);
            color: #FFFFFF;
        }

        .stButton button:focus-visible {
            outline: 2px solid var(--accent);
            outline-offset: 2px;
        }

        .stButton button p { color: inherit; }

        /* ---------- Chat messages ---------- */
        [data-testid="stChatMessage"] {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.9rem;
        }

        /* User bubble */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background-color: var(--user-bg);
            border-color: var(--user-border);
        }

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {
            color: var(--text) !important;
            line-height: 1.75;
        }

        [data-testid="stChatMessage"] a {
            color: var(--accent) !important;
            text-decoration: underline;
        }

        [data-testid="stChatMessage"] code {
            color: var(--accent) !important;
            background-color: #0B111B;
            border-radius: 6px;
            padding: 0.1rem 0.35rem;
        }

        [data-testid="stChatMessage"] table,
        [data-testid="stChatMessage"] th,
        [data-testid="stChatMessage"] td {
            color: var(--text) !important;
            border-color: var(--border) !important;
        }

        /* ---------- Chat input ---------- */
        [data-testid="stBottom"],
        [data-testid="stBottom"] > div {
            background-color: var(--bg) !important;
        }

        [data-testid="stChatInput"] {
            background-color: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 16px !important;
        }

        [data-testid="stChatInput"]:focus-within {
            border-color: var(--accent-strong) !important;
            box-shadow: 0 0 0 3px rgba(45, 212, 191, 0.18);
        }

        [data-testid="stChatInput"] textarea {
            background-color: var(--surface) !important;
            color: var(--text) !important;
            -webkit-text-fill-color: var(--text) !important;
            caret-color: var(--accent) !important;
            font-size: 1rem !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: var(--text-soft) !important;
            -webkit-text-fill-color: var(--text-soft) !important;
            opacity: 1 !important;
        }

        [data-testid="stChatInput"] button {
            background-color: var(--accent-strong) !important;
            color: var(--accent-ink) !important;
            border-radius: 10px !important;
        }

        [data-testid="stChatInput"] button:hover {
            background-color: var(--accent) !important;
        }

        /* ---------- Misc ---------- */
        [data-testid="stCaptionContainer"] { color: var(--text-soft); }

        [data-testid="stAlert"] { border-radius: 12px; }

        [data-testid="stExpander"] {
            background-color: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
        }

        .small-note {
            color: var(--text-soft);
            font-size: 0.82rem;
            text-align: center;
            margin-top: 1.2rem;
        }

        @media (prefers-reduced-motion: reduce) {
            * { transition: none !important; animation: none !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Assistant
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def load_assistant():
    """Create one assistant instance for the Streamlit process."""
    logger.info("Initializing HR assistant for Streamlit.")
    return build_hr_assistant()


def extract_answer(agent, question: str) -> str:
    """Run the guardrails and the agent, and return plain text."""

    logger.info("User question: '%s'", question)

    # Input guard: block unsafe or out-of-scope questions
    input_is_safe, _ = check_input(question)
    if not input_is_safe:
        return REFUSAL_MESSAGE

    response = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )

    answer = response["messages"][-1].content

    if isinstance(answer, list):
        answer = "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in answer
        )

    answer = str(answer).strip()
    logger.info("Final answer: '%s'", answer)

    # Output guard: block unsafe answers
    output_is_safe, _ = check_output(answer)
    if not output_is_safe:
        return REFUSAL_MESSAGE

    return answer


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

inject_css()

if "messages" not in st.session_state:
    st.session_state.messages = []


def queue_question(question: str) -> None:
    """Queue a question and rerun so it is handled in the main flow."""
    st.session_state.pending_question = question
    st.rerun()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("<div class='brand'>People Policy</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='brand-sub'>Your HR policy assistant</div>",
        unsafe_allow_html=True,
    )
    st.caption("Answers come from your company's HR policy document.")

    user_turns = sum(1 for m in st.session_state.messages if m["role"] == "user")
    st.markdown(
        f"<div class='stat-box'><b>{user_turns}</b> "
        f"question{'s' if user_turns != 1 else ''} asked this session</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("**Try asking**")
    for suggestion in SUGGESTIONS:
        if st.button(
            suggestion,
            key=f"suggestion_{suggestion}",
            use_container_width=True,
        ):
            queue_question(suggestion)

    st.divider()

    if st.button(
        "Clear conversation",
        key="clear_chat",
        use_container_width=True,
        disabled=not st.session_state.messages,
    ):
        st.session_state.messages = []
        st.session_state.pop("pending_question", None)
        st.rerun()

    st.caption(
        "For policy guidance only. Contact People Ops for personal cases."
    )


# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------

if not st.session_state.messages:
    st.markdown(
        "<div class='pill'><span class='dot'></span>Policy assistant online</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='hero-title'>HR answers, without the hunt.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='hero-copy'>Ask in plain language. I search your company's "
        "HR policy and give you a clear, practical answer.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='section-label'>Pick a topic to start</div>",
        unsafe_allow_html=True,
    )

    columns = st.columns(3)
    for column, (icon, title, question_text) in zip(columns, TOPICS):
        with column:
            if st.button(
                f"{icon}  {title}",
                key=f"topic_{title}",
                use_container_width=True,
            ):
                queue_question(question_text)
else:
    st.markdown(
        "<div class='hero-title' style='font-size:1.8rem;'>"
        "Policy conversation</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Initialize assistant
# ---------------------------------------------------------------------------

try:
    assistant = load_assistant()

except Exception as error:
    logger.exception("HR assistant initialization failed.")

    st.error(
        "I couldn't start the policy assistant. "
        "Check your API keys, policy document, and application logs."
    )

    with st.expander("Technical details"):
        st.exception(error)

    st.stop()


# ---------------------------------------------------------------------------
# Conversation
# ---------------------------------------------------------------------------

for message in st.session_state.messages:
    avatar = "🧑" if message["role"] == "user" else "💬"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


question = st.chat_input(
    "Ask about leave, benefits, remote work, or any HR policy..."
)

# Support sidebar and topic buttons
if not question:
    question = st.session_state.pop("pending_question", None)


if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "time": datetime.now().isoformat(),
        }
    )

    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="💬"):
        with st.spinner("Looking through the policy..."):
            try:
                answer = extract_answer(assistant, question)

                if not answer:
                    answer = (
                        "I couldn't find a clear answer in the policy. "
                        "Try rephrasing your question."
                    )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "time": datetime.now().isoformat(),
                    }
                )

                logger.info("Answered HR policy question successfully.")

            except Exception:
                logger.exception("Failed to answer HR policy question.")

                answer = (
                    "I couldn't process that question. "
                    "Please try again in a moment."
                )

                st.error(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "time": datetime.now().isoformat(),
                    }
                )

    st.rerun()


st.markdown(
    "<p class='small-note'>Responses are based on the HR policy document "
    "available to this assistant.</p>",
    unsafe_allow_html=True,
)