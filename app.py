
"""Streamlit interface for the HR Policy Assistant.

Run with:
    streamlit run app.py
"""

from datetime import datetime

import streamlit as st

from Hr_assistant.logger import get_logger
from Hr_assistant.pipeline import build_hr_assistant


logger = get_logger(__name__)

st.set_page_config(
    page_title="People Policy | HR Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_css() -> None:
    """Apply a simple, accessible color theme to the Streamlit app."""

    st.markdown(
        """
        <style>
        /* ---------- Main application ---------- */

        .stApp {
            background-color: #F5F7F4;
            color: #24332C;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #F5F7F4;
        }

        [data-testid="stHeader"] {
            background-color: #F5F7F4;
        }

        .block-container {
            max-width: 1100px;
            padding-top: 2.5rem;
            padding-bottom: 2rem;
        }

        /* ---------- Headings and normal text ---------- */

        h1, h2, h3 {
            color: #173D30 !important;
        }

        p, li, label {
            color: #28372F;
        }

        .hero-title {
            font-family: Georgia, serif;
            font-size: clamp(2.3rem, 5vw, 4.2rem);
            font-weight: 700;
            line-height: 1.08;
            color: #173D30;
            margin: 0.5rem 0 1rem 0;
        }

        .eyebrow {
            color: #477653;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .hero-copy {
            max-width: 720px;
            color: #526158;
            font-size: 1.05rem;
            line-height: 1.7;
        }

        /* ---------- Sidebar ---------- */

        [data-testid="stSidebar"] {
            background-color: #173D30;
            border-right: 1px solid #2D5747;
        }

        [data-testid="stSidebar"] * {
            color: #F5F8F4;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] .stCaption {
            color: #D6E3D9;
        }

        [data-testid="stSidebar"] hr {
            border-color: #496B5A;
        }

        [data-testid="stSidebar"] .stButton button {
            background-color: #285640;
            color: #FFFFFF;
            border: 1px solid #739580;
            border-radius: 9px;
            font-weight: 600;
        }

        [data-testid="stSidebar"] .stButton button:hover {
            background-color: #356C4E;
            border-color: #C6E4B5;
        }

        .status-dot {
            color: #B8E28B;
            font-size: 1.1rem;
        }

        /* ---------- Feature cards ---------- */

        .feature-card {
            background-color: #E8F0E7;
            border: 1px solid #D5E2D4;
            border-radius: 14px;
            padding: 1.15rem;
            min-height: 120px;
        }

        .feature-card strong {
            display: block;
            color: #214D37;
            margin: 0.5rem 0;
            font-size: 1rem;
        }

        .feature-card span {
            color: #526458;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* ---------- Chat messages ---------- */

        [data-testid="stChatMessage"] {
            border: 1px solid #DFE5DF;
            border-radius: 14px;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
            background-color: #FFFFFF;
        }

        /* Assistant response: white background, dark readable text */
        [data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-assistant"]
        ) {
            background-color: #FFFFFF;
            border-color: #DDE5DD;
        }

        /* User question: light green background, dark readable text */
        [data-testid="stChatMessage"]:has(
            [data-testid="chatAvatarIcon-user"]
        ) {
            background-color: #E5F2E7;
            border-color: #C8E0CC;
        }

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] em {
            color: #26352D !important;
            line-height: 1.7;
        }

        [data-testid="stChatMessage"] a {
            color: #176B43 !important;
            text-decoration: underline;
        }

        [data-testid="stChatMessage"] code {
            color: #243D2F !important;
            background-color: #EEF2EC;
        }

        /* ---------- Chat input ---------- */

        [data-testid="stChatInput"] {
            background-color: #FFFFFF !important;
            border: 1px solid #B9C9BC !important;
            border-radius: 14px !important;
            box-shadow: 0 2px 8px rgba(24, 54, 37, 0.06);
        }

        [data-testid="stChatInput"]:focus-within {
            border-color: #397A50 !important;
            box-shadow: 0 0 0 2px rgba(57, 122, 80, 0.15);
        }

        [data-testid="stChatInput"] textarea {
            color: #202D25 !important;
            -webkit-text-fill-color: #202D25 !important;
            background-color: #FFFFFF !important;
            caret-color: #236B40 !important;
            font-size: 1rem !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #69766D !important;
            -webkit-text-fill-color: #69766D !important;
            opacity: 1 !important;
        }

        [data-testid="stChatInput"] button {
            background-color: #E5F0E5 !important;
            color: #204D34 !important;
            border-radius: 9px !important;
        }

        [data-testid="stChatInput"] button:hover {
            background-color: #D0E5D1 !important;
        }

        /* ---------- Other buttons and form fields ---------- */

        .stButton button {
            border-radius: 9px;
            font-weight: 600;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            background-color: #FFFFFF !important;
            color: #24332C !important;
            border-color: #BCCBBF !important;
        }

        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
            color: #69766D !important;
            opacity: 1 !important;
        }

        /* ---------- Status and helper text ---------- */

        [data-testid="stCaptionContainer"] {
            color: #657269;
        }

        .small-note {
            color: #657269;
            font-size: 0.82rem;
            text-align: center;
            margin-top: 1rem;
        }

        /* Keep alerts readable */
        [data-testid="stAlert"] {
            border-radius: 10px;
        }

        /* Avoid forcing white text on the main page */
        [data-testid="stMain"] {
            color: #26352D;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner=False)
def load_assistant():
    """Create one assistant instance for the Streamlit process."""
    logger.info("Initializing HR assistant for Streamlit.")
    return build_hr_assistant()


def extract_answer(agent, question: str) -> str:
    """Run the agent and convert its final response into plain text."""

    response = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )

    answer = response["messages"][-1].content

    if isinstance(answer, list):
        return "".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in answer
        ).strip()

    return str(answer).strip()


# Apply theme
inject_css()


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------- Sidebar ----------

with st.sidebar:
    st.markdown("## People Policy")

    st.markdown(
        "<span class='status-dot'>●</span> "
        "<span>Policy assistant online</span>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("**A private place for policy questions.**")
    st.caption(
        "Answers are grounded in your company HR policy document."
    )

    st.markdown("### Try asking")

    suggestions = [
        "How many annual leave days do I have?",
        "What is the probation notice period?",
        "What are the work-from-home rules?",
    ]

    for suggestion in suggestions:
        if st.button(
            suggestion,
            key=f"suggestion_{suggestion}",
            use_container_width=True,
        ):
            st.session_state.pending_question = suggestion
            st.rerun()

    st.divider()

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pending_question", None)
        st.rerun()

    st.caption(
        "For policy guidance only — contact People Ops for personal cases."
    )


# ---------- Main page ----------

st.markdown(
    "<div class='eyebrow'>YOUR POLICY, MADE CLEAR</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div class='hero-title'>HR answers, without the hunt.</div>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p class="hero-copy">
        Ask in plain language. I'll search your company's HR policy
        and give you a clear, practical answer.
    </p>
    """,
    unsafe_allow_html=True,
)


if not st.session_state.messages:
    columns = st.columns(3)

    cards = [
        (
            "◌",
            "Leave & holidays",
            "Time off, eligibility and public holidays",
        ),
        (
            "⌂",
            "Flexible work",
            "Remote work and workplace guidelines",
        ),
        (
            "✦",
            "Your journey",
            "Probation, benefits and exit policies",
        ),
    ]

    for column, (icon, title, description) in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div class="feature-card">
                    <span>{icon}</span>
                    <strong>{title}</strong>
                    <span>{description}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("")


# ---------- Initialize assistant ----------

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


# ---------- Display previous messages ----------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------- Accept user question ----------

question = st.chat_input(
    "Ask about leave, benefits, remote work, or any HR policy..."
)

# Support sidebar suggestion buttons
if not question:
    question = st.session_state.pop("pending_question", None)


# ---------- Generate answer ----------

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
            "time": datetime.now().isoformat(),
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Looking through the policy..."):
            try:
                answer = extract_answer(assistant, question)

                if not answer:
                    answer = (
                        "I couldn't find a clear answer in the policy. "
                        "Please try rephrasing your question."
                    )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "time": datetime.now().isoformat(),
                    }
                )

                logger.info(
                    "Answered HR policy question successfully."
                )

            except Exception:
                logger.exception("Failed to answer HR policy question.")

                answer = (
                    "Sorry, I couldn't process that question right now. "
                    "Please try again in a moment."
                )

                st.error(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )


st.markdown(
    """
    <p class="small-note">
        Responses are based on the HR policy document available to this assistant.
    </p>
    """,
    unsafe_allow_html=True,
)
