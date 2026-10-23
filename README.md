# genfarmer_boxphone

GenFarmer Support Center – hướng dẫn BoxPhone, 4 ngôn ngữ.

| Ngôn ngữ | Xem online |
|---|---|
| English | https://vietgit04.github.io/genfarmer_boxphone/ |
| Tiếng Việt | https://vietgit04.github.io/genfarmer_boxphone/vi.html |
| Español | https://vietgit04.github.io/genfarmer_boxphone/es.html |
| 日本語 | https://vietgit04.github.io/genfarmer_boxphone/ja.html |

## Cấu trúc

- `index.html`, `vi.html`, `es.html`, `ja.html` – các trang đã ghép, được GitHub Pages đăng lên.
- `anh/` – ảnh dùng chung cho cả 4 trang.
- `src/head.html`, `src/tail.html` – phần `<head>` (CSS) và script dùng chung.
- `src/<lang>/NN.html` – nội dung từng ngôn ngữ, chia thành 9 phần.
- `tools/build.py` – ghép `src/` thành 4 trang.
- `tools/check.py` – kiểm tra bản dịch giữ nguyên cấu trúc HTML của bản tiếng Anh.

## Sửa nội dung

1. Sửa file trong `src/en/` (và bản tương ứng trong `src/vi/`, `src/es/`, `src/ja/`).
2. `python3 tools/check.py vi` (tương tự `es`, `ja`) – phải ra `ok` hết.
3. `python3 tools/build.py`
4. Commit và push lên `main`; GitHub Pages tự cập nhật.
