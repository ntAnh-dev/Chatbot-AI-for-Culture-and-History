
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.server.api import app

from src.helper import download_hugging_face_embeddings


# app = Flask(__name__)
# CORS(app)
load_dotenv()

# PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
# GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# embeddings_384 = download_hugging_face_embeddings("BAAI/bge-m3")

# index_name_384 = "cultutreandhistory-bge-m3-new-data"

# docsearch_384 = PineconeVectorStore.from_existing_index(
#     index_name=index_name_384,
#     embedding=embeddings_384
# )

# retriever_384 = docsearch_384.as_retriever(search_type="similarity", search_kwargs={"k":3})

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-pro",
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
#     # other params...
# )

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ]
# )

# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# rag_chain = create_retrieval_chain(retriever_384, question_answer_chain)

# @app.route('/model', methods=['GET'])
# def getModel():
#     return jsonify({"models": models})

# @app.route('/question', methods=['POST'])
# def answer_question():
#     data = request.get_json()
#     if not data or 'question' not in data:
#         return jsonify({"error": "Missing 'question' in request body"}), 400
    
#     question = data['question']

#     if 'model' not in data:
#         response = rag_chain.invoke({"input": question})
#         return jsonify({"answer": response["answer"]})

#     model = data['model']

#     found_item = next((item for item in models if item['model'] == model), None)

#     if found_item == None:
#         response = rag_chain.invoke({"input": question})
#         return jsonify({"answer": response["answer"]})

#     finded_data = retriever_384.invoke(question)
#     contexts = [doc.page_content for doc in finded_data]
#     print(contexts)
#     contexts_string = "\n\n".join(contexts)

#     response = getOutput(provider=found_item["provider"], model=found_item["model"], input=contexts_string)

#     return jsonify({"answer": response.content})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)