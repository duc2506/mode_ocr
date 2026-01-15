# Hướng dẫn chuyển code sang folder khác

## Cách 1: Dùng model mặc định (không cần copy model)

**Copy các file:**
```
deploy_inference.py    # File vừa tạo
anh_2_page-0001.jpg   # Ảnh cần OCR
```

**Chạy:**
```bash
cd <folder_mới>
pip install paddlepaddle paddleocr
python deploy_inference.py
```

---

## Cách 2: Dùng model đã train custom

**Copy toàn bộ:**
```
deploy_inference.py           # File inference
output/korean_hw_rec/         # Model đã train
anh_2_page-0001.jpg          # Ảnh cần OCR
```

**Sửa trong deploy_inference.py (dòng 92):**
```python
# Uncomment dòng này:
ocr = KoreanOCR(model_path="./output/korean_hw_rec/best_accuracy")
```

**Chạy:**
```bash
cd <folder_mới>
pip install paddlepaddle paddleocr
python deploy_inference.py
```

---

## Cách 3: Export model sang ONNX (nhẹ hơn, chạy nhanh hơn)

```bash
# Trong folder PaddleOCR hiện tại
pip install paddle2onnx

# Export model
paddle2onnx \
    --model_dir output/korean_hw_rec/best_accuracy \
    --model_filename inference.pdmodel \
    --params_filename inference.pdiparams \
    --save_file korean_ocr.onnx \
    --opset_version 11

# Copy file korean_ocr.onnx sang folder mới
```

---

## Cách sử dụng deploy_inference.py

**1. Xử lý 1 ảnh:**
```bash
python deploy_inference.py anh_1.jpg
```

**2. Xử lý và lưu file text custom:**
```bash
python deploy_inference.py anh_1.jpg output.txt
```

**3. Xử lý nhiều ảnh (sửa code):**
```python
for img in ["anh_1.jpg", "anh_2.jpg", "anh_3.jpg"]:
    ocr.process_image(img)
```

---

## Requirements

File `requirements.txt` để cài đặt dependencies:
```
paddlepaddle>=2.5.0
paddleocr>=2.7.0
```

Cài đặt:
```bash
pip install -r requirements.txt
```
