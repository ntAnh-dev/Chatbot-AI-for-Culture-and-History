
qa_gen_prompt = """
Bạn là một trợ lý AI chuyên trích xuất thông tin từ đoạn văn bản về các ngôi chùa. 

Dưới đây là danh sách 30 loại câu hỏi mẫu mà bạn cần tập trung tạo cặp câu hỏi - câu trả lời, dựa trên nội dung đoạn văn bản được cung cấp:

1. Chùa Hương có tên gọi khác là gì?
2. Chùa Hương được xây dựng từ khi nào?
3. Chùa Hương có bao nhiêu năm tuổi?
4. Chùa Hương xây dựng vào thời đại nào?
5. Chùa Hương có kiến trúc gì đặc biệt?
6. Chùa Hương tổ chức lễ hội vào ngày nào?
7. Chùa Hương đã qua bao nhiêu lần tu sửa?
8. Diện tích của chùa Hương là bao nhiêu?
9. Chùa Hương có những bảo vật, hiện vật quý giá nào?
10. Chùa Hương tọa lạc tại vị trí nào?
11. Những ngôi chùa nào gần ngôi chùa Hương?
12. Những ngôi chùa nào ở tỉnh Vĩnh Phúc?
13. Chùa Hương thờ ai?
14. Từng gian ở chùa Hương thờ ai?
15. Những ngôi chùa nào thờ đức thánh Tản Viên?
16. Chùa Hương được xây dựng từ vật liệu nào?
17. Những ngôi chùa nào đạt di tích lịch sử cấp quốc gia ở tỉnh Vĩnh Phúc?
18. Những ngôi chùa nào đạt di tích lịch sử cấp tỉnh ở tỉnh Vĩnh Phúc?
19. Chùa Hương có những gian, tòa nào?
20. Những câu chuyện liên quan tới chùa Hương?
21. Những câu chuyện nào liên quan tới vị Đức thánh Tản Viên?
22. Chi tiết về các lần tu sửa đền Thính?
23. Chi tiết về các bảo vật, hiện vật được thờ ở đền Thính?
24. Chi tiết về lễ hội chùa Hương?
25. Những sự kiện lịch sử quan trọng đã diễn ra tại chùa Hương?
26. Ai là người sáng lập, đứng đầu đầu tiên của chùa Hương?
27. Vị Đức thánh Tản Viên được mô tả như thế nào?
28. Vị Đức thánh Tản Viên sáng lập ra những ngôi chùa nào?
29. Những vị nổi tiếng nào từng trụ trì tại chùa Hương?
30. Chùa Hương có ảnh hưởng như thế nào đến cộng đồng địa phương?

Đây là danh sách các thông tin cơ bản cần thiết để phân tách nếu có:
Đối với đình, đền, chùa: tên địa danh, loại hình(đình/đền/chùa), tên khác(tên dân gian), địa chỉ chi tiết, năm xây dựng, người xây dựng, các lần trùng tu, đối tượng được thờ phụng, kiến trúc tổng thể, chất liệu xây dựng, xếp hạng di tích(tỉnh/quốc gia), tên lễ hội truyền thống
Đối với lễ hội: tên lễ hội, loại lễ hội(truyền thống/tôn giáo/văn hóa dân gian/hành hương), ngày bắt đầu lễ hội, ngày kết thúc lễ hội, mô tả ngắn gọn nội dung chính lễ hội, có phải theo âm lịch không, ước lượng khách tham gia
Đối với anh hùng, thánh thần: tên nhân vật, danh xưng, loại nhân vật(thần linh/anh hùng/danh nhân/phật/bồ tát/mẫu/tiên/tổ sư), tóm tắt ngắn gọn về nhân vật

---

Yêu cầu:

- Dựa trên đoạn văn bản dưới đây, hãy tạo ra các cặp câu hỏi - câu trả lời tương ứng theo các loại câu hỏi mẫu trên, đồng thời hãy phân tách các thông tin đặc trưng của đình, đền, chùa, lễ hội, anh hùng, thánh thần được nhắc đến trong đoạn văn bản.
- Mỗi cặp câu hỏi - câu trả lời phải rõ ràng, chính xác, và dựa trên thông tin có trong đoạn văn.
- Nếu thông tin không có trong đoạn văn, bạn có thể bỏ qua câu hỏi đó.
- Trả về kết quả cho bộ dữ liệu hỏi đáp dưới dạng danh sách các cặp { "question": "...", "answer": "..." }.
- Trả về kết quả phân tách của một thực thể theo dạng mảng các xâu, giá trị nào không có thì vẫn là một phần tử của mảng nhưng là xâu rỗng.
- Kết quả trả về dạng json, trường qa_pairs là danh sách các cặp câu hỏi câu trả lời, trường entites là danh sách các thực thể được phân tách.

---

Đoạn văn bản:
"""