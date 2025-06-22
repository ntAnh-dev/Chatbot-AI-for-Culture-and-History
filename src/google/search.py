import time
import logging
from newspaper import Article
from googlesearch import search
from sentence_transformers import SentenceTransformer, util

# Load BGE-M3 model
model = SentenceTransformer("BAAI/bge-m3")

logging.basicConfig(filename="crawl_errors.log", level=logging.WARNING)

def extract_article_safe(url):
    try:
        article = Article(url, language='vi')
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logging.warning(f"❌ Fail at {url}: {e}")
        return None

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def search_and_get_top_2_chunks(query):
    try:
        urls = list(search(query, num_results=1))
    except Exception as e:
        print(f"❌ Lỗi khi tìm kiếm: {e}")
        return []

    if not urls:
        print("❗ Không tìm thấy URL nào.")
        return []

    url = urls[0]
    print(f"📄 Đang lấy nội dung từ: {url}")
    text = extract_article_safe(url)

    if not text or len(text.strip()) < 300:
        print("❌ Nội dung không đủ dài.")
        return []

    # Tách chunk
    chunks = chunk_text(text, chunk_size=500, overlap=50)

    # Tính embedding và similarity
    query_emb = model.encode(query, convert_to_tensor=True)
    chunk_embs = model.encode(chunks, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, chunk_embs)[0]

    top_indices = scores.topk(k=2).indices

    results = []
    for idx in top_indices:
        idx = idx.item()
        results.append({
            "content": chunks[idx],
            "similarity": float(scores[idx]),
            "source": url
        })

    return results
