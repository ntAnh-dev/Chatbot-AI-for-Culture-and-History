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
from src.method.rag_with_extract_entity import rag_with_extract_entity
from src.google.search import search_and_get_top_2_chunks

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

def extract_source(top_k):
    source = "\n\n📚 **Nguồn tham khảo:**\n"
    seen = set()
    for doc in top_k:
        source_url = doc[0].metadata["source"] if "source" in doc[0].metadata else None
        if source_url and source_url not in seen:
            source += f"- [{source_url}]({source_url})\n"
            seen.add(source_url)
    return source

def extract_question(questions):
    extra = extra = "\n\n❓ **Câu hỏi mở rộng:**\n"
    for i, q in enumerate(questions):
        extra += f"- 👉 {q}\n"

def method0(prompt): # Using gemini
    response = method(prompt=prompt)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
def method1(prompt): # RAG + sentence-transformers/all-MiniLM-L6-v2 + Dữ liệu thủ công
    json_data = simple_rag_expand(prompt)
    response = json_data['answer']
    suggested_questions = json_data['extra_questions']
    extra = "\n\n❓ **Câu hỏi mở rộng:**\n"
    for i, q in enumerate(suggested_questions):
        extra += f"- 👉 {q}\n"
    for word in (response + extra).split():
        yield word + " "
        time.sleep(0.05)
def method2(prompt): # RAG + BAAI/bge-m3 + Dữ liệu làm đầy
    top_3_similarity = document_docsearch.similarity_search_with_relevance_scores(prompt, k=3)
    json_data = simple_rag_expand(prompt)
    response = json_data['answer']
    suggested_questions = json_data['extra_questions']
    extra = extract_source(top_3_similarity)
    extra += "\n\n❓ **Câu hỏi mở rộng:**\n"
    for i, q in enumerate(suggested_questions):
        extra += f"- 👉 {q}\n"
    for word in (response + extra).split(" "):
        yield word + " "
        time.sleep(0.05)
def method3(question, lastMessage): # RAG + BAAI/bge-m3 + Dữ liệu tổng quát + Phân tách thực thể
    query = build_prompt(text=lastMessage, question=question)
    llm_response = llm.invoke(query)
    contents = llm_response.content.split('\n')
    prompt = contents[0]
    entities = contents[1:]

    extra_context = ""
    if len(entities) > 1:
        for entity in entities:
            top_3_similarity = document_docsearch.similarity_search_with_relevance_scores(entity, k=3)
            top_3_similarity_v2 = document_docsearch_v2.similarity_search_with_relevance_scores(entity, k=3)

            combined = top_3_similarity + top_3_similarity_v2
            combined_sorted = sorted(combined, key=lambda x: x[-1], reverse=True)

            count = 0
            for doc in combined_sorted:
                if int(doc[-1]) >= 0.75:
                    extra_context += doc[0].page_content + "\n"
                    count += 1
                if count >= 2:
                    break
    
    top_3_similarity = document_docsearch.similarity_search_with_relevance_scores(prompt, k=3)
    top_3_similarity_v2 = document_docsearch_v2.similarity_search_with_relevance_scores(prompt, k = 3)
    json_data = rag_with_extract_entity(extra_context + prompt)
    response = json_data['answer']
    suggested_questions = json_data['extra_questions']
    extra = extract_source(top_3_similarity + top_3_similarity_v2)
    extra += "\n\n❓ **Câu hỏi mở rộng:**\n"
    for i, q in enumerate(suggested_questions):
        extra += f"- 👉 {q}\n"
    for word in (response + extra).split(" "):
        yield word + " "
        time.sleep(0.05)
def response_generator(question, lastMessage):
    query = build_prompt(text=lastMessage, question=question)
    llm_response = llm.invoke(query)
    contents = llm_response.content.split('\n')
    prompt = contents[0]
    entities = contents[1:]

    extra_context = ""
    if len(entities) > 1:
        for entity in entities:
            top_3_similarity = document_docsearch.similarity_search_with_relevance_scores(entity, k=3)
            top_3_similarity_v2 = document_docsearch_v2.similarity_search_with_relevance_scores(entity, k=3)

            combined = top_3_similarity + top_3_similarity_v2
            combined_sorted = sorted(combined, key=lambda x: x[-1], reverse=True)

            count = 0
            for doc in combined_sorted:
                if int(doc[-1]) >= 0.75:
                    extra_context += doc[0].page_content + "\n"
                    count += 1
                if count >= 2:
                    break
    
    top_3_similarity = document_docsearch.similarity_search_with_relevance_scores(prompt, k=3)
    top_3_similarity_v2 = document_docsearch_v2.similarity_search_with_relevance_scores(prompt, k = 3)
    results = search_and_get_top_2_chunks(prompt)
    for i, r in enumerate(results):
        if r['similarity'] > 0.75:
            extra_context += r['content']
    json_data = rag_with_extract_entity(extra_context + prompt)
    response = json_data['answer']
    suggested_questions = json_data['extra_questions']
    extra = extract_source(top_3_similarity + top_3_similarity_v2)
    extra += "\n\n❓ **Câu hỏi mở rộng:**\n"
    for i, q in enumerate(suggested_questions):
        extra += f"- 👉 {q}\n"
    for word in (response + extra).split(" "):
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

# Lấy câu trả lời gần nhất từ assistant
def get_last_assistant_response():
    for msg in reversed(st.session_state.messages):
        if msg["role"] == "assistant":
            return msg["content"]
    return ""

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

    last_response = get_last_assistant_response()
    full_prompt = f"{last_response}. {prompt}"

    selected_function = method_map[method]

    with st.chat_message("assistant"):
        response = st.write_stream(selected_function(prompt, last_response))

    st.session_state.messages.append({"role": "assistant", "content": response})