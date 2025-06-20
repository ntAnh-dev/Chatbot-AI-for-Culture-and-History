import streamlit as st
import random
import time
from src.embedding.pinecone import document_docsearch, document_docsearch_v2
from src.chatbot.chain import answer_gen_rag_chain, question_gen_rag_chain
from src.prompt.gemini_prompt import build_prompt
from src.genimi.llm import llm
import json
from src.method.gemini import gemini
from src.method.rag_eng_handmade import rag_eng_handmade
from src.method.simple_rag_expand import simple_rag_expand

# Using "with" notation
with st.sidebar:
    method = st.radio(
        "Phương pháp",
        (
            "Gemini",
            "RAG + sentence-transformers/all-MiniLM-L6-v2 + Dữ liệu thủ công",
            "RAG + BAAI/bge-m3 + Dữ liệu làm đầy",
            "RAG + BAAI/bge-m3 + Dữ liệu tổng quát + Phân tách thực thể",
            "Final"
        )
    )

def method0(prompt): # Using gemini
    response = gemini(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
def method1(prompt): # RAG + sentence-transformers/all-MiniLM-L6-v2 + Dữ liệu thủ công
    response = rag_eng_handmade(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
def method2(prompt): # RAG + BAAI/bge-m3 + Dữ liệu làm đầy
    response = simple_rag_expand(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
def method3(prompt): # RAG + BAAI/bge-m3 + Dữ liệu tổng quát + Phân tách thực thể
    response = rag_eng_handmade(prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
def response_generator(prompt):
    rag_response = answer_gen_rag_chain.invoke({ "input": prompt })
    rag_json = json.loads(rag_response['answer'][8:-4])
    response = rag_json['answer']
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

method_map = {
    "Gemini": method0,
    "RAG + sentence-transformers/all-MiniLM-L6-v2 + Dữ liệu thủ công": method1,
    "RAG + BAAI/bge-m3 + Dữ liệu làm đầy": method2,
    "RAG + BAAI/bge-m3 + Dữ liệu tổng quát + Phân tách thực thể": method3,
    "Final": response_generator
}

st.title("Chatbot For Culture and History")

if "current_method" not in st.session_state:
    st.session_state.current_method = method

if method != st.session_state.current_method:
    st.session_state.messages = [] 
    st.session_state.current_method = method

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Hỏi tôi về đình, đền, chùa Việt Nam"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    selected_function = method_map[method]

    with st.chat_message("assistant"):
        response = st.write_stream(selected_function(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})