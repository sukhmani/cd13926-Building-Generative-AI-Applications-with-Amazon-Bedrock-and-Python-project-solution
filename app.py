# app.py
import streamlit as st
from bedrock_utils import valid_prompt, query_knowledge_base, generate_response

st.set_page_config(page_title="Bedrock Chat App", layout="wide")
st.title("Bedrock Chat Application")


MODEL_OPTIONS = [
    "anthropic.claude-3-haiku-20240307-v1:0",
    "anthropic.claude-3-5-sonnet-20240620-v1:0"
]
model_id = st.sidebar.selectbox("Select LLM Model", MODEL_OPTIONS)
kb_id = st.sidebar.text_input("Knowledge Base ID", "QHUGGZNJNV")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2)
top_p = st.sidebar.slider("Top_P", 0.0, 1.0, 0.9)


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


prompt = st.chat_input("What would you like to know?")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    if valid_prompt(prompt):

        kb_results = query_knowledge_base(prompt, kb_id)
        if kb_results:

            context_pieces = []
            for r in kb_results:

                content = r.get("content", {})
                text = ""
                if isinstance(content, dict):

                    text = content.get("text") or content.get("body") or str(content)
                else:
                    text = str(content)
                context_pieces.append(text)
            context = "\n\n".join(context_pieces)
        else:
            context = "No relevant context found in the knowledge base."

        full_prompt = f"Context:\n{context}\n\nUser question:\n{prompt}\n\nAnswer:"
        response = generate_response(full_prompt, model_id, temperature, top_p)
    else:
        response = "Sorry, I can only answer questions related to heavy machinery."


    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
