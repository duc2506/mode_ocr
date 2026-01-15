"""
Script inference standalone - có thể copy sang folder khác
Yêu cầu: pip install paddlepaddle paddleocr
"""
from paddleocr import PaddleOCR
import re
import sys
import os

class KoreanOCR:
    def __init__(self, model_path=None):
        """
        model_path: Đường dẫn đến model custom (nếu có)
                   Nếu None, sẽ dùng model mặc định của PaddleOCR
        """
        if model_path:
            # Sử dụng model đã train
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang="korean",
                rec_model_dir=model_path
            )
        else:
            # Sử dụng model mặc định
            self.ocr = PaddleOCR(lang="korean")
    
    def clean_text(self, text):
        """Xóa ký tự rác từ kết quả OCR"""
        # Xóa các từ rác cụ thể
        text = re.sub(r'\brl\b|\bba\b|\bσ\b|\^\b', '', text, flags=re.IGNORECASE)
        
        # Xóa các số độc lập
        text = re.sub(r'\b\d+\b', '', text)
        
        # Giữ lại chữ Hàn, Latin, số, dấu câu
        cleaned = re.sub(r'[^\uac00-\ud7afa-zA-Z0-9\s\.\,\!\?\-\(\)，。！？·\u3000]', '', text)
        
        # Xóa khoảng trắng thừa
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def process_image(self, image_path, output_path=None):
        """
        Xử lý OCR cho ảnh
        Args:
            image_path: Đường dẫn ảnh đầu vào
            output_path: Đường dẫn file text đầu ra (mặc định: <image_name>.txt)
        Returns:
            str: Văn bản đã OCR
        """
        if not os.path.exists(image_path):
            print(f"❌ Không tìm thấy file: {image_path}")
            return None
        
        # OCR ảnh
        print(f"🔍 Đang xử lý OCR cho: {image_path}")
        result = self.ocr.ocr(image_path)
        
        # Xử lý kết quả
        full_text = ""
        if result and isinstance(result, list) and len(result) > 0:
            page_result = result[0]
            
            if isinstance(page_result, dict) and 'rec_texts' in page_result:
                texts = page_result.get('rec_texts', [])
                scores = page_result.get('rec_scores', [])
                
                for i, text in enumerate(texts):
                    if text.strip():
                        cleaned_text = self.clean_text(text)
                        if cleaned_text:
                            score = scores[i] if i < len(scores) else 0
                            print(f"  {cleaned_text} ({score:.2%})")
                            full_text += cleaned_text + " "
        
        full_text = full_text.strip()
        
        # Lưu file
        if output_path is None:
            output_path = os.path.splitext(image_path)[0] + ".txt"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        
        print(f"✅ Đã lưu kết quả vào: {output_path}")
        return full_text


if __name__ == "__main__":
    # Cách dùng 1: Dùng model mặc định
    ocr = KoreanOCR()
    
    # Cách dùng 2: Dùng model đã train (uncomment nếu có)
    # ocr = KoreanOCR(model_path="./output/korean_hw_rec/best_accuracy")
    
    # Xử lý ảnh từ command line hoặc hardcode
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        ocr.process_image(image_path, output_path)
    else:
        # Mặc định xử lý ảnh này
        ocr.process_image("anh_2_page-0001.jpg", "essay.txt")
        
        # Hoặc xử lý nhiều ảnh:
        # for img in ["anh_1.jpg", "anh_2.jpg"]:
        #     ocr.process_image(img)
