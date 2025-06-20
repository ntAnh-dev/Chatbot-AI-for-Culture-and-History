import os
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.retrievers import EnsembleRetriever
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embedding = download_hugging_face_embeddings("BAAI/bge-m3")
eng_embedding = download_hugging_face_embeddings("sentence-transformers/all-MiniLM-L6-v2")

documents_index_name = "chatbot-documents"
documents_index_name_v2 = "chatbot-documents-v2"
entities_index_name = "entities-data"

document_docsearch = PineconeVectorStore.from_existing_index(
  index_name=documents_index_name,
  embedding=embedding
)

document_docsearch_v2 = PineconeVectorStore.from_existing_index(
  index_name=documents_index_name,
  embedding=embedding
)

eng_docsearch = PineconeVectorStore.from_existing_index(
  index_name=documents_index_name,
  embedding=eng_embedding
)

# entity_docsearch = PineconeVectorStore.from_existing_index(
#   index_name=entities_index_name,
#   embedding=embedding
# )

document_retriever = document_docsearch.as_retriever(search_type="mmr", search_kwargs={"k": 3})

document_retriever_v2 = document_docsearch_v2.as_retriever(search_type="mmr", search_kwargs={"k": 3})

eng_retriever = eng_docsearch.as_retriever(search_type="mmr", search_kwargs={"k": 5})

# entity_retriever = entity_docsearch.as_retriever(search_type="mmr", search_kwargs={"k": 5})

combined_retriever = EnsembleRetriever(retrievers=[document_retriever_v2, document_retriever])