import sys
from pathlib import Path

# Add dashboard to path
sys.path.insert(0, str(Path(__file__).parent / 'dashboard'))

from app import app

if __name__ == '__main__':
    print("Đang khởi chạy bảng điều khiển phân tích thời trang Tiki...")
    print("Mở trình duyệt tại: http://localhost:8050")
    app.run(debug=True, port=8050)
