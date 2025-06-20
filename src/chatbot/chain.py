from langchain_core.prompts import ChatPromptTemplate
from src.prompt.gemini_prompt import get_answer_prompt, extra_questions_gen_prompt
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.genimi.llm import llm
from langchain.chains import create_retrieval_chain
from  src.embedding.pinecone import document_retriever, combined_retriever, eng_retriever

answer_prompt = ChatPromptTemplate.from_messages(
  [
    ("system", get_answer_prompt),
    ("human", "{input}")
  ]
)

gen_question_prompt = ChatPromptTemplate.from_messages(
  [
    ("system", extra_questions_gen_prompt),
    ("human", "{input}")
  ]
)

gen_answer_chain = create_stuff_documents_chain(llm, answer_prompt)

gen_question_chain = create_stuff_documents_chain(llm, gen_question_prompt)

answer_gen_rag_chain = create_retrieval_chain(combined_retriever, gen_answer_chain)

question_gen_rag_chain = create_retrieval_chain(combined_retriever, gen_question_chain)

eng_rag_chain = create_retrieval_chain(eng_retriever, gen_answer_chain)

simple_rag_chain = create_retrieval_chain(document_retriever, gen_answer_chain)
