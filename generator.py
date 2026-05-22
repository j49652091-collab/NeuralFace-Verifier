import cv2
import numpy as np
from PIL import Image, ImageEnhance

def make_real(uploaded_file):
    try:
        # 1. قراءة الصورة المرفوعة وتحويلها بصيغة يقرأها البرتامج
        uploaded_file.seek(0)
        image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image)
        
        # 2. تحويل الألوان لمعالجتها عبر OpenCV
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        # 3. إزالة تأثير البلاستيك والأنمي عبر تنعيم البشرة بطريقة فوتوغرافية طبيعية
        smoothed = cv2.bilateralFilter(img_bgr, d=9, sigmaColor=75, sigmaSpace=75)
        
        # 4. إرجاع الصورة لصيغة PIL لتعديل الإضاءة
        enhanced_img = Image.fromarray(cv2.cvtColor(smoothed, cv2.COLOR_BGR2RGB))
        
        # 5. ضبط تباين الألوان والإضاءة (تعديل الفلاتر لتصبح كإضاءة الكاميرا الحقيقية)
        contrast = ImageEnhance.Contrast(enhanced_img).enhance(1.1)  # زيادة التباين قليلاً
        brightness = ImageEnhance.Brightness(contrast).enhance(1.05) # تحسين الإضاءة
        sharpness = ImageEnhance.Sharpness(brightness).enhance(1.2)   # زيادة حدة الملامح الطبيعية
        
        return sharpness
    except:
        # في حال حدوث أي مشكلة، يتم إرجاع الصورة الأصلية لكي لا يعلق الموقع
        uploaded_file.seek(0)
        return Image.open(uploaded_file)
