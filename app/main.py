
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import pipeline

# Tạo ứng dụng FastAPI với một số thông tin mô tả cơ bản
app = FastAPI(
    title="Sentiment Analysis API",
    description="FastAPI application using a Hugging Face model for sentiment analysis.",
    version="1.0.0"
)

# Tên model trên Hugging Face
MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

# Khi server khởi động, ta load model đúng 1 lần để tránh mỗi request lại load lại
try:
    # pipeline("sentiment-analysis") là cách nhanh nhất để dùng model phân tích cảm xúc
    sentiment_pipeline = pipeline("sentiment-analysis", model=MODEL_NAME)
    model_loaded = True          # cờ đánh dấu model load thành công
    model_error = None           # không có lỗi
except Exception as e:
    # Nếu có lỗi khi load model, lưu lại để endpoint /health hoặc /predict báo ra
    sentiment_pipeline = None
    model_loaded = False
    model_error = str(e)


# Schema dữ liệu đầu vào cho POST /predict
class PredictRequest(BaseModel):
    # text là dữ liệu bắt buộc, min_length=1 giúp kiểm tra cơ bản ngay từ Pydantic
    text: str = Field(..., min_length=1, description="Input text for sentiment analysis")


# Schema dữ liệu đầu ra cho POST /predict
class PredictResponse(BaseModel):
    model: str
    input_text: str
    label: str
    score: float


@app.get("/")
def root():
    # Endpoint giới thiệu ngắn gọn về hệ thống theo đúng yêu cầu đề
    return {
        "message": "Welcome to the Sentiment Analysis API",
        "description": "This API uses a Hugging Face model to analyze the sentiment of input text.",
        "available_endpoints": {
            "GET /": "Short introduction to the system",
            "GET /health": "Check system status",
            "POST /predict": "Analyze sentiment from input text"
        },
        "model": MODEL_NAME
    }


@app.get("/health")
def health():
    # Endpoint kiểm tra trạng thái hoạt động của hệ thống
    if model_loaded:
        return {
            "status": "ok",
            "model_loaded": True,
            "model": MODEL_NAME
        }

    # Nếu model load lỗi thì trả thông tin lỗi để dễ kiểm tra
    return {
        "status": "error",
        "model_loaded": False,
        "model": MODEL_NAME,
        "detail": model_error
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    # Nếu model chưa load thành công thì không thể suy luận
    if not model_loaded or sentiment_pipeline is None:
        raise HTTPException(
            status_code=500,
            detail="Model is not loaded successfully."
        )

    # Loại bỏ khoảng trắng ở đầu/cuối chuỗi
    text = request.text.strip()

    # Dù Pydantic đã kiểm tra min_length=1, người dùng vẫn có thể gửi "   "
    # nên cần kiểm tra thêm sau khi strip
    if not text:
        raise HTTPException(
            status_code=400,
            detail="Field 'text' must not be empty."
        )

    try:
        # Gọi mô hình để suy luận
        # Kết quả thường có dạng:
        # [{"label": "POSITIVE", "score": 0.9998}]
        result = sentiment_pipeline(text)

        # Kiểm tra kết quả trả về có hợp lệ không
        if not result or not isinstance(result, list):
            raise HTTPException(
                status_code=500,
                detail="Invalid response returned from model."
            )

        # Lấy phần tử đầu tiên vì pipeline trả về list
        prediction = result[0]

        # Trả về JSON theo đúng schema PredictResponse
        return PredictResponse(
            model=MODEL_NAME,
            input_text=text,
            label=prediction["label"],
            score=round(float(prediction["score"]), 6)  # làm gọn số thập phân cho đẹp
        )

    except HTTPException:
        # Nếu đây đã là lỗi HTTPException thì ném lại nguyên trạng
        raise
    except Exception as e:
        # Các lỗi phát sinh khác trong quá trình suy luận
        raise HTTPException(
            status_code=500,
            detail=f"Error during inference: {str(e)}"
        )
