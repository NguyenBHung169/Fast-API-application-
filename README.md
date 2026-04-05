# Fast-API-application-
Building basic Web using Fast API from Hugging Face 
# Fast-API-application-

## 1. Thông tin sinh viên
- Họ và tên:Nguyễn Bảo Hưng
- MSSV: 24120057
- Lớp: 24CTT5
- Môn học: Tư Duy Tính Toán
- Trường: Trường Đại học Khoa Học Tự Nhiên TP.HCM
- Khoa: Công Nghệ Thông Tin

## 2. Tên mô hình và liên kết Hugging Face
- Tên mô hình: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`
- Liên kết mô hình: `https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english`

## 3. Mô tả ngắn về chức năng của hệ thống
Hệ thống này được xây dựng dưới dạng Web API bằng FastAPI để khai thác mô hình AI trên Hugging Face cho bài toán phân tích cảm xúc văn bản.

Người dùng gửi một câu hoặc đoạn văn bản tiếng Anh đến API, hệ thống sẽ sử dụng mô hình `distilbert/distilbert-base-uncased-finetuned-sst-2-english` để phân tích cảm xúc của văn bản đó và trả về kết quả dưới dạng JSON, bao gồm:
- văn bản đầu vào,
- nhãn cảm xúc (`POSITIVE` hoặc `NEGATIVE`),
- độ tin cậy của dự đoán.

Hệ thống cung cấp 3 endpoint chính:
- `GET /` để giới thiệu ngắn gọn về API,
- `GET /health` để kiểm tra trạng thái hoạt động của hệ thống,
- `POST /predict` để thực hiện chức năng phân tích cảm xúc.

## 4. Hướng dẫn cài đặt thư viện
Cài đặt các thư viện cần thiết bằng lệnh:

```bash
pip install -r requirements.txt
5. Hướng dẫn chạy chương trình

Sau khi cài đặt xong thư viện, chạy ứng dụng FastAPI bằng lệnh:

python -m uvicorn app.main:app --reload

Khi chương trình chạy thành công, API sẽ hoạt động tại địa chỉ:

http://127.0.0.1:8000

Giao diện Swagger để kiểm thử API:

http://127.0.0.1:8000/docs
6. Hướng dẫn gọi API và ví dụ request/response
6.1. Endpoint GET /

Dùng để trả về thông tin giới thiệu ngắn gọn về hệ thống.

Ví dụ response:

{
  "message": "Welcome to the Sentiment Analysis API",
  "description": "This API uses a Hugging Face model to analyze the sentiment of input text.",
  "available_endpoints": {
    "GET /": "Short introduction to the system",
    "GET /health": "Check system status",
    "POST /predict": "Analyze sentiment from input text"
  },
  "model": "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
}
6.2. Endpoint GET /health

Dùng để kiểm tra trạng thái hoạt động của hệ thống và model.

Ví dụ response:

{
  "status": "ok",
  "model_loaded": true,
  "model": "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
}
6.3. Endpoint POST /predict

Dùng để gửi văn bản đầu vào và nhận kết quả phân tích cảm xúc.

Ví dụ request:

{
  "text": "I really love this product. It is amazing."
}

Ví dụ response:

{
  "model": "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
  "input_text": "I really love this product. It is amazing.",
  "label": "POSITIVE",
  "score": 0.999873
}
6.4. Kiểm thử API bằng file Python

Project có file test_api.py để kiểm thử các endpoint bằng thư viện requests.

Chạy lệnh:

python test_api.py
7. Liên kết video demo
Video demo: [...](https://drive.google.com/file/d/1QS4XSjEP_AkwDLGCZVOR0yEwmndt_cI0/view?usp=sharing)
8. Cấu trúc thư mục dự án
Fast-API-application-/
│── app/
│   └── main.py
│── requirements.txt
│── test_api.py
│── README.md 
