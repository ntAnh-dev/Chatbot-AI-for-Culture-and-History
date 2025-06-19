from flask import Flask, jsonify, request
from flask_cors import CORS
from src.embedding.pinecone import document_docsearch, document_docsearch_v2
from src.chatbot.chain import answer_gen_rag_chain, question_gen_rag_chain
from src.prompt.gemini_prompt import build_prompt
from src.genimi.llm import llm
import json

app = Flask(__name__)
CORS(app)

@app.route('/question', methods=['POST'])
def answer_question():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Missing 'question' in request body"}), 400
    
    question = data['question']
    extra = data['extra']
    full_question = question
    entities = []
    if extra and len(extra) > 0:
        query = build_prompt(text=extra, question=question)
        response = llm.invoke(query)
        contents = response.content.split("\n")
        full_question = contents[0]
        entities = contents[1:]

    top_3_similarity = document_docsearch.similarity_search_with_relevance_scores(full_question, k = 3)
    top_3_similarity_v2 = document_docsearch_v2.similarity_search_with_relevance_scores(full_question, k = 3)
    min_rel = 1
    min_accept = 0.75

    sources = []
    for doc in top_3_similarity_v2 + top_3_similarity:
        if int(doc[-1]) < min_accept: min_rel = doc[-1]
        source_url = doc[0].metadata["source"] if "source" in doc[0].metadata else None
        if source_url: sources.append(source_url)

    extra_context = ""
    for entity in entities:
        top_3_similarity = document_docsearch.similarity_search_with_relevance_scores(entity, k = 3)
        for doc in top_3_similarity:
            if int(doc[-1]) >= min_accept:
                extra_context += doc[0].page_content + '\n'

    if min_rel >= min_accept:
        response = answer_gen_rag_chain.invoke({ "input": extra_context + full_question })
        answer = json.loads(response['answer'][8:-4])
        if "extra_questions" in answer and isinstance(answer["extra_questions"], list):
            answer["extra_questions"].extend(sources)
        else:
            answer["extra_questions"] = sources
        return answer
    else:
        response = question_gen_rag_chain.invoke({ "input": full_question })
        answer = json.loads(response['answer'][8:-4])
        return {
            "answer": "Bạn vui lòng hãy làm rõ câu hỏi của bạn muốn hỏi hơn, có vẻ chúng tôi không tìm thấy các tài liệu liên quan đến câu hỏi của bạn.",
            "extra_questions": answer
        }
    
        # TODO: adding step search google