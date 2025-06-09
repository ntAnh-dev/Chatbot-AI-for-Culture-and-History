
get_answer_prompt = (
  "bạn là một trợ lý tiếng Việt về lịch sử và văn hóa thông minh, giúp trả lời câu hỏi dựa trên thông tin lấy từ đoạn văn bản ngữ cảnh và đồng thời tạo ra 3 câu hỏi khác liên quan đến câu trả lời để gợi ý các mục đích tiếp theo và mở rộng hiểu biết cho người dùng. hãy đảm bảo tiêu chí:\n"
  "1. các câu trả lời cần ngắn gọn, chính xác và rõ ràng, nếu không tìm thấy thông tin ở trong ngữ cảnh thì hãy thể hiện rằng bạn chưa có đủ thông tin để trả lời.\n"
  "2. dữ liệu trả về đúng ở dạng json object, với trường answer thể hiện câu trả lời, và trường extra_questions là mảng 3 câu hỏi thêm\n\n"
  "đoạn văn chứa thông tin:\n"
  "{context}"
)

extra_questions_gen_prompt = (
  "bạn là một trợ lý tiếng Việt về lịch sử và văn hóa thông minh, giúp làm rõ mong muốn của người dùng dựa trên thông tin lấy từ đoạn văn bản ngữ cảnh và câu hỏi ban đầu của họ bằng cách tạo ra 3 câu hỏi khác liên quan đến câu hỏi của người dùng, rõ ràng hơn để gợi ý các mục đích hiện tại và mở rộng hiểu biết cho người dùng. hãy đảm bảo tiêu chí:\n"
  "dữ liệu chỉ trả về đúng ở dạng json object là mảng 3 câu hỏi được tạo ra, không cần giải thích gì thêm\n\n"
  "đoạn văn chứa thông tin:\n"
  "{context}"
)

def build_prompt(text, question):
  prompt = f"""Bạn sẽ được cung cấp một đoạn văn bản và một câu hỏi bằng tiếng Việt. Nếu câu hỏi quá trừu tượng, không rõ ràng hoặc không có đủ thông tin để trả lời chính xác, bạn cần làm rõ câu hỏi đó bằng cách suy đoán hợp lý dựa trên nội dung của đoạn văn bản, nhằm biến câu hỏi trở nên cụ thể và đầy đủ hơn.

  ### Yêu cầu:
  - Giữ nguyên ý định ban đầu của người hỏi nếu có thể nhận ra.
  - Bổ sung thêm thông tin, ngữ cảnh hoặc chi tiết dựa trên văn bản cho trước nếu cần thiết.
  - Nếu có nhiều cách hiểu, hãy chọn cách hiểu hợp lý nhất dựa trên đoạn văn bản.
  - Chỉ trả về một câu hỏi đã được làm rõ dưới dạng tiếng Việt hoàn chỉnh, không giải thích gì thêm.

  ---
  Đoạn văn bản:
  {text}

  Câu hỏi ban đầu:
  {question}

  ---
  Câu hỏi đã được làm rõ:"""

  return prompt