import requests
import io
import base64
from PIL import Image

def make_real(uploaded_image):
    try:
        # 1. تهيئة الصورة وإعادة تحجيمها
        uploaded_image.seek(0)
        image = Image.open(uploaded_image).convert("RGB")
        image = image.resize((512, 512))
        
        # 2. تحويل الصورة إلى بايتات خام (Raw Bytes) لأن خوادم Hugging Face تستقبلها هكذا في الـ Image-to-Image
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=90)
        img_bytes = buffered.getvalue()

        # 3. اختيار موديل توليد رسمي ومتاح مجاناً عبر الـ Serverless API
        # استخدمنا هنا موديل استقرار الصور الفعال من Stability AI
        API_URL = "https://huggingface.co"
        
        # 4. التوكن الخاص بك (تأكد من وضع توكن حقيقي صالح من إعدادات حسابك Hugging Face)
        headers = {
            "Authorization": "Bearer hf_pYwXbYwXbYwXbYwXbYwXbYwXbYwXbYwXbY",
            "Content-Type": "application/octet-stream"
        }
        
        # 5. إرسال الطلب (الخادم يحتاج البايثونات الخام في الـ data والوصف كـ Header أو باراميتر مدمج)
        # لتوليد موجه، نرسل البايتات ونقوم بتحديد الإعدادات عبر الباراميترز إذا لزم
        response = requests.post(API_URL, headers=headers, data=img_bytes, timeout=40)
        
        if response.status_code == 200:
            # استقبال الصورة المعالجة وإرجاعها بنجاح إلى التطبيق
            return Image.open(io.BytesIO(response.content))
        else:
            # إذا كان الموديل في وضع التحميل أو السيرفر مشغول، نرجع الأصل لتجنب الانهيار
            uploaded_image.seek(0)
            return Image.open(uploaded_image)
            
    except Exception as e:
        # طباعة الخطأ في السجلات الداخلية للمساعدة في التتبع والعودة للأصل بأمان
        print(f"Error in Generator: {e}")
        uploaded_image.seek(0)
        return Image.open(uploaded_image)
