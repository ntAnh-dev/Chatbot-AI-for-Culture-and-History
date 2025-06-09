import time
import random
from googlesearch import search
from newspaper import Article
import logging
from pathlib import Path
import json

logging.basicConfig(filename="crawl_errors.log", level=logging.WARNING)

def extract_article_safe(url):
    try:
        article = Article(url, language='vi')
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logging.warning(f"Fail at {url}: {e}")
        return None

# folder_path = Path("../Đình, đền, chùa Việt Nam")
# pdf_files = [f.stem for f in folder_path.glob("*.pdf")]

def is_figure(text):
    forbidden_words = ["đình", "đền", "chùa", "miếu", "đồn", "lễ hội"]
    return not any(word in text.lower() for word in forbidden_words)

with open('../research/entities.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)
# json_data = json.loads('../research/entities.json')

converted_names = []

# for name in pdf_files:
#     if " - " in name:
#         dia_phuong, ten_den = name.split(" - ", 1)
#         # converted = f"Lễ hội {ten_den} - {dia_phuong}"
#         converted = f"{ten_den} - {dia_phuong}"
#         converted_names.append(converted)
#     # else:
#     #     converted_names.append(name)

for item in json_data:
    for subitem in item:
        # if is_figure(subitem[0]) and not subitem[0] in converted_names:
            # converted_names.append(subitem[0])

        for subsubitem in subitem:
            if is_figure(subsubitem) and not subsubitem in converted_names:
                converted_names.append(subsubitem)
            break

crawled_json = {}

print(len(converted_names))
i = 0

for festival in converted_names:
    i+=1
    print(i)
    print(f"🔍 Đang tìm kiếm: {festival}")
    try:
        urls = list(search(festival, num_results=5))
    except Exception as e:
        print(f"❌ Lỗi khi tìm kiếm Google: {e}")
        continue

    temp = {}
    for url in urls:
        print(f"⏬ Lấy bài từ: {url}")
        text = extract_article_safe(url)
        if text:
            temp[url] = text
        else:
            print(f"Bỏ qua {url} vì lỗi.\n")
        
        # 💤 Nghỉ ngẫu nhiên sau mỗi request (giảm nguy cơ bị chặn)
        time.sleep(5)

    crawled_json[festival] = temp
    print(f"✅ Đã lưu dữ liệu {festival}.\n")

    # 💤 Delay sau mỗi lần tìm kiếm Google (tránh Google block IP)
    time.sleep(20)

# Ghi ra file JSON
with open("figure_crawl.json", "w", encoding="utf-8") as f:
    json.dump(crawled_json, f, ensure_ascii=False, indent=2)

print("✅ Đã lưu figure_crawl.json")
