import os
import json
from PyPDF2 import PdfReader

# Thư mục chứa các file PDF
folder_path = '../Đình, đền, chùa Việt Nam'

# Kết quả JSON dạng dictionary
result = {}

# Lặp qua từng file trong thư mục
for filename in os.listdir(folder_path):
    if filename.endswith('.pdf') and '-' in filename:
        file_path = os.path.join(folder_path, filename)
        pdf_reader = PdfReader(file_path)

        # Gộp toàn bộ nội dung các trang
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text() or ''  # tránh None

        # Tên file không có đuôi .pdf
        name = os.path.splitext(filename)[0]

        # Thêm vào dict
        result[name] = {"unknown": text.strip()}

# Ghi vào file JSON
with open('festival_hand_crawl.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Đã xử lý {len(result)} file PDF và lưu vào festival_hand_crawl.json")