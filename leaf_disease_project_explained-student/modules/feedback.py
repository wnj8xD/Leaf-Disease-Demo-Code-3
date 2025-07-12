import json
import os
from datetime import datetime

def save_feedback(username, image_base64, predictions, feedback_status):
    # Lấy thời gian hiện tại
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Địa điểm: Dùng một giá trị cố định, trong ứng dụng thực tế có thể cần API định vị
    location = "Web App (Không xác định vị trí cụ thể)"

    # Tạo thư mục 'data/records' nếu chưa tồn tại
    output_dir = "data/records"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tên tệp phản hồi
    filename = os.path.join(output_dir, f"{username}_{timestamp}.json")

    # Dữ liệu phản hồi
    feedback_data = {
        "username": username,
        "timestamp": timestamp,
        "location": location,
        "image_base64_preview": image_base64[:100] + "...", # Lưu một phần nhỏ để xem trước
        "full_image_base64": image_base64, # Lưu toàn bộ base64 ảnh
        "predictions": predictions, # Lưu toàn bộ kết quả dự đoán
        "feedback_status": "Correct" if feedback_status else "Incorrect"
    }

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(feedback_data, f, ensure_ascii=False, indent=4)
        print(f"Phản hồi đã được lưu vào: {filename}")
        return True
    except Exception as e:
        print(f"Lỗi khi lưu phản hồi: {e}")
        return False
