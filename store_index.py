from dotenv import load_dotenv
import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from src.helper import download_hugging_face_embeddings, load_pdf_file, text_split

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

extracted_data = load_pdf_file(data="Data/")
text_chunks = text_split(extracted_data)
embeddings_384 = download_hugging_face_embeddings("sentence-transformers/all-MiniLM-L6-v2")

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name_384 = "cultutreandhistory-384"

# Run for the new index
# pc.create_index(
#     name=index_name_384,
#     dimension=384, # Replace with your model dimensions
#     metric="cosine", # Replace with your model metric
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     ) 
# )

docsearch_384 = PineconeVectorStore.from_documents(
    documents=text_chunks,
    index_name=index_name_384,
    embedding=embeddings_384,
)