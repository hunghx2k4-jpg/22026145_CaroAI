Dự án Caro AI - Minimax & Alpha-Beta Pruning (9x9)

Đồ án thực hành môn học Trí tuệ Nhân tạo xây dựng chương trình cờ Caro đối kháng trực quan giữa Người chơi và Máy tính (AI).

📌 Sinh viên thực hiện

Họ và tên: Đào Duy Hưng

Mã số sinh viên (MSV): 22026145

📂 Cấu trúc thư mục Repository

Thư mục dự án được tổ chức đồng bộ và chuẩn hóa chính xác theo yêu cầu nộp bài:

22026145_CaroAI/
│
├── source_code/
│   └── caro.py            # Chứa toàn bộ mã nguồn chương trình (Logic game, Thuật toán, GUI Tkinter, Phân tích Lv3)
│
├── requirements.txt       # Định nghĩa môi trường chạy (Python thuần)
└── README.md              # Tài liệu hướng dẫn cài đặt và vận hành hệ thống


🎨 Các tính năng nổi bật của chương trình

Giao diện đồ họa (GUI) trực quan: Thiết kế bằng thư viện Tkinter phẳng mịn, chia ô cờ rõ ràng với lưới màu sắc bắt mắt. Phản hồi chuột tức thì.

Cấu hình thuật toán linh hoạt: Người chơi có thể tự do chuyển đổi giữa chế độ Minimax thuần (Level 1) hoặc Alpha-Beta Pruning (Level 2) trực tiếp ngay trong ván đấu.

Độ sâu tìm kiếm tùy chỉnh: Cho phép tùy chỉnh mức độ sâu tìm kiếm (depth từ 1 đến 5) để thay đổi độ thông minh của AI.

Hệ thống đo đạc hiệu năng thời gian thực: Hiển thị trực tiếp các thông số kỹ thuật (Số trạng thái đã duyệt, Thời gian xử lý, Điểm lượng giá thế cờ) sau mỗi nước đi của AI.

Chế độ kiểm thử tự động (Level 3): Tích hợp tính năng chạy ngầm kịch bản thử nghiệm tự động 4 trạng thái thế trận mẫu để so sánh hiệu năng của hai thuật toán, hỗ trợ trực tiếp việc làm báo cáo.

⚙️ Hướng dẫn cài đặt và chạy chương trình

1. Yêu cầu hệ thống

Hệ điều hành: Windows, macOS, hoặc Linux.

Môi trường: Đã cài đặt sẵn Python phiên bản 3.8 trở lên.

Thư viện giao diện đồ họa Tkinter đã đi kèm sẵn trong gói cài đặt Python mặc định của bạn.

2. Các bước khởi chạy chi tiết

Bước 1: Tải mã nguồn về máy tính

Bạn tiến hành clone repository này về máy thông qua Git:

git clone [https://github.com/hunghx2k4-jpg/22026145_CaroAI.git](https://github.com/hunghx2k4-jpg/22026145_CaroAI.git)
cd 22026145_CaroAI

(Hoặc tải file nén .zip từ Github về và giải nén).

Bước 2: Di chuyển vào thư mục mã nguồn

Mở Terminal (trên macOS/Linux) hoặc Command Prompt/PowerShell (trên Windows) và di chuyển vào thư mục chứa code:

cd source_code

Bước 3: Chạy chương trình

Thực thi file mã nguồn Python để khởi động trò chơi:

python caro.py

(Nếu hệ thống của bạn dùng lệnh python3, hãy gõ: python3 caro.py)

🎮 Hướng dẫn trải nghiệm trò chơi trên GUI

Khởi đầu ván cờ: Bạn (X - màu đỏ) đi trước, nhấp chuột trực tiếp vào bất kỳ ô nào trên bàn cờ để đặt quân cờ.

AI phản công: Sau khi bạn đánh, AI (O - màu xanh lá) sẽ tự động tính toán nước đi tốt nhất dựa trên cấu hình đang chọn và đi nước đi của mình.

Xem chỉ số: Quan sát bảng "Chỉ Số Đo Đạc Hiệu Năng Hệ Thống" ở cạnh dưới cùng để xem số node duyệt và thời gian thực hiện nước đi đó.

Sử dụng tính năng Level 3 (Kiểm thử tự động): * Bấm vào nút màu tím "Chạy Thử Nghiệm Tự Động (Lv3)" ở góc trên bên phải.

Hệ thống sẽ tự nạp 4 thế cờ mẫu để đối chứng hiệu năng giữa Minimax và Alpha-Beta.

Kết quả bảng dữ liệu dạng ma trận so sánh sẽ được in trực tiếp ra màn hình Terminal (Console) của bạn. Hãy chụp ảnh hoặc copy bảng này vào báo cáo cuối kỳ.

📚 Tài liệu tham khảo & Repo mẫu đã sử dụng

Stuart Russell & Peter Norvig, "Artificial Intelligence: A Modern Approach", Chapter 5: Adversarial Search.

Ý tưởng thiết kế trạng thái bàn cờ dạng mảng hai chiều quét vectơ hướng chéo từ Repo mẫu: https://github.com/husus/gomokuAI-py.

Ý tưởng gán trọng số điểm phạt phòng ngự cho các chuỗi nguy hiểm của đối phương từ Repo mẫu: https://github.com/MonHauVD/Caro_AI.
