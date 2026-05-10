# ĐỒ ÁN CUỐI KỲ

# TRỰC QUAN HÓA DỮ LIỆU

## Nội dung

- Trình bày một dự án ứng dụng trực quan sử dụng **dashboard** để
    phân tích dữ liệu
- Ngữ cảnh của dữ liệu là Việt Nam
- Các nhóm trình bày trong buổi vấn đáp.

## Yêu cầu về dữ liệu

Dữ liệu là dữ liệu thật có liên quan đất nước Việt Nam. Dữ liệu phải
có tối thiểu **7 biến độc lập** và **tối thiểu 2000 dòng**. Tổng số dữ liệu
liên quan đến Việt Nam phải trên **50%** dữ liệu

## Các tiêu chí để đánh giá

1. Kết hợp nguồn dữ liệu đáng tin cậy:
    - Nếu có bất kỳ nguồn dữ liệu nào được sử dụng, đảm bảo rằng
       nó đáng tin cậy và được cung cấp một cách minh bạch.
    - Kiểm tra xem liệu có bất kỳ thiếu sót nào trong quy trình xử
       lý dữ liệu hay không.
2. Phù hợp với mục đích:

### 1


- Trực quan hóa phải phản ánh mục đích cụ thể của nó. Ví dụ,
    biểu đồ cột thích hợp để so sánh dữ liệu, trong khi biểu đồ
    đường thích hợp để theo dõi xu hướng thời gian.
- Cân nhắc xem liệu trực quan hóa có phù hợp với đối tượng
    mục tiêu hay không.
3. Rõ ràng và dễ hiểu:
- Trực quan hóa nên truyền đạt thông điệp một cách rõ ràng
và dễ hiểu.
- Biểu đồ và đồ thị nên được thiết kế sao cho người xem có thể
nhanh chóng nhận thức và hiểu thông tin.
4. Sự tích hợp và liên kết:
- Nếu có nhiều biểu đồ hoặc đồ thị, đảm bảo sự liên kết và tích
hợp giữa chúng.
- Mối quan hệ giữa các phần của trực quan hóa nên được làm
rõ.
5. Tương tác và điều hướng:
- Sự tương tác, nếu có, nên được tích hợp một cách hợp lý để
người xem có thể thăm dò dữ liệu.
- Hệ thống điều hướng nên được xây dựng một cách dễ sử dụng.
6. Thiết kế hấp dẫn:
- Thiết kế đồ họa và màu sắc nên làm cho trực quan hóa trở
nên hấp dẫn và dễ thu hút sự chú ý.
- Sử dụng màu sắc một cách có ý nghĩa và tránh sự quá tải
màu.
7. **Phân tích dữ liệu** :
- Trực quan hóa nên thể hiện sự thay đổi và xu hướng theo
thời gian nếu có.
- Mối quan hệ giữa các biến cần phải rõ ràng.
- _Những kết luận và câu chuyện liên quan_.
8. **Tích hợp AI:** Thiết kế và vận hành

### 2
# HƯỚNG DẪN TÍCH HỢP AI

## 1 Yêu cầu tích hợp AI

Tích hợp tính năng AI vào phân tích dữ liệu: có thể là ứng dụng **độc lập** hoặc
tích hợp vào dashboard hoặc tạo API để các ứng dụng khác sử dụng.
_Khuyến khích tạo API để các ứng dụng khác sử dụng_

### 1.1 Nguyên tắc cơ bản

- **AI:** Đóng vai trò
    **-** trợ giúp đề xuất ý tưởng
    **-** viết code dựa vào yêu cầu của người dùng
    **-** trình bày kết quả phân tích với số liệu và hình ảnh, biểu đồ được
       cung cấp bởi con người, không được tự ý thêm số liệu hay hình ảnh
       khác.
- **Con người:** Đóng vai trò
    **-** định hướng, đề xuất các yêu cầu phân tích, ra quyết định thực thi
       code.
    **-** nếu con người chưa biết, chưa có ý tưởng về cách phân tích như
       thế nào thì có thể yêu cầu AI đưa ra các gợi ý, phương pháp để con
       người lựa chọn.
- **Thực thi code:** phải trên môi trường local của người dùng. Không
    được thực thi trên môi trường online.

## 2 Nguyên tắc “không thực thi ngầm”

AI không được phép tự ý thay đổi dữ liệu gốc hay âm thầm chạy các thuật
toán.


- **Hiển thị code bắt buộc:** Mỗi khi AI tạo code theo yêu cầu của con
    người, nó **bắt buộc** phải hiển thị rõ ràng.
- **Giải thích bằng ngôn ngữ tự nhiên:** Ngay trên đoạn code đó, AI
    phải đính kèm các dòng comment giải thích bằng ngôn ngữ tự nhiên:
    _“Đoạn code này sẽ xóa 15 dòng có giá trị NULL ở cột Doanh Thu, sử_
    _dụng hàmdropna()của Pandas.”_

### 2.1 Nguyên tắc phê duyệt

Thể hiện vai trò “Người quyết định”.

- **Trạng thái chờ:** Code do AI sinh ra ban đầu sẽ ở trạng thái “Chờ
    duyệt”. Con người có thể thay đổi, bổ sung hoặc loại bỏ code này.
- **Chỉnh sửa:** Con người có quyền trực tiếp can thiệp, gõ sửa các tham
    số trong đoạn code AI vừa viết (ví dụ: đổi giới hạn outlier từ 3 standard
    deviations xuống 2).
- **Chấp nhận & thực thi:** Đoạn code chỉ được thực thi và trả về kết
    quả/biểu đồ khi và chỉ khi con người chấp thuận.

### 2.2 Nguyên tắc lưu trữ

Hệ thống phải lưu trữ tất cả các yêu cầu, mã nguồn, kết quả phân tích và giải
thích để có thể truy xuất lại được.

## 3 Trong vấn đáp

Các nhóm sẽ được yêu cầu sử dụng module AI đã phát triển để trả lời các câu
hỏi phân tích dựa trên dữ liệu của nhóm và các câu hỏi phân tích đã chuẩn
bị sẵn, nhằm tránh lan man. Tuy nhiên, vẫn có thể được yêu cầu trả lời câu
hỏi ngoài lề để đánh giá mức độ linh hoạt của AI. Lưu ý, số lượng câu hỏi tối
thiểu bằng số lượng thành viên trong nhóm.

## 4 Trong báo cáo

Phải tóm tắt lại quá trình sử dụng AI, những yêu cầu đã đặt ra, những kết
quả đã nhận được, những thay đổi đã thực hiện và những nhận xét về AI.

## 5 Gợi ý thiết kế

Phân chia cấu trúc API và Frontend


### 5.1 Phần Giao diện & Tương tác người dùng (Frontend)

Công nghệ phát triển giao diện Frontend là **tùy chọn** (có thể dùng Streamlit,
Gradio, React, hoặc các công cụ Dashboard có khả năng tương tác, ...). Các
nhóm chỉ cần đảm bảo các chức năng cơ bản. Khuyến khích các nhóm tạo ra
những giao diện đẹp, trực quan, dễ sử dụng cho người dùng.

- **Chức năng nhận yêu cầu:**
    **-** Ví dụ: Một ô chat hoặc form nhập liệu để người dùng gửi yêu cầu
       phân tích/viết code cho AI.
- **Chức năng xem & chỉnh sửa mã nguồn**
- **Chức năng phê duyệt**
- **Chức năng hiển thị kết quả**

### 5.2 Phần API

- **API AI (bắt buộc):**
    **-** Tiếp nhận yêu cầu từ Front-end.
    **-** Gửi kèm ngữ cảnh (ví dụ: cấu trúc dữ liệu hiện có) cho mô hình
       AI (Gemini/OpenAI) (được sử dụng local model).
    **-** Yêu cầu AI trả về cả **code** và **giải thích** tương ứng; hoặc **kết quả**
       **trình bày**.
- **API Thực thi (bắt buộc):**
    **-** Tiếp nhận đoạn mã đã được con người “chỉnh sửa” và “phê duyệt”
       từ frontend.
    **-** Thực hiện chạy code trực tiếp trên dữ liệu tại máy.
    **-** Thu thập kết quả (ảnh biểu đồ, bảng dữ liệu, logs) để trả về cho
       frontend hiển thị.
- **API Logs (bắt buộc):**
    **-** Lưu trữ tất cả các yêu cầu, mã nguồn, kết quả phân tích và giải
       thích.

# YÊU CẦU ĐỂ LÀM PHÂN TÍCH DỮ LIỆU
- Dữ liệu đã nói được gì, thể hiện rõ ràng ra là từ dữ liệu trong dataset đó mà suy ra được ý nghĩa. Phải đưa ra các insights có ý nghĩa cho nguồn dữ liệu trên. Lúc đưa ra chiến lược thì phải chứng minh được lý lẽ đó từ chỗ nào ở nguồn dữ liệu mà suy ra.
- Phải đi phân tích sâu vào 1 đặc điểm chính chứ đừng dàn trải cái gì cũng phân tích và phân tích nông, không đi sâu. Ví dụ: Mặt hàng giá rẻ từ 100-500k vnd đang chiếm số lượng nhiều, thì mặt hàng nào có giá rẻ như này thì phân tích sâu vào, các mặt hàng tương tự, số lượng bán ra có thật sự như những gì mình nói thôi. Phải đưa ra bức tranh tổng thể rồi đi sâu vào từng mục chính. Xem có phải thị trường ngách không? Đầu tư vào thì có doanh thu được như họ không => Dùng mô hình dự đoán hoặc assumption khi có review count