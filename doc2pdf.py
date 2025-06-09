import os
from docx2pdf import convert

def convert_all_docx_to_pdf(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Thư mục không tồn tại: {folder_path}")
        return

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".docx"):
            docx_path = os.path.join(folder_path, filename)
            pdf_path = os.path.join(folder_path, filename[:-5] + ".pdf")
            try:
                convert(docx_path, pdf_path)
                print(f"Đã chuyển: {filename} -> {filename[:-5] + '.pdf'}")
            except Exception as e:
                print(f"Lỗi chuyển file {filename}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Vui lòng truyền đường dẫn thư mục chứa file DOCX làm tham số.")
        print("Cách dùng: python convert_docx_to_pdf.py đường_dẫn_thư_mục")
    else:
        folder = sys.argv[1]
        convert_all_docx_to_pdf(folder)
