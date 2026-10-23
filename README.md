# genfarmer_boxphone

GenFarmer Support Center – hướng dẫn BoxPhone, 4 ngôn ngữ.

Xem online: https://vietgit04.github.io/genfarmer_boxphone/

Đổi ngôn ngữ bằng nút 🌐 trên thanh trên cùng (English, Tiếng Việt, Español, 日本語); trang tự nhớ
lựa chọn và lần đầu sẽ theo ngôn ngữ của trình duyệt. Link theo ngôn ngữ: `#/vi/home`, `#/es/adb`, `#/ja/usb`…

## Cấu trúc

- `index.html` – trang đã ghép, chứa cả 4 ngôn ngữ; được GitHub Pages đăng lên.
- `vi.html`, `es.html`, `ja.html` – chỉ chuyển hướng về `index.html#/<ngôn ngữ>/...` cho link cũ.
- `anh/` – ảnh dùng chung cho cả 4 trang.
- `src/head.html`, `src/tail.html` – phần `<head>` (CSS, hiệu ứng) và script (đổi ngôn ngữ, tìm kiếm, phóng ảnh).
- `src/<lang>/NN.html` – nội dung từng ngôn ngữ, chia thành 9 phần.
- `tools/build.py` – ghép `src/` thành `index.html`.
- `tools/check.py` – kiểm tra bản dịch giữ nguyên cấu trúc HTML của bản tiếng Anh.

## Sửa nội dung

1. Sửa file trong `src/en/` (và bản tương ứng trong `src/vi/`, `src/es/`, `src/ja/`).
2. `python3 tools/check.py vi` (tương tự `es`, `ja`) – phải ra `ok` hết.
3. `python3 tools/build.py`
4. Commit và push lên `main`; GitHub Pages tự cập nhật.
