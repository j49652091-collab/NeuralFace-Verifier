import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

def make_real(uploaded_file):
    try:
        # 1. قراءة الصورة بدقة عالية وتحويلها إلى مصفوفة ألوان
        uploaded_file.seek(0)
        image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image)
        
        # 2. تحويل الصورة إلى نظام ألوان OpenCV ومعالجة الإضاءة الرقمية
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        # 3. تطبيق فلتر التنعيم الفوتوغرافي لفصل الخطوط الكرتونية الحادة عن البشرة
        dst = cv2.edgePreservingFilter(img_bgr, flags=1, sigma_s=60, sigma_r=0.4)
        
        # 4. توليد طبقة مسام اصطناعية تحاكي جلد الإنسان الحقيقي (Film Grain Texture)
        noise = np.zeros(dst.shape, np.int8)
        cv2.randn(noise, (0,0,0), (20,20,20))
        real_skin_texture = cv2.addWeighted(dst, 1.0, noise, 0.1, 0, dtype=cv2.CV_8U)
        
        # 5. تحويل الصورة الناتجة إلى Pillow لإضافة فلاتر الكاميرا السينمائية
        final_img = Image.fromarray(cv2.cvtColor(real_skin_texture, cv2.COLOR_BGR2RGB))
        
        # 6. تعزيز ملامح العينين والنظارات والملابس لتبدو ثلاثية الأبعاد وواقعية
        final_img = final_img.filter(ImageFilter.SHARPEN)
        
        # 7. ضبط درجة حرارة الألوان وتباينها لتشبه تصوير استوديو حقيقي
        contrast = ImageEnhance.Contrast(final_img).enhance(1.25)
        color = ImageEnhance.Color(contrast).enhance(0.85) # تقليل تشبع الألوان الكرتونية الفاقعة
        brightness = ImageEnhance.Brightness(color).enhance(1.02)
        
        return brightness
    except:
        # في حال حدوث أي خطأ، يتم إرجاع الصورة الأصلية لضمان استقرار التطبيق
        uploaded_file.seek(0)
        return Image.open(uploaded_file)
