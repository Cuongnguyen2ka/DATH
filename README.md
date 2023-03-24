# DATH
Đề tài ứng dụng công nghệ RFID và xử lý trong bãi giữ xe ô tô chung cư
Nguyên lý hoạt động của toàn bộ hệ thống:
      Khối nguồn sử dụng là Adapter 5VDC, 3A để cung cấp cho Raspberry Pi 4 là nguồn nuôi chính của toàn bộ hệ thống.
      Khối Camera được mở khi chạy chương trình và tiến hành chụp ảnh khi có thẻ từ quẹt vào RFID reader.
      Servo ra vào sẽ thực thi đóng mở thanh chắn cho xe vào bãi và ra ngoài khi đã xử lý đúng biển và thẻ được đăng ký trước đó.
      Khối hiển thị sẽ chịu trách nhiệm hiển thị các thông tin cơ bản như biển số xe, tên khách hàng, số chỗ trống còn lại trong bãi, mã thẻ RFID. 
      Khối cảm biến và LED sẽ thực thi việc nhận biết khi xe vào/ra chuồng thông qua việc cảm biến vật cản hồng ngoại sẽ gửi tín hiệu đến Raspberry 
      và yêu cầu tắt led khi có xe vào và bật lại khi xe ra khỏi chuồng. 
      Khối Buzzer sẽ hú 3 giây khi sai thẻ hoặc biển số đã đăng ký trên thẻ và trong trường hợp không trùng khớp thông tin trên thẻ.
