from paddleocr import PaddleOCR
import re

# KHỞI TẠO OCR
ocr = PaddleOCR(lang="korean")

# OCR ẢNH BÀI VĂN
result = ocr.ocr("anh_1.jpg")

def clean_ocr_text(text):
    """Xóa ký tự rác từ kết quả OCR"""
    # Xóa các từ rác cụ thể: "rl", "bạ", "σ" v.v.
    text = re.sub(r'\brl\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bba\b|\brl\b|\bσ\b|\^\b', '', text, flags=re.IGNORECASE)
    
    # Xóa các số độc lập (chỉ số đứng riêng lẻ, không phải trong từ)
    # Ví dụ: "21" hoặc "σ" nhưng giữ lại các từ chứa số
    text = re.sub(r'\b\d+\b', '', text)
    
    # Chỉ xóa các ký tự lạ như σ, ^, v.v., giữ lại chữ Hàn, Latin, số, dấu câu
    cleaned = re.sub(r'[^\uac00-\ud7afa-zA-Z0-9\s\.\,\!\?\-\(\)，。！？·\u3000]', '', text)
    
    # Xóa khoảng trắng thừa
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    return cleaned

# LƯU RA FILE TEXT (UTF-8)
with open("essay.txt", "w", encoding="utf-8") as f:
    if result and isinstance(result, list) and len(result) > 0:
        page_result = result[0]
        
        # Kiểm tra xem result[0] là dictionary hay list
        if isinstance(page_result, dict) and 'rec_texts' in page_result:
            # Cấu trúc mới: result[0] là dict với 'rec_texts' và 'rec_scores'
            texts = page_result.get('rec_texts', [])
            scores = page_result.get('rec_scores', [])
            
            full_text = ""
            for i, text in enumerate(texts):
                if text.strip():  # Bỏ qua các ô trống
                    # Làm sạch text
                    cleaned_text = clean_ocr_text(text)
                    if cleaned_text:  # Chỉ xử lý nếu còn text sau khi làm sạch
                        score = scores[i] if i < len(scores) else 0
                        if score > 0:
                            print(f"{cleaned_text} (độ tin cậy: {score:.2%})")
                        else:
                            print(f"{cleaned_text}")
                        full_text += cleaned_text + " "  # Ghép lại với nhau
            
            # Ghi toàn bộ text thành một đoạn
            f.write(full_text.strip())
        else:
            print("⚠️ Cấu trúc dữ liệu không xác định được")

print("✅ OCR HOÀN TẤT – KẾT QUẢ TRONG essay.txt (đã xóa ký tự rác)")
