import requests

# Địa chỉ server FastAPI đang chạy local
BASE_URL = "http://127.0.0.1:8000"


def test_root():
    # Gửi request GET tới endpoint /
    response = requests.get(f"{BASE_URL}/")

    print("GET /")
    print("Status code:", response.status_code)   # in mã trạng thái HTTP
    print("Response:", response.json())           # in nội dung JSON trả về
    print("-" * 60)


def test_health():
    # Gửi request GET tới endpoint /health để kiểm tra trạng thái hệ thống
    response = requests.get(f"{BASE_URL}/health")

    print("GET /health")
    print("Status code:", response.status_code)
    print("Response:", response.json())
    print("-" * 60)


def test_predict_valid():
    # Trường hợp dữ liệu hợp lệ
    payload = {
        "text": "I really love this product. It is amazing."
    }

    # Gửi request POST tới /predict kèm dữ liệu JSON
    response = requests.post(f"{BASE_URL}/predict", json=payload)

    print("POST /predict - valid input")
    print("Status code:", response.status_code)
    print("Response:", response.json())
    print("-" * 60)


def test_predict_empty():
    # Trường hợp text chỉ toàn khoảng trắng -> server nên báo lỗi
    payload = {
        "text": "   "
    }

    response = requests.post(f"{BASE_URL}/predict", json=payload)

    print("POST /predict - empty text")
    print("Status code:", response.status_code)
    print("Response:", response.json())
    print("-" * 60)


def test_predict_missing_field():
    # Trường hợp thiếu hẳn trường text -> Pydantic/FastAPI sẽ báo lỗi 422
    payload = {}

    response = requests.post(f"{BASE_URL}/predict", json=payload)

    print("POST /predict - missing field")
    print("Status code:", response.status_code)
    print("Response:", response.json())
    print("-" * 60)


if __name__ == "__main__":
    # Chạy lần lượt tất cả các test khi gọi file này trực tiếp
    test_root()
    test_health()
    test_predict_valid()
    test_predict_empty()
    test_predict_missing_field()
