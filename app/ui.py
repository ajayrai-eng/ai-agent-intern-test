import os
import streamlit as st
from dotenv import load_dotenv

from app.agent import SupportAgent


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="Aster & Row Support",
    page_icon="🛍️",
    layout="centered",
)


# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            max-width: 900px;
            margin: auto;
        }

        .hero {
            padding: 25px 0 10px 0;
        }

        .hero h1 {
            margin-bottom: 5px;
        }

        .hero p {
            color: #666;
            font-size: 16px;
        }

        .source {
            font-size: 12px;
            color: #777;
            margin-top: 8px;
        }

        .status {
            padding: 8px 12px;
            border-radius: 8px;
            background: #f1f5f9;
            margin-bottom: 15px;
            font-size: 13px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🛍️ Aster & Row Support</h1>
        <p>
            AI-powered customer support for orders, returns,
            shipping, products, and policies.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "agent" not in st.session_state:
    st.session_state.agent = SupportAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        """
        This demo uses a retrieval-augmented AI agent to answer
        customer support questions using Aster & Row's knowledge base.
        """
    )

    st.divider()

    st.subheader("Capabilities")

    st.write("📚 Knowledge-base RAG")
    st.write("📦 Order lookup")
    st.write("🧠 Conversation context")
    st.write("🔒 Privacy protection")
    st.write("🛡️ Prompt-injection defense")
    st.write("📎 Source attribution")

    st.divider()

    if st.button("Clear conversation", use_container_width=True):

        st.session_state.agent = SupportAgent()
        st.session_state.messages = []

        st.rerun()


# ---------------------------------------------------------
# Example questions
# ---------------------------------------------------------

if not st.session_state.messages:

    st.markdown(
        '<div class="status">Try one of these questions:</div>',
        unsafe_allow_html=True,
    )

    examples = [
        "What is your return policy?",
        "Where is ORD-1007?",
        "Do you ship internationally?",
        "What about Canada?",
    ]

    cols = st.columns(2)

    for i, example in enumerate(examples):

        with cols[i % 2]:

            if st.button(
                example,
                use_container_width=True
            ):
                st.session_state.pending_question = example
                st.rerun()


# ---------------------------------------------------------
# Display chat history
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------------------------------------------------
# User input
# ---------------------------------------------------------

question = st.chat_input(
    "Ask about returns, shipping, products, or an order..."
)


# Handle example buttons
if (
    "pending_question" in st.session_state
    and st.session_state.pending_question
):

    question = st.session_state.pending_question

    del st.session_state.pending_question


# ---------------------------------------------------------
# Process question
# ---------------------------------------------------------

if question:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                answer = st.session_state.agent.answer(
                    question
                )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as error:

                error_message = (
                    "Sorry, I couldn't process that request. "
                    "Please try again."
                )

                st.error(error_message)

                # Useful during development
                with st.expander("Technical error"):
                    st.code(str(error))

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )